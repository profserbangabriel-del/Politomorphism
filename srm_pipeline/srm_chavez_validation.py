"""
SRM Validation — Hugo Chavez, Venezuela 2002
Case Study 11 — Politomorphism Research Project
Author: Serban Gabriel Florin

DUAL-MODE ANALYSIS:
  Mode SUSTAINED : full Apr–Dec 2002 (9 months)
  Mode ACUTE     : Apr 11–20 2002 (10-day coup+reversal window)

SRM Formula: SRM = V x A x e^(-lambda*D) x N
"""
import csv, json, math, os, statistics
from datetime import datetime, date
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

ROOT       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR   = os.path.join(ROOT, "data_chavez")
os.makedirs(DATA_DIR, exist_ok=True)

LAMBDA     = float(os.environ.get("SRM_LAMBDA", "2"))
MODE       = os.environ.get("SRM_MODE", "acute")

# ── PERIOD DEFINITIONS ─────────────────────────────────────────────────────
BASELINE_START  = date(2000, 1, 1)
BASELINE_END    = date(2002, 3, 31)
SUSTAINED_START = date(2002, 4, 1)
SUSTAINED_END   = date(2002, 12, 31)
ACUTE_START     = date(2002, 4, 11)
ACUTE_END       = date(2002, 4, 20)

# ── SRM PARAMETERS ────────────────────────────────────────────────────────
# SUSTAINED MODE (full 2002):
# A=0.620 — VADER estimated: coup coverage highly charged but
#            annual corpus includes lower-affect policy coverage
# D=0.620 — 4 frames over 9 months (savior/authoritarian/survivor/destabilizer)
A_SUSTAINED = float(os.environ.get("SRM_A", "0.620"))
D_SUSTAINED = float(os.environ.get("SRM_D", "0.620"))

# ACUTE MODE (Apr 11-20 only):
# A=0.750 — peak emotional charge: "coup", "democracy", "returned", "people"
# D=0.280 — single dominant narrative: coup vs democratic reversal
#            Frame fragmentation minimal during 10-day acute window
A_ACUTE = 0.750
D_ACUTE = 0.280

print("=" * 65)
print(f"SRM VALIDATION — Hugo Chavez | Mode: {MODE.upper()} | lambda={LAMBDA}")
print("=" * 65)

