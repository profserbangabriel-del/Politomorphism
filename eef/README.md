# EEF — Entropic Equilibrium Function

Politomorphism Framework | Serban Gabriel Florin
ORCID: 0009-0000-2266-3356 | OSF: https://doi.org/10.17605/OSF.IO/HYDNZ
GitHub: https://github.com/profserbangabriel-del/Politomorphism

## Overview

The Entropic Equilibrium Function (EEF) measures political systemic instability as Shannon entropy over institutional state distributions. It produces a static score S(t)/S_max per domain, an aggregate entropy score with zone classification, and a sensitivity analysis.

FIIM v2.0 (Fuzzy Institutional Instability Model) extends EEF by replacing hard threshold mapping with continuous fuzzy membership functions and combining Shannon entropy with a severity index: IS = 0.5 x H(p) + 0.5 x V(p).

## Formula

S(t) = -sum( p_i(t) * log(p_i(t)) )    Shannon entropy
S_max = log(N)                           maximum entropy for N states
ratio = S(t) / S_max                     normalized instability score

FIIM: IS(p) = 0.5 * H(p) + 0.5 * V(p)
  H(p) = normalized Shannon entropy
  V(p) = 0.5*p1 + 1.0*p2  (severity index)

dS/dt = Pi(t) - Phi(t)
  Pi(t)  = disorder-generating forces
  Phi(t) = order-restoring forces

Equilibrium: dS/dt = 0

## Entropy zones

| S(t)/S_max | Zone | Interpretation |
|---|---|---|
| > 80% | CRITICAL | Structural instability; disorder exceeds self-regulation |
| 60-80% | HIGH | Significant fragmentation; reform capacity under strain |
| 40-60% | MODERATE | Manageable tensions; stress containable |
| < 40% | LOW | System near equilibrium |

## State space (three domains, three states each)

| Domain | State 0 | State 1 | State 2 |
|---|---|---|---|
| Justice | Functional independence | Political capture | Paralysis/vacuum |
| Electoral | Legitimate functioning | Crisis/contested | Delegitimized/captured |
| Coalition | Stable and coherent | Fragile/conflictual | Collapse/reconfiguration |

## Cross-national results (2024)

| Country | Justice | Electoral | Coalition | Aggregate | Zone |
|---|---|---|---|---|---|
| Romania | 90.8% | 82.7% | 80.7% | 84.7% | CRITICAL |
| Hungary | 73.0% | 94.6% | 62.6% | 76.7% | HIGH |
| Poland | 97.1% | 84.3% | 88.7% | 90.1% | CRITICAL |

Sources: Freedom House NIT 2024; BTI 2026; EC Rule of Law 2024; Venice Commission 2024; INSCOP January 2026; EU Justice Scoreboard 2025.

## Files

| File | Description |
|---|---|
| compute_eef.py | Main script — computes EEF scores, sensitivity |
| config_eef_romania.json | Romania 2024 baseline calibration with sources |
| config_eef_hungary.json | Hungary 2024 cross-national validation |
| config_eef_poland.json | Poland 2024 cross-national validation |
| eef_longitudinal.py | Longitudinal validation 2005-2024 (FH NIT + BTI) |
| eef_interrater.py | Inter-rater reliability — Krippendorff alpha + Cohen kappa |
| eef_fiim.py | FIIM v2.0 — fuzzy membership + IS = H + V |
| eef_comparison_table.py | EEF vs FIIM comparison — hard vs fuzzy thresholds |
| eef_bootstrap.py | Bootstrap 95% CI for FIIM IS scores (n=1000) |

## Usage

Run EEF original:
python compute_eef.py --config config_eef_romania.json

Run FIIM v2.0:
python eef_fiim.py

Run longitudinal validation:
python eef_longitudinal.py

Run inter-rater reliability:
python eef_interrater.py

Run bootstrap CI:
python eef_bootstrap.py

## Adding a new country

Create a JSON config file with this structure:

{
  "country": "CountryName",
  "year": "2024",
  "domains": {
    "Justice":   [p_functional, p_capture, p_paralysis],
    "Electoral": [p_legitimate, p_crisis, p_delegitimized],
    "Coalition": [p_stable, p_fragile, p_collapse]
  },
  "sources": {
    "Justice":   ["Source 1", "Source 2"],
    "Electoral": ["Source 1", "Source 2"],
    "Coalition": ["Source 1", "Source 2"]
  }
}

Then run:
python compute_eef.py --config config_eef_yourcountry.json

## Requirements

Python >= 3.10. No external dependencies.

## Citation

Florin, S.G. (2026). Politomorphism and the Measurement of Political Systemic Instability: The Entropic Equilibrium Function (EEF). Politomorphism Framework Working Paper. OSF: https://doi.org/10.17605/OSF.IO/HYDNZ

## License

CC BY 4.0 — Open for replication, extension, and empirical validation.
