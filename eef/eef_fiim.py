"""
EEF — Fuzzy Institutional Instability Model (FIIM)
====================================================
Politomorphism Engine — Component 2, Version 2.0

IS(p) = alpha * H(p) + (1 - alpha) * V(p)
  H(p) = Shannon entropy (normalized 0-1)
  V(p) = Severity index = 0.5*p1 + 1.0*p2
  alpha = 0.5

Author : Prof. Serban Gabriel Florin | ORCID: 0009-0000-2266-3356
Project: Politomorphism Engine | OSF: 10.17605/OSF.IO/HYDNZ
"""

import math
import csv


def smf(x, a, b):
    if x <= a: return 0.0
    if x >= b: return 1.0
    if x <= (a + b) / 2: return 2 * ((x - a) / (b - a)) ** 2
    return 1 - 2 * ((x - b) / (b - a)) ** 2

def zmf(x, a, b): return 1.0 - smf(x, a, b)

def trimf_clipped(x, center, half_width):
    return max(0.0, 1.0 - abs(x - center) / half_width)

def normalize(mus):
    total = sum(mus) + 1e-10
    return [round(m / total, 6) for m in mus]


def fuzzy_fh_judicial(score):
    mu_s0 = smf(score, 3.0, 6.0)
    mu_s1 = trimf_clipped(score, 4.0, 3.5)
    mu_s2 = zmf(score, 1.0, 5.0)
    return normalize([mu_s0, mu_s1, mu_s2])

def fuzzy_fh_electoral(score):
    mu_s0 = smf(score, 3.0, 6.0)
    mu_s1 = trimf_clipped(score, 3.75, 3.25)
    mu_s2 = zmf(score, 1.0, 5.0)
    return normalize([mu_s0, mu_s1, mu_s2])

def fuzzy_bti_participation(score):
    mu_s0 = smf(score, 4.5, 9.0)
    mu_s1 = trimf_clipped(score, 6.0, 5.0)
    mu_s2 = zmf(score, 1.0, 7.5)
    return normalize([mu_s0, mu_s1, mu_s2])


def entropy_component(p):
    S = -sum(x * math.log(x) for x in p if x > 0)
    return S / math.log(3)

def severity_component(p):
    return 0.5 * p[1] + 1.0 * p[2]

def instability_score(p, alpha=0.5):
    return alpha * entropy_component(p) + (1 - alpha) * severity_component(p)

def is_zone(score):
    if score > 0.70:   return "CRITICAL"
    elif score > 0.55: return "HIGH"
    elif score > 0.40: return "MODERATE"
    else:              return "LOW"


ELECTORAL_OVERRIDES = {
    ("Hungary",  2011): [0.05, 0.45, 0.50],
    ("Hungary",  2014): [0.05, 0.40, 0.55],
    ("Poland",   2015): [0.20, 0.55, 0.25],
    ("Poland",   2019): [0.08, 0.48, 0.44],
    ("Romania",  2024): [0.08, 0.52, 0.40],
}

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

BTI_PARTICIPATION_BIENNIAL = {
    "Romania": {
        2006:7.5, 2008:7.5, 2010:7.5, 2012:7.0, 2014:7.5,
        2016:7.5, 2018:7.5, 2020:7.0, 2022:7.0, 2024:7.0,
    },
    "Hungary": {
        2006:8.5, 2008:8.5, 2010:8.0, 2012:7.0, 2014:6.0,
        2016:5.5, 2018:5.0, 2020:4.5, 2022:4.5, 2024:4.5,
    },
    "Poland": {
        2006:9.0, 2008:9.0, 2010:9.0, 2012:9.0, 2014:9.0,
        2016:8.5, 2018:7.5, 2020:7.0, 2022:7.0, 2024:7.5,
    },
}

YEARS     = list(range(2005, 2025))
COUNTRIES = ["Romania", "Hungary", "Poland"]
ALPHA     = 0.5


def interpolate_bti(country, year):
    data = BTI_PARTICIPATION_BIENNIAL[country]
    if year in data: return data[year]
    ys = sorted(data.keys())
    for i in range(len(ys) - 1):
        y0, y1 = ys[i], ys[i + 1]
        if y0 < year < y1:
            return data[y0] + (data[y1]-data[y0])*(year-y0)/(y1-y0)
    return data[ys[0]] if year < ys[0] else data[ys[-1]]


