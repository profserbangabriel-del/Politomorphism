# EEF â€” Entropic Equilibrium Function

**Politomorphism Engine | Complete Methodology Documentation**

Sections 3.2 Â· 3.3 Â· 3.4 Â· 3.5 Â· 3.6 Â· 3.7 Â· Validation Â· Appendix

Prof. Serban Gabriel Florin | ORCID: 0009-0000-2266-3356
OSF: https://doi.org/10.17605/OSF.IO/HYDNZ | GitHub: profserbangabriel-del/Politomorphism

---

## Overview

The Entropic Equilibrium Function (EEF) measures political systemic instability as Shannon entropy over institutional state distributions. It produces a static score H(t) per domain, an aggregate instability score with zone classification, and a sensitivity analysis.

FIIM v2.1 (Fuzzy Institutional Instability Model) extends EEF by replacing hard threshold mapping with continuous fuzzy membership functions and combining normalized entropy with an expected institutional cost index.

---

## Architecture

```mermaid
flowchart TD
    A[Freedom House NIT] --> D[pâ‚€ pâ‚ pâ‚‚ per domain]
    B[BTI Participation] --> D
    C[EC Rule of Law] --> D
    D --> E1[Justice domain]
    D --> E2[Electoral domain]
    D --> E3[Coalition domain]
    E1 --> F1["H(t) â€” Shannon entropy"]
    E2 --> F1
    E3 --> F1
    E1 --> F2["V(t) â€” Expected institutional cost"]
    E2 --> F2
    E3 --> F2
    F1 --> G["IS(t) = Î±Â·H(t) + (1âˆ’Î±)Â·V(t)   Î±=0.5"]
    F2 --> G
    G --> H["Î”IS(t) = IS(t) âˆ’ IS(tâˆ’1)"]
    H --> I["IS_comp(t) = IS(t) + Î²Â·Î”IS(t)   Î²=0.2"]
    I --> J{Zone classification}
    J --> K["CRITICAL  >0.70"]
    J --> L["HIGH      0.55â€“0.70"]
    J --> M["MODERATE  0.40â€“0.55"]
    J --> N["LOW       <0.40"]
    G --> O[delta_FH â€” directional indicator]
    O --> P{Direction}
    P --> Q[DETERIORATING]
    P --> R[STABLE]
    P --> S[CONSOLIDATING]
```

---

## Notation

| Symbol | Definition |
|---|---|
| $S(t)$ | Raw Shannon entropy: $S(t) = -\sum p_i(t) \cdot \ln(p_i(t))$ [nats, base e] |
| $S_{\max}$ | Maximum entropy: $\ln(N) = \ln(3) \approx 1.0986$ nats |
| $H(t)$ | Normalized entropy: $H(t) = S(t) / S_{\max} \in [0,1]$ |
| $V(t)$ | Expected institutional cost: $V(t) = 0.0 \cdot p_0 + 0.5 \cdot p_1 + 1.0 \cdot p_2$ |
| $IS(t)$ | Static instability score: $IS(t) = \alpha \cdot H(t) + (1-\alpha) \cdot V(t),\ \alpha = 0.5$ |
| $\Delta IS(t)$ | Discrete dynamics: $\Delta IS(t) = IS(t) - IS(t-1)$ |
| $\Pi(t)$ | Disorder-increasing component: $\Pi(t) = \max(0, \Delta IS(t))$ |
| $\Phi(t)$ | Order-restoring component: $\Phi(t) = \max(0, -\Delta IS(t))$ |
| $IS_{\text{comp}}(t)$ | Composite forward-looking score: $IS_{\text{comp}}(t) = IS(t) + \beta \cdot \Delta IS(t),\ \beta = 0.2$ |

---

## 3.2 Operationalization of the EEF

For each institutional domain $d \in \{\text{Justice, Electoral, Coalition}\}$, the system state at time $t$ is modeled as a discrete random variable with 3 ordered states:

| State | Label | Interpretation |
|---|---|---|
| $S_0$ | Favorable / Stable | Functional institutions; tensions absent or minor |
| $S_1$ | Intermediate / Strained | Significant dysfunctions; regulatory capacity under pressure |
| $S_2$ | Critical / Dysfunctional | Partial or total institutional failure; self-regulation exhausted |

### Shannon Entropy and Normalized Score

$$S(t) = -\sum_i p^d_i(t) \cdot \ln(p^d_i(t))$$

$$S_{\max} = \ln(3) \approx 1.0986 \text{ nats}$$

$$H(t) = \frac{S(t)}{S_{\max}} \in [0,1]$$

$$R_{EEF}(t) = \frac{1}{3} \cdot \sum_d H^d(t)$$

### Risk Zone Classification