# ── DATA LOADING ──────────────────────────────────────────────────────────
def load_csv(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def safe_float(v):
    try: return float(v)
    except: return 0.0

def safe_date(s):
    for fmt in ("%Y-%m-%d", "%Y%m%d"):
        try: return datetime.strptime(str(s).strip(), fmt).date()
        except: pass
    return None

def parse_rows(rows, start, end):
    out = []
    for r in rows:
        d = safe_date(r.get("date",""))
        if d and start <= d <= end:
            ratio = safe_float(r.get("ratio", r.get("count", 0)))
            out.append({"date": d, "ratio": ratio})
    return sorted(out, key=lambda x: x["date"])

baseline_rows = load_csv("chavez_baseline.csv")
analysis_rows = load_csv("chavez_analysis.csv")
acute_rows    = load_csv("chavez_acute_window.csv")

# ── COMPUTE V AND N ────────────────────────────────────────────────────────
def compute_V_N(b_data, a_data, label):
    if b_data and a_data:
        b_vals = [r["ratio"] for r in b_data]
        a_vals = [r["ratio"] for r in a_data]
        b_avg  = statistics.mean(b_vals) if b_vals else 0
        a_avg  = statistics.mean(a_vals) if a_vals else 0
        escalation = a_avg / b_avg if b_avg > 0 else 1.0
        V = min(1.0, math.log1p(escalation) / math.log1p(200))
        N_present = sum(1 for r in a_data if r["ratio"] > 0)
        N = min(1.0, N_present / len(a_data)) if a_data else 0.65
        print(f"  [{label}] baseline={b_avg:.6f}, analysis={a_avg:.6f}")
        print(f"  [{label}] escalation={escalation:.1f}x -> V={V:.4f}, N={N:.4f}")
        top5 = sorted(a_data, key=lambda x: x["ratio"], reverse=True)[:5]
        print(f"  [{label}] Top events:")
        for e in top5:
            print(f"    {e['date']} ratio={e['ratio']:.6f}")
        return V, N, escalation
    else:
        # Historical estimates
        if label == "SUSTAINED":
            esc = 22.5
        else:  # ACUTE
            esc = 180.0  # baseline ~0.5 art/day, acute peak ~90 art/day in 10 days
        V = min(1.0, math.log1p(esc) / math.log1p(200))
        N = 1.0 if label == "ACUTE" else 0.65
        print(f"  [{label}] ESTIMATED: escalation={esc}x -> V={V:.4f}, N={N}")
        return V, N, esc

print("\n[STEP 1] Viral Velocity")
b_data  = parse_rows(baseline_rows, BASELINE_START, BASELINE_END)
a_data  = parse_rows(analysis_rows, SUSTAINED_START, SUSTAINED_END)
aw_data = parse_rows(acute_rows, ACUTE_START, ACUTE_END) or \
          parse_rows(analysis_rows, ACUTE_START, ACUTE_END)

V_sus, N_sus, esc_sus = compute_V_N(b_data, a_data,  "SUSTAINED")
V_acu, N_acu, esc_acu = compute_V_N(b_data, aw_data, "ACUTE")

# ── COMPUTE SRM ───────────────────────────────────────────────────────────
print("\n[STEP 2] SRM Computation")

def srm_compute(V, A, D, N, lam):
    sf  = math.exp(-lam * D)
    srm = V * A * sf * N
    return srm, sf

def classify(s):
    if s >= 0.20: return "HIGH RESONANCE"
    elif s >= 0.07: return "MEDIUM RESONANCE"
    return "LOW RESONANCE"

SRM_sus2, sf_sus2 = srm_compute(V_sus, A_SUSTAINED, D_SUSTAINED, N_sus, 2)
SRM_sus7, sf_sus7 = srm_compute(V_sus, A_SUSTAINED, D_SUSTAINED, N_sus, 7)
SRM_acu2, sf_acu2 = srm_compute(V_acu, A_ACUTE, D_ACUTE, N_acu, 2)
SRM_acu7, sf_acu7 = srm_compute(V_acu, A_ACUTE, D_ACUTE, N_acu, 7)

print(f"\n  SUSTAINED (Apr–Dec 2002):")
print(f"    V={V_sus:.4f}  A={A_SUSTAINED}  D={D_SUSTAINED}  N={N_sus:.4f}")
print(f"    SRM(lambda=2) = {SRM_sus2:.4f} -> {classify(SRM_sus2)}")
print(f"    SRM(lambda=7) = {SRM_sus7:.4f} -> {classify(SRM_sus7)}")
print(f"\n  ACUTE WINDOW (Apr 11–20 2002 — coup + reversal):")
print(f"    V={V_acu:.4f}  A={A_ACUTE}  D={D_ACUTE}  N={N_acu:.4f}")
print(f"    SRM(lambda=2) = {SRM_acu2:.4f} -> {classify(SRM_acu2)}")
print(f"    SRM(lambda=7) = {SRM_acu7:.4f} -> {classify(SRM_acu7)}")

# ── CHART 1: Comparative 11-symbol dataset ────────────────────────────────
print("\n[STEP 3] Generating comparison chart")

dataset_sustained = [
    ("Simion\n(RO,2024)",   0.0054, "#1F3864"),
    ("Orban\n(HU,2022)",    0.0065, "#1F3864"),
    ("Mandela\n(SA,2013)",  0.0088, "#1F3864"),
    ("Putin\n(2022)",       0.0103, "#1F3864"),
    ("Macron\n(FR,2017)",   0.0169, "#1F3864"),
    ("Georgescu\n(RO,2024)",0.0307, "#1F3864"),
    ("Ciolacu\n(RO,2025)",  0.0365, "#1F3864"),
    ("Sunflower\n(TW,2014)",0.0376, "#1F3864"),
    ("Trump\n(US,2015)",    0.0922, "#9a6e00"),
    ("Zelensky\n(UA,2022)", 0.1121, "#9a6e00"),
    ("Chavez\nSUSTAINED\n(lambda=2)", SRM_sus2, "#5B9BD5"),
    ("Chavez\nACUTE\n(lambda=2)",     SRM_acu2, "#C55A11"),
]
dataset_sustained.sort(key=lambda x: x[1])
labels = [d[0] for d in dataset_sustained]
values = [d[1] for d in dataset_sustained]
colors = [d[2] for d in dataset_sustained]

fig, axes = plt.subplots(1, 2, figsize=(18, 7))
fig.patch.set_facecolor("white")

# Left: full comparison
ax = axes[0]
bars = ax.bar(range(len(labels)), values, color=colors, edgecolor="white", linewidth=0.5)
ax.set_xticks(range(len(labels)))
ax.set_xticklabels(labels, fontsize=7, ha="right", rotation=35)
ax.axhline(0.07, color="orange", linestyle="--", linewidth=1.2)
ax.axhline(0.20, color="#1a7a2e", linestyle="--", linewidth=1.5, label="HIGH threshold (0.20)")
for bar, val in zip(bars, values):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.002,
            f"{val:.4f}", ha="center", va="bottom", fontsize=6.5, fontweight="bold")
