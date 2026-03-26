"""
calibrate_alpha.py — Calibrate alpha (PE/ICI weight) for SRM D operationalization
Politomorphism Research Project | Serban Gabriel Florin
License: CC BY 4.0

Citește valorile reale PE/ICI din D_result_<Symbol>.json (produse de compute_D.py).
Dacă un fișier lipsește, folosește estimările structurale ca fallback.
"""

import numpy as np
import json
import glob
from scipy.optimize import minimize_scalar
from scipy.stats import pearsonr, spearmanr


# ── DATASET (fallback — estimări structurale) ─────────────────────────────────
# Coloana json_symbol = valoarea exactă din --symbol când ai rulat compute_D.py
CASES_FALLBACK = [
    # name,                  D_legacy,  PE_est,  ICI_est,  lam,    typology,                   json_symbol
    ("Sunflower Movement",   0.774,     0.72,    0.83,     None,   "Civic Mobilization",       "Sunflower Movement"),
    ("Călin Georgescu",      0.881,     0.65,    0.97,     65.33,  "Flash Viral",              "Georgescu"),
    ("Marcel Ciolacu",       0.841,     0.78,    0.88,     6.57,   "Campaign/Ascension",       "Ciolacu"),
    ("Donald Trump",         0.734,     0.75,    0.71,     7.01,   "Campaign/Ascension",       "Trump"),
    ("Volodymyr Zelensky",   0.680,     0.60,    0.74,     5.11,   "Institutionally Durable",  "Zelensky"),
    ("Vladimir Putin",       0.847,     0.80,    0.89,     4.90,   "Institutionally Durable",  "Putin"),
    ("George Simion",        0.812,     0.70,    0.86,     12.41,  "Electorally Volatile",     "Simion"),
    ("Viktor Orbán",         0.798,     0.82,    0.77,     2.31,   "Institutionally Durable",  "Orban"),
    ("Nelson Mandela",       0.742,     0.68,    0.79,     19.66,  "Electorally Volatile",     "Mandela"),
    ("Emmanuel Macron",      0.810,     0.77,    0.84,     12.53,  "Electorally Volatile",     "Macron"),
    ("Hugo Chávez (sust.)",  0.720,     0.71,    0.73,     16.67,  "Electorally Volatile",     "Chavez"),
    ("Hugo Chávez (acute)",  0.380,     0.30,    0.44,     16.67,  "Electorally Volatile",     "Chavez_acute"),
]

FALLBACK_BY_NAME     = {c[0]: c for c in CASES_FALLBACK}
FALLBACK_BY_JSON_SYM = {c[6]: c for c in CASES_FALLBACK}


# ── LOAD REAL VALUES FROM compute_D.py OUTPUT ────────────────────────────────

def load_real_values():
    """
    Scanează toate D_result_*.json din directorul curent.
    FIX 1: citește din data["D_result"] (nested), nu de la rădăcină.
    FIX 2: curăță ghilimelele extra din symbol (bug vechi workflow).
    """
    real = {}
    for path in glob.glob("D_result_*.json"):
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)

            symbol = data.get("symbol") or data.get("name")

            # FIX 1: valorile sunt în data["D_result"], nu la rădăcină
            inner = data.get("D_result", data)

            pe  = inner.get("PE")  or inner.get("pe")
            ici = inner.get("ICI") or inner.get("ici")
            d   = inner.get("D")   or inner.get("D_new") or inner.get("d")

            # FIX 2: curăță ghilimelele extra
            if symbol:
                symbol = symbol.strip().strip('"')

            if symbol and pe is not None and ici is not None:
                real[symbol] = {
                    "PE":    float(pe),
                    "ICI":   float(ici),
                    "D":     float(d) if d is not None else None,
                    "_norm": symbol.lower().strip()
                }
                print(f"  ✓ {symbol}: PE={pe}, ICI={ici}, D={d}  [{path}]")
        except Exception as e:
            print(f"  ⚠ Could not read {path}: {e}")
    return real


def find_real(real: dict, name: str):
    """
    Match în trei trepte:
    1. Exact
    2. Normalizat (lowercase, strip)
    3. Parțial (name conținut în cheie sau invers)
    """
    if not name:
        return None
    if name in real:
        return real[name]
    norm = name.lower().strip()
    for v in real.values():
        if v.get("_norm") == norm:
            return v
    for k, v in real.items():
        if norm in k.lower() or k.lower() in norm:
            return v
    return None


