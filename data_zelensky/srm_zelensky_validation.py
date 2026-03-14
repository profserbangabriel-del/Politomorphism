"""
Social Resonance Model (SRM) — Validation on "Volodymyr Zelensky" Symbol
=========================================================================
Part of the Politomorphism Research Project
Author: Serban Gabriel Florin
GitHub: profserbangabriel-del/politomorphism

Methodology: mirrors SRM_Trump_Validation.docx
Data: Media Cloud (mediacloud.org)
  - first_period  : baseline pre-invasion  (May 2019 – Feb 2022)
  - second_period : main analysis period   (May 2022 – Feb 2026)
  - usa_collection: US National collection (May 2022 – Feb 2026)
  - europe_collection: Europe collection   (May 2022 – Feb 2026)

SRM Formula:  SRM = V × A × e^(−λD) × N    (λ = 2)
"""

import csv
import json
import math
import statistics
import os
from datetime import datetime

# ──────────────────────────────────────────────
# 0. CONFIG — adjust paths if running locally
# ──────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

FILES = {
    "first_period":  "counts_zelensky_first_period.csv",
    "second_period": "counts_zelensky_second_period.csv",
    "usa":           "counts_zelensky_usa.csv",
    "europe":        "counts_zelensky_europe.csv",
}

LAMBDA = 2  # exponential penalization factor (same as Trump validation)

# ──────────────────────────────────────────────
# A and D: set manually after expert analysis
# (same approach as Trump: D was expert-estimated,
#  A via VADER — instructions in README.md)
# ──────────────────────────────────────────────
A_AFFECTIVE_WEIGHT = float(os.environ.get("SRM_A", "0.640"))
D_SEMANTIC_DRIFT   = float(os.environ.get("SRM_D", "0.680"))


