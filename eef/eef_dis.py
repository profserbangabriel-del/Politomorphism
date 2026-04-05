"""
EEF — Distributional Instability Score (DIS)
=============================================
Version 2.0 — Combined fuzzy membership + severity weighting

Replaces pure Shannon entropy with a composite score that captures
two independent dimensions of institutional instability:

  H(p) = Shannon entropy component  — distributional uncertainty
          "How uncertain is the system between institutional states?"

  G(p) = Severity component         — weighted state severity
          "How serious is the dominant institutional state?"

  DIS(p) = w_H * H_norm(p) + w_G * G(p)    [default: w_H = w_G = 0.5]

Properties:
  p = [1, 0, 0]  fully stable    -> DIS = 0.00  (LOW)
  p = [0, 0, 1]  fully critical  -> DIS = 0.50  (MODERATE)
  p = [.33,.33,.33] uniform      -> DIS = 0.75  (CRITICAL)
  p = [0, 1, 0]  purely strained -> DIS = 0.25  (LOW)

Interpretation:
  DIS is maximized when both uncertainty AND severity are high simultaneously.
  A fully captured authoritarian system (low uncertainty, high severity)
  scores lower than a contested system (high uncertainty, mixed severity).
  This correctly distinguishes democratic backsliding (HIGH DIS) from
  completed autocratic consolidation (MODERATE DIS).

Zones (recalibrated for DIS scale):
  DIS > 0.65  ->  CRITICAL
  DIS 0.45-0.65  ->  HIGH
  DIS 0.25-0.45  ->  MODERATE
  DIS < 0.25  ->  LOW

Fuzzy membership functions:
  trimf(x, a, b, c) — triangular
  smf(x, a, b)      — S-shaped (sigmoid-like, rising)
  zmf(x, a, b)      — Z-shaped (sigmoid-like, falling)

Author : Prof. Serban Gabriel Florin | ORCID: 0009-0000-2266-3356
Project: Politomorphism Engine | OSF: 10.17605/OSF.IO/HYDNZ
Script : eef/eef_dis.py
"""

import math
import csv

# ── FUZZY PRIMITIVES ──────────────────────────────────────────────────────────

def smf(x, a, b):
    """S-shaped membership: 0 at x<=a, 1 at x>=b, smooth in between."""
    if x <= a: return 0.0
    if x >= b: return 1.0
    if x <= (a + b) / 2:
        return 2 * ((x - a) / (b - a)) ** 2
    return 1 - 2 * ((x - b) / (b - a)) ** 2

def zmf(x, a, b):
    """Z-shaped membership: 1 at x<=a, 0 at x>=b."""
    return 1.0 - smf(x, a, b)

def normalize(mus):
    """Normalize membership values to sum to 1."""
    total = sum(mus) + 1e-10
    return [round(m / total, 6) for m in mus]


# ── FUZZY MEMBERSHIP FUNCTIONS ────────────────────────────────────────────────
#
# Design: all three membership functions are active simultaneously
# in the middle range, producing smooth three-way distributions.
# Overlap is intentionally wide to avoid discontinuous jumps.

def fuzzy_fh_judicial(score):
    """
    FH NIT Judicial Framework & Independence (1-7 scale).
    S0 rises from 3.0; S2 falls from 5.0; S1 peaks at 4.0.
    Wide overlap ensures smooth transition around 3.0-5.0.
    """
    mu_s0 = smf(score, 3.0, 6.0)
    mu_s1 = max(0.0, 1.0 - abs(score - 4.0) / 3.5)
    mu_s2 = zmf(score, 1.0, 5.0)
    return normalize([mu_s0, mu_s1, mu_s2])

def fuzzy_fh_electoral(score):
    """
    FH NIT Electoral Process (1-7 scale).
    Slightly more sensitive to low scores than Judicial
    (elections are discrete events; collapse is faster).
    S1 peaks at 3.75 reflecting the contested midrange.
    """
    mu_s0 = smf(score, 3.0, 6.0)
    mu_s1 = max(0.0, 1.0 - abs(score - 3.75) / 3.25)
    mu_s2 = zmf(score, 1.0, 5.0)
    return normalize([mu_s0, mu_s1, mu_s2])