def build_dataset():
    """
    Combină valorile reale (din JSON) cu fallback-urile hardcodate.
    FIX 3: matching folosește json_symbol (coloana 7) înainte de name.
    """
    real = load_real_values()
    sources = {}

    names, d_leg, pe_arr, ici_arr, lambdas, types = [], [], [], [], [], []

    for c in CASES_FALLBACK:
        name, d_legacy, pe_est, ici_est, lam, typ, json_sym = c

        # Încearcă json_symbol primul, apoi name complet
        match = find_real(real, json_sym) or find_real(real, name)

        if match:
            pe  = match["PE"]
            ici = match["ICI"]
            src = "compute_D.py (real)"
        else:
            pe  = pe_est
            ici = ici_est
            src = "structural estimate (fallback)"

        names.append(name)
        d_leg.append(d_legacy)
        pe_arr.append(pe)
        ici_arr.append(ici)
        lambdas.append(lam)
        types.append(typ)
        sources[name] = src

    for sym in real:
        if sym not in FALLBACK_BY_JSON_SYM and sym not in FALLBACK_BY_NAME:
            print(f"  ℹ '{sym}' găsit în JSON dar nu în CASES_FALLBACK — omis din calibrare")

    return (names,
            np.array(d_leg),
            np.array(pe_arr),
            np.array(ici_arr),
            lambdas,
            types,
            sources)


# ── CALIBRATION FUNCTIONS ─────────────────────────────────────────────────────

def D_new(alpha, PE, ICI):
    return alpha * PE + (1 - alpha) * ICI


def calibrate_global(NAMES, D_legacy, PE_est, ICI_est):
    def rmse(alpha):
        return float(np.sqrt(np.mean((D_new(alpha, PE_est, ICI_est) - D_legacy) ** 2)))
    def mae(alpha):
        return float(np.mean(np.abs(D_new(alpha, PE_est, ICI_est) - D_legacy)))

    result    = minimize_scalar(rmse, bounds=(0.0, 1.0), method="bounded")
    alpha_opt = round(result.x, 4)

    pred_opt = D_new(alpha_opt, PE_est, ICI_est)
    r_p, p_p = pearsonr(pred_opt, D_legacy)
    r_s, p_s = spearmanr(pred_opt, D_legacy)

    return {
        "alpha_optimal":      alpha_opt,
        "RMSE_at_alpha_opt":  round(result.fun, 4),
        "MAE_at_alpha_opt":   round(mae(alpha_opt), 4),
        "RMSE_at_alpha_05":   round(rmse(0.5), 4),
        "MAE_at_alpha_05":    round(mae(0.5), 4),
        "pearson_r":          round(float(r_p), 4),
        "pearson_p":          round(float(p_p), 4),
        "spearman_r":         round(float(r_s), 4),
        "spearman_p":         round(float(p_s), 4),
        "verdict": "Use alpha=0.5" if abs(alpha_opt - 0.5) < 0.05
                   else f"Consider updating to alpha={alpha_opt}"
    }


def calibrate_by_typology(NAMES, D_legacy, PE_est, ICI_est, TYPES):
    results = {}
    for typ in set(TYPES):
        idx = [i for i, t in enumerate(TYPES) if t == typ]
        if len(idx) < 2:
            results[typ] = {"n": len(idx), "note": "Insufficient cases (n<2)"}
            continue
        PE_t  = PE_est[idx]
        ICI_t = ICI_est[idx]
        D_t   = D_legacy[idx]

        def rmse_t(alpha):
            return float(np.sqrt(np.mean((D_new(alpha, PE_t, ICI_t) - D_t) ** 2)))

        res     = minimize_scalar(rmse_t, bounds=(0.0, 1.0), method="bounded")
        alpha_t = round(res.x, 4)
        interp  = ("ICI-dominant" if alpha_t < 0.35 else
                   "PE-dominant"  if alpha_t > 0.65 else "Balanced")
        results[typ] = {
            "n":             len(idx),
            "cases":         [NAMES[i] for i in idx],
            "alpha_optimal": alpha_t,
            "RMSE":          round(res.fun, 4),
            "PE_mean":       round(float(PE_t.mean()), 4),
            "ICI_mean":      round(float(ICI_t.mean()), 4),
            "D_legacy_mean": round(float(D_t.mean()), 4),
            "interpretation": interp
        }
    return results