| $R_{EEF}(t)$ | Zone | Interpretation |
|---|---|---|
| $> 0.80$ | CRITICAL | Structural instability; disorder exceeds self-regulation |
| $0.60 - 0.80$ | HIGH | Significant fragmentation; reform capacity under strain |
| $0.40 - 0.60$ | MODERATE | Manageable tensions; stress is containable |
| $< 0.40$ | LOW | System near equilibrium |

---

## 3.3 Entropic Dynamics: Operationalization of Î”IS(t)

> Note: Shannon entropy is computed on discrete annual distributions. Continuous-time notation dS/dt is replaced by discrete Î”IS(t) = IS(t) âˆ’ IS(tâˆ’1).

$$\Pi(t) = \max(0,\ \Delta IS(t)) \quad \text{disorder-increasing component}$$

$$\Phi(t) = \max(0,\ -\Delta IS(t)) \quad \text{order-restoring component}$$

$$IS_{\text{comp}}(t) = IS(t) + \beta \cdot \Delta IS(t), \quad \beta = 0.2$$

| Value of $\Delta IS(t)$ | Interpretation |
|---|---|
| $> 0$ | System deteriorating â€” disorder exceeds regulatory capacity |
| $= 0$ | Dynamic equilibrium â€” tensions are containable |
| $< 0$ | System consolidating â€” reforms outpace disruptive pressures |

---

## 3.4 Longitudinal Validation: 2005â€“2024

The EEF framework was applied to a 20-year panel dataset covering Romania, Hungary, and Poland (2005â€“2024), using Freedom House NIT (Judicial Framework & Independence; Electoral Process, annual) and BTI Political Participation (biennial, odd years linearly interpolated).

### Table 3.4.1 â€” EEF Aggregate Scores (Selected Years)

| Year | Romania R_EEF | Zone | Hungary R_EEF | Zone | Poland R_EEF | Zone |
|---|---|---|---|---|---|---|
| 2005 | 88.3% | CRITICAL | 89.5% | CRITICAL | 83.5% | CRITICAL |
| 2011 | 89.2% | CRITICAL | 85.1% | CRITICAL | 84.0% | CRITICAL |
| 2015â€  | 89.9% | CRITICAL | 77.6% | HIGH | 89.0% | CRITICAL |
| 2018 | 89.2% | CRITICAL | 76.7% | HIGH | 90.2% | CRITICAL |
| 2024 | 87.8% | CRITICAL | 66.8% | HIGH | 90.2% | CRITICAL |

â€  2015: Hungary zone transition CRITICAL â†’ HIGH coincides with FH NIT Judicial score crossing below 2.25.

### Longitudinal Trajectories

![IS_agg Longitudinal 2005â€“2024](../eef_chart_longitudinal.png)

**Key findings:**
- **Hungary**: monotonic escalation from MODERATE (2005, IS=49.99) to HIGH (2024, IS=68.43). Critical inflection point: 2011 (OrbÃ¡n constitutional reforms, IS jumps to 60.36).
- **Poland**: full backsliding-then-recovery arc. Peak in 2019 (IS=61.66, HIGH) during judicial crisis. Recovery to MODERATE by 2024 (IS=54.60) under Tusk government â€” the only case capturing a complete democratic erosion and reversal cycle.
- **Romania**: stable MODERATE band (IS=52â€“57) throughout, with a 2024 spike to HIGH (IS=57.56) driven by the Georgescu electoral shock.

---

## 3.5 FIIM v2.1 â€” Fuzzy Institutional Instability Model

FIIM v2.1 replaces hard threshold mapping with continuous fuzzy membership functions, eliminating arbitrary boundary discontinuities. The instability score IS(t) combines two conceptually distinct components:

$$IS(t) = \alpha \cdot H(t) + (1-\alpha) \cdot V(t), \quad \alpha = 0.5$$

| Component | Formula | Interpretation |
|---|---|---|
| $H(t)$ | $S(t) / \ln(3) \in [0,1]$ | Distributional uncertainty â€” how contested is the system? |
| $V(t)$ | $0.0 \cdot p_0 + 0.5 \cdot p_1 + 1.0 \cdot p_2$ | Expected institutional cost $E[c(X)]$ â€” how severe is the dominant state? |

### Fuzzy Membership Functions

$$\mu_{S_0}(x) = \text{smf}(x, a, b) \quad \text{S-shaped: 0 at } x \leq a,\ 1 \text{ at } x \geq b$$

$$\mu_{S_1}(x) = \text{trimf}(x, c, hw) \quad \text{Triangular: peak at center } c$$

$$\mu_{S_2}(x) = \text{zmf}(x, a, b) \quad \text{Z-shaped: 1 at } x \leq a,\ 0 \text{ at } x \geq b$$