def fuzzy_bti_participation(score):
    """
    BTI Political Participation (1-10 scale).
    Context-calibrated for Central/Eastern Europe:
    BTI 7.0 (= 70% of maximum) treated as strained, not stable,
    reflecting regional institutional norms.
    S0 rises from 4.5; S2 falls from 7.5; S1 peaks at 6.0.
    """
    mu_s0 = smf(score, 4.5, 9.0)
    mu_s1 = max(0.0, 1.0 - abs(score - 6.0) / 5.0)
    mu_s2 = zmf(score, 1.0, 7.5)
    return normalize([mu_s0, mu_s1, mu_s2])


# ── DIS SCORE ─────────────────────────────────────────────────────────────────

def H_norm(p):
    """Normalized Shannon entropy: 0 (certain) to 1 (uniform)."""
    s = -sum(x * math.log(x) for x in p if x > 0)
    return s / math.log(len(p))

def G(p):
    """
    Weighted severity score: 0 (fully stable) to 1 (fully critical).
    S0 contributes 0.0 (stable = no instability)
    S1 contributes 0.5 (strained = partial instability)
    S2 contributes 1.0 (critical = full instability)
    """
    return p[0] * 0.0 + p[1] * 0.5 + p[2] * 1.0

def DIS(p, w_H=0.5, w_G=0.5):
    """
    Distributional Instability Score.
    Combines entropy uncertainty and severity weighting.
    Default weights: equal contribution (0.5 / 0.5).
    """
    return w_H * H_norm(p) + w_G * G(p)

def dis_zone(dis_value):
    """Zone classification on DIS scale."""
    if dis_value > 0.65:   return "CRITICAL"
    elif dis_value > 0.45: return "HIGH"
    elif dis_value > 0.25: return "MODERATE"
    else:                  return "LOW"


# ── RAW DATA ──────────────────────────────────────────────────────────────────

FH_JUDICIAL = {
    "Romania": {
        2005:3.50, 2006:3.50, 2007:3.75, 2008:3.75, 2009:4.00,
        2010:4.00, 2011:3.75, 2012:3.75, 2013:4.00, 2014:4.00,
        2015:4.25, 2016:4.25, 2017:4.00, 2018:3.75, 2019:3.75,
        2020:4.00, 2021:4.00, 2022:4.00, 2023:4.25, 2024:4.50,
    },
    "Hungary": {
        2005:4.25, 2006:4.25, 2007:4.25, 2008:4.25, 2009:4.25,
        2010:4.00, 2011:3.50, 2012:3.00, 2013:2.75, 2014:2.50,
        2015:2.25, 2016:2.00, 2017:2.00, 2018:2.00, 2019:2.00,
        2020:2.00, 2021:1.75, 2022:1.75, 2023:1.75, 2024:1.75,
    },
    "Poland": {
        2005:4.25, 2006:4.25, 2007:4.50, 2008:4.50, 2009:4.50,
        2010:4.50, 2011:4.50, 2012:4.75, 2013:4.75, 2014:4.75,
        2015:4.75, 2016:4.25, 2017:3.75, 2018:3.50, 2019:3.25,
        2020:3.00, 2021:3.00, 2022:3.00, 2023:3.25, 2024:3.50,
    },
}

FH_ELECTORAL = {
    "Romania": {
        2005:3.25, 2006:3.25, 2007:3.50, 2008:3.50, 2009:3.50,
        2010:3.50, 2011:3.50, 2012:3.50, 2013:3.75, 2014:3.75,
        2015:3.75, 2016:3.75, 2017:3.75, 2018:3.75, 2019:3.75,
        2020:3.75, 2021:3.75, 2022:3.75, 2023:3.75, 2024:3.25,
    },
    "Hungary": {
        2005:4.00, 2006:4.00, 2007:4.00, 2008:4.00, 2009:3.75,
        2010:3.75, 2011:3.50, 2012:3.25, 2013:3.00, 2014:2.75,
        2015:2.75, 2016:2.75, 2017:2.50, 2018:2.50, 2019:2.50,
        2020:2.50, 2021:2.25, 2022:2.25, 2023:2.25, 2024:2.00,
    },
    "Poland": {
        2005:4.50, 2006:4.50, 2007:4.75, 2008:4.75, 2009:4.75,
        2010:4.75, 2011:4.75, 2012:4.75, 2013:4.75, 2014:4.75,
        2015:4.75, 2016:4.50, 2017:4.25, 2018:4.00, 2019:4.00,
        2020:3.75, 2021:3.75, 2022:3.75, 2023:3.75, 2024:4.00,
    },
}

