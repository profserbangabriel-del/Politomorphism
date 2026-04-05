"""
EEF — Fuzzy Institutional Instability Model (FIIM)
====================================================
Politomorphism Engine — Component 2, Version 2.1

NOTATION (v2.1 clarifications):
  S(t)     = raw Shannon entropy [nats, base e / ln]
  S_max    = ln(N) = ln(3) ≈ 1.0986 nats
  H(t)     = S(t) / S_max ∈ [0,1]  normalized entropy
  V(t)     = expected institutional cost = sum_i(w_i * p_i)
             w = [0.0, 0.5, 1.0]  ordinal distance from equilibrium
             Interpretation: E[c(X)] where c(S0)=0, c(S1)=0.5, c(S2)=1
  IS(t)    = alpha * H(t) + (1-alpha) * V(t)   static instability score
  Delta_IS = IS(t) - IS(t-1)                   discrete dynamics (not dS/dt)
  IS_comp  = IS(t) + beta * Delta_IS(t)        composite forward-looking score
             beta = 0.2 (trajectory weight 20%, state weight 80%)

LOGARITHMIC BASE:
  Natural logarithm (ln, base e) throughout.
  S_max = ln(3) ≈ 1.0986 nats for N=3 states.
  Normalization is base-invariant: H(t) = S(t)/S_max cancels the base.

NOTE on dS/dt:
  Shannon entropy is computed on discrete distributions at annual intervals.
  Continuous-time notation dS/dt is replaced by discrete Delta_IS(t) = IS(t) - IS(t-1).
  Pi(t)  = max(0, Delta_IS(t))   entropy-increasing component
  Phi(t) = max(0, -Delta_IS(t))  entropy-decreasing component

Author : Prof. Serban Gabriel Florin | ORCID: 0009-0000-2266-3356
Project: Politomorphism Engine | OSF: 10.17605/OSF.IO/HYDNZ
"""

import math
import csv


# ── FUZZY PRIMITIVES ──────────────────────────────────────────────────────────

def smf(x, a, b):
    """S-shaped membership: 0 at x<=a, 1 at x>=b."""
    if x <= a: return 0.0
    if x >= b: return 1.0
    if x <= (a + b) / 2: return 2 * ((x - a) / (b - a)) ** 2
    return 1 - 2 * ((x - b) / (b - a)) ** 2

def zmf(x, a, b):
    """Z-shaped membership: 1 at x<=a, 0 at x>=b."""
    return 1.0 - smf(x, a, b)

def trimf_clipped(x, center, half_width):
    """Triangular membership centered at center."""
    return max(0.0, 1.0 - abs(x - center) / half_width)

def normalize(mus):
    """Normalize membership values to sum to 1."""
    total = sum(mus) + 1e-10
    return [round(m / total, 6) for m in mus]


# ── DOMAIN MEMBERSHIP FUNCTIONS ───────────────────────────────────────────────

def fuzzy_fh_judicial(score):
    """FH NIT Judicial Framework — scale 1.0 to 7.0."""
    mu_s0 = smf(score, 3.0, 6.0)
    mu_s1 = trimf_clipped(score, 4.0, 3.5)
    mu_s2 = zmf(score, 1.0, 5.0)
    return normalize([mu_s0, mu_s1, mu_s2])

def fuzzy_fh_electoral(score):
    """FH NIT Electoral Process — scale 1.0 to 7.0."""
    mu_s0 = smf(score, 3.0, 6.0)
    mu_s1 = trimf_clipped(score, 3.75, 3.25)
    mu_s2 = zmf(score, 1.0, 5.0)
    return normalize([mu_s0, mu_s1, mu_s2])

def fuzzy_bti_participation(score):
    """BTI Political Participation — scale 1.0 to 10.0."""
    mu_s0 = smf(score, 4.5, 9.0)
    mu_s1 = trimf_clipped(score, 6.0, 5.0)
    mu_s2 = zmf(score, 1.0, 7.5)
    return normalize([mu_s0, mu_s1, mu_s2])


# ── INSTABILITY SCORE COMPONENTS ──────────────────────────────────────────────

def H_norm(p):
    """
    Normalized Shannon entropy H(t) = S(t) / S_max.
    S(t) = -sum(p_i * ln(p_i))  [nats, base e]
    S_max = ln(3) ≈ 1.0986 nats for N=3 states.
    H(t) ∈ [0,1] — base-invariant after normalization.
    """
    S = -sum(x * math.log(x) for x in p if x > 0)
    return S / math.log(3)

def V(p):
    """
    Expected institutional cost V(t) = E[c(X)] = sum_i(w_i * p_i).
    Weights: w = [0.0, 0.5, 1.0] reflect ordinal distance from equilibrium.
      c(S0) = 0.0  stable — zero institutional cost
      c(S1) = 0.5  strained — partial dysfunction
      c(S2) = 1.0  critical — full institutional failure
    V(t) ∈ [0,1].
    """
    return 0.0 * p[0] + 0.5 * p[1] + 1.0 * p[2]

