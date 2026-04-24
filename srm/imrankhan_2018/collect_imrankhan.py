import json
import time
import requests
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

SYMBOL       = "Imran Khan"
SYMBOL_SLUG  = "imrankhan_2018"
WINDOW_START = "2018-07-01"
WINDOW_END   = "2018-08-22"
PEAK_DATE    = "2018-07-25"
WIKI_ARTICLE = "Imran_Khan"
GDELT_QUERY  = '"Imran Khan" sourcelang:eng'

RESULTS_DIR  = Path("srm/imrankhan_2018/results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def collect_google_trends():
    from pytrends.request import TrendReq
    print("[1/3] Google Trends...")
    pt = TrendReq(hl="en-US", tz=0, timeout=(10, 25), retries=3, backoff_factor=0.5)
    df = None
    for attempt in range(3):
        try:
            pt.build_payload([SYMBOL], timeframe=f"{WINDOW_START} {WINDOW_END}", geo="")
            df = pt.interest_over_time()
            time.sleep(2)
            break
        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}")
            time.sleep(30)
    if df is None or df.empty:
        raise RuntimeError("Google Trends returned empty dataframe.")
    series   = df[SYMBOL].tolist()
    dates    = [str(d.date()) for d in df.index]
    peak_idx = int(np.argmax(series))
    peak_val = int(series[peak_idx])
    post = [v for v in series[peak_idx:] if v > 0]
    lambda_fit = None
    if len(post) >= 3:
        t = np.arange(len(post), dtype=float)
        y = np.array(post, dtype=float)
        valid = y > 0
        if valid.sum() >= 2:
            coeffs = np.polyfit(t[valid], np.log(y[valid]), 1)
            lambda_fit = round(float(-coeffs[0]), 4)
    V = round(peak_val / 100.0, 4)
    print(f"  V={V}, lambda={lambda_fit}, peak={dates[peak_idx]}")
    return {
        "source": "google_trends",
        "dates": dates,
        "interest_series": [int(v) for v in series],
        "peak_date": dates[peak_idx],
        "peak_value": peak_val,
        "V_viral_velocity": V,
        "lambda_decay_fit": lambda_fit,
    }


def collect_wikipedia_pageviews():
    print("[2/3] Wikipedia Pageviews...")
    s = WINDOW_START.replace("-", "") + "00"
    e = WINDOW_END.replace("-", "") + "00"
    url = (
        f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article"
        f"/en.wikipedia/all-access/all-agents/{WIKI_ARTICLE}/daily/{s}/{e}"
    )
    headers = {"User-Agent": "Politomorphism-SRM/1.0 (osf.io/hydnz)"}
    r = None
    for attempt in range(3):
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            break
        print(f"  Attempt {attempt+1}: status {r.status_code}")
        time.sleep(5 * (attempt + 1))
    if r is None or r.status_code != 200:
        raise RuntimeError(f"Wikipedia API failed: {r.status_code}")
    items  = r.json()["items"]
    dates  = [item["timestamp"][:8] for item in items]
    views  = [item["views"] for item in items]
    total  = sum(views)
    peak_v = max(views)
    peak_d = dates[views.index(peak_v)]
    N = round(min(np.log10(total + 1) / 6.3, 1.0), 4)
    print(f"  N={N}, total={total:,}, peak_date={peak_d}")
    return {
        "source": "wikipedia_pageviews",
        "dates": dates,
        "daily_views": views,
        "total_views": total,
        "peak_views": peak_v,
        "peak_date": peak_d,
        "N_network_coverage": N,
    }


def collect_gdelt_tone():
    print("[3/3] GDELT tone...")
    base_url = "https://api.gdeltproject.org/api/v2/doc/doc"
    weekly_tones = []
    start_dt = datetime.strptime(WINDOW_START, "%Y-%m-%d")
    end_dt   = datetime.strptime(WINDOW_END,   "%Y-%m-%d")
    current  = start_dt
    while current < end_dt:
        week_end = min(current + timedelta(days=7), end_dt)
        params = {
            "query":         GDELT_QUERY,
            "mode":          "artlist",
            "startdatetime": current.strftime("%Y%m%d%H%M%S"),
            "enddatetime":   week_end.strftime("%Y%m%d%H%M%S"),
            "maxrecords":    "250",
            "format":        "json",
        }
        try:
            r = requests.get(base_url, params=params, timeout=20)
            time.sleep(1.5)
            if r.status_code == 200:
                articles = r.json().get("articles", [])
                tones = [
                    float(a["tone"].split(",")[0])
                    for a in articles if a.get("tone")
                ]
                if tones:
                    avg = float(np.mean(tones))
                    weekly_tones.append({
                        "week_start": current.strftime("%Y-%m-%d"),
                        "n_articles": len(articles),
                        "avg_tone":   round(avg, 4)
                    })
                    print(f"  {current.strftime('%Y-%m-%d')}: n={len(articles)}, tone={avg:.2f}")
        except Exception as e:
            print(f"  Week {current.strftime('%Y-%m-%d')} error: {e}")
        current = week_end
    if not weekly_tones:
        raise RuntimeError("GDELT returned no tone data.")
    overall = float(np.mean([w["avg_tone"] for w in weekly_tones]))
    A = round(max(0.0, min(1.0, (overall + 100) / 200.0)), 4)
    print(f"  A={A}, overall_tone={overall:.3f}")
    return {
        "source": "gdelt",
        "weekly_breakdown": weekly_tones,
        "overall_avg_tone": round(overall, 4),
        "A_affective_weight": A,
    }


def main():
    print("=" * 55)
    print(f"SRM Collection: {SYMBOL} | {WINDOW_START} -> {WINDOW_END}")
    print("=" * 55)
    raw = {}
    errors = []
    for fn, key in [
        (collect_google_trends,       "google_trends"),
        (collect_wikipedia_pageviews, "wikipedia"),
        (collect_gdelt_tone,          "gdelt"),
    ]:
        try:
            raw[key] = fn()
        except Exception as e:
            errors.append({"source": key, "error": str(e)})
            print(f"  [ERROR] {key}: {e}")
    with open(RESULTS_DIR / f"{SYMBOL_SLUG}_raw.json", "w") as f:
        json.dump(raw, f, indent=2)
    params = {
        "symbol":      SYMBOL,
        "symbol_slug": SYMBOL_SLUG,
        "peak_event":  "Pakistan General Elections",
        "peak_date":   PEAK_DATE,
        "window":      f"{WINDOW_START}:{WINDOW_END}",
        "collected_at": datetime.utcnow().isoformat() + "Z",
        "srm_params": {
            "V":      raw.get("google_trends", {}).get("V_viral_velocity"),
            "lambda": raw.get("google_trends", {}).get("lambda_decay_fit"),
            "N":      raw.get("wikipedia",     {}).get("N_network_coverage"),
            "A":      raw.get("gdelt",         {}).get("A_affective_weight"),
            "PE":     None,
            "ICI":    None,
            "D":      None,
            "SRM":    None,
        },
        "srm_formula": "SRM = V x A x exp(-lambda x D) x N",
        "errors": errors
    }
    with open(RESULTS_DIR / f"{SYMBOL_SLUG}_srm_params.json", "w") as f:
        json.dump(params, f, indent=2)
    p = params["srm_params"]
    print("\n" + "=" * 55)
    print(f"  V      = {p['V']}")
    print(f"  lambda = {p['lambda']}")
    print(f"  N      = {p['N']}")
    print(f"  A      = {p['A']}")
    print("=" * 55)


if __name__ == "__main__":
    main()
