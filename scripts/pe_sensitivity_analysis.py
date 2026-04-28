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
        results[f"pe_std_K{k}"] = round(pe_stats["pe_std"], 6)
        results[f"pe_ci_low_K{k}"] = round(pe_stats["pe_ci_low"], 6)
        results[f"pe_ci_high_K{k}"] = round(pe_stats["pe_ci_high"], 6)
        results[f"npmi_K{k}"] = round(npmi, 6)
        results[f"lda_time_s_K{k}"] = round(elapsed, 1)
        log.info(
            f"  K={k}: PE={pe_stats['pe_mean']:.4f} "
            f"[{pe_stats['pe_ci_low']:.4f}, {pe_stats['pe_ci_high']:.4f}] "
            f"| NPMI={npmi:.4f} | t={elapsed:.1f}s"
        )

    pe_k10 = results.get(f"pe_K{K_PRIMARY}", None)
    if pe_k10 is not None and pe_k10 > 0:
        deviations = [
            abs(results.get(f"pe_K{k}", pe_k10) - pe_k10)
            for k in k_values
        ]
        results["max_abs_deviation_from_K10"] = round(max(deviations), 6)
        results["cv_pe"] = round(
            np.std([results[f"pe_K{k}"] for k in k_values]) /
            np.mean([results[f"pe_K{k}"] for k in k_values]),
            6
        )
        npmi_vals = {
            k: results.get(f"npmi_K{k}", float("-inf"))
            for k in k_values
        }
        results["best_npmi_K"] = max(npmi_vals, key=npmi_vals.get)
    return results


def build_summary_report(all_results, k_values):
    lines = []
    lines.append("=" * 70)
    lines.append("PE SENSITIVITY ANALYSIS — POLITOMORPHISM RESEARCH PROJECT")
    lines.append(f"K values tested: {k_values} | Primary K: {K_PRIMARY}")
    lines.append("=" * 70)
    lines.append("")

    max_devs = [
        r["max_abs_deviation_from_K10"]
        for r in all_results
        if "max_abs_deviation_from_K10" in r
    ]
    cvs = [r["cv_pe"] for r in all_results if "cv_pe" in r]

    if max_devs:
        lines.append("AGGREGATE STABILITY METRICS")
        lines.append("  Max absolute deviation from K=10 across all symbols:")
        lines.append(f"    Mean:  {np.mean(max_devs):.4f}")
        lines.append(f"    Max:   {np.max(max_devs):.4f}")
        lines.append(f"    Min:   {np.min(max_devs):.4f}")
        lines.append("  Coefficient of variation of PE across K values:")
        lines.append(f"    Mean:  {np.mean(cvs):.4f}")
        lines.append(f"    Max:   {np.max(cvs):.4f}")
        lines.append("")

    lines.append("PER-SYMBOL PE TABLE")
    lines.append(
        f"{'Symbol':<20} {'PE_K5':>8} {'PE_K10':>8} {'PE_K15':>8} "
        f"{'MaxDev':>8} {'CV':>7} {'BestNPMI_K':>12}"
    )
    lines.append("-" * 75)
    for r in all_results:
        lines.append(
            f"{r['symbol']:<20} "
            f"{r.get('pe_K5', float('nan')):>8.4f} "
            f"{r.get('pe_K10', float('nan')):>8.4f} "
            f"{r.get('pe_K15', float('nan')):>8.4f} "
            f"{r.get('max_abs_deviation_from_K10', float('nan')):>8.4f} "
            f"{r.get('cv_pe', float('nan')):>7.4f} "
            f"{str(r.get('best_npmi_K', '—')):>12}"
        )

    lines.append("")
    lines.append("NPMI COHERENCE TABLE")
    lines.append(
        f"{'Symbol':<20} {'NPMI_K5':>9} {'NPMI_K10':>10} {'NPMI_K15':>10}"
    )
    lines.append("-" * 55)
    for r in all_results:
        lines.append(
            f"{r['symbol']:<20} "
            f"{r.get('npmi_K5', float('nan')):>9.4f} "
            f"{r.get('npmi_K10', float('nan')):>10.4f} "
            f"{r.get('npmi_K15', float('nan')):>10.4f}"
        )

    lines.append("")
    lines.append("INTERPRETATION GUIDE")
    lines.append("  MaxDev < 0.005  : PE stable — K=10 choice is robust.")
    lines.append("  MaxDev 0.005-0.010 : Moderate sensitivity — note in Supplementary.")
    lines.append("  MaxDev > 0.010  : High sensitivity — investigate corpus.")
    lines.append(
        "  Higher NPMI = better topic coherence; "
        "BestNPMI_K shows if K=10 is optimal."
    )
    lines.append("")
    lines.append("Reproducibility: random_state=42, sklearn LDA batch mode,")
    lines.append("max_iter=20, doc_topic_prior=None (sklearn default=1/K),")
    lines.append("topic_word_prior=0.01.")
    lines.append("=" * 70)
    return "\n".join(lines)


def parse_args():
    p = argparse.ArgumentParser(
        description="PE Sensitivity Analysis: K=5 vs K=10 vs K=15"
    )
    p.add_argument("--input_dir", type=Path, default=Path("./corpora"))
    p.add_argument(
        "--symbols", nargs="+",
        default=["Trump", "Modi_2014", "Putin", "Sunflower", "CharlieHebdo"]
    )
    p.add_argument("--output_dir", type=Path, default=Path("./sensitivity_results"))
    p.add_argument("--bootstrap_n", type=int, default=200)
    p.add_argument("--random_state", type=int, default=42)
    p.add_argument("--k_values", nargs="+", type=int, default=[5, 10, 15])
    return p.parse_args()


def main():
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    global K_VALUES
    K_VALUES = args.k_values

    log.info(f"Symbols:    {args.symbols}")
    log.info(f"K values:   {K_VALUES}")
    log.info(f"Bootstrap:  n={args.bootstrap_n}")
    log.info(f"Input dir:  {args.input_dir}")
    log.info(f"Output dir: {args.output_dir}")

    all_results = []
    failed = []

    for symbol in args.symbols:
        log.info(f"--- {symbol} ---")
        try:
            corpus_path = find_corpus_file(args.input_dir, symbol)
            texts = load_corpus(corpus_path)
            result = analyse_symbol(
                symbol=symbol,
                texts=texts,
                k_values=K_VALUES,
                bootstrap_n=args.bootstrap_n,
                random_state=args.random_state,
            )
            all_results.append(result)
        except Exception as e:
            log.error(f"  FAILED: {e}")
            failed.append((symbol, str(e)))

    if not all_results:
        log.error("No symbols completed successfully. Exiting.")
        sys.exit(1)

    df = pd.DataFrame(all_results)

    pe_table_path = args.output_dir / "pe_sensitivity_table.csv"
    df.to_csv(pe_table_path, index=False, float_format="%.6f")
    log.info(f"Saved: {pe_table_path}")

    npmi_cols = ["symbol"] + [f"npmi_K{k}" for k in K_VALUES] + ["best_npmi_K"]
    npmi_cols = [c for c in npmi_cols if c in df.columns]
    npmi_path = args.output_dir / "npmi_coherence_table.csv"
    df[npmi_cols].to_csv(npmi_path, index=False, float_format="%.6f")
    log.info(f"Saved: {npmi_path}")

    report = build_summary_report(all_results, K_VALUES)
    report_path = args.output_dir / "pe_sensitivity_summary.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    log.info(f"Saved: {report_path}")

    print("\n" + report)

    if failed:
        log.warning(f"Failed: {[s for s, _ in failed]}")
        sys.exit(2)


if __name__ == "__main__":
    main()
