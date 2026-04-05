"""
FIIM vs EEF Comparison Table
Politomorphism Engine
"""

import math

# ── FUZZY FUNCTIONS (FIIM v2.0) ───────────────────────────────────────────────

def smf(x, a, b):
    if x <= a: return 0.0
    if x >= b: return 1.0
    if x <= (a + b) / 2: return 2 * ((x - a) / (b - a)) ** 2
    return 1 - 2 * ((x - b) / (b - a)) ** 2

def zmf(x, a, b): return 1.0 - smf(x, a, b)

def trimf_c(x, center, hw): return max(0.0, 1.0 - abs(x - center) / hw)

def norm(mus):
    t = sum(mus) + 1e-10
    return [m / t for m in mus]

def fuzzy_judicial(s):
    return norm([smf(s,3.0,6.0), trimf_c(s,4.0,3.5), zmf(s,1.0,5.0)])

def fuzzy_electoral(s):
    return norm([smf(s,3.0,6.0), trimf_c(s,3.75,3.25), zmf(s,1.0,5.0)])

def fuzzy_bti(s):
    return norm([smf(s,4.5,9.0), trimf_c(s,6.0,5.0), zmf(s,1.0,7.5)])

def H(p): return (-sum(x*math.log(x) for x in p if x>0)) / math.log(3)
def V(p): return 0.5*p[1] + 1.0*p[2]
def IS(p, alpha=0.5): return alpha*H(p) + (1-alpha)*V(p)

def is_zone(s):
    if s > 0.70: return "CRITICAL"
    elif s > 0.55: return "HIGH"
    elif s > 0.40: return "MODERATE"
    else: return "LOW"

# ── HARD THRESHOLD FUNCTIONS (EEF original) ───────────────────────────────────

def hard_judicial(score):
    if score >= 5.5:  return [0.70, 0.25, 0.05]
    elif score >= 5.0: return [0.55, 0.35, 0.10]
    elif score >= 4.5: return [0.40, 0.45, 0.15]
    elif score >= 4.0: return [0.25, 0.55, 0.20]
    elif score >= 3.5: return [0.15, 0.55, 0.30]
    elif score >= 3.0: return [0.10, 0.50, 0.40]
    elif score >= 2.5: return [0.05, 0.40, 0.55]
    elif score >= 2.0: return [0.03, 0.30, 0.67]
    else:              return [0.02, 0.18, 0.80]

def hard_electoral(score):
    if score >= 5.5:  return [0.70, 0.25, 0.05]
    elif score >= 5.0: return [0.55, 0.35, 0.10]
    elif score >= 4.5: return [0.40, 0.45, 0.15]
    elif score >= 4.0: return [0.25, 0.52, 0.23]
    elif score >= 3.5: return [0.18, 0.55, 0.27]
    elif score >= 3.0: return [0.12, 0.52, 0.36]
    elif score >= 2.5: return [0.08, 0.48, 0.44]
    elif score >= 2.0: return [0.05, 0.38, 0.57]
    else:              return [0.02, 0.23, 0.75]

def hard_bti(score):
    if score >= 9.0:  return [0.70, 0.25, 0.05]
    elif score >= 8.0: return [0.55, 0.35, 0.10]
    elif score >= 7.5: return [0.40, 0.48, 0.12]
    elif score >= 7.0: return [0.25, 0.57, 0.18]
    elif score >= 6.5: return [0.18, 0.57, 0.25]
    elif score >= 6.0: return [0.12, 0.55, 0.33]
    elif score >= 5.5: return [0.08, 0.52, 0.40]
    elif score >= 5.0: return [0.06, 0.44, 0.50]
    elif score >= 4.5: return [0.04, 0.35, 0.61]
    else:              return [0.02, 0.23, 0.75]

def eef_R(p):
    S = -sum(x*math.log(x) for x in p if x>0)
    return S / math.log(3)

def eef_zone(r):
    if r > 0.80: return "CRITICAL"
    elif r > 0.60: return "HIGH"
    elif r > 0.40: return "MODERATE"
    else: return "LOW"

# ── OVERRIDES ─────────────────────────────────────────────────────────────────

OVERRIDES = {
    ("Hungary",  2011): [0.05, 0.45, 0.50],
    ("Hungary",  2014): [0.05, 0.40, 0.55],
    ("Poland",   2015): [0.20, 0.55, 0.25],
    ("Poland",   2019): [0.08, 0.48, 0.44],
    ("Romania",  2024): [0.08, 0.52, 0.40],
}

# ── DATA ──────────────────────────────────────────────────────────────────────

FH_J = {
    "Romania": {2005:3.50,2010:4.00,2015:4.25,2017:4.00,2018:3.75,2019:3.75,2020:4.00,2023:4.25,2024:4.50},
    "Hungary": {2005:4.25,2010:4.00,2011:3.50,2012:3.00,2013:2.75,2014:2.50,2015:2.25,2016:2.00,2021:1.75,2024:1.75},
    "Poland":  {2005:4.25,2010:4.50,2015:4.75,2016:4.25,2017:3.75,2018:3.50,2019:3.25,2020:3.00,2023:3.25,2024:3.50},
}

