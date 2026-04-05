import math, json, argparse, os, sys
from datetime import datetime

def shannon_entropy(probs):
    t = sum(probs)
    p = [x/t for x in probs]
    return -sum(x*math.log(x) for x in p if x > 0)

def eef_score(probs):
    n = len(probs)
    S = shannon_entropy(probs)
    S_max = math.log(n)
    r = S / S_max
    zone = "CRITICAL" if r>0.80 else "HIGH" if r>0.60 else "MODERATE" if r>0.40 else "LOW"
    return {"S": round(S,6), "S_max": round(S_max,6), "ratio": round(r,6), "pct": round(r*100,2), "zone": zone}

def sensitivity(domains, deltas=[-0.20,-0.10,0.00,+0.10,+0.20]):
    results = {}
    for delta in deltas:
        scores = {}
        for name, probs in domains.items():
            p = [x/sum(probs) for x in probs]
            di = p.index(max(p))
            p_new = max(0.01, min(0.99, p[di]+delta))
            res = 1-p_new
            os_ = sum(x for i,x in enumerate(p) if i!=di)
            pert = [p_new if i==di else x*res/os_ for i,x in enumerate(p)]
            sc = eef_score(pert)
            scores[name] = sc["pct"]
        agg = sum(scores.values())/len(scores)
        label = f"{delta:+.0%}"
        results[label] = {"domains": scores, "agg": round(agg,2),
                          "zone": "CRITICAL" if agg>80 else "HIGH" if agg>60 else "MODERATE",
                          "baseline": delta==0}
    return results

def run(cfg):
    domains = cfg["domains"]
    country = cfg.get("country","Unknown")
    year = cfg.get("year","2024")
    scores = {k: eef_score(v) for k,v in domains.items()}
    agg_r = sum(s["ratio"] for s in scores.values())/len(scores)
    agg_zone = "CRITICAL" if agg_r>0.80 else "HIGH" if agg_r>0.60 else "MODERATE" if agg_r>0.40 else "LOW"
    sens = sensitivity(domains)

    print(f"\n{'='*60}")
    print(f"  EEF: {country} {year}")
    print(f"{'='*60}")
    print(f"  {'Domain':<16} {'S(t)':>8} {'S_max':>8} {'%':>8}  Zone")
    print(f"  {'-'*54}")
    for name, sc in scores.items():
        print(f"  {name:<16} {sc['S']:>8.4f} {sc['S_max']:>8.4f} {sc['pct']:>7.1f}%  {sc['zone']}")
    print(f"  {'-'*54}")
    print(f"  {'AGGREGATE':<16} {'':>8} {'':>8} {agg_r*100:>7.1f}%  {agg_zone}")
    print(f"\n  SENSITIVITY ANALYSIS")
    print(f"  {'Scenario':<10}", end="")
    for name in domains: print(f"  {name:>10}", end="")
    print(f"  {'Aggregate':>10}  Zone")
    for label, sc in sens.items():
        marker = " <-- baseline" if sc["baseline"] else ""
        print(f"  {label:<10}", end="")
        for name in domains: print(f"  {sc['domains'][name]:>9.1f}%", end="")
        print(f"  {sc['agg']:>9.1f}%  {sc['zone']}{marker}")
    print(f"{'='*60}\n")

    out = {"country":country,"year":year,"domains":scores,"aggregate":{"pct":round(agg_r*100,2),"zone":agg_zone},"sensitivity":sens}
    fname = f"EEF_{country.replace(' ','_')}_{year}.json"
    with open(fname,"w") as f: json.dump(out,f,indent=2)
    print(f"  Saved: {fname}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True, help="Path to JSON config file")
    args = p.parse_args()
    with open(args.config) as f:
        cfg = json.load(f)
    run(cfg)
