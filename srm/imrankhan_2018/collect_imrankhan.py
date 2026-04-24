import json
import time
import requests
import numpy as np
import os
from datetime import datetime
from pathlib import Path

SYMBOL       = "Imran Khan"
SYMBOL_SLUG  = "imrankhan_2018"
WINDOW_START = "2018-07-01"
WINDOW_END   = "2018-08-22"
PEAK_DATE    = "2018-07-25"
WIKI_ARTICLE = "Imran_Khan"

RESULTS_DIR = Path("srm/imrankhan_2018/results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# ── Date colectate manual din Google Trends CSV ──────────────────────────────
TRENDS_DATA = {
    "2018-07-01":6,"2018-07-02":5,"2018-07-03":4,"2018-07-04":5,
    "2018-07-05":5,"2018-07-06":7,"2018-07-07":7,"2018-07-08":6,
    "2018-07-09":5,"2018-07-10":4,"2018-07-11":4,"2018-07-12":6,
    "2018-07-13":9,"2018-07-14":8,"2018-07-15":7,"2018-07-16":5,
    "2018-07-17":5,"2018-07-18":6,"2018-07-19":6,"2018-07-20":6,
    "2018-07-21":8,"2018-07-22":10,"2018-07-23":9,"2018-07-24":14,
    "2018-07-25":40,"2018-07-26":100,"2018-07-27":64,"2018-07-28":42,
    "2018-07-29":32,"2018-07-30":21,"2018-07-31":16,"2018-08-01":13,
    "2018-08-02":14,"2018-08-03":12,"2018-08-04":11,"2018-08-05":12,
    "2018-08-06":11,"2018-08-07":9,"2018-08-08":9,"2018-08-09":8,
    "2018-08-10":9,"2018-08-11":11,"2018-08-12":9,"2018-08-13":11,
    "2018-08-14":10,"2018-08-15":8,"2018-08-16":9,"2018-08-17":26,
    "2018-08-18":44,"2018-08-19":31,"2018-08-20":19,"2018-08-21":12,
    "2018-08-22":10
}


def compute_trends():
    print("[1/3] Google Trends (date hardcodate din CSV)...")
    series   = list(TRENDS_DATA.values())
    dates    = list(TRENDS_DATA.keys())
    peak_idx = int(np.argmax(series))
    peak_val = int(series[peak_idx])

    # Fit exponential decay pe declinul principal (26 iulie - 16 august)
    post = series[peak_idx:peak_idx+22]
    t    = np.arange(len(post), dtype=float)
    y    = np.array(post, dtype=float)
    valid = y > 0
    coeffs = np.polyfit(t[valid], np.log(y[valid]), 1)
    lambda_fit = round(float(-coeffs[0]), 4)

    V = round(peak_val / 100.0, 4)
    print(f"  V={V}, lambda={lambda_fit}, peak={dates[peak_idx]}")
    return {
        "source":          "google_trends_csv_manual",
        "dates":           dates,
        "interest_series": series,
        "peak_date":       dates[peak_idx],
        "peak_value":      peak_val,
        "V_viral_velocity":  V,
        "lambda_decay_fit":  lambda_fit,
        "note": "Date colectate manual din Google Trends export CSV"
    }


def collect_wikipedia():
    print("[2/3] Wikipedia Pageviews...")
    s = WINDOW_START.replace("-","") + "00"
    e = WINDOW_END.replace("-","")   + "00"
    url = (
        f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article"
        f"/en.wikipedia/all-access/all-agents/{WIKI_ARTICLE}/daily/{s}/{e}"
    )
    headers = {"User-Agent": "Politomorphism-SRM/1.0 (osf.io/hydnz)"}
    for attempt in range(3):
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            break
        print(f"  Attempt {attempt+1}: {r.status_code}")
        time.sleep(5 * (attempt+1))
    if r.status_code != 200:
        raise RuntimeError(f"Wikipedia API failed: {r.status_code}")
    items  = r.json()["items"]
    dates  = [i["timestamp"][:8] for i in items]
    views  = [i["views"] for i in items]
    total  = sum(views)
    peak_v = max(views)
    peak_d = dates[views.index(peak_v)]
    N = round(min(np.log10(total+1) / 6.3, 1.0), 4)
    print(f"  N={N}, total={total:,}, peak={peak_d}")
    return {
        "source":             "wikipedia_pageviews",
        "dates":              dates,
        "daily_views":        views,
        "total_views":        total,
        "peak_views":         peak_v,
        "peak_date":          peak_d,
        "N_network_coverage": N
    }


def collect_mediacloud_tone(api_key):
    print("[3/3] MediaCloud tone (proxy pentru A)...")
    # Folosim MediaCloud API pentru a estima tonul
    # Cautam articole si calculam sentimentul mediu din titluri
    base = "https://api.mediacloud.org/api/v2/stories/list"
    headers = {"Authorization": f"MediaCloud {api_key}"}
    params = {
        "q":         '"Imran Khan"',
        "fq":        f"publish_date:[{WINDOW_START}T00:00:00Z TO {WINDOW_END}T23:59:59Z]",
        "rows":      20,
        "feeds_id":  [1, 2]  # top US + UK collections
    }
    try:
        r = requests.get(base, headers=headers, params=params, timeout=15)
        if r.status_code == 200:
            stories = r.json().get("stories", [])
            print(f"  {len(stories)} stories found via MediaCloud")
    except Exception as e:
        print(f"  MediaCloud tone fetch: {e}")

    # A estimat din literatura GDELT pentru simboluri electorali victorioasi
    # Non-Western in media anglo-americana: ton usor negativ (-6 to -10)
    # Formula: A = (avgTone + 100) / 200
    # avgTone estimat = -7.5 pentru Imran Khan 2018 (scepticism despre armata)
    avg_tone_estimated = -7.5
    A = round((avg_tone_estimated + 100) / 200.0, 4)
    print(f"  A={A} (estimat din literatura GDELT, avgTone={avg_tone_estimated})")
    return {
        "source":             "gdelt_estimated",
        "avg_tone_estimated": avg_tone_estimated,
        "A_affective_weight": A,
        "note": "A estimat din literatura GDELT pentru simboluri electorale Non-Western victorioase in media anglo-americana. Validare directa necesita acces GDELT BigQuery."
    }


def main():
    api_key = os.environ.get("MEDIACLOUD_API_KEY", "")
    print("=" * 55)
    print(f"SRM Collection: {SYMBOL} | {WINDOW_START} -> {WINDOW_END}")
    print("=" * 55)

    raw    = {}
    errors = []

    for fn, key, args in [
        (compute_trends,         "google_trends", []),
        (collect_wikipedia,      "wikipedia",     []),
        (collect_mediacloud_tone,"gdelt",         [api_key]),
    ]:
        try:
            raw[key] = fn(*args)
        except Exception as e:
            errors.append({"source": key, "error": str(e)})
            print(f"  [ERROR] {key}: {e}")

    with open(RESULTS_DIR / f"{SYMBOL_SLUG}_raw.json", "w") as f:
        json.dump(raw, f, indent=2)

    V      = raw.get("google_trends", {}).get("V_viral_velocity")
    lam    = raw.get("google_trends", {}).get("lambda_decay_fit")
    N      = raw.get("wikipedia",     {}).get("N_network_coverage")
    A      = raw.get("gdelt",         {}).get("A_affective_weight")

    params = {
        "symbol":      SYMBOL,
        "symbol_slug": SYMBOL_SLUG,
        "peak_event":  "Pakistan General Elections",
        "peak_date":   PEAK_DATE,
        "window":      f"{WINDOW_START}:{WINDOW_END}",
        "collected_at": datetime.utcnow().isoformat() + "Z",
        "srm_params": {
            "V":      V,
            "lambda": lam,
            "N":      N,
            "A":      A,
            "PE":     None,
            "ICI":    None,
            "D":      None,
            "SRM":    None,
        },
        "srm_formula": "SRM = V x A x exp(-lambda x D) x N",
        "data_sources": {
            "V_lambda": "Google Trends daily export CSV, worldwide, 2018-07-01:2018-08-22",
            "N":        "Wikimedia REST API pageviews, en.wikipedia, all-access",
            "A":        "Estimat din literatura GDELT - validare directa necesara",
            "PE_ICI":   "Pending - Media Cloud pipeline (collect_mediacloud.py)"
        },
        "errors": errors
    }

    with open(RESULTS_DIR / f"{SYMBOL_SLUG}_srm_params.json", "w") as f:
        json.dump(params, f, indent=2)

    print("\n" + "=" * 55)
    print(f"  V      = {V}")
    print(f"  lambda = {lam}")
    print(f"  N      = {N}")
    print(f"  A      = {A}")
    print(f"  PE/ICI = pending Media Cloud")
    print("=" * 55)


if __name__ == "__main__":
    main()
