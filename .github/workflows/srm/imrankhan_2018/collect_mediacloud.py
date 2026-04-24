"""
SRM Media Cloud Pipeline — Imran Khan 2018
Calculează PE (LDA Jensen-Shannon) și ICI (SBERT cosine distance) → D → SRM
Necesită: MEDIACLOUD_API_KEY în environment
"""

import os
import json
import time
import numpy as np
from pathlib import Path
from datetime import datetime

SYMBOL        = "Imran Khan"
SYMBOL_SLUG   = "imrankhan_2018"
WINDOW_START  = "2018-07-01"
WINDOW_END    = "2018-08-22"
QUERY         = '"Imran Khan"'
COLLECTION_IDS = [34412234, 38379429]
TARGET_ARTICLES = 3000
ARTICLES_PER_PAGE = 100
LDA_N_TOPICS  = 10
LDA_PASSES    = 15
LDA_RANDOM    = 42
SBERT_MODEL   = "all-MiniLM-L6-v2"
MIN_ARTICLES_PER_OUTLET = 5

RESULTS_DIR = Path("srm/imrankhan_2018/results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def collect_articles(api_key):
    import mediacloud.api as mc
    print(f"[MC] Fetching articles...")
    client = mc.MediaCloud(api_key)
    all_articles = []
    last_id = None

    while len(all_articles) < TARGET_ARTICLES:
        kwargs = {
            "solr_filter": [
                mc.dates_as_query_clause(WINDOW_START, WINDOW_END),
                f"tags_id_media:({' OR '.join(str(c) for c in COLLECTION_IDS)})"
            ],
            "rows": ARTICLES_PER_PAGE,
            "text": True
        }
        if last_id:
            kwargs["last_processed_stories_id"] = last_id

        try:
            results = client.storyList(QUERY, **kwargs)
        except Exception as e:
            print(f"  Error: {e}. Retrying...")
            time.sleep(10)
            continue

        if not results:
            break

        for s in results:
            all_articles.append({
                "story_id":   s.get("stories_id"),
                "url":        s.get("url", ""),
                "title":      s.get("title", ""),
                "media_name": s.get("media", {}).get("name", "unknown"),
                "text":       s.get("story_text", "") or ""
            })

        last_id = results[-1]["processed_stories_id"]
        print(f"  Fetched {len(all_articles)}...")
        time.sleep(0.5)

    articles = [a for a in all_articles if len(a.get("text", "")) > 150]
    print(f"  {len(articles)} articles after filter")
    return articles


def compute_PE(articles):
    from gensim import corpora, models
    from gensim.utils import simple_preprocess
    from scipy.spatial.distance import jensenshannon
    print("[PE] Computing Polysemy Entropy...")

    outlet_groups = {}
    for a in articles:
        outlet_groups.setdefault(a["media_name"], []).append(a["text"])
    outlets = {k: v for k, v in outlet_groups.items()
               if len(v) >= MIN_ARTICLES_PER_OUTLET}

    if len(outlets) < 2:
        raise RuntimeError(f"Too few outlets: {len(outlets)}")

    print(f"  Outlets: {list(outlets.keys())}")

    all_texts = [simple_preprocess(t, deacc=True)
                 for texts in outlets.values() for t in texts]
    dictionary = corpora.Dictionary(all_texts)
    dictionary.filter_extremes(no_below=3, no_above=0.85)
    corpus = [dictionary.doc2bow(t) for t in all_texts]

    lda = models.LdaModel(
        corpus,
        num_topics=LDA_N_TOPICS,
        id2word=dictionary,
        passes=LDA_PASSES,
        random_state=LDA_RANDOM
    )

    def outlet_dist(texts):
        processed = [simple_preprocess(t, deacc=True) for t in texts]
        bows = [dictionary.doc2bow(p) for p in processed]
        dists = []
        for bow in bows:
            d = dict(lda.get_document_topics(bow, minimum_probability=0))
            dists.append([d.get(i, 0) for i in range(LDA_N_TOPICS)])
        return np.mean(dists, axis=0)

    names = list(outlets.keys())
    dists = {n: outlet_dist(outlets[n]) for n in names}

    jsd_vals, pairs = [], []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            n1, n2 = names[i], names[j]
            jsd = float(jensenshannon(dists[n1], dists[n2]))
            jsd_vals.append(jsd)
            pairs.append({"outlet_1": n1, "outlet_2": n2, "jsd": round(jsd, 6)})

    PE = round(float(np.mean(jsd_vals)), 4)
    print(f"  PE={PE} ({len(pairs)} pairs)")
    return {"PE": PE, "n_pairs": len(pairs), "outlet_pairs": pairs}


def compute_ICI(articles):
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    print("[ICI] Computing Intra-contextual Incoherence...")

    model = SentenceTransformer(SBERT_MODEL)

    outlet_groups = {}
    for a in articles:
        outlet_groups.setdefault(a["media_name"], []).append(a["text"][:1000])
    outlets = {k: v for k, v in outlet_groups.items()
               if len(v) >= MIN_ARTICLES_PER_OUTLET}

    if len(outlets) < 2:
        raise RuntimeError(f"Too few outlets: {len(outlets)}")

    embeddings = {}
    for name, texts in outlets.items():
        emb = model.encode(texts, batch_size=32, show_progress_bar=False)
        embeddings[name] = np.mean(emb, axis=0)
        print(f"  Embedded {name}: {len(texts)} articles")

    names = list(embeddings.keys())
    cos_dists, pairs = [], []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            n1, n2 = names[i], names[j]
            sim  = float(cosine_similarity(
                embeddings[n1].reshape(1, -1),
                embeddings[n2].reshape(1, -1)
            )[0][0])
            dist = round(1.0 - sim, 6)
            cos_dists.append(dist)
            pairs.append({"outlet_1": n1, "outlet_2": n2, "cosine_distance": dist})

    ICI = round(float(np.mean(cos_dists)), 4)
    ccfi = ICI > 0.84
    print(f"  ICI={ICI} | CCFI={'CONFIRMAT' if ccfi else 'nu'} (prag 0.84)")
    return {"ICI": ICI, "n_pairs": len(pairs), "outlet_pairs": pairs,
            "ccfi_flag": ccfi, "ccfi_threshold": 0.84}


def main():
    api_key = os.environ.get("MEDIACLOUD_API_KEY")
    if not api_key:
        raise EnvironmentError("MEDIACLOUD_API_KEY not set.")

    print("=" * 55)
    print(f"Media Cloud Pipeline: {SYMBOL}")
    print("=" * 55)

    articles   = collect_articles(api_key)
    pe_result  = compute_PE(articles)
    ici_result = compute_ICI(articles)

    PE  = pe_result["PE"]
    ICI = ici_result["ICI"]
    D   = round(PE + ICI, 4)
    print(f"\n[D] {PE} + {ICI} = {D}")

    with open(RESULTS_DIR / f"{SYMBOL_SLUG}_pe_ici.json", "w") as f:
        json.dump({
            "symbol": SYMBOL,
            "window": f"{WINDOW_START}:{WINDOW_END}",
            "n_articles": len(articles),
            "pe": pe_result,
            "ici": ici_result,
            "D": D,
            "computed_at": datetime.utcnow().isoformat() + "Z"
        }, f, indent=2)

    params_path = RESULTS_DIR / f"{SYMBOL_SLUG}_srm_params.json"
    if params_path.exists():
        with open(params_path) as f:
            params = json.load(f)
        p = params["srm_params"]
        p["PE"]  = PE
        p["ICI"] = ICI
        p["D"]   = D

        V, A, lam, N = p.get("V"), p.get("A"), p.get("lambda"), p.get("N")
        if all(v is not None for v in [V, A, lam, N]):
            SRM = round(float(V * A * np.exp(-lam * D) * N), 6)
            p["SRM"] = SRM
            print(f"[SRM] = {SRM}")

        with open(params_path, "w") as f:
            json.dump(params, f, indent=2)

    print("\n" + "=" * 55)
    print(f"  PE   = {PE}")
    print(f"  ICI  = {ICI}  {'← CCFI CONFIRMAT' if ici_result['ccfi_flag'] else ''}")
    print(f"  D    = {D}")
    print(f"  SRM  = {params['srm_params'].get('SRM')}")
    print("=" * 55)


if __name__ == "__main__":
    main()
