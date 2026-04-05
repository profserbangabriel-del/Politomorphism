"""
EEF Inter-Rater Reliability — Politomorphism Engine
====================================================
Krippendorff's Alpha + Cohen's Kappa (weighted, ordinal)
pentru clasificarea S0/S1/S2 pe toate domeniile EEF.

Author : Prof. Serban Gabriel Florin | ORCID: 0009-0000-2266-3356
Project: Politomorphism Engine | OSF: 10.17605/OSF.IO/HYDNZ
"""

import sys, math, csv
sys.path.insert(0, '.')

from eef_longitudinal import (
    COUNTRIES, YEARS,
    FH_JUDICIAL, FH_ELECTORAL,
    ELECTORAL_OVERRIDES,
    interpolate_bti,
    fh_judicial_to_probs,
    fh_electoral_to_probs,
    bti_participation_to_probs,
)

def probs_to_state(probs):
    return probs.index(max(probs))

def classify(country, year, delta=0.0):
    jud  = FH_JUDICIAL[country].get(year)
    elec = FH_ELECTORAL[country].get(year)
    bti  = interpolate_bti(country, year)
    if jud is None or elec is None:
        return None
    p_j = fh_judicial_to_probs(max(1.0, min(7.0,  jud  + delta)))
    p_e = ELECTORAL_OVERRIDES.get((country, year),
          fh_electoral_to_probs(max(1.0, min(7.0,  elec + delta))))
    p_c = bti_participation_to_probs(max(1.0, min(10.0, bti  + delta)))
    return {"Justice":   probs_to_state(p_j),
            "Electoral": probs_to_state(p_e),
            "Coalition": probs_to_state(p_c)}

def weighted_kappa(a, b):
    n = len(a)
    p_o = sum(1 - abs(x-y)/2 for x,y in zip(a,b)) / n
    da  = [a.count(k)/n for k in range(3)]
    db  = [b.count(k)/n for k in range(3)]
    p_e = sum((1-abs(i-j)/2)*da[i]*db[j] for i in range(3) for j in range(3))
    kappa = (p_o - p_e) / (1.0 - p_e) if p_e != 1.0 else 1.0
    return round(kappa, 4), round(p_o, 4), round(p_e, 4)

def krippendorff_alpha(rdata):
    n_cats = 3
    coincidences = [[0.0]*n_cats for _ in range(n_cats)]
    for u in range(len(rdata[0])):
        vals = [rdata[r][u] for r in range(len(rdata)) if rdata[r][u] is not None]
        m = len(vals)
        if m < 2: continue
        for i in range(n_cats):
            for j in range(n_cats):
                nij = sum(1 for v in vals if v==i) * sum(1 for v in vals if v==j)
                if i == j: nij -= sum(1 for v in vals if v==i)
                coincidences[i][j] += nij / (m - 1)
    n_total = sum(coincidences[i][j] for i in range(n_cats) for j in range(n_cats))
    mg = [sum(coincidences[k])/n_total for k in range(n_cats)]
    D_o = sum(coincidences[i][j]*(i-j)**2 for i in range(n_cats) for j in range(n_cats)) / n_total
    D_e = sum(mg[i]*mg[j]*(i-j)**2 for i in range(n_cats) for j in range(n_cats))
    return round(1 - D_o/D_e, 4) if D_e != 0 else 1.0

def interpret_kappa(k):
    if k >= 0.80: return "Almost perfect"
    elif k >= 0.61: return "Substantial"
    elif k >= 0.41: return "Moderate"
    else: return "Fair/Poor"

def interpret_alpha(a):
    if a >= 0.80: return "Reliable"
    elif a >= 0.667: return "Tentatively reliable"
    else: return "Low reliability"

if __name__ == "__main__":
    domains = ["Justice", "Electoral", "Coalition"]
    ratings = {d: {"R1":[], "R2":[], "R3":[], "labels":[]} for d in domains}

    for country in COUNTRIES:
        for year in YEARS:
            r1 = classify(country, year,  0.00)
            r2 = classify(country, year, -0.25)
            r3 = classify(country, year, +0.25)
            if r1 is None: continue
            for d in domains:
                ratings[d]["R1"].append(r1[d])
                ratings[d]["R2"].append(r2[d] if r2 else None)
                ratings[d]["R3"].append(r3[d] if r3 else None)
                ratings[d]["labels"].append((country, year))

    print("\n" + "="*65)
    print("  EEF INTER-RATER RELIABILITY")
    print("  Rater1=baseline | Rater2=−0.25 shift | Rater3=+0.25 shift")
    print("="*65)
    print(f"  {'Domain':<12} {'κ(R1,R2)':>9} {'κ(R1,R3)':>9} {'α(all)':>8}  Result")
    print("─"*65)

    all_r1, all_r2, all_r3 = [], [], []
    for d in domains:
        r1 = ratings[d]["R1"]
        r2 = [v if v is not None else 0 for v in ratings[d]["R2"]]
        r3 = [v if v is not None else 0 for v in ratings[d]["R3"]]
        k12, _, _ = weighted_kappa(r1, r2)
        k13, _, _ = weighted_kappa(r1, r3)
        alpha = krippendorff_alpha([r1, r2, r3])
        print(f"  {d:<12} {k12:>9.4f} {k13:>9.4f} {alpha:>8.4f}  "
              f"{interpret_alpha(alpha)}")
        all_r1.extend(r1); all_r2.extend(r2); all_r3.extend(r3)

    print("─"*65)
    k12a,_,_ = weighted_kappa(all_r1, all_r2)
    k13a,_,_ = weighted_kappa(all_r1, all_r3)
    alpha_all = krippendorff_alpha([all_r1, all_r2, all_r3])
    print(f"  {'AGGREGATE':<12} {k12a:>9.4f} {k13a:>9.4f} {alpha_all:>8.4f}  "
          f"{interpret_alpha(alpha_all)}")
    print("="*65)
    print(f"\n  Aggregate α = {alpha_all:.4f} → {interpret_alpha(alpha_all)}")
    print(f"  N observations per domain: {len(ratings['Justice']['R1'])}")
    print(f"  Total: {3 * len(ratings['Justice']['R1'])} observations\n")
