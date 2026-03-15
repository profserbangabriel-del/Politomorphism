import sys, json, math, os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

symbol = sys.argv[1] if len(sys.argv) > 1 else "Nelson Mandela"
print(f"STEP 5 - Final SRM for: {symbol}")

os.makedirs('rezultate', exist_ok=True)

def load_json(path, default):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return default

pas3 = load_json('rezultate/pas3_semantic_drift.json', {"D": 0.320})
D = pas3.get("D", 0.320)

# Load CSV data
baseline_path = 'data_mandela/mandela_baseline.csv'
analysis_path = 'data_mandela/mandela_analysis.csv'
titles_path = 'data_mandela/mandela_titles.csv'

# Debug: list files
print("Files in data_mandela/:")
if os.path.exists('data_mandela'):
    for f in os.listdir('data_mandela'):
        size = os.path.getsize(f'data_mandela/{f}')
        print(f"  {f} ({size} bytes)")
else:
    print("  data_mandela/ folder NOT FOUND")

V = 0.920  # default
N = 1.000  # default
A = 0.520  # default

if os.path.exists(baseline_path) and os.path.exists(analysis_path):
    df_b = pd.read_csv(baseline_path)
    df_a = pd.read_csv(analysis_path)

    print(f"\nBaseline: {len(df_b)} months")
    print(df_b.head())
    print(f"\nAnalysis: {len(df_a)} months")
    print(df_a.head())

    b_avg = df_b['count'].mean()
    a_avg = df_a['count'].mean()

    if b_avg > 0:
        escalation = a_avg / b_avg
        V = min(1.0, math.log1p(escalation) / math.log1p(200))
    else:
        V = 0.920

    days_present = int((df_a['count'] > 0).sum())
    N = days_present / len(df_a) if len(df_a) > 0 else 1.0

    print(f"\nBaseline avg: {b_avg:.1f} | Analysis avg: {a_avg:.1f}")
    print(f"Escalation: {a_avg/b_avg if b_avg > 0 else 'inf'}x → V={V:.4f}")
    print(f"N = {N:.4f} ({days_present}/{len(df_a)} months)")
else:
    print(f"\nCSV not found — using pre-computed values V={V}, N={N}")

# VADER on titles
if os.path.exists(titles_path):
    df_t = pd.read_csv(titles_path)
    titluri = df_t['title'].dropna().tolist()
    print(f"\nVADER titles: {len(titluri)}")
    if titluri:
        analyzer = SentimentIntensityAnalyzer()
        scores = [abs(analyzer.polarity_scores(str(t))['compound']) for t in titluri]
        A = sum(scores) / len(scores)
        print(f"A = {A:.4f}")
else:
    print(f"Titles not found — using A={A}")

lam = 2
semantic_factor = math.exp(-lam * D)
SRM = V * A * semantic_factor * N

interpretation = "LOW RESONANCE" if SRM < 0.07 else "MEDIUM RESONANCE" if SRM < 0.20 else "HIGH RESONANCE"

result = {
    "symbol": symbol,
    "V": round(V, 4), "A": round(A, 4), "D": round(D, 4),
    "semantic_factor": round(semantic_factor, 4),
    "N": round(N, 4), "SRM": round(SRM, 4),
    "interpretation": interpretation,
    "formula": f"SRM = {V:.4f} x {A:.4f} x {semantic_factor:.4f} x {N:.4f}",
    "data_source": "New York Times Archive API",
    "typology": "High Resonance Anchor"
}

with open('rezultate/SRM_mandela_result.json', 'w') as f:
    json.dump(result, f, indent=2)

print(f"\n{'='*40}")
print(f"V={V:.4f} A={A:.4f} D={D:.4f} N={N:.4f}")
print(f"SRM = {SRM:.4f} -> {interpretation}")
print(f"{'='*40}")

# Chart
dataset = [
    ("Simion\n(RO,2025)", 0.0054),
    ("Orbán\n(HU,2026)", 0.0065),
    ("Putin\n(2022-26)", 0.0103),
    ("Georgescu\n(RO,2024)", 0.0307),
    ("Ciolacu\n(RO,2026)", 0.0365),
    ("Sunflower\n(TW,2014)", 0.0376),
    ("Trump\n(US,2016)", 0.0922),
    ("Zelensky\n(2022-26)", 0.1121),
    ("Mandela\n(SA,1990)", round(SRM, 4)),
]
dataset_sorted = sorted(dataset, key=lambda x: x[1])
labels = [d[0] for d in dataset_sorted]
values = [d[1] for d in dataset_sorted]
colors = ['#FFD700' if 'Mandela' in d[0] else
          '#27AE60' if d[1] >= 0.20 else
          '#3498DB' if d[1] >= 0.07 else '#E8A09A'
          for d in dataset_sorted]

fig, ax = plt.subplots(figsize=(14, 6))
fig.patch.set_facecolor('white')
bars = ax.bar(labels, values, color=colors, alpha=0.85, edgecolor='white', width=0.6)
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.002,
            f'{val:.4f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
ax.axhline(y=0.07, color='#E67E22', linewidth=1.5, linestyle='--', alpha=0.7)
ax.axhline(y=0.20, color='#27AE60', linewidth=1.5, linestyle='--', alpha=0.7)
ax.text(8.4, 0.072, 'Medium threshold', fontsize=8, color='#E67E22', ha='right')
ax.text(8.4, 0.202, 'High threshold', fontsize=8, color='#27AE60', ha='right')
ax.set_title(f'SRM Score — {symbol}\nNine-Symbol Comparative Dataset', fontsize=12, fontweight='bold')
ax.set_ylabel('SRM Score', fontsize=10)
ax.set_facecolor('#FAFAFA')
ax.grid(axis='y', alpha=0.3, linestyle=':')
legend_elements = [
    mpatches.Patch(color='#FFD700', label='Mandela (this study)'),
    mpatches.Patch(color='#E8A09A', label='Low Resonance'),
    mpatches.Patch(color='#3498DB', label='Medium Resonance'),
    mpatches.Patch(color='#27AE60', label='High Resonance'),
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=9)
plt.tight_layout()
plt.savefig('rezultate/SRM_mandela_chart.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("Saved: SRM_mandela_result.json + SRM_mandela_chart.png")