BTI_BIENNIAL = {
    "Romania": {2006:7.5,2008:7.5,2010:7.5,2012:7.0,2014:7.5,
                2016:7.5,2018:7.5,2020:7.0,2022:7.0,2024:7.0},
    "Hungary": {2006:8.5,2008:8.5,2010:8.0,2012:7.0,2014:6.0,
                2016:5.5,2018:5.0,2020:4.5,2022:4.5,2024:4.5},
    "Poland":  {2006:9.0,2008:9.0,2010:9.0,2012:9.0,2014:9.0,
                2016:8.5,2018:7.5,2020:7.0,2022:7.0,2024:7.5},
}

ELECTORAL_OVERRIDES = {
    ("Hungary", 2011): [0.05, 0.45, 0.50],
    ("Hungary", 2014): [0.05, 0.40, 0.55],
    ("Poland",  2015): [0.20, 0.55, 0.25],
    ("Poland",  2019): [0.08, 0.48, 0.44],
    ("Romania", 2024): [0.08, 0.52, 0.40],
}

YEARS     = list(range(2005, 2025))
COUNTRIES = ["Romania", "Hungary", "Poland"]


def interpolate_bti(country, year):
    data = BTI_BIENNIAL[country]
    if year in data:
        return data[year]
    ys = sorted(data.keys())
    for i in range(len(ys)-1):
        y0, y1 = ys[i], ys[i+1]
        if y0 < year < y1:
            return data[y0] + (data[y1]-data[y0])*(year-y0)/(y1-y0)
    return data[ys[0]] if year < ys[0] else data[ys[-1]]


# ── COMPUTE ───────────────────────────────────────────────────────────────────

def compute_all(w_H=0.5, w_G=0.5):
    results = {}
    for country in COUNTRIES:
        results[country] = {}
        prev_DIS = None
        for year in YEARS:
            fhj  = FH_JUDICIAL[country].get(year)
            fhe  = FH_ELECTORAL[country].get(year)
            bti  = interpolate_bti(country, year)
            if fhj is None or fhe is None:
                continue

            p_j = fuzzy_fh_judicial(fhj)
            p_e = ELECTORAL_OVERRIDES.get((country, year),
                  fuzzy_fh_electoral(fhe))
            p_c = fuzzy_bti_participation(bti)

            dis_j = DIS(p_j, w_H, w_G)
            dis_e = DIS(p_e, w_H, w_G)
            dis_c = DIS(p_c, w_H, w_G)

            # Component breakdown for transparency
            h_j, g_j = H_norm(p_j), G(p_j)
            h_e, g_e = H_norm(p_e), G(p_e)
            h_c, g_c = H_norm(p_c), G(p_c)

            dis_eef = (dis_j + dis_e + dis_c) / 3
            zone    = dis_zone(dis_eef)

            if prev_DIS is not None:
                delta   = dis_eef - prev_DIS
                trend   = ("DETERIORATING" if delta >  0.005 else
                           "CONSOLIDATING" if delta < -0.005 else
                           "STABLE")
            else:
                delta = None
                trend = "baseline"

            results[country][year] = {
                "country": country, "year": year,
                "FH_Judicial": fhj, "FH_Electoral": fhe,
                "BTI": round(bti, 2),
                # probability vectors
                "p_Justice":   p_j,
                "p_Electoral": p_e,
                "p_Coalition": p_c,
                # entropy components
                "H_Justice":   round(h_j*100, 2),
                "G_Justice":   round(g_j*100, 2),
                "H_Electoral": round(h_e*100, 2),
                "G_Electoral": round(g_e*100, 2),
                "H_Coalition": round(h_c*100, 2),
                "G_Coalition": round(g_c*100, 2),
                # DIS scores
                "DIS_Justice":   round(dis_j*100, 2),
                "DIS_Electoral": round(dis_e*100, 2),
                "DIS_Coalition": round(dis_c*100, 2),
                "DIS_EEF":       round(dis_eef*100, 2),
                "zone":          zone,
                "delta_DIS":     round(delta*100, 3) if delta is not None else None,
                "trend":         trend,
                "override":      (country, year) in ELECTORAL_OVERRIDES,
            }
            prev_DIS = dis_eef

    return results