def IS(p, alpha=0.5):
    """
    Static Instability Score IS(t) = alpha * H(t) + (1-alpha) * V(t).
    alpha = 0.5: equal weight to distributional uncertainty and severity.
    IS(t) ∈ [0,1].
    """
    return alpha * H_norm(p) + (1 - alpha) * V(p)

def IS_composite(IS_t, Delta_IS_t, beta=0.2):
    """
    Composite forward-looking score.
    IS_comp(t) = IS(t) + beta * Delta_IS(t)
    beta = 0.2: trajectory contributes 20%, current state 80%.
    Clipped to [0,1].
    """
    return max(0.0, min(1.0, IS_t + beta * Delta_IS_t))

def is_zone(score):
    """Classify IS score into instability zone."""
    if score > 0.70:   return "CRITICAL"
    elif score > 0.55: return "HIGH"
    elif score > 0.40: return "MODERATE"
    else:              return "LOW"


# ── ELECTORAL OVERRIDES ───────────────────────────────────────────────────────

ELECTORAL_OVERRIDES = {
    ("Hungary",  2011): [0.05, 0.45, 0.50],
    ("Hungary",  2014): [0.05, 0.40, 0.55],
    ("Poland",   2015): [0.20, 0.55, 0.25],
    ("Poland",   2019): [0.08, 0.48, 0.44],
    ("Romania",  2024): [0.08, 0.52, 0.40],
}


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
BETA      = 0.2


def interpolate_bti(country, year):
    data = BTI_PARTICIPATION_BIENNIAL[country]
    if year in data: return data[year]
    ys = sorted(data.keys())
    for i in range(len(ys) - 1):
        y0, y1 = ys[i], ys[i + 1]
        if y0 < year < y1:
            return data[y0] + (data[y1] - data[y0]) * (year - y0) / (y1 - y0)
    return data[ys[0]] if year < ys[0] else data[ys[-1]]


# ── MAIN COMPUTATION ──────────────────────────────────────────────────────────

def compute_fiim():
    results = {}
    for country in COUNTRIES:
        results[country] = {}
        prev_IS_agg = None
        prev_fh_j   = None

        for year in YEARS:
            jud  = FH_JUDICIAL[country].get(year)
            elec = FH_ELECTORAL[country].get(year)
            bti  = interpolate_bti(country, year)
            if jud is None or elec is None:
                continue

            p_j = fuzzy_fh_judicial(jud)
            p_e = ELECTORAL_OVERRIDES.get((country, year),
                  fuzzy_fh_electoral(elec))
            p_c = fuzzy_bti_participation(bti)

            # Per-domain scores
            H_j = H_norm(p_j);  V_j = V(p_j);  IS_j = IS(p_j, ALPHA)
            H_e = H_norm(p_e);  V_e = V(p_e);  IS_e = IS(p_e, ALPHA)
            H_c = H_norm(p_c);  V_c = V(p_c);  IS_c = IS(p_c, ALPHA)

            # Aggregate static IS
            IS_agg = (IS_j + IS_e + IS_c) / 3
            zone   = is_zone(IS_agg)

            # Discrete dynamics: Delta_IS replaces dS/dt
            if prev_IS_agg is not None:
                Delta_IS = IS_agg - prev_IS_agg
                Pi_t     = max(0.0, Delta_IS)
                Phi_t    = max(0.0, -Delta_IS)
                trend    = ("ESCALATING"    if Delta_IS >  0.01 else
                            "DE-ESCALATING" if Delta_IS < -0.01 else
                            "STABLE")
                IS_comp  = IS_composite(IS_agg, Delta_IS, BETA)
                zone_comp = is_zone(IS_comp)
            else:
                Delta_IS = Pi_t = Phi_t = None
                IS_comp  = IS_agg
                trend    = "baseline"
                zone_comp = zone

            # Directional indicator
            if prev_fh_j is not None:
                delta_fh  = jud - prev_fh_j
                direction = ("IMPROVING"     if delta_fh >  0.10 else
                             "DETERIORATING" if delta_fh < -0.10 else
                             "STABLE")
            else:
                delta_fh  = None
                direction = "baseline"

            results[country][year] = {
                "year": year, "country": country,
                "FH_Judicial": jud, "FH_Electoral": elec,
                "BTI": round(bti, 2),
                # probability vectors
                "p_Justice":   p_j,
                "p_Electoral": p_e,
                "p_Coalition": p_c,
                # H(t) — normalized entropy per domain
                "H_Justice":   round(H_j, 4),
                "H_Electoral": round(H_e, 4),
                "H_Coalition": round(H_c, 4),
                # V(t) — expected cost per domain
                "V_Justice":   round(V_j, 4),
                "V_Electoral": round(V_e, 4),
                "V_Coalition": round(V_c, 4),
                # IS per domain
                "IS_Justice":   round(IS_j, 4),
                "IS_Electoral": round(IS_e, 4),
                "IS_Coalition": round(IS_c, 4),
                # aggregate
                "IS_agg":   round(IS_agg, 4),
                "IS_pct":   round(IS_agg * 100, 2),
                "zone":     zone,
                # composite forward-looking
                "IS_comp":    round(IS_comp, 4),
                "IS_comp_pct":round(IS_comp * 100, 2),
                "zone_comp":  zone_comp,
                # discrete dynamics
                "Delta_IS": round(Delta_IS, 4) if Delta_IS is not None else None,
                "Pi_t":     round(Pi_t, 4)     if Pi_t    is not None else None,
                "Phi_t":    round(Phi_t, 4)    if Phi_t   is not None else None,
                "trend":    trend,
                # directional
                "delta_FH":  round(delta_fh, 2) if delta_fh is not None else None,
                "direction": direction,
                "electoral_override": (country, year) in ELECTORAL_OVERRIDES,
            }
            prev_IS_agg = IS_agg
            prev_fh_j   = jud

    return results


