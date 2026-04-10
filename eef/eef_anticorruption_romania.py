"""
EEF — Anti-Corruption Domain Extension for Romania
====================================================
Politomorphism Engine — Component 2, Version 2.1

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

def trimf_clipped(x, center, hw):
    return max(0.0, 1.0 - abs(x - center) / hw)

def normalize(mus):
    t = sum(mus) + 1e-10
    return [round(m / t, 6) for m in mus]


def fuzzy_cpi(score):
    mu_s0 = smf(score, 40.0, 55.0)
    mu_s1 = trimf_clipped(score, 43.0, 12.0)
    mu_s2 = zmf(score, 30.0, 45.0)
    return normalize([mu_s0, mu_s1, mu_s2])

def fuzzy_prosecution_rate(rate):
    mu_s0 = smf(rate, 0.45, 0.80)
    mu_s1 = trimf_clipped(rate, 0.50, 0.40)
    mu_s2 = zmf(rate, 0.20, 0.55)
    return normalize([mu_s0, mu_s1, mu_s2])

def fuzzy_conviction_rate(rate):
    mu_s0 = smf(rate, 0.78, 0.95)
    mu_s1 = trimf_clipped(rate, 0.80, 0.20)
    mu_s2 = zmf(rate, 0.60, 0.82)
    return normalize([mu_s0, mu_s1, mu_s2])

def combine_ac_domain(p_cpi, p_pros, p_conv, w=(0.40, 0.35, 0.25)):
    p_combined = [
        w[0]*p_cpi[i] + w[1]*p_pros[i] + w[2]*p_conv[i]
        for i in range(3)
    ]
    total = sum(p_combined)
    return [round(x/total, 6) for x in p_combined]

def H_norm(p):
    S = -sum(x * math.log(x) for x in p if x > 0)
    return S / math.log(3)

def V(p):
    return 0.0 * p[0] + 0.5 * p[1] + 1.0 * p[2]

def IS(p, alpha=0.5):
    return alpha * H_norm(p) + (1 - alpha) * V(p)

def is_zone(score):
    if score > 0.70:   return "CRITICAL"
    elif score > 0.55: return "HIGH"
    elif score > 0.40: return "MODERATE"
    else:              return "LOW"


CPI_ROMANIA = {
    2005:30, 2006:31, 2007:37, 2008:38, 2009:38,
    2010:37, 2011:36, 2012:44, 2013:43, 2014:43,
    2015:46, 2016:48, 2017:48, 2018:47, 2019:44,
    2020:45, 2021:45, 2022:46, 2023:46, 2024:46,
}

DNA_PROSECUTION_RATE = {
    2005:0.18, 2006:0.20, 2007:0.28, 2008:0.32, 2009:0.38,
    2010:0.42, 2011:0.48, 2012:0.52, 2013:0.55, 2014:0.65,
    2015:0.75, 2016:1.00, 2017:0.72, 2018:0.60, 2019:0.55,
    2020:0.45, 2021:0.50, 2022:0.55, 2023:0.58, 2024:0.60,
}

DNA_CONVICTION_RATE = {
    2005:0.72, 2006:0.74, 2007:0.78, 2008:0.80, 2009:0.82,
    2010:0.84, 2011:0.85, 2012:0.87, 2013:0.88, 2014:0.90,
    2015:0.91, 2016:0.92, 2017:0.85, 2018:0.80, 2019:0.78,
    2020:0.76, 2021:0.78, 2022:0.82, 2023:0.85, 2024:0.88,
}

AC_EVENTS = {
    2012: "Suspension of President Basescu",
    2013: "Kovesi appointed DNA chief",
    2017: "OUG13 — decriminalization attempt",
    2018: "Legislative package weakening anti-corruption",
    2019: "Kovesi departure",
    2022: "Record rechizitorii DNA",
    2024: "CCR electoral annulment",
}

YEARS = list(range(2005, 2025))


def compute_ac_domain():
    results = []
    prev_IS_ac = None
    for year in YEARS:
        cpi  = CPI_ROMANIA[year]
        pros = DNA_PROSECUTION_RATE[year]
        conv = DNA_CONVICTION_RATE[year]
        p_cpi  = fuzzy_cpi(cpi)
        p_pros = fuzzy_prosecution_rate(pros)
        p_conv = fuzzy_conviction_rate(conv)
        p_ac   = combine_ac_domain(p_cpi, p_pros, p_conv)
        IS_ac  = IS(p_ac)
        zone   = is_zone(IS_ac)
        if prev_IS_ac is not None:
            delta_IS = IS_ac - prev_IS_ac
            trend = ("ESCALATING"    if delta_IS >  0.01 else
                     "DE-ESCALATING" if delta_IS < -0.01 else
                     "STABLE")
        else:
            delta_IS = None
            trend = "baseline"
        results.append({
            "year":      year,
            "CPI":       cpi,
            "pros_rate": pros,
            "conv_rate": conv,
            "p0_ac":     p_ac[0],
            "p1_ac":     p_ac[1],
            "p2_ac":     p_ac[2],
            "H_ac":      round(H_norm(p_ac), 4),
            "V_ac":      round(V(p_ac), 4),
            "IS_ac":     round(IS_ac, 4),
            "IS_pct":    round(IS_ac * 100, 2),
            "zone":      zone,
            "delta_IS":  round(delta_IS, 4) if delta_IS is not None else None,
            "trend":     trend,
            "event":     AC_EVENTS.get(year, ""),
        })
        prev_IS_ac = IS_ac
    return results


def print_results(results):
    print("\n" + "="*80)
    print("  EEF — Anti-Corruption Domain — Romania 2005-2024")
    print("="*80)
    print(f"  {'Year':>4}  {'CPI':>4}  {'Pros':>5}  {'Conv':>5}  "
          f"{'IS%':>6}  {'Zone':>10}  {'Trend':>14}  Event")
    print("  " + "─"*78)
    for r in results:
        ev = r["event"][:30] if r["event"] else ""
        print(f"  {r['year']:>4}  {r['CPI']:>4}  {r['pros_rate']:>5.2f}  "
              f"{r['conv_rate']:>5.2f}  "
              f"{r['IS_pct']:>5.1f}%  {r['zone']:>10}  "
              f"{r['trend']:>14}  {ev}")


if __name__ == "__main__":
    print("\n  Politomorphism — Anti-Corruption Domain Romania")
    results = compute_ac_domain()
    print_results(results)
    print("\n  Done.\n")