# ── SENSITIVITY: WEIGHT ANALYSIS ──────────────────────────────────────────────

def weight_sensitivity(country="Romania", year=2024):
    """
    Show how DIS_EEF changes as w_H varies from 0 to 1.
    Demonstrates robustness of zone classification to weight choice.
    """
    print(f"\n{'─'*60}")
    print(f"  Weight Sensitivity — {country} {year}")
    print(f"  w_H = weight of entropy component")
    print(f"  w_G = 1 - w_H = weight of severity component")
    print(f"{'─'*60}")
    print(f"  {'w_H':>5} {'w_G':>5}  {'DIS_J%':>7} {'DIS_E%':>7} "
          f"{'DIS_C%':>7} {'DIS_EEF%':>9}  Zone")
    print(f"  {'─'*56}")

    fhj = FH_JUDICIAL[country].get(year)
    fhe = FH_ELECTORAL[country].get(year)
    bti = interpolate_bti(country, year)
    p_j = fuzzy_fh_judicial(fhj)
    p_e = ELECTORAL_OVERRIDES.get((country, year), fuzzy_fh_electoral(fhe))
    p_c = fuzzy_bti_participation(bti)

    for w in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
        dj = DIS(p_j, w, 1-w)*100
        de = DIS(p_e, w, 1-w)*100
        dc = DIS(p_c, w, 1-w)*100
        deef = (dj+de+dc)/3
        z = dis_zone(deef/100)
        marker = " <-- default" if abs(w-0.5) < 0.01 else ""
        print(f"  {w:>5.1f} {1-w:>5.1f}  {dj:>7.1f} {de:>7.1f} "
              f"{dc:>7.1f} {deef:>9.1f}  {z}{marker}")


# ── PRINT ─────────────────────────────────────────────────────────────────────

def print_results(results):
    for country in COUNTRIES:
        rows = sorted(results[country].values(), key=lambda r: r["year"])
        print(f"\n{'='*82}")
        print(f"  DIS — {country.upper()}")
        print(f"{'='*82}")
        print(f"  {'Yr':>4}  {'FHJ':>5} {'FHE':>5} {'BTI':>5}  "
              f"{'H-J%':>6} {'G-J%':>6}  "
              f"{'DIS-J%':>7} {'DIS-E%':>7} {'DIS-C%':>7}  "
              f"{'DIS_EEF%':>9}  {'Zone':>10}  Trend")
        print(f"  {'─'*80}")
        for r in rows:
            print(f"  {r['year']:>4}  {r['FH_Judicial']:>5.2f} "
                  f"{r['FH_Electoral']:>5.2f} {r['BTI']:>5.2f}  "
                  f"{r['H_Justice']:>6.1f} {r['G_Justice']:>6.1f}  "
                  f"{r['DIS_Justice']:>7.1f} {r['DIS_Electoral']:>7.1f} "
                  f"{r['DIS_Coalition']:>7.1f}  "
                  f"{r['DIS_EEF']:>9.1f}  {r['zone']:>10}  {r['trend']}")