$$p_i = \frac{\mu_{S_i}(x)}{\sum_j \mu_{S_j}(x)} \quad \text{[normalization]}$$

> **Key advantage:** A score of 3.74 and 3.76 produce smoothly different probability vectors â€” not identical outputs or discontinuous jumps as in hard-threshold mapping. This eliminates the boundary sensitivity problem identified in the original EEF.

### FIIM v2.1 Results â€” 2024

![Domain Scores by Country (2024)](../eef_chart_domains_2024.png)

| Country | IS Justice | IS Electoral | IS Coalition | IS_agg / Zone |
|---|---|---|---|---|
| Romania | 50.7% | 74.4% | 47.6% | **57.6% / HIGH** |
| Hungary | 69.9% | 70.7% | 64.6% | **68.4% / HIGH** |
| Poland | 62.5% | 57.9% | 43.3% | **54.6% / MODERATE** |

> FIIM produces lower IS scores than EEF original because fuzzy membership distributes probability across all three states simultaneously, reducing entropy compared to hard-threshold vectors that concentrate mass in one state. The directional indicator Î”FH_NIT supplements IS to distinguish democratic consolidation from autocratic capture.

### EEF vs FIIM Comparison

![EEF vs FIIM Comparison (2024)](../eef_chart_comparison.png)

---

## 3.6 Anti-Corruption Domain Extension â€” Romania

For Romania, a fourth domain is operationalized using three indicators unique to the Romanian institutional context: the Transparency International Corruption Perceptions Index (CPI, annual), the DNA normalized prosecution rate (annual indicted persons normalized to peak year 2016), and the DNA conviction rate (fraction of definitively judged persons convicted).

$$p_{AC}(t) = 0.40 \cdot p_{CPI} + 0.35 \cdot p_{\text{prosecution}} + 0.25 \cdot p_{\text{conviction}}$$

Weights reflect relative validity: CPI (40%) is the most comprehensive external validator; prosecution rate (35%) captures institutional activity; conviction rate (25%) captures prosecution quality.

### Table 3.6.1 â€” Anti-Corruption Domain Indicators â€” Romania 2005â€“2024 (Selected)

| Year | CPI | DNA Pros. Rate | DNA Conv. Rate | IS_AC% | Event |
|---|---|---|---|---|---|
| 2005 | 30 | 0.18 | 0.72 | â€” | Baseline |
| 2013 | 43 | 0.55 | 0.88 | â€” | Kovesi appointed |
| 2016 | 48 | 1.00 | 0.92 | Peak | DNA all-time peak |
| 2017 | 48 | 0.72 | 0.85 | â†‘ ESCALATING | OUG13 |
| 2019 | 44 | 0.55 | 0.78 | â†‘ ESCALATING | Kovesi departure |
| 2024 | 46 | 0.60 | 0.88 | â†“ STABLE | CCR annulment |

Source: Transparency International CPI 2005â€“2024; DNA Annual Reports (dna.ro); DNA 2025 Annual Report (conviction rate 90.41%).

![Anti-Corruption Domain Romania 2005â€“2024](../eef_chart_anticorruption.png)

---

## 3.7 Inter-Rater Reliability

A systematic inter-rater reliability test was conducted across 180 domain-year observations (3 domains Ã— 3 countries Ã— 20 years). Three virtual raters were simulated: Rater 1 (baseline), Rater 2 (pessimistic shift âˆ’0.25), Rater 3 (optimistic shift +0.25).

| Domain | Weighted Îº (R1 vs R2) | Krippendorff Î± | Result |
|---|---|---|---|
| Justice | 0.8148 | 0.7513 | OK |
| Electoral | 0.7143 | 0.4303 | * |
| Coalition | 0.9247 | 0.9457 | OK |
| **AGGREGATE** | **0.8679** | **0.8116** | **OK** |

\* Electoral domain Î± = 0.43 due to boundary-proximate observations in Poland 2007â€“2014 and Hungary 2017â€“2020. Acknowledged limitation; additional OSCE sources recommended for future validation.

Aggregate Krippendorff Î± = 0.8116 exceeds the conventional threshold of Î± â‰¥ 0.800 (Krippendorff 2004). All 28 disagreements (15.6%) were strictly off-by-one on the ordinal scale; no Sâ‚€â†”Sâ‚‚ disagreements were found.

---

## Validation Results

### Bootstrap 95% Confidence Intervals

![Bootstrap CI](../eef_chart_bootstrap_ci.png)

### Sensitivity Analysis (Î± = 0.3â€“0.7)

![Sensitivity Analysis](../eef_chart_sensitivity.png)

### V-Dem Convergent Validity

![V-Dem Validity](../eef_chart_vdem_validity.png)

### Out-of-Sample Validation

![Out-of-Sample](../eef_chart_outofsampe.png)

### Summary Table