FH_E = {
    "Romania": {2005:3.25,2010:3.50,2015:3.75,2024:3.25},
    "Hungary": {2005:4.00,2010:3.75,2011:3.50,2013:3.00,2014:2.75,2017:2.50,2021:2.25,2024:2.00},
    "Poland":  {2005:4.50,2010:4.75,2015:4.75,2017:4.25,2018:4.00,2019:4.00,2020:3.75,2023:3.75,2024:4.00},
}

BTI_J = {
    "Romania": {2005:7.5,2010:7.5,2015:7.5,2020:7.0,2024:7.0},
    "Hungary": {2005:8.5,2010:8.0,2012:7.0,2014:6.0,2016:5.5,2018:5.0,2020:4.5,2024:4.5},
    "Poland":  {2005:9.0,2010:9.0,2015:8.75,2017:8.0,2018:7.5,2019:7.25,2020:7.0,2024:7.5},
}

# Selected years for comparison table
SELECT = [2005, 2010, 2011, 2012, 2013, 2014, 2015, 2016,
          2017, 2018, 2019, 2020, 2021, 2023, 2024]

COUNTRIES = ["Romania", "Hungary", "Poland"]

# ── COMPARISON TABLE ──────────────────────────────────────────────────────────

def get_data(country, year):
    # Get closest available data point
    def closest(d, y):
        if y in d: return d[y]
        keys = sorted(d.keys())
        return d[min(keys, key=lambda k: abs(k-y))]

    jud  = closest(FH_J[country], year)
    elec = closest(FH_E[country], year)
    bti  = closest(BTI_J[country], year)
    return jud, elec, bti

def compute_row(country, year):
    jud, elec, bti = get_data(country, year)

    # EEF original
    pj_h = hard_judicial(jud)
    pe_h = OVERRIDES.get((country, year), hard_electoral(elec))
    pc_h = hard_bti(bti)
    R_eef = (eef_R(pj_h) + eef_R(pe_h) + eef_R(pc_h)) / 3

    # FIIM v2.0
    pj_f = fuzzy_judicial(jud)
    pe_f = OVERRIDES.get((country, year), fuzzy_electoral(elec))
    pc_f = fuzzy_bti(bti)
    IS_fiim = (IS(pj_f) + IS(pe_f) + IS(pc_f)) / 3

    return {
        "country": country, "year": year,
        "FH_J": jud, "FH_E": elec, "BTI": bti,
        "EEF_R": round(R_eef * 100, 1),
        "EEF_zone": eef_zone(R_eef),
        "FIIM_IS": round(IS_fiim * 100, 1),
        "FIIM_zone": is_zone(IS_fiim),
        "agree": eef_zone(R_eef) == is_zone(IS_fiim),
    }

# ── PRINT ─────────────────────────────────────────────────────────────────────

print("\n" + "="*85)
print("  COMPARISON TABLE: EEF (hard thresholds) vs FIIM (fuzzy + severity)")
print("  Politomorphism Engine | Prof. Serban Gabriel Florin")
print("="*85)

for country in COUNTRIES:
    print(f"\n  {country.upper()}")
    print(f"  {'Year':>4}  {'FH-J':>5}  {'FH-E':>5}  {'BTI':>5}  "
          f"{'EEF R%':>7}  {'EEF Zone':>10}  "
          f"{'FIIM IS%':>8}  {'FIIM Zone':>10}  Match")
    print("  " + "─"*80)

    agree_count = 0
    total = 0
    for year in SELECT:
        try:
            r = compute_row(country, year)
            match = "✓" if r["agree"] else "✗"
            if r["agree"]: agree_count += 1
            total += 1
            ovr = "*" if (country, year) in OVERRIDES else " "
            print(f"  {year:>4}  {r['FH_J']:>5.2f}  {r['FH_E']:>5.2f}{ovr} "
                  f"{r['BTI']:>5.2f}  "
                  f"{r['EEF_R']:>6.1f}%  {r['EEF_zone']:>10}  "
                  f"{r['FIIM_IS']:>7.1f}%  {r['FIIM_zone']:>10}  {match}")
        except Exception:
            pass

    pct = 100 * agree_count / total if total > 0 else 0
    print(f"  {'─'*80}")
    print(f"  Zone agreement: {agree_count}/{total} ({pct:.0f}%)")

print("\n  * = electoral override applied")
print("\n  KEY DIFFERENCES:")
print("  EEF: pure Shannon entropy on hard-threshold p vectors → CRITICAL for most")
print("  FIIM: fuzzy p + combined H+V score → gradient between zones, captures")
print("        both uncertainty (H) and severity (V) independently")
print("  FIIM correctly distinguishes:")
print("    - Contested transitions (high H, moderate V) → HIGH")
print("    - Captured systems (low H, high V)           → HIGH")
print("    - Stable democracies (low H, low V)          → LOW/MODERATE")
print("="*85)