def export_csv(results, path="EEF_DIS_All.csv"):
    fields = [
        "country","year","FH_Judicial","FH_Electoral","BTI",
        "p0_Justice","p1_Justice","p2_Justice",
        "p0_Electoral","p1_Electoral","p2_Electoral",
        "p0_Coalition","p1_Coalition","p2_Coalition",
        "H_Justice","G_Justice","H_Electoral","G_Electoral",
        "H_Coalition","G_Coalition",
        "DIS_Justice","DIS_Electoral","DIS_Coalition",
        "DIS_EEF","zone","delta_DIS","trend","override"
    ]
    rows = []
    for country in COUNTRIES:
        for year in YEARS:
            if year in results[country]:
                r = results[country][year]
                rows.append({
                    "country": r["country"], "year": r["year"],
                    "FH_Judicial": r["FH_Judicial"],
                    "FH_Electoral": r["FH_Electoral"],
                    "BTI": r["BTI"],
                    "p0_Justice":   r["p_Justice"][0],
                    "p1_Justice":   r["p_Justice"][1],
                    "p2_Justice":   r["p_Justice"][2],
                    "p0_Electoral": r["p_Electoral"][0],
                    "p1_Electoral": r["p_Electoral"][1],
                    "p2_Electoral": r["p_Electoral"][2],
                    "p0_Coalition": r["p_Coalition"][0],
                    "p1_Coalition": r["p_Coalition"][1],
                    "p2_Coalition": r["p_Coalition"][2],
                    "H_Justice":    r["H_Justice"],
                    "G_Justice":    r["G_Justice"],
                    "H_Electoral":  r["H_Electoral"],
                    "G_Electoral":  r["G_Electoral"],
                    "H_Coalition":  r["H_Coalition"],
                    "G_Coalition":  r["G_Coalition"],
                    "DIS_Justice":  r["DIS_Justice"],
                    "DIS_Electoral":r["DIS_Electoral"],
                    "DIS_Coalition":r["DIS_Coalition"],
                    "DIS_EEF":      r["DIS_EEF"],
                    "zone":         r["zone"],
                    "delta_DIS":    r["delta_DIS"],
                    "trend":        r["trend"],
                    "override":     r["override"],
                })
    rows.sort(key=lambda r: (r["country"], r["year"]))
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"\n  CSV exported: {path}")


# ── SUMMARY COMPARISON TABLE ──────────────────────────────────────────────────

def print_summary(results):
    print(f"\n{'='*70}")
    print(f"  DIS CROSS-NATIONAL SUMMARY 2024")
    print(f"  DIS = 0.5 * H_norm(p) + 0.5 * G(p)")
    print(f"{'='*70}")
    print(f"  {'Country':<10} {'DIS-J%':>8} {'DIS-E%':>8} {'DIS-C%':>8} "
          f"{'DIS_EEF%':>10}  Zone")
    print(f"  {'─'*60}")
    for country in COUNTRIES:
        if 2024 in results[country]:
            r = results[country][2024]
            print(f"  {country:<10} {r['DIS_Justice']:>8.1f} "
                  f"{r['DIS_Electoral']:>8.1f} {r['DIS_Coalition']:>8.1f} "
                  f"{r['DIS_EEF']:>10.1f}  {r['zone']}")

    print(f"\n  Interpretation:")
    print(f"  CRITICAL (DIS>0.65): High uncertainty AND high severity")
    print(f"  HIGH     (DIS>0.45): Significant instability, one dimension dominant")
    print(f"  MODERATE (DIS>0.25): Manageable tensions")
    print(f"  LOW      (DIS<0.25): Near equilibrium")
    print(f"{'='*70}")


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n  Politomorphism Engine — EEF Distributional Instability Score (DIS)")
    print(f"  Countries : {', '.join(COUNTRIES)}")
    print(f"  Period    : {YEARS[0]}–{YEARS[-1]}")
    print(f"  Formula   : DIS = 0.5 * H_norm(p) + 0.5 * G(p)")
    print(f"  Mapping   : Continuous fuzzy membership (smf / zmf)")

    results = compute_all()
    print_summary(results)
    print_results(results)

    # Weight sensitivity for Romania 2024
    weight_sensitivity("Romania", 2024)
    weight_sensitivity("Hungary", 2024)

    export_csv(results)
    print("\n  Done.\n")
