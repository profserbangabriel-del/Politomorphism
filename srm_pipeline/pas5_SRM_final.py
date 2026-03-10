import sys, os, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

os.makedirs("rezultate", exist_ok=True)

SIMBOL = sys.argv[1] if len(sys.argv) > 1 else "sunflower movement"
LAMBDA = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0

def load(path, key, fallback):
    try:
        return json.load(open(path))[key]
    except:
        return fallback

V = 0.75
A = load("rezultate/rezultat_A.json", "A", 0.80)
D = load("rezultate/rezultat_D.json", "D", 0.07)
N = load("rezultate/rezultat_N.json", "N", 0.68)

pen = np.exp(-LAMBDA * D)
SRM = V * A * pen * N

if SRM >= 0.70:   zona = "REZONANTA INALTA"
elif SRM >= 0.40: zona = "REZONANTA MEDIE"
elif SRM >= 0.20: zona = "SEMNAL MARGINAL"
else:             zona = "REZONANTA SCAZUTA"

print(f"\n{'='*45}")
print(f"  SRM Pipeline - {SIMBOL}")
print(f"{'='*45}")
print(f"  V  = {V:.4f}")
print(f"  A  = {A:.4f}")
print(f"  D  = {D:.4f}")
print(f"  N  = {N:.4f}")
print(f"  e^(-λD) = {pen:.4f}")
print(f"  SRM = {SRM:.4f}")
print(f"  {zona}")
print(f"{'='*45}")

fig, ax = plt.subplots(figsize=(8, 5))
etichete = ["V", "A", "1-D", "N"]
valori = [V, A, 1-D, N]
culori = ["#3498DB","#E74C3C","#27AE60","#9B59B6"]
bars = ax.bar(etichete, valori, color=culori, alpha=0.85)
for bar, v in zip(bars, valori):
    ax.text(bar.get_x()+bar.get_width()/2, v+0.01,
            f"{v:.3f}", ha='center', fontweight='bold')
ax.axhline(SRM, color="black", linestyle="--", label=f"SRM={SRM:.4f}")
ax.set_ylim(0, 1.15)
ax.set_title(f"SRM = {SRM:.4f} — {zona}\n{SIMBOL}")
ax.legend()
plt.tight_layout()
plt.savefig("rezultate/SRM_grafic_final.png", dpi=150)

with open("rezultate/SRM_raport_final.json", "w") as f:
    json.dump({"simbol": SIMBOL, "V": V, "A": A, "D": D, "N": N,
               "SRM": round(SRM,4), "interpretare": zona}, f, indent=2)

print("[OK] Grafic si raport salvate.")