def compute_fiim():
    results = {}
    for country in COUNTRIES:
        results[country] = {}
        prev_IS = None
        prev_fh_j = None
        for year in YEARS:
            jud  = FH_JUDICIAL[country].get(year)
            elec = FH_ELECTORAL[country].get(year)
            bti  = interpolate_bti(country, year)
            if jud is None or elec is None: continue

            p_j = fuzzy_fh_judicial(jud)
            p_e = ELECTORAL_OVERRIDES.get((country, year),
                  fuzzy_fh_electoral(elec))
            p_c = fuzzy_bti_participation(bti)

            IS_j = instability_score(p_j, ALPHA)
            IS_e = instability_score(p_e, ALPHA)
            IS_c = instability_score(p_c, ALPHA)
            IS_agg = (IS_j + IS_e + IS_c) / 3
            zone   = is_zone(IS_agg)

            if prev_fh_j is not None:
                delta_fh = jud - prev_fh_j
                direction = ("IMPROVING"     if delta_fh >  0.10 else
                             "DETERIORATING" if delta_fh < -0.10 else
                             "STABLE")
            else:
                delta_fh = None
                direction = "baseline"

            if prev_IS is not None:
                delta_IS = IS_agg - prev_IS
                trend = ("ESCALATING"    if delta_IS >  0.01 else
                         "DE-ESCALATING" if delta_IS < -0.01 else
                         "STABLE")
            else:
                delta_IS = None
                trend = "baseline"

            results[country][year] = {
                "year": year, "country": country,
                "FH_Judicial": jud, "FH_Electoral": elec,
                "BTI": round(bti, 2),
                "p_Justice": p_j, "p_Electoral": p_e, "p_Coalition": p_c,
                "IS_Justice":   round(IS_j, 4),
                "IS_Electoral": round(IS_e, 4),
                "IS_Coalition": round(IS_c, 4),
                "IS_agg":  round(IS_agg, 4),
                "IS_pct":  round(IS_agg * 100, 2),
                "zone":    zone,
                "delta_IS":  round(delta_IS, 4) if delta_IS is not None else None,
                "trend":     trend,
                "delta_FH":  round(delta_fh, 2) if delta_fh is not None else None,
                "direction": direction,
                "electoral_override": (country, year) in ELECTORAL_OVERRIDES,
            }
            prev_IS   = IS_agg
            prev_fh_j = jud
    return results


def print_results(results):
    for country in COUNTRIES:
        rows = sorted(results[country].values(), key=lambda r: r["year"])
        print(f"\n{'='*85}")
        print(f"  FIIM v2.0 — {country.upper()}  |  alpha={ALPHA}")
        print(f"{'='*85}")
        print(f"  {'Year':>4}  {'FH-J':>5}  {'FH-E':>5}  {'BTI':>5}  "
              f"{'IS-J':>6}  {'IS-E':>6}  {'IS-C':>6}  "
              f"{'IS%':>6}  {'Zone':>10}  {'Trend':>14}  Direction")
        print(f"  {'─'*83}")
        for r in rows:
            ovr = "*" if r["electoral_override"] else " "
            print(f"  {r['year']:>4}  {r['FH_Judicial']:>5.2f}  "
                  f"{r['FH_Electoral']:>5.2f}  {r['BTI']:>5.2f}  "
                  f"{r['IS_Justice']:>6.3f}  {r['IS_Electoral']:>6.3f}{ovr} "
                  f"{r['IS_Coalition']:>6.3f}  "
                  f"{r['IS_pct']:>5.1f}%  {r['zone']:>10}  "
                  f"{r['trend']:>14}  {r['direction']}")


if __name__ == "__main__":
    print("\n  Politomorphism Engine — FIIM v2.0")
    print(f"  IS = {ALPHA}*H(entropy) + {1-ALPHA}*V(severity)")
    print(f"  Countries: {', '.join(COUNTRIES)}")
    print(f"  Period   : {YEARS[0]}-{YEARS[-1]}")
    results = compute_fiim()
    print_results(results)
    print("\n  Done.\n")
