"""
vader_sentiment.py
==================
Computes Affective Weight (A) for the SRM model
using VADER sentiment analysis on article headlines/snippets
fetched from Media Cloud.

Usage:
  python vader_sentiment.py --csv data/counts_zelensky_usa.csv \
                            --api-key YOUR_MEDIACLOUD_API_KEY \
                            --output A_result.json

Or, if you already have a CSV with article titles (title column):
  python vader_sentiment.py --titles-csv data/zelensky_titles.csv \
                            --output A_result.json

Requirements:
  pip install vaderSentiment requests
"""

import json
import argparse
import statistics


def compute_A_from_scores(compound_scores: list[float]) -> float:
    """
    Convert VADER compound scores [-1, +1] to A value [0, 1].

    Method (same as Trump validation):
      - Take absolute value of each compound score (polarity intensity)
      - A = mean of |compound_scores|
    This captures emotional charge regardless of positive/negative valence.
    """
    if not compound_scores:
        return 0.0
    intensities = [abs(s) for s in compound_scores]
    return round(statistics.mean(intensities), 4)


def run_vader_on_titles(titles: list[str]) -> float:
    """Run VADER on a list of article titles and return A."""
    try:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    except ImportError:
        raise ImportError("Install with: pip install vaderSentiment")

    analyzer = SentimentIntensityAnalyzer()
    scores = []
    for title in titles:
        if title and title.strip():
            vs = analyzer.polarity_scores(title)
            scores.append(vs["compound"])

    A = compute_A_from_scores(scores)
    print(f"[VADER] Analyzed {len(scores)} titles → A = {A:.4f}")
    return A


def fetch_from_mediacloud_and_analyze(api_key: str, query: str = "zelensky",
                                       start: str = "2022-05-20",
                                       end: str = "2026-02-23",
                                       collection_id: int = 34412234,  # US National
                                       sample_size: int = 1000) -> float:
    """
    Fetch article stories from Media Cloud and run VADER.
    Uses /api/v2/stories/list endpoint (sample).

    NOTE: Full VADER analysis requires fetching article text, which
    requires Media Cloud's premium API. For SRM validation, a sample
    of ~500–1000 titles is sufficient (same approach as Trump paper).
    """
    import requests

    print(f"[MediaCloud] Fetching up to {sample_size} stories for '{query}'...")
    base_url = "https://api.mediacloud.org/api/v2"
    headers  = {"Authorization": f"MediaCloud {api_key}"}

    stories = []
    last_id = 0
    per_page = 200

    while len(stories) < sample_size:
        params = {
            "q": query,
            "fq": f"publish_date:[{start}T00:00:00Z TO {end}T23:59:59Z]",
            "collections[]": collection_id,
            "rows": per_page,
            "last_processed_stories_id": last_id,
        }
        resp = requests.get(f"{base_url}/stories/list", headers=headers, params=params)
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        stories.extend(batch)
        last_id = batch[-1]["processed_stories_id"]
        if len(batch) < per_page:
            break

    titles = [s.get("title", "") for s in stories[:sample_size]]
    print(f"[MediaCloud] Retrieved {len(titles)} stories")
    return run_vader_on_titles(titles)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute SRM variable A via VADER")
    parser.add_argument("--titles-csv",  help="CSV file with 'title' column (offline mode)")
    parser.add_argument("--api-key",     help="Media Cloud API key (online mode)")
    parser.add_argument("--query",       default="zelensky")
    parser.add_argument("--start",       default="2022-05-20")
    parser.add_argument("--end",         default="2026-02-23")
    parser.add_argument("--output",      default="A_result.json")
    args = parser.parse_args()

    if args.titles_csv:
        import csv
        with open(args.titles_csv, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        titles = [r.get("title", "") for r in rows]
        A = run_vader_on_titles(titles)
    elif args.api_key:
        A = fetch_from_mediacloud_and_analyze(args.api_key, args.query,
                                               args.start, args.end)
    else:
        print("ERROR: provide --titles-csv or --api-key")
        raise SystemExit(1)

    result = {"A_affective_weight": A}
    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)
    print(f"[SAVED] A = {A}  →  {args.output}")