def per_case_decomposition(NAMES, D_legacy, PE_est, ICI_est, TYPES, sources, alpha=0.5):
    rows = []
    for i, name in enumerate(NAMES):
        d = round(D_new(alpha, PE_est[i], ICI_est[i]), 4)
        rows.append({
            "symbol":      name,
            "typology":    TYPES[i],
            "D_legacy":    D_legacy[i],
            "PE":          PE_est[i],
            "ICI":         ICI_est[i],
            "D_new":       d,
            "delta":       round(d - D_legacy[i], 4),
            "dominant":    "PE" if PE_est[i] > ICI_est[i] else "ICI",
            "data_source": sources.get(name, "unknown"),
        })
    return rows


def test_H1(NAMES, PE_est, ICI_est, TYPES):
    flash     = [i for i, t in enumerate(TYPES) if t == "Flash Viral"]
    non_flash = [i for i, t in enumerate(TYPES) if t != "Flash Viral"]
    f_ratio   = np.mean([ICI_est[i] / PE_est[i] for i in flash])
    nf_ratio  = np.mean([ICI_est[i] / PE_est[i] for i in non_flash])
    return {
        "hypothesis":            "H1: Flash Viral symbols are ICI-dominant (ICI > PE)",
        "flash_viral_cases":     [NAMES[i] for i in flash],
        "flash_ICI_mean":        round(float(np.mean([ICI_est[i] for i in flash])), 4),
        "flash_PE_mean":         round(float(np.mean([PE_est[i] for i in flash])), 4),
        "flash_ICI_PE_ratio":    round(float(f_ratio), 4),
        "nonflash_ICI_PE_ratio": round(float(nf_ratio), 4),
        "supported": bool(f_ratio > nf_ratio and
                          all(ICI_est[i] > PE_est[i] for i in flash)),
    }


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n=== calibrate_alpha.py ===")

    NAMES, D_legacy, PE_est, ICI_est, LAMBDAS, TYPES, sources = build_dataset()

    real_count = sum(1 for s in sources.values() if "real" in s)
    print(f"\nDate reale disponibile: {real_count}/{len(NAMES)} simboluri")
    if real_count < len(NAMES):
        fallback_list = [n for n, s in sources.items() if "fallback" in s]
        print(f"Fallback estimat pentru: {fallback_list}\n")

    print("--- Global alpha calibration ---")
    global_result = calibrate_global(NAMES, D_legacy, PE_est, ICI_est)
    for k, v in global_result.items():
        print(f"  {k}: {v}")

    print("\n--- Per-typology calibration ---")
    typo_result = calibrate_by_typology(NAMES, D_legacy, PE_est, ICI_est, TYPES)
    for typ, res in typo_result.items():
        print(f"\n  [{typ}]")
        for k, v in res.items():
            print(f"    {k}: {v}")

    print("\n--- Per-case decomposition (alpha=0.5) ---")
    cases = per_case_decomposition(NAMES, D_legacy, PE_est, ICI_est, TYPES, sources)
    print(f"  {'Symbol':<30} {'D_leg':>6} {'PE':>6} {'ICI':>6} {'D_new':>6} {'Δ':>6} {'Src':>5}")
    print("  " + "-" * 75)
    for c in cases:
        src_tag = "REAL" if "real" in c["data_source"] else "est."
        print(f"  {c['symbol']:<30} {c['D_legacy']:>6.3f} {c['PE']:>6.3f} "
              f"{c['ICI']:>6.3f} {c['D_new']:>6.3f} {c['delta']:>+6.3f} {src_tag:>5}")

    print("\n--- H1 test ---")
    h1 = test_H1(NAMES, PE_est, ICI_est, TYPES)
    for k, v in h1.items():
        print(f"  {k}: {v}")

    output = {
        "data_sources":           sources,
        "real_values_count":      real_count,
        "total_cases":            len(NAMES),
        "global_calibration":     global_result,
        "typology_calibration":   typo_result,
        "per_case_decomposition": cases,
        "H1_test":                h1
    }
    with open("alpha_calibration_results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print("\nSaved: alpha_calibration_results.json")