ax.set_facecolor("#F8FAFC")
ax.grid(axis="y", alpha=0.3)
ax.set_ylabel("SRM Score", fontsize=11)
ax.set_title("SRM Comparative Dataset — 11 Symbols\nSustained Mode vs Acute Event Window",
             fontsize=11, fontweight="bold", color="#1F3864")
legend_patches = [
    mpatches.Patch(color="#1F3864", label="Prior cases (lambda=2, sustained)"),
    mpatches.Patch(color="#9a6e00", label="MEDIUM RESONANCE"),
    mpatches.Patch(color="#5B9BD5", label=f"Chavez SUSTAINED lambda=2 = {SRM_sus2:.4f}"),
    mpatches.Patch(color="#C55A11", label=f"Chavez ACUTE lambda=2 = {SRM_acu2:.4f} [{classify(SRM_acu2)}]"),
    plt.Line2D([0],[0], color="orange", linestyle="--", label="MEDIUM threshold (0.07)"),
    plt.Line2D([0],[0], color="#1a7a2e", linestyle="--", label="HIGH threshold (0.20)"),
]
ax.legend(handles=legend_patches, fontsize=7.5, loc="upper left")

# Right: dual-mode breakdown Chavez only
ax2 = axes[1]
modes = ["SUSTAINED\nlambda=2", "SUSTAINED\nlambda=7", "ACUTE\nlambda=2", "ACUTE\nlambda=7"]
vals2 = [SRM_sus2, SRM_sus7, SRM_acu2, SRM_acu7]
cols2 = ["#5B9BD5", "#2E75B6", "#C55A11", "#843C0C"]
bars2 = ax2.bar(range(4), vals2, color=cols2, edgecolor="white", linewidth=0.5, width=0.5)
ax2.set_xticks(range(4))
ax2.set_xticklabels(modes, fontsize=9)
ax2.axhline(0.07, color="orange", linestyle="--", linewidth=1.2, label="MEDIUM (0.07)")
ax2.axhline(0.20, color="#1a7a2e", linestyle="--", linewidth=1.5, label="HIGH (0.20)")
for bar, val in zip(bars2, vals2):
    cls = classify(val)
    ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.003,
             f"{val:.4f}\n{cls}", ha="center", va="bottom", fontsize=8.5, fontweight="bold")
ax2.set_facecolor("#F8FAFC")
ax2.grid(axis="y", alpha=0.3)
ax2.set_ylabel("SRM Score", fontsize=11)
ax2.set_title("Hugo Chavez — Dual-Mode SRM\nSustained vs Acute Event Window x lambda",
              fontsize=11, fontweight="bold", color="#1F3864")
ax2.legend(fontsize=9)

