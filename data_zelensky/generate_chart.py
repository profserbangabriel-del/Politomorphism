"""
generate_chart.py
=================
Generates two charts mirroring the Trump validation paper:
  1. SRM_zelensky_chart.png  — variable profile bar chart
  2. SRM_zelensky_temporal.png — temporal distribution of symbol
"""

import json
import csv
import math
import os

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np
except ImportError:
    print("[SKIP] matplotlib not installed — no charts generated")
    raise SystemExit(0)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
RESULT_FILE = os.path.join(os.path.dirname(__file__), "SRM_zelensky_result.json")

# Load result
with open(RESULT_FILE, encoding="utf-8") as f:
    result = json.load(f)

V   = result["variables"]["V"]
A   = result["variables"]["A"]
D   = result["variables"]["D"]
N   = result["variables"]["N"]
SF  = result["variables"]["semantic_factor"]
SRM = result["SRM"]
lam = result["variables"]["lambda"]

# ─────────────────────────────────────
# CHART 1 — Variable Profile (bar chart)
# Mirrors Figure 1 from Trump validation
# ─────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 4.5))
fig.patch.set_facecolor("#1a1a2e")
ax.set_facecolor("#16213e")

VARIABLES = {
    "V\nViral\nVelocity":     (V,       "#4fc3f7"),
    "A\nAffective\nWeight":   (A,       "#81c784"),
    "1−D\nSemantic\nCoherence": (1-D,   "#ffb74d"),
    "N\nNetwork\nCoverage":   (N,       "#ce93d8"),
}

labels = list(VARIABLES.keys())
values = [v[0] for v in VARIABLES.values()]
colors = [v[1] for v in VARIABLES.values()]

x = np.arange(len(labels))
bars = ax.bar(x, values, color=colors, width=0.55, zorder=3, edgecolor="none")

for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.015,
            f"{val:.3f}",
            ha="center", va="bottom", color="white", fontsize=11, fontweight="bold")

ax.set_xticks(x)
ax.set_xticklabels(labels, color="white", fontsize=9)
ax.set_ylim(0, 1.15)
ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
ax.tick_params(colors="white")
ax.yaxis.set_tick_params(labelcolor="white")
ax.spines[:].set_color("#555")
ax.grid(axis="y", color="#333", linewidth=0.5, zorder=0)

# SRM score box
ax.text(0.98, 0.97,
        f"SRM = {SRM:.4f}\n{result['interpretation']}",
        transform=ax.transAxes,
        ha="right", va="top",
        color="white", fontsize=12, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#0f3460", edgecolor="#4fc3f7", linewidth=1.5))

ax.set_title(
    f'SRM Profile — "zelensky" symbol\n'
    f'(UA/EU/US | May 2022 – Feb 2026 | λ={lam})',
    color="white", fontsize=12, pad=12
)
ax.set_ylabel("Score [0–1]", color="white", fontsize=10)

plt.tight_layout()
out1 = os.path.join(os.path.dirname(__file__), "SRM_zelensky_chart.png")
plt.savefig(out1, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
print(f"[SAVED] {out1}")
plt.close()


# ─────────────────────────────────────
# CHART 2 — Temporal Distribution
# Mirrors Figure 2 from Trump validation
# ─────────────────────────────────────
def load_csv_dates(filename):
    path = os.path.join(DATA_DIR, filename)
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                from datetime import datetime
                rows.append((datetime.strptime(r["date"], "%Y-%m-%d"), float(r["ratio"])))
            except (ValueError, KeyError):
                pass
    return rows

usa_data    = load_csv_dates("counts_zelensky_usa.csv")
europe_data = load_csv_dates("counts_zelensky_europe.csv")

fig2, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), sharex=False)
fig2.patch.set_facecolor("#1a1a2e")

for ax, data, color, title in [
    (ax1, usa_data,    "#4fc3f7", "USA Collection"),
    (ax2, europe_data, "#ce93d8", "Europe Collection"),
]:
    ax.set_facecolor("#16213e")
    dates  = [d[0] for d in data]
    ratios = [d[1] for d in data]
    ax.fill_between(dates, ratios, alpha=0.4, color=color)
    ax.plot(dates, ratios, color=color, linewidth=0.8, alpha=0.9)

    # Mark peak
    if data:
        peak = max(data, key=lambda x: x[1])
        ax.axvline(peak[0], color="red", linewidth=1, linestyle="--", alpha=0.7)
        ax.text(peak[0], peak[1] * 0.85, f"Peak\n{peak[0].strftime('%b %Y')}",
                color="red", fontsize=8, ha="left")

    ax.set_title(f'"zelensky" symbol — {title}', color="white", fontsize=10)
    ax.set_ylabel("Daily ratio", color="white", fontsize=9)
    ax.tick_params(colors="white", labelsize=8)
    ax.spines[:].set_color("#555")
    ax.grid(color="#333", linewidth=0.3)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_color("white")

fig2.suptitle(
    'Temporal distribution of "zelensky" symbol in media (Media Cloud, 2022–2026)',
    color="white", fontsize=11, y=1.01
)

plt.tight_layout()
out2 = os.path.join(os.path.dirname(__file__), "SRM_zelensky_temporal.png")
plt.savefig(out2, dpi=150, bbox_inches="tight", facecolor=fig2.get_facecolor())
print(f"[SAVED] {out2}")
plt.close()