# ──────────────────────────────────────────────
# 1. UTILS
# ──────────────────────────────────────────────
def load_csv(filename: str) -> list[dict]:
    path = os.path.join(DATA_DIR, filename)
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def safe_float(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


# ──────────────────────────────────────────────
# 2. LOAD DATA
# ──────────────────────────────────────────────
print("=" * 60)
print("SRM VALIDATION — 'zelensky' symbol")
print("=" * 60)

first   = load_csv(FILES["first_period"])
second  = load_csv(FILES["second_period"])
usa     = load_csv(FILES["usa"])
europe  = load_csv(FILES["europe"])

print(f"\n[DATA LOADED]")
print(f"  first_period  : {first[0]['date']} → {first[-1]['date']}  ({len(first)} rows)")
print(f"  second_period : {second[0]['date']} → {second[-1]['date']}  ({len(second)} rows)")
print(f"  usa           : {usa[0]['date']} → {usa[-1]['date']}  ({len(usa)} rows)")
print(f"  europe        : {europe[0]['date']} → {europe[-1]['date']}  ({len(europe)} rows)")


# ──────────────────────────────────────────────
# 3. VARIABLE V — Viral Velocity
#
# Method: log-normalized escalation ratio
#   escalation = peak_ratio / baseline_mean
#   V = log(escalation) / log(100)   [capped at 1.0]
#
# Baseline: mean daily ratio in first_period (pre-invasion)
# Peak    : max daily ratio in usa collection (post-invasion)
#
# Same formula used for Trump (82.3x escalation → V=0.958)
# ──────────────────────────────────────────────

baseline_ratios = [safe_float(r["ratio"]) for r in first if safe_float(r["ratio"]) > 0]
baseline_mean   = statistics.mean(baseline_ratios)

# Find peak day in USA collection (primary corpus, like Trump used US National)
usa_by_ratio = sorted(usa, key=lambda r: safe_float(r["ratio"]), reverse=True)
peak_row_usa  = usa_by_ratio[0]
peak_ratio_usa = safe_float(peak_row_usa["ratio"])
escalation_usa = peak_ratio_usa / baseline_mean

# Also compute for Europe (cross-validation)
europe_by_ratio   = sorted(europe, key=lambda r: safe_float(r["ratio"]), reverse=True)
peak_row_europe   = europe_by_ratio[0]
peak_ratio_europe = safe_float(peak_row_europe["ratio"])
escalation_europe = peak_ratio_europe / baseline_mean

# Log-normalize (reference = 100x = V_max = 1.0)
V_usa    = min(math.log(escalation_usa)    / math.log(100), 1.0) if escalation_usa    > 1 else 0.0
V_europe = min(math.log(escalation_europe) / math.log(100), 1.0) if escalation_europe > 1 else 0.0

# Use the average of both collections as final V
V = round((V_usa + V_europe) / 2, 4)

print(f"\n[V — VIRAL VELOCITY]")
print(f"  Baseline mean ratio (first_period): {baseline_mean:.6f}")
print(f"  Peak ratio USA     : {peak_ratio_usa:.6f}  ({peak_row_usa['date']})")
print(f"  Peak ratio Europe  : {peak_ratio_europe:.6f}  ({peak_row_europe['date']})")
print(f"  Escalation USA     : {escalation_usa:.1f}x  → V_usa    = {V_usa:.4f}")
print(f"  Escalation Europe  : {escalation_europe:.1f}x  → V_europe = {V_europe:.4f}")
print(f"  V (average)        = {V:.4f}")


# ──────────────────────────────────────────────
# 4. VARIABLE N — Network Coverage
#
# Method: proportion of days in analysis period
#   where the symbol appears in the corpus
#
# Use second_period as main collection
# (smaller, more conservative — avoids overestimation)
# Cross-check with USA + Europe for context.
# ──────────────────────────────────────────────

def coverage(rows):
    total   = len(rows)
    present = sum(1 for r in rows if int(r["count"]) > 0)
    return present / total if total > 0 else 0.0

N_second  = coverage(second)
N_usa     = coverage(usa)
N_europe  = coverage(europe)

# Final N: use second_period (conservative, avoids 1.0 saturation artefact)
N = round(N_second, 4)

print(f"\n[N — NETWORK COVERAGE]")
print(f"  second_period : {N_second:.4f}  ({sum(1 for r in second if int(r['count'])>0)}/{len(second)} days)")
print(f"  USA collection: {N_usa:.4f}  ({sum(1 for r in usa if int(r['count'])>0)}/{len(usa)} days)")
print(f"  Europe coll.  : {N_europe:.4f}  ({sum(1 for r in europe if int(r['count'])>0)}/{len(europe)} days)")
print(f"  N (second_period, conservative) = {N:.4f}")


# ──────────────────────────────────────────────
# 5. VARIABLE A — Affective Weight (VADER)
#
# Requires running vader_sentiment.py on actual
# article texts fetched from Media Cloud API.
# See README.md → Step 4 for full instructions.
#
# Value is injected via SRM_A environment variable
# (set in GitHub Actions secrets or .env file)
# ──────────────────────────────────────────────
A = round(A_AFFECTIVE_WEIGHT, 4)
print(f"\n[A — AFFECTIVE WEIGHT]")
print(f"  A = {A:.4f}  (VADER sentiment, set via SRM_A env var)")


# ──────────────────────────────────────────────
# 6. VARIABLE D — Semantic Drift
#
# Expert-estimated from frame analysis.
# Zelensky semantic frames identified:
#   1. War hero / resistance leader
#   2. Democratic legitimacy / elected president
#   3. NATO ally / Western proxy
#   4. Peace negotiator / diplomatic actor
#   5. Electoral legitimacy controversy (2024–2025)
#   6. Post-war political actor
#
# D=0.680 estimated: lower drift than Trump (0.734)
# — fewer competing frames, but still significant
# fragmentation between Western heroism narrative
# and realpolitik/negotiation discourse.
#
# Value injected via SRM_D environment variable.
# ──────────────────────────────────────────────
D = round(D_SEMANTIC_DRIFT, 4)
print(f"\n[D — SEMANTIC DRIFT]")
print(f"  D = {D:.4f}  (expert-estimated, set via SRM_D env var)")
print(f"  Semantic factor e^(−λD) = e^(−{LAMBDA}×{D}) = {math.exp(-LAMBDA*D):.4f}")


# ──────────────────────────────────────────────
# 7. SRM CALCULATION
# ──────────────────────────────────────────────
semantic_factor = math.exp(-LAMBDA * D)
SRM = V * A * semantic_factor * N

# Interpretation thresholds (from Trump paper)
def interpret(score):
    if score >= 0.20:
        return "HIGH RESONANCE"
    elif score >= 0.07:
        return "MEDIUM RESONANCE"
    elif score >= 0.02:
        return "LOW RESONANCE"
    else:
        return "MINIMAL RESONANCE"

interpretation = interpret(SRM)

print(f"\n{'=' * 60}")
print(f"SRM RESULT")
print(f"{'=' * 60}")
print(f"  V  (Viral Velocity)     = {V:.4f}")
print(f"  A  (Affective Weight)   = {A:.4f}")
print(f"  D  (Semantic Drift)     = {D:.4f}")
print(f"  e^(−λD) semantic factor = {semantic_factor:.4f}")
print(f"  N  (Network Coverage)   = {N:.4f}")
print(f"  ─────────────────────────────")
print(f"  SRM = {V} × {A} × {semantic_factor:.4f} × {N}")
print(f"  SRM = {SRM:.4f}")
print(f"  Interpretation: {interpretation}")
print(f"{'=' * 60}")


# ──────────────────────────────────────────────
# 8. COMPARATIVE TABLE (all 4 symbols)
# ──────────────────────────────────────────────
print(f"\n[COMPARATIVE DATASET — 4 Symbols]")
print(f"{'Symbol':<28} {'V':>6} {'A':>6} {'D':>6} {'N':>6} {'SRM':>8}  Interpretation")
print("-" * 80)

dataset = [
    ("Sunflower Mvt (TW, 2014)",    0.680, 0.420, 0.7737, 0.580),
    ("Călin Georgescu (RO, 2024)",  0.750, 0.398, 0.8813, 0.600),
    ("Donald Trump (US, 2015-16)",  0.958, 0.580, 0.7340, 0.720),
    (f"Zelensky (UA/EU, 2022-26)",  V,     A,     D,      N    ),
]

for name, v, a, d, n in dataset:
    sf    = math.exp(-LAMBDA * d)
    score = v * a * sf * n
    label = interpret(score)
    print(f"  {name:<26} {v:>6.3f} {a:>6.3f} {d:>6.4f} {n:>6.3f} {score:>8.4f}  {label}")

print()


# ──────────────────────────────────────────────
# 9. SAVE JSON RESULT
# ──────────────────────────────────────────────
result = {
    "symbol": "zelensky",
    "context": "UA/EU/US — 2022–2026",
    "generated_at": datetime.utcnow().isoformat() + "Z",
    "variables": {
        "V": V,
        "A": A,
        "D": D,
        "semantic_factor": round(semantic_factor, 4),
        "N": N,
        "lambda": LAMBDA,
    },
    "SRM": round(SRM, 4),
    "interpretation": interpretation,
    "data_summary": {
        "baseline_mean_ratio": round(baseline_mean, 6),
        "escalation_usa": round(escalation_usa, 1),
        "escalation_europe": round(escalation_europe, 1),
        "peak_date_usa": peak_row_usa["date"],
        "peak_date_europe": peak_row_europe["date"],
        "N_second_period": round(N_second, 4),
        "N_usa": round(N_usa, 4),
        "N_europe": round(N_europe, 4),
    }
}

output_path = os.path.join(os.path.dirname(__file__), "SRM_zelensky_result.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"[SAVED] {output_path}")