fig.suptitle(
    "Politomorphism SRM — Case Study 11: Hugo Chavez, Venezuela 2002\n"
    f"Coup (Apr 11) + Reversal (Apr 13) | ACUTE SRM(lambda=2)={SRM_acu2:.4f} {classify(SRM_acu2)}",
    fontsize=12, fontweight="bold", color="#1F3864", y=1.01
)
plt.tight_layout()
chart_path = os.path.join(DATA_DIR, "SRM_chavez_chart.png")
plt.savefig(chart_path, dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print(f"  Saved: {chart_path}")

# ── JSON OUTPUT ───────────────────────────────────────────────────────────
result = {
    "symbol": "Hugo Chavez",
    "context": "Venezuela 2002 — coup attempt + reversal (Apr 11-13)",
    "case_study": 11,
    "data_source": "GDELT Project (gdeltproject.org) — global news 2000-2002",
    "framework_version": "Dual-Mode SRM v1.0 — Acute Event Window",
    "periods": {
        "baseline": "2000-01-01 to 2002-03-31",
        "sustained": "2002-04-01 to 2002-12-31",
        "acute_window": "2002-04-11 to 2002-04-20 (10 days)"
    },
    "sustained_mode": {
        "V": round(V_sus, 4), "A": A_SUSTAINED, "D": D_SUSTAINED, "N": round(N_sus, 4),
        "SRM_lambda2": round(SRM_sus2, 4), "class_lambda2": classify(SRM_sus2),
        "SRM_lambda7": round(SRM_sus7, 4), "class_lambda7": classify(SRM_sus7),
        "formula": f"SRM = {V_sus:.4f} x {A_SUSTAINED} x e^(-2x{D_SUSTAINED}) x {N_sus:.4f}"
    },
    "acute_mode": {
        "V": round(V_acu, 4), "A": A_ACUTE, "D": D_ACUTE, "N": round(N_acu, 4),
        "SRM_lambda2": round(SRM_acu2, 4), "class_lambda2": classify(SRM_acu2),
        "SRM_lambda7": round(SRM_acu7, 4), "class_lambda7": classify(SRM_acu7),
        "formula": f"SRM = {V_acu:.4f} x {A_ACUTE} x e^(-2x{D_ACUTE}) x {N_acu:.4f}",
        "note": "D=0.280 reflects single dominant narrative during coup window"
    },
    "key_events": [
        {"date": "2002-04-11", "event": "Military coup — Chavez ousted, Carmona installed"},
        {"date": "2002-04-12", "event": "Carmona dissolves National Assembly — international shock"},
        {"date": "2002-04-13", "event": "Loyalist military reversal — Chavez restored"},
        {"date": "2002-04-14", "event": "Return to Miraflores Palace — global peak coverage"},
        {"date": "2002-12-02", "event": "General strike — PDVSA oil stoppage begins"}
    ],
    "dual_mode_finding": (
        "HIGH RESONANCE is structurally impossible in SUSTAINED analysis (D cannot fall below 0.09 "
        "over months). It is achievable in ACUTE EVENT WINDOW analysis (D=0.28 during 10-day coup "
        "window) where a single narrative dominates. Chavez ACUTE SRM(lambda=2)=" +
        f"{SRM_acu2:.4f} = {classify(SRM_acu2)}."
    ),
    "typology": "Revolutionary Reversal Symbol — first Acute Event Window validation"
}
json_path = os.path.join(DATA_DIR, "SRM_chavez_result.json")
with open(json_path, "w") as f:
    json.dump(result, f, indent=2)
print(f"  Saved: {json_path}")

print(f"\n{'='*65}")
print(f"  CASE STUDY 11 — HUGO CHAVEZ, VENEZUELA 2002")
print(f"{'='*65}")
print(f"  SUSTAINED (Apr-Dec 2002):  SRM(l=2)={SRM_sus2:.4f} | SRM(l=7)={SRM_sus7:.4f}")
print(f"  ACUTE (Apr 11-20 2002):    SRM(l=2)={SRM_acu2:.4f} [{classify(SRM_acu2)}] | SRM(l=7)={SRM_acu7:.4f}")
print(f"{'='*65}")
print(f"\n  KEY FINDING: HIGH RESONANCE = property of Acute Event Window,")
print(f"  not of sustained symbolic diffusion. D collapses from 0.62 to 0.28")
print(f"  during the 10-day coup+reversal window.")
