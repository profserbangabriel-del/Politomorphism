#!/usr/bin/env python3
"""
compute_eef.py — Entropic Equilibrium Function (EEF) Calculator
Politomorphism Framework | Serban Gabriel Florin | ORCID: 0009-0000-2266-3356
OSF: https://osf.io/hydnz | GitHub: github.com/profserbangabriel-del/Politomorphism

Usage:
    python compute_eef.py --config config_eef.json
    python compute_eef.py --country "Romania" --domain Justice 0.25 0.55 0.20 \
                          --domain Electoral 0.08 0.52 0.40 \
                          --domain Coalition 0.15 0.65 0.20

Output:
    EEF scores per domain + aggregate + sensitivity analysis
    JSON output saved to results/EEF_{country}_{year}.json
"""

import argparse
import json
import math
import os
import sys
from datetime import datetime


# ── Core EEF computation ───────────────────────────────────────────────

def shannon_entropy(probs: list[float]) -> float:
    """Shannon entropy H = -sum(p * log(p)) for a probability distribution."""
    total = sum(probs)
    normalized = [p / total for p in probs]
    return -sum(p * math.log(p) for p in normalized if p > 0)


def eef_score(probs: list[float]) -> dict:
    """
    Compute EEF score for a single domain.

    Args:
        probs: list of state probabilities (will be normalized to sum=1)

    Returns:
        dict with S, S_max, ratio, zone, classification
    """
    n = len(probs)
    if n < 2:
        raise ValueError("EEF requires at least N=2 states per domain.")

    S = shannon_entropy(probs)
    S_max = math.log(n)
    ratio = S / S_max

    if ratio > 0.80:
        zone = "CRITICAL"
        description = "Structural instability; disorder production exceeds self-regulation."
    elif ratio > 0.60:
        zone = "HIGH"
        description = "Significant institutional fragmentation; reform capacity under strain."
    elif ratio > 0.40:
        zone = "MODERATE"
        description = "Manageable tensions; institutional stress present but containable."
    else:
        zone = "LOW"
        description = "System near equilibrium; order-sustaining mechanisms functional."

    return {
        "S": round(S, 6),
        "S_max": round(S_max, 6),
        "ratio": round(ratio, 6),
        "ratio_pct": round(ratio * 100, 2),
        "zone": zone,
        "description": description,
        "n_states": n,
        "probs_normalized": [round(p / sum(probs), 4) for p in probs],
    }


def compute_aggregate(domain_scores: dict) -> dict:
    """Compute aggregate EEF score across all domains."""
    ratios = [d["ratio"] for d in domain_scores.values()]
    agg = sum(ratios) / len(ratios)

    if agg > 0.80:
        zone = "CRITICAL"
    elif agg > 0.60:
        zone = "HIGH"
    elif agg > 0.40:
        zone = "MODERATE"
    else:
        zone = "LOW"

    return {
        "ratio": round(agg, 6),
        "ratio_pct": round(agg * 100, 2),
        "zone": zone,
        "n_domains": len(domain_scores),
    }


# ── Sensitivity analysis ───────────────────────────────────────────────

def sensitivity_analysis(domains: dict, deltas: list[float] = None) -> dict:
    """
    Vary dominant state probability by ±delta, redistribute residual
    proportionally to other states. Reports aggregate EEF per scenario.

    Args:
        domains: {domain_name: [p1, p2, ...]}
        deltas: list of perturbations (default: [-0.20, -0.10, 0.00, +0.10, +0.20])

    Returns:
        dict of {delta: {domain: score, aggregate: score}}
    """
    if deltas is None:
        deltas = [-0.20, -0.10, 0.00, +0.10, +0.20]

    results = {}
    for delta in deltas:
        scenario_scores = {}
        for name, probs in domains.items():
            probs_arr = [p / sum(probs) for p in probs]
            dom_idx = probs_arr.index(max(probs_arr))

            p_new = probs_arr[dom_idx] + delta
            p_new = max(0.01, min(0.99, p_new))

            residual = 1.0 - p_new
            other_sum = sum(p for i, p in enumerate(probs_arr) if i != dom_idx)

            perturbed = []
            for i, p in enumerate(probs_arr):
                if i == dom_idx:
                    perturbed.append(p_new)
                else:
                    perturbed.append(p * residual / other_sum if other_sum > 0 else residual / (len(probs_arr) - 1))

            score = eef_score(perturbed)
            scenario_scores[name] = {
                "ratio_pct": score["ratio_pct"],
                "zone": score["zone"],
                "dominant_p": round(p_new, 3),
            }

        agg = sum(v["ratio_pct"] for v in scenario_scores.values()) / len(scenario_scores)
        agg_zone = "CRITICAL" if agg > 80 else ("HIGH" if agg > 60 else ("MODERATE" if agg > 40 else "LOW"))

        label = f"{delta:+.0%}"
        results[label] = {
            "domains": scenario_scores,
            "aggregate_pct": round(agg, 2),
            "aggregate_zone": agg_zone,
            "is_baseline": delta == 0.0,
        }

    return results


# ── IRR protocol helper ────────────────────────────────────────────────

