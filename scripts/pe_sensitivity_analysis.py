"""
PE Sensitivity Analysis: K=5 vs K=10 vs K=15
Politomorphism Research Project — Serban Gabriel Florin
ORCID: 0009-0000-2266-3356
"""

import argparse
import itertools
import logging
import math
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

K_VALUES = [5, 10, 15]
K_PRIMARY = 10
RANDOM_STATE = 42
MAX_ITER = 20
MIN_DOCS = 50


def load_corpus(filepath):
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Corpus file not found: {filepath}")
    if filepath.suffix.lower() == ".csv":
        df = pd.read_csv(filepath, encoding="utf-8", on_bad_lines="skip")
        col = next((c for c in df.columns if c.lower() == "title"), None)
        if col is None:
            raise ValueError(
                f"{filepath.name}: no 'title' column found. "
                f"Available columns: {list(df.columns)}"
            )
        titles = df[col].dropna().astype(str).tolist()
    else:
        with open(filepath, encoding="utf-8") as f:
            titles = [line.strip() for line in f if line.strip()]
    log.info(f"  Loaded {len(titles)} titles from {filepath.name}")
    if len(titles) < MIN_DOCS:
        log.warning(f"  Only {len(titles)} documents — results may be unstable.")
    return titles


def find_corpus_file(input_dir, symbol):
    for ext in (".csv", ".txt"):
        p = Path(input_dir) / f"{symbol}{ext}"
        if p.exists():
            return p
    raise FileNotFoundError(
        f"No corpus file found for symbol '{symbol}' in {input_dir}. "
        f"Expected: {symbol}.csv or {symbol}.txt"
    )


def build_dtm(texts):
    vectorizer = CountVectorizer(
        max_df=0.95,
        min_df=2,
        stop_words="english",
        max_features=5000,
        token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z]+\b",
    )
    dtm = vectorizer.fit_transform(texts)
    vocab = vectorizer.get_feature_names_out()
    return dtm, vectorizer, vocab


def fit_lda(dtm, n_topics, random_state=RANDOM_STATE):
    lda = LatentDirichletAllocation(
        n_components=n_topics,
        random_state=random_state,
        max_iter=MAX_ITER,
        learning_method="batch",
        doc_topic_prior=None,
        topic_word_prior=0.01,
    )
    lda.fit(dtm)
    return lda


def get_doc_topic_matrix(lda, dtm):
    raw = lda.transform(dtm)
    row_sums = raw.sum(axis=1, keepdims=True)
    row_sums = np.where(row_sums == 0, 1, row_sums)
    return raw / row_sums


def jsd(p, q, eps=1e-10):
    p = np.clip(p, eps, 1)
    q = np.clip(q, eps, 1)
    m = 0.5 * (p + q)
    kl_pm = np.sum(p * np.log(p / m))
    kl_qm = np.sum(q * np.log(q / m))
    return float(0.5 * (kl_pm + kl_qm))


def compute_pe(doc_topic, bootstrap_n, rng):
    n = len(doc_topic)
    if n <= 500:
        idx_pairs = list(itertools.combinations(range(n), 2))
        all_jsds = [jsd(doc_topic[i], doc_topic[j]) for i, j in idx_pairs]
    else:
        pairs = rng.integers(0, n, size=(10_000, 2))
        pairs = pairs[pairs[:, 0] != pairs[:, 1]]
        all_jsds = [jsd(doc_topic[a], doc_topic[b]) for a, b in pairs]
    pe_point = float(np.mean(all_jsds))

    boot_means = []
    sample_size = min(n, 500)
    for _ in range(bootstrap_n):
        sample_idx = rng.choice(n, size=sample_size, replace=True)
        sample = doc_topic[sample_idx]
        if len(sample) < 2:
            continue
        n_s = len(sample)
        if n_s <= 200:
            pairs_b = list(itertools.combinations(range(n_s), 2))
            jsds_b = [jsd(sample[i], sample[j]) for i, j in pairs_b]
        else:
            p_b = rng.integers(0, n_s, size=(3_000, 2))
            p_b = p_b[p_b[:, 0] != p_b[:, 1]]
            jsds_b = [jsd(sample[a], sample[b]) for a, b in p_b]
        boot_means.append(float(np.mean(jsds_b)))

    ci_low, ci_high = np.percentile(boot_means, [2.5, 97.5])
    return {
        "pe_mean": pe_point,
        "pe_std": float(np.std(boot_means)),
        "pe_ci_low": float(ci_low),
        "pe_ci_high": float(ci_high),
        "n_docs": n,
        "n_bootstrap": bootstrap_n,
    }


def compute_npmi_coherence(lda, dtm, vocab, top_n=10):
    n_docs = dtm.shape[0]
    dtm_dense = (dtm > 0).toarray().astype(np.float32)
    word_counts = dtm_dense.sum(axis=0)
    p_w = word_counts / n_docs
    npmi_scores = []
    for topic_idx in range(lda.n_components):
        topic_dist = lda.components_[topic_idx]
        top_word_idx = np.argsort(topic_dist)[::-1][:top_n]
        for i, j in itertools.combinations(top_word_idx, 2):
            co_count = (dtm_dense[:, i] * dtm_dense[:, j]).sum()
            p_co = co_count / n_docs
            if p_co < 1e-10 or p_w[i] < 1e-10 or p_w[j] < 1e-10:
                continue
            pmi = math.log(p_co / (p_w[i] * p_w[j]))
            npmi = pmi / (-math.log(p_co))
            npmi_scores.append(npmi)
    return float(np.mean(npmi_scores)) if npmi_scores else float("nan")


def analyse_symbol(symbol, texts, k_values, bootstrap_n, random_state):
    log.info(f"  Building document-term matrix ({len(texts)} docs)...")
    dtm, vectorizer, vocab = build_dtm(texts)
    rng = np.random.default_rng(random_state)
    results = {"symbol": symbol, "n_docs": len(texts)}

    for k in k_values:
        log.info(f"  Fitting LDA K={k}...")
        t0 = time.time()
        lda = fit_lda(dtm, n_topics=k, random_state=random_state)
        elapsed = time.time() - t0
        log.info(f"  Computing PE (bootstrap n={bootstrap_n})...")
        doc_topic = get_doc_topic_matrix(lda, dtm)
        pe_stats = compute_pe(doc_topic, bootstrap_n=bootstrap_n, rng=rng)
        log.info(f"  Computing NPMI coherence...")
        npmi = compute_npmi_coherence(lda, dtm, vocab)
        results[f"pe_K{k}"] = round(pe_stats["pe_mean"], 6)
        results[f"pe_std_K{k}"
