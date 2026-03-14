import sys, json, math, os
import pandas as pd

symbol = sys.argv[1] if len(sys.argv) > 1 else "Putin"
print(f"STEP 5 - Final SRM for: {symbol}")

os.makedirs('rezultate', exist_ok=True)

def load_json(path, default):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return default

pas2 = load_json('rezultate/pas2_sentiment.json', {"A": 0.2593})
pas3 = load_json('rezultate/pas3_semantic_drift.json', {"D": 0.847})
pas4 = load_json('rezultate/pas4_network_coverage.json', {"N": 1.0000})

A = pas2.get("A", 0.2593)
D = pas3.get("D", 0.847)
N = pas4.get("N", 1.0000)

# Compute V from CSV
V = 0.2170
baseline_path = 'data_putin/PUTIN_DATA_FIRST_PERIOD_ATTENTION.csv'
analysis_path = 'data_putin/PUTIN_DATA_SECOND_PERIOD_ATTENTION.csv'

if os.path.exists(baseline_path) and os.path.exists(analysis_path):
    df_b = pd.read_csv(baseline_path)
    df_a = pd.read_csv(analysis_path)
    df_b['date'] = pd.to_datetime(df_b['date'])
    df_a['date'] = pd.to_datetime(df_a['date'])
    cut = pd.Timestamp('2022-02-24')
    baseline = df_b[df_b['date'] < cut]
    analysis = df_a[df_a['date'] >= cut]
    b_avg = baseline['ratio'].mean()
    a_avg = analysis['ratio'].mean()
    escalation = a_avg / b_avg
    V = min(1.0, math.log1p(escalation) / math.log1p(200))
    print(f"V computed from CSV: escalation {escalation:.2f}x -> V={V:.4f}")

lam = 2
semantic_factor = math.exp(-lam * D)
SRM = V * A * semantic_factor * N

if SRM < 0.07:
    interpretation = "LOW RESONANCE"
elif SRM < 0.20:
    interpretation = "MEDIUM RESONANCE"
else:
    interpretation = "HIGH RESONANCE"

result = {
    "symbol": symbol,
    "V": round(V, 4),
    "A": round(A, 4),
    "D": round(D, 4),
    "semantic_factor": round(semantic_factor, 4),
    "N": round(N, 4),
    "SRM": round(SRM, 4),
    "interpretation": interpretation,
    "formula": f"SRM = {V:.4f} x {A:.4f} x {semantic_factor:.4f} x {N:.4f}"
}

with open('rezultate/SRM_putin_result.json', 'w') as f:
    json.dump(result, f, indent=2)

print(f"\n{'='*40}")
print(f"V = {V:.4f}")
print(f"A = {A:.4f}")
print(f"D = {D:.4f}")
print(f"e^(-2D) = {semantic_factor:.4f}")
print(f"N = {N:.4f}")
print(f"SRM = {SRM:.4f}")
print(f"Result: {interpretation}")
print(f"{'='*40}")
print("Saved: rezultate/SRM_putin_result.json")