def generate_irr_worksheet(country: str, year: str, domains: dict, sources: dict) -> str:
    """
    Generate a plain-text IRR coding worksheet for independent coders.
    Coder assigns p_i(t) values independently; compare with ICC afterward.
    """
    lines = [
        "=" * 70,
        f"EEF INTER-RATER RELIABILITY WORKSHEET",
        f"Country: {country} | Year: {year}",
        f"Coder ID: _____________ | Date: _____________",
        "=" * 70,
        "",
        "INSTRUCTIONS:",
        "  For each domain, assign probabilities to the three states.",
        "  Probabilities must sum to 1.00.",
        "  Base your estimates ONLY on the sources listed below.",
        "  Do NOT consult the baseline calibration before completing this form.",
        "",
        "STATE DEFINITIONS (identical across all domains):",
        "  State 1 (Functional/Legitimate/Stable): institutions operating",
        "           within constitutional norms, independent of political capture",
        "  State 2 (Capture/Crisis/Fragile): primary state is compromised",
        "           or contested; dominant dysfunction present",
        "  State 3 (Paralysis/Delegitimized/Collapse): institutional breakdown,",
        "           non-functionality, or loss of normative authority",
        "",
    ]

    for domain_name, source_list in sources.items():
        lines += [
            "-" * 70,
            f"DOMAIN: {domain_name.upper()}",
            "Sources to consult:",
        ]
        for src in source_list:
            lines.append(f"  - {src}")
        lines += [
            "",
            f"  p(State 1 — Functional/Legitimate/Stable):  ______",
            f"  p(State 2 — Capture/Crisis/Fragile):        ______",
            f"  p(State 3 — Paralysis/Delegitimized):       ______",
            f"  SUM (must = 1.00):                          ______",
            f"  Notes / justification:",
            f"  ________________________________________________________________",
            f"  ________________________________________________________________",
            "",
        ]

    lines += [
        "=" * 70,
        "AGGREGATE ASSESSMENT (circle one):",
        "  LOW (<40%)   MODERATE (40-60%)   HIGH (60-80%)   CRITICAL (>80%)",
        "",
        "Overall confidence in calibration (1=low, 5=high): ______",
        "=" * 70,
    ]

    return "\n".join(lines)


# ── Reporting ──────────────────────────────────────────────────────────

def print_report(country: str, year: str, domain_scores: dict,
                 aggregate: dict, sensitivity: dict) -> None:
    """Print formatted EEF report to stdout."""
    print("\n" + "=" * 70)
    print(f"  EEF REPORT: {country} {year}")
    print("=" * 70)

    print(f"\n{'Domain':<20} {'S(t)':>8} {'S_max':>8} {'%':>8} {'Zone':<10}")
    print("-" * 60)
    for name, sc in domain_scores.items():
        print(f"  {name:<18} {sc['S']:>8.4f} {sc['S_max']:>8.4f} "
              f"{sc['ratio_pct']:>7.1f}% {sc['zone']:<10}")

    print("-" * 60)
    print(f"  {'AGGREGATE':<18} {'':>8} {'':>8} "
          f"{aggregate['ratio_pct']:>7.1f}% {aggregate['zone']:<10}")

    print(f"\n{'SENSITIVITY ANALYSIS':^70}")
    print(f"{'Scenario':<16} {'Justice':>9} {'Electoral':>10} {'Coalition':>10} "
          f"{'Aggregate':>10} {'Zone'}")
    print("-" * 70)
    for label, sc in sensitivity.items():
        marker = " ← baseline" if sc["is_baseline"] else ""
        domains_pct = list(sc["domains"].values())
        cols = "  ".join(f"{d['ratio_pct']:>7.1f}%" for d in domains_pct)
        print(f"  {label:<14} {cols}  {sc['aggregate_pct']:>7.1f}%  "
              f"{sc['aggregate_zone']}{marker}")

    print("=" * 70)


# ── CLI ────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Compute EEF scores for political entropy analysis."
    )
    parser.add_argument("--config", help="Path to JSON config file")
    parser.add_argument("--country", help="Country name")
    parser.add_argument("--year", default=str(datetime.now().year), help="Year")
    parser.add_argument("--domain", nargs="+", action="append",
                        help="Domain name followed by probabilities: --domain Justice 0.25 0.55 0.20")
    parser.add_argument("--irr", action="store_true",
                        help="Generate IRR coding worksheet")
    parser.add_argument("--out", help="Output JSON file path")
    return parser.parse_args()


def load_config(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def main():
    args = parse_args()

    # Load from config or CLI
    if args.config:
        cfg = load_config(args.config)
        country = cfg.get("country", "Unknown")
        year = cfg.get("year", str(datetime.now().year))
        domains_raw = cfg.get("domains", {})
        sources = cfg.get("sources", {d: [] for d in domains_raw})
    elif args.domain and args.country:
        country = args.country
        year = args.year
        domains_raw = {}
        for d in args.domain:
            name = d[0]
            probs = [float(x) for x in d[1:]]
            domains_raw[name] = probs
        sources = {name: ["(no sources specified)"] for name in domains_raw}
    else:
        print("ERROR: Provide either --config or --country + --domain arguments.")
        print(__doc__)
        sys.exit(1)

    # Compute scores
    domain_scores = {name: eef_score(probs) for name, probs in domains_raw.items()}
    aggregate = compute_aggregate(domain_scores)
    sensitivity = sensitivity_analysis(domains_raw)

    # Print report
    print_report(country, year, domain_scores, aggregate, sensitivity)

    # Save JSON
    out_path = args.out or f"EEF_{country.replace(' ', '_')}_{year}.json"
    os.makedirs(os.path.dirname(out_path) if os.path.dirname(out_path) else ".", exist_ok=True)
    result = {
        "country": country,
        "year": year,
        "computed_at": datetime.now().isoformat(),
        "domains": domain_scores,
        "aggregate": aggregate,
        "sensitivity": sensitivity,
        "sources": sources,
    }
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n  Results saved to: {out_path}")

    # IRR worksheet
    if args.irr:
        ws = generate_irr_worksheet(country, year, domains_raw, sources)
        ws_path = f"IRR_worksheet_{country.replace(' ', '_')}_{year}.txt"
        with open(ws_path, "w") as f:
            f.write(ws)
        print(f"  IRR worksheet saved to: {ws_path}")


if __name__ == "__main__":
    main()
