import sys, json, math, os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

symbol = sys.argv[1] if len(sys.argv) > 1 else "Viktor Orban"
print(f"STEP 5 - Final SRM for: {symbol}")

os.makedirs('rezultate', exist_ok=True)

def load_json(path, default):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return default

pas2 = load_json('rezultate/pas2_sentiment.json', {"A": 0.2359})
pas3 = load_json('rezultate/pas3_semantic_drift.json', {"D": 0.798})
pas4 = load_json('rezultate/pas4_network_coverage.json', {"N": 0.8118})

A = pas2.get("A", 0.2359)
D = pas3.get("D", 0.798)
N = pas4.get("N", 0.8118)

V = 0.1684
baseline_path = 'data_orban/victor_orban_first_period.csv'
analysis_path = 'data_orban/Victor_orban_second_period.csv'

if os.path.exists(baseline_path) and os.path.exists(analysis_path):
    df_b = pd.read_csv(baseline_path)
    df_a = pd.read_csv(analysis_path)
    df_b['date'] = pd.to_datetime(df_b['date'])
    df_a['date'] = pd.to_datetime(df_a['date'])
    b_avg = df_b['ratio'].mean()
    a_avg = df_a['ratio'].mean()
    escalation = a_avg / b_avg
    V = min(1.0, math.log1p(escalation) / math.log1p(200))
    print(f"V computed: escalation {escalation:.2f}x -> V={V:.4f}")

lam = 2
semantic_factor = math.exp(-lam * D)
SRM = V * A * semantic_factor * N
interpretation = "LOW RESONANCE" if SRM < 0.07 else "MEDIUM RESONANCE" if SRM < 0.20 else "HIGH RESONANCE"

result = {
    "symbol": symbol, "V": round(V, 4), "A": round(A, 4),
    "D": round(D, 4), "semantic_factor": round(semantic_factor, 4),
    "N": round(N, 4), "SRM": round(SRM, 4),
    "interpretation": interpretation,
    "formula": f"SRM = {V:.4f} x {A:.4f} x {semantic_factor:.4f} x {N:.4f}",
    "typology": "Longevity Saturation Symbol"
}

with open('rezultate/SRM_orban_result.json', 'w') as f:
    json.dump(result, f, indent=2)

print(f"\n{'='*40}")
print(f"V={V:.4f} A={A:.4f} D={D:.4f} N={N:.4f}")
print(f"SRM = {SRM:.4f} -> {interpretation}")
print(f"{'='*40}")

# Chart
dataset = [
    ("Simion\n(RO,2025)", 0.0054),
    (f"Orb\u00e1n\n(HU,2026)", round(SRM, 4)),
    ("Putin\n(2022-26)", 0.0103),
    ("Georgescu\n(RO,2024)", 0.0307),
    ("Ciolacu\n(RO,2026)", 0.0365),
    ("Sunflower\n(TW,2014)", 0.0376),
    ("Trump\n(US,2016)", 0.0922),
    ("Zelensky\n(2022-26)", 0.1121),
]
labels = [d[0] for d in dataset]
values = [d[1] for d in dataset]
colors = ['#8E44AD' if 'rb' in d[0] else '#E8A09A' if d[1] < 0.07 else '#3498DB' for d in dataset]

fig, ax = plt.subplots(figsize=(13, 6))
fig.patch.set_facecolor('white')
bars = ax.bar(labels, values, color=colors, alpha=0.85, edgecolor='white', width=0.6)
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.0003,
            f'{val:.4f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
ax.axhline(y=0.07, color='#E67E22', linewidth=1.5, linestyle='--', alpha=0.7)
ax.axhline(y=0.20, color='#27AE60', linewidth=1.5, linestyle='--', alpha=0.7)
ax.text(7.4, 0.072, 'Medium threshold', fontsize=8, color='#E67E22', ha='right')
ax.set_title(f'SRM Score — {symbol}\nEight-Symbol Comparative Dataset', fontsize=12, fontweight='bold')
ax.set_ylabel('SRM Score', fontsize=10)
ax.set_facecolor('#FAFAFA')
ax.grid(axis='y', alpha=0.3, linestyle=':')
legend_elements = [
    mpatches.Patch(color='#8E44AD', label='Orban (this study)'),
    mpatches.Patch(color='#E8A09A', label='Low Resonance'),
    mpatches.Patch(color='#3498DB', label='Medium Resonance'),
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=9)
plt.tight_layout()
plt.savefig('rezultate/SRM_orban_chart.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("Saved: rezultate/SRM_orban_result.json + SRM_orban_chart.png")
