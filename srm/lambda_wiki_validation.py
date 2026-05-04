import numpy as np
import requests
from scipy.optimize import brentq
import json
import matplotlib.pyplot as plt

# -----------------------------
# CONFIG
# -----------------------------

API_URL = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article"
PROJECT = "en.wikipedia.org"
ACCESS = "all-access"
AGENT = "user"

# simboluri (exemplu – adaptează la datasetul tău)
SYMBOLS = {
    "Trump_2016": "Donald_Trump",
    "Modi_2019": "Narendra_Modi",
    "Bolsonaro_2022": "Jair_Bolsonaro"
}

START = "20150101"
END = "20241231"

T_YEARS = 1.0  # durata analizei (ajustează)

# -----------------------------
# CORE FUNCTIONS
# -----------------------------

def fetch_wikipedia_pageviews(article):
    url = f"{API_URL}/{PROJECT}/{ACCESS}/{AGENT}/{article}/daily/{START}/{END}"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    data = r.json()
    return np.array([d["views"] for d in data["items"]])


def avg_peak_ratio(series):
    peak = np.max(series)
    avg = np.mean(series)
    if peak == 0:
        return None
    return avg / peak


def lambda_from_ratio(ratio, T):
    def f(lmbda):
        return (1 - np.exp(-lmbda * T)) / (lmbda * T) - ratio

    try:
        return brentq(f, 0.0001, 200)
    except:
        return None


# -----------------------------
# BASELINE ESTIMATION
# -----------------------------

def estimate_baseline(series, method="p10"):
    if method == "p10":
        return np.percentile(series, 10)
    elif method == "median":
        return np.median(series)
    else:
        raise ValueError("Unknown baseline method")


def remove_baseline(series, B):
    corrected = series - B
    corrected[corrected < 0] = 0
    return corrected


# -----------------------------
# MAIN PIPELINE
# -----------------------------

results = []

for symbol, article in SYMBOLS.items():
    print(f"Processing: {symbol}")

    data = fetch_wikipedia_pageviews(article)
    if data is None or len(data) < 10:
        print("Skipping (no data)")
        continue

    # --- RAW ---
    r_raw = avg_peak_ratio(data)
    lambda_raw = lambda_from_ratio(r_raw, T_YEARS)

    # --- BASELINE ---
    B = estimate_baseline(data, method="p10")

    data_corrected = remove_baseline(data, B)

    r_corr = avg_peak_ratio(data_corrected)
    lambda_corr = lambda_from_ratio(r_corr, T_YEARS)

    # --- STORE ---
    results.append({
        "symbol": symbol,
        "baseline_B": float(B),
        "lambda_wiki_raw": float(lambda_raw) if lambda_raw else None,
        "lambda_wiki_corrected": float(lambda_corr) if lambda_corr else None
    })


# -----------------------------
# SAVE RESULTS
# -----------------------------

with open("lambda_wiki_baseline_results.json", "w") as f:
    json.dump(results, f, indent=4)

print("Saved results to lambda_wiki_baseline_results.json")


# -----------------------------
# OPTIONAL: COMPARISON WITH λ_trends
# -----------------------------
# Dacă ai deja λ_trends într-un dict:

lambda_trends = {
    "Trump_2016": 7.01,
    "Modi_2019": 6.33,
    "Bolsonaro_2022": 10.43
}

for r in results:
    sym = r["symbol"]
    if sym in lambda_trends:
        r["lambda_trends"] = lambda_trends[sym]
        if r["lambda_wiki_raw"]:
            r["delta_raw_pct"] = abs(r["lambda_wiki_raw"] - lambda_trends[sym]) / lambda_trends[sym] * 100
        if r["lambda_wiki_corrected"]:
            r["delta_corrected_pct"] = abs(r["lambda_wiki_corrected"] - lambda_trends[sym]) / lambda_trends[sym] * 100


# -----------------------------
# SAVE UPDATED
# -----------------------------

with open("lambda_wiki_baseline_results_with_trends.json", "w") as f:
    json.dump(results, f, indent=4)


# -----------------------------
# PLOT (IMPORTANT FOR PAPER)
# -----------------------------

for r in results:
    if "lambda_trends" in r:
        labels = ["Trends", "Wiki Raw", "Wiki Corrected"]
        values = [
            r["lambda_trends"],
            r["lambda_wiki_raw"],
            r["lambda_wiki_corrected"]
        ]

        plt.figure()
        plt.bar(labels, values)
        plt.title(r["symbol"])
        plt.ylabel("Lambda")
        plt.savefig(f"{r['symbol']}_lambda_comparison.png")
        plt.close()