| Validation | Result |
|---|---|
| Krippendorff alpha (inter-rater reliability) | 0.8116 |
| Bootstrap CI width â€” MODERATE zone (n=1000) | 2.20â€“4.62 pp |
| Bootstrap CI width â€” HIGH zone (n=1000) | 1.20â€“2.88 pp |
| V-Dem convergent validity â€” Hungary (Pearson r) | âˆ’0.980, p<0.0001 |
| V-Dem convergent validity â€” Poland (Pearson r) | âˆ’0.941, p<0.0001 |
| V-Dem convergent validity â€” Romania (Pearson r) | âˆ’0.180, p=0.446 |
| Out-of-sample F1 â€” Romania 2024 (EEF vs FH) | 0.333 vs 0.000 |
| LOOCV accuracy (n=60) | 1.000 |
| LOOCV F1 macro (n=60) | 1.000 |
| LOOCV threshold stability (mean Â± SD) | 0.5524 Â± 0.0003 |

> **Note on Romania V-Dem:** The non-significant correlation (p=0.446) reflects structural instability without directional democratic change. The EEF captures static high-entropy institutional fragmentation, while V-Dem LDI measures liberal democratic quality which has not dramatically shifted in Romania over the observation period. This is a substantively interpretable finding, not a validity threat.

---

## Files

| File | Description |
|---|---|
| `compute_eef.py` | Main script â€” computes EEF scores, sensitivity |
| `config_eef_romania.json` | Romania 2024 baseline calibration with sources |
| `config_eef_hungary.json` | Hungary 2024 cross-national validation |
| `config_eef_poland.json` | Poland 2024 cross-national validation |
| `eef_longitudinal.py` | Longitudinal validation 2005â€“2024 (FH NIT + BTI) |
| `eef_interrater.py` | Inter-rater reliability â€” Krippendorff alpha + Cohen kappa |
| `eef_fiim.py` | FIIM v2.1 â€” fuzzy membership, H(t), V(t), IS_comp |
| `eef_comparison_table.py` | EEF vs FIIM comparison â€” hard vs fuzzy thresholds |
| `eef_bootstrap.py` | Bootstrap 95% CI for FIIM IS scores (n=1000) |
| `eef_anticorruption_romania.py` | Anti-corruption validation Romania â€” CPI correlation |
| `eef_visualize.py` | All visualization charts (PNG) |
| `eef_vdem_validation.py` | V-Dem convergent validity â€” Pearson r, Spearman rho |
| `eef_sensitivity_alpha.py` | Sensitivity analysis alpha=0.3â€“0.7 |
| `eef_outofsampe.py` | Out-of-sample validation â€” F1 vs FH baseline |
| `eef_loocv.py` | Leave-One-Out Cross-Validation â€” accuracy=1.000, F1=1.000 |

---

## Usage

```bash
# Run EEF original
python compute_eef.py --config config_eef_romania.json

# Run FIIM v2.1
python eef_fiim.py

# Run longitudinal validation
python eef_longitudinal.py

# Run inter-rater reliability
python eef_interrater.py

# Run bootstrap CI
python eef_bootstrap.py

# Run V-Dem convergent validity
python eef_vdem_validation.py

# Run sensitivity analysis
python eef_sensitivity_alpha.py

# Run out-of-sample validation
python eef_outofsampe.py

# Run LOOCV
python eef_loocv.py
```

---

## Adding a New Country

Create a JSON config file with this structure:

```json
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
```

Then run:

```bash
python compute_eef.py --config config_eef_yourcountry.json
```

---

## Requirements

Python >= 3.10. No external dependencies.

---

## Key References

- Freedom House. *Nations in Transit 2005â€“2024*. freedomhouse.org
- Bertelsmann Stiftung. *Transformation Index (BTI) 2006â€“2024*. bti-project.org
- Transparency International. *Corruption Perceptions Index 2005â€“2024*. transparency.org
- DNA. *Annual Activity Reports 2005â€“2024*. dna.ro
- European Commission. *Rule of Law Report 2020â€“2024*.
- Krippendorff, K. (2004). *Content Analysis: An Introduction to Its Methodology*. Sage.
- Landis, J.R. & Koch, G.G. (1977). The measurement of observer agreement for categorical data. *Biometrics* 33(1), 159â€“174.
- Shannon, C.E. (1948). A mathematical theory of communication. *Bell System Technical Journal* 27, 379â€“423.

---

## Citation

Florin, S.G. (2026). Politomorphism and the Measurement of Political Systemic Instability: The Entropic Equilibrium Function (EEF). Politomorphism Framework Working Paper. OSF: https://doi.org/10.17605/OSF.IO/HYDNZ

---

## License

CC BY 4.0 â€” Open for replication, extension, and empirical validation.