# ── OUTPUT ────────────────────────────────────────────────────────────────────

def print_results(results):
    for country in COUNTRIES:
        rows = sorted(results[country].values(), key=lambda r: r["year"])
        print(f"\n{'='*95}")
        print(f"  FIIM v2.1 — {country.upper()}")
        print(f"  IS = {ALPHA}*H(t) + {1-ALPHA}*V(t)  |  IS_comp = IS + {BETA}*Delta_IS")
        print(f"{'='*95}")
        print(f"  {'Year':>4}  {'FH-J':>5}  {'FH-E':>5}  {'BTI':>5}  "
              f"{'IS%':>6}  {'Zone':>10}  "
              f"{'IS_comp%':>9}  {'Zone_c':>10}  "
              f"{'Delta_IS':>9}  {'Trend':>14}  Direction")
        print(f"  {'─'*93}")
        for r in rows:
            ovr  = "*" if r["electoral_override"] else " "
            dIS  = f"{r['Delta_IS']:+.4f}" if r["Delta_IS"] is not None else "    —   "
            print(f"  {r['year']:>4}  {r['FH_Judicial']:>5.2f}  "
                  f"{r['FH_Electoral']:>5.2f}  {r['BTI']:>5.2f}  "
                  f"{r['IS_pct']:>5.1f}%  {r['zone']:>10}  "
                  f"{r['IS_comp_pct']:>8.1f}%  {r['zone_comp']:>10}{ovr} "
                  f"{dIS:>9}  {r['trend']:>14}  {r['direction']}")


def export_csv(results, path="EEF_FIIM_v21_All.csv"):
    fields = [
        "country","year","FH_Judicial","FH_Electoral","BTI",
        "p0_Justice","p1_Justice","p2_Justice",
        "p0_Electoral","p1_Electoral","p2_Electoral",
        "p0_Coalition","p1_Coalition","p2_Coalition",
        "H_Justice","V_Justice","IS_Justice",
        "H_Electoral","V_Electoral","IS_Electoral",
        "H_Coalition","V_Coalition","IS_Coalition",
        "IS_agg","IS_pct","zone",
        "IS_comp","IS_comp_pct","zone_comp",
        "Delta_IS","Pi_t","Phi_t","trend",
        "delta_FH","direction","electoral_override"
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
                    "H_Justice":  r["H_Justice"],
                    "V_Justice":  r["V_Justice"],
                    "IS_Justice": r["IS_Justice"],
                    "H_Electoral":  r["H_Electoral"],
                    "V_Electoral":  r["V_Electoral"],
                    "IS_Electoral": r["IS_Electoral"],
                    "H_Coalition":  r["H_Coalition"],
                    "V_Coalition":  r["V_Coalition"],
                    "IS_Coalition": r["IS_Coalition"],
                    "IS_agg":   r["IS_agg"],
                    "IS_pct":   r["IS_pct"],
                    "zone":     r["zone"],
                    "IS_comp":     r["IS_comp"],
                    "IS_comp_pct": r["IS_comp_pct"],
                    "zone_comp":   r["zone_comp"],
                    "Delta_IS": r["Delta_IS"],
                    "Pi_t":     r["Pi_t"],
                    "Phi_t":    r["Phi_t"],
                    "trend":    r["trend"],
                    "delta_FH":  r["delta_FH"],
                    "direction": r["direction"],
                    "electoral_override": r["electoral_override"],
                })
    rows.sort(key=lambda r: (r["country"], r["year"]))
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"\n  CSV exported: {path}")


if __name__ == "__main__":
    print("\n  Politomorphism Engine — FIIM v2.1")
    print(f"  Notation: H(t)=normalized entropy, V(t)=expected cost, IS=alpha*H+beta*V")
    print(f"  Log base: natural (ln), S_max = ln(3) ≈ 1.0986 nats")
    print(f"  Dynamics: discrete Delta_IS(t) = IS(t) - IS(t-1)")
    print(f"  Composite: IS_comp = IS + {BETA}*Delta_IS")
    print(f"  Countries: {', '.join(COUNTRIES)}")
    print(f"  Period   : {YEARS[0]}-{YEARS[-1]}")
    results = compute_fiim()
    print_results(results)
    export_csv(results)
    print("\n  Done.\n")
