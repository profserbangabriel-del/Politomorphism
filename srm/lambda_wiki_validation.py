"""
Lambda Robustness Test: Wikipedia Pageviews vs Google Trends
Politomorphism Framework — SRM Validation (Stratul 3)
"""

import requests
import numpy as np
from scipy.optimize import brentq
from scipy.stats import pearsonr, spearmanr
import json
import time

SYMBOLS = [
    ("IranIsrael",   "2024 Iran–Israel conflict",           0.5,   17.81),
    ("Chavez",       "Hugo Chávez",                         0.5,   16.67),
    ("Modi2014",     "Narendra Modi",                       0.6,    2.37),
    ("Trump",        "Donald Trump",                        1.0,    7.01),
    ("Modi2024",     "2024 Indian general election",        0.5,    9.11),
    ("Modi2019",     "2019 Indian general election",        0.5,    6.33),
    ("Sunflower",    "Sunflower Student Movement",          0.5,    2.00),
    ("Bolsonaro",    "Jair Bolsonaro",                      1.0,   10.43),
    ("Duterte",      "Rodrigo Duterte",                     0.5,    5.02),
    ("Buhari",       "Muhammadu Buhari",                    0.5,    7.95),
    ("Macron",       "Emmanuel Macron",                     0.5,   12.53),
    ("Netanyahu",    "Benjamin Netanyahu",                  1.0,    7.02),
    ("CharlieHebdo", "Charlie Hebdo shooting",              0.1,  104.66),
    ("Putin",        "Vladimir Putin",                      1.0,    4.90),
    ("Erdogan",      "Recep Tayyip Erdoğan",                0.5,   18.52),
    ("Simion",       "George Simion",                       0.5,   12.41),
    ("Ciolacu",      "Marcel Ciolacu",                      0.5,    6.57),
    ("Georgescu",    "Călin Georgescu",                     0.3,   65.33),
    ("Orban",        "Viktor Orbán",                        1.0,    2.31),
    ("Zelensky",     "Volodymyr Zelenskyy",                 1.0,    5.11),
    ("Mandela",      "Nelson Mandela",                      0.5,   19.66),
    ("ChavezAcute",  "Hugo Chávez",                         0.2,   16.67),
]

def get_wikipedia_pageviews(article_title):
    title_encoded = requests.utils.quote(
        article_title.replace(" ", "_"), safe=""
    )
    url = (
        f"https://en.wikipedia.org/w/api.php"
        f"?action=query&titles={title_encoded}"
        f"&prop=pageviews&pvipdays=365&format=json"
    )
    headers = {"User-Agent": "PolitomorphismResearch/1.0 (academic)"}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            pages = data.get("query", {}).get("pages", {})
            for page in pages.values():
                pv = page.get("pageviews", {})
                views = [v for v in pv.values() if v is not None]
                return views
        return None
    except Exception:
        return None

def compute_lambda(views, T_years):
    if not views or max(views) == 0:
        return None
    ratio = np.mean(views) / max(views)
    if ratio <= 0 or ratio >= 1:
        return None
    def eq(lam):
        if lam * T_years > 700:
            return ratio
        return (1 - np.exp(-lam * T_years)) / (lam * T_years) - ratio
    try:
        if eq(0.1) * eq(200) > 0:
            return None
        return round(brentq(eq, 0.1, 200, xtol=1e-6, maxiter=100), 4)
    except Exception:
        return None

def run():
    print("=" * 65)
    print("LAMBDA ROBUSTNESS TEST — Wikipedia vs Google Trends")
    print("=" * 65)

    results, failed = [], []

    for name, wiki_title, T, lam_t in SYMBOLS:
        print(f"[{name}] ...", end=" ", flush=True)
        views = get_wikipedia_pageviews(wiki_title)
        time.sleep(0.5)

        if not views or len(views) < 3:
            print("FAILED (no data)")
            failed.append(name)
            continue

        lam_w = compute_lambda(views, T)
        if lam_w is None:
            print("FAILED (compute error)")
            failed.append(name)
            continue

        pct = abs(lam_w - lam_t) / lam_t * 100
        results.append({
            "symbol": name,
            "lambda_trends": lam_t,
            "lambda_wiki": lam_w,
            "pct_diff": round(pct, 2),
            "n_days": len(views)
        })
        print(f"λ_trends={lam_t:.2f} | λ_wiki={lam_w:.2f} | Δ={pct:.1f}%")

    print()
    print("=" * 65)

    if len(results) < 5:
        print("Prea putine simboluri valide. Verifica conexiunea.")
        return

    lt = [r["lambda_trends"] for r in results]
    lw = [r["lambda_wiki"]   for r in results]

    r_p, p_p = pearsonr(np.log(lt), np.log(lw))
    r_s, p_s = spearmanr(lt, lw)
    mean_d   = np.mean([r["pct_diff"] for r in results])

    print(f"N valid:         {len(results)} / {len(SYMBOLS)}")
    print(f"Pearson r:       {r_p:.4f}  (p={p_p:.4f})")
    print(f"Spearman rho:    {r_s:.4f}  (p={p_s:.4f})")
    print(f"Deviatie medie:  {mean_d:.1f}%")
    print()

    if r_p >= 0.80 and p_p < 0.05:
        print("VERDICT: CIRCULARITATE BENIGNA CONFIRMATA")
        print(f"  r={r_p:.3f}, p={p_p:.4f} — obiecția metodologica este eliminata.")
    elif r_p >= 0.65:
        print("VERDICT: CORELARE MODERATA — argument partial.")
    else:
        print("VERDICT: CORELARE SLABA — investigheaza outlieri.")

    print()
    print(f"{'Symbol':<15} {'λ_trends':>10} {'λ_wiki':>10} {'Δ%':>8}")
    print("-" * 48)
    for r in sorted(results, key=lambda x: x["pct_diff"]):
        print(f"{r['symbol']:<15} {r['lambda_trends']:>10.2f}"
              f" {r['lambda_wiki']:>10.2f} {r['pct_diff']:>8.1f}%")

    if failed:
        print(f"\nFailed: {', '.join(failed)}")

    with open("lambda_wiki_results.json", "w") as f:
        json.dump({
            "pearson_r": r_p, "pearson_p": p_p,
            "spearman_r": r_s, "spearman_p": p_s,
            "mean_pct_diff": mean_d,
            "n_valid": len(results),
            "results": results,
            "failed": failed
        }, f, indent=2)
    print("\nSalvat: lambda_wiki_results.json")

if __name__ == "__main__":
    run()
