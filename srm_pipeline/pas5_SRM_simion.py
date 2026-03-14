import sys, json, math, os
import pandas as pd

symbol = sys.argv[1] if len(sys.argv) > 1 else "George Simion"
print(f"STEP 5 - Final SRM for: {symbol}")

os.makedirs('rezultate', exist_ok=True)

def load_json(path, default):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return default

pas2 = load_json('rezultate/pas2_sentiment.json', {"A": 0.0994})
pas3 = load_json('rezultate/pas3_semantic_drift.json', {"D": 0.812})
pas4 = load_json('rezultate/pas4_network_coverage.json', {"N": 0.9962})

A = pas2.get("A", 0.0994)
D = pas3.get("D", 0.812)
N = pas4.get("N", 0.9962)

V = 0.2790
baseline_path = 'data_simion/George_simion_period_1.csv'
analysis_path = 'data_simion/George_Simion_Counts.csv'

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
    "symbol": symbol,
    "V": round(V, 4),
    "A": round(A, 4),
    "D": round(D, 4),
    "semantic_factor": round(semantic_factor, 4),
    "N": round(N, 4),
    "SRM": round(SRM, 4),
    "interpretation": interpretation,
    "formula": f"SRM = {V:.4f} x {A:.4f} x {semantic_factor:.4f} x {N:.4f}",
    "note": "A is lower bound due to VADER English calibration on Romanian text"
}

with open('rezultate/SRM_simion_result.json', 'w') as f:
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
print("Saved: rezultate/SRM_simion_result.json")
