# Politomorphism — Social Resonance Model (SRM)

**Serban Gabriel Florin** | Independent Researcher  
ORCID: [0009-0000-2266-3356](https://orcid.org/0009-0000-2266-3356) | DOI: [10.17605/OSF.IO/HYDNZ](https://doi.org/10.17605/OSF.IO/HYDNZ)  
GitHub: [profserbangabriel-del/politomorphism](https://github.com/profserbangabriel-del/politomorphism)

---

## What is Politomorphism?

Politomorphism is a theoretical framework that treats political symbols as **morphogenetic agents** — entities that transform power structures through the process of symbolic diffusion. Its computational component, the **Social Resonance Model (SRM)**, provides a quantitative measure of how effectively a political symbol mobilizes public space.

---

## The SRM Formula

**SRM = V × A × e^(−λD) × N** (λ = 2)

| Variable | Name | What it measures | Range |
|----------|------|-----------------|-------|
| V | Viral Velocity | Log-normalized escalation ratio between peak media presence and pre-event baseline | 0–1 |
| A | Affective Weight | Emotional intensity of coverage — computed via VADER sentiment analysis on article titles | 0–1 |
| D | Semantic Drift | How fragmented the symbol's meaning is across different contexts. **Most impactful variable** due to its exponential position | 0–1 |
| N | Network Coverage | Proportion of days where the symbol appears in the corpus | 0–1 |

---

## How to Read the SRM Score

| 0.00 | 0.07 | 0.20 | 1.00 |
|------|------|------|------|
| LOW RESONANCE | → | MEDIUM RESONANCE | HIGH RESONANCE |

---

## The 6 Diagnostic Categories

### 1. Fragmented Diffusion Symbol
High visibility, extreme semantic drift, politically inert. Example: **Călin Georgescu (D=0.881)**.

### 2. Post-Executive Symbolic Trap
Institutional role transition generates unavoidable semantic fragmentation. Example: **Marcel Ciolacu (D=0.841)**.

### 3. High-Velocity Campaign Symbol
Exceptional diffusion speed, moderate semantic coherence. Example: **Donald Trump (V=0.958, SRM=0.0922)**.

### 4. Sustained Wartime Medium-Resonance Symbol
Multi-year high visibility, coherence through crisis framing. Example: **Volodymyr Zelensky (D=0.680, SRM=0.1121)**.

### 5. Pre-Saturated Contradicted Symbol
Maximum visibility, low resonance due to acute pre-saturation and geopolitical contradiction. Example: **Vladimir Putin (V=0.217, N=1.000, SRM=0.0103)**.

### 6. Longevity Saturation Symbol *(new — Case Study 8)*
Chronic long-term media presence prevents symbolic emergence. Example: **Viktor Orbán (V=0.168, 15+ years baseline, SRM=0.0065)**.

### 7. Legacy Resonance Symbol *(new — Case Study 9)*
Acute death/memorial spike combined with near-universal semantic consensus suppresses SRM despite high V. Example: **Nelson Mandela (V=0.311, D=0.742, SRM=0.0088)**.

### 8. Rapid Emergence Symbol *(new — Case Study 10)*
Fast escalation from near-zero baseline suppressed by high Semantic Drift and low Affective Weight. Example: **Emmanuel Macron (V=0.507, D=0.810, A=0.168, SRM=0.0169)**.
Acute death/memorial spike combined with near-universal semantic consensus suppresses SRM despite high V. Example: **Nelson Mandela (V=0.311, D=0.742, SRM=0.0088)**.

---

## Comparative Dataset — 10 Validated Symbols

| Symbol / Context | V | A | D | N | SRM | Category |
|-----------------|---|---|---|---|-----|----------|
| George Simion (RO, 2024–26) | 0.279 | 0.099* | 0.812 | 0.996 | 0.0054 | Low — Fragmented Diffusion |
| Viktor Orbán (HU, 2022–26) | 0.168 | 0.236 | 0.798 | 0.812 | 0.0065 | Low — Longevity Saturation |
| **Nelson Mandela (SA, 2013)** | **0.311** | **0.246** | **0.742** | **0.510** | **0.0088** | **Low — Legacy Resonance** |
| Vladimir Putin (2022–26) | 0.217 | 0.259 | 0.847 | 1.000 | 0.0103 | Low — Pre-Saturated Contradicted |
| **Emmanuel Macron (FR, 2017)** | **0.507** | **0.168** | **0.810** | **1.000** | **0.0169** | **Low — Rapid Emergence** |
| Călin Georgescu (RO, 2024) | 0.750 | 0.398 | 0.881 | 0.600 | 0.0307 | Low — Fragmented Diffusion |
| Marcel Ciolacu (RO, 2025–26) | 0.720 | 0.420 | 0.841 | 0.650 | 0.0365 | Low — Post-Executive Trap |
| Sunflower Mvt (TW, 2014) | 0.680 | 0.420 | 0.774 | 0.580 | 0.0376 | Low — Fragmented Diffusion |
| Donald Trump (US, 2015–16) | 0.958 | 0.580 | 0.734 | 0.720 | 0.0922 | Medium — High-Velocity Campaign |
| Zelensky (UA/EU/US, 2022–26) | 0.873 | 0.640 | 0.680 | 0.781 | 0.1121 | Medium — Wartime Symbol |

*\* A=0.099 is lower bound due to VADER English calibration on Romanian text.*

---

## Case Studies

### Case Study 1 — Sunflower Movement (Taiwan, 2014)

| V | A | D | N | SRM | Interpretation |
|---|---|---|---|-----|----------------|
| 0.680 | 0.420 | 0.7737 | 0.580 | 0.0376 | LOW RESONANCE |

### Case Study 2 — Călin Georgescu (Romania, Oct–Dec 2024)

| V | A | D | N | SRM | Interpretation |
|---|---|---|---|-----|----------------|
| 0.750 | 0.398 | 0.8813 | 0.600 | 0.0307 | LOW RESONANCE |

Results: [SRM_raport_final.json](SRM_raport_final.json) | Chart: [SRM_grafic_final.png](SRM_grafic_final.png)

### Case Study 3 — Marcel Ciolacu (Romania, Dec 2025 – Mar 2026)

Data: Media Cloud Romania National + State & Local | 339 articles | 91 days

| V | A | D | N | SRM | Interpretation |
|---|---|---|---|-----|----------------|
| 0.720 | 0.420 | 0.8412 | 0.650 | 0.0365 | LOW RESONANCE |

Paper: [SRM_Ciolacu_Validation.docx](SRM_Ciolacu_Validation.docx) | Data: [data_ciolacu/](data_ciolacu/)

### Case Study 4 — Donald Trump (USA, Feb 2015 – Nov 2016)

Data: Media Cloud US National + State & Local | 640 daily observations

| V | A | D | N | SRM | Interpretation |
|---|---|---|---|-----|----------------|
| 0.958 | 0.580 | 0.7340 | 0.720 | 0.0922 | MEDIUM RESONANCE |

Results: [SRM_trump_result.json](SRM_trump_result.json) | Chart: [SRM_trump_grafic.png](SRM_trump_grafic.png)

### Case Study 5 — Volodymyr Zelensky (UA/EU/US, May 2022 – Feb 2026)

Data: Media Cloud US National + Europe | 2,387 daily observations

| V | A | D | N | SRM | Interpretation |
|---|---|---|---|-----|----------------|
| 0.873 | 0.640 | 0.680 | 0.781 | 0.1121 | MEDIUM RESONANCE |

Paper: [SRM_Zelensky_Validation.docx](SRM_Zelensky_Validation.docx) | Data: [data_zelensky/](data_zelensky/)

### Case Study 6 — Vladimir Putin (2022–2026)

Data: Media Cloud US National + US State & Local | 2,472 daily observations

| V | A | D | N | SRM | Interpretation |
|---|---|---|---|-----|----------------|
| 0.217 | 0.259 | 0.847 | 1.000 | 0.0103 | LOW RESONANCE |

**Pre-Saturation Paradox:** N=1.000 every day yet SRM=0.0103. **First Antagonistic Symbol Pair** with Zelensky — SRM gap 0.1018.

![SRM Putin Chart](data_putin/SRM_Putin_chart.png)

Paper: [SRM_Putin_Validation.docx](SRM_Putin_Validation_FINAL_V4.docx) | Data: [data_putin/](data_putin/)

### Case Study 7 — George Simion (Romania, Oct 2024 – Mar 2026)

Data: Media Cloud Romanian National + State & Local | 1,533 daily observations

| V | A | D | N | SRM | Interpretation |
|---|---|---|---|-----|----------------|
| 0.279 | 0.099* | 0.812 | 0.996 | 0.0054 | LOW RESONANCE |

**Romanian Triada:** Georgescu + Ciolacu + Simion — first within-country controlled comparison. All three produce Low Resonance. **Peak:** May 2025 (ratio=0.253) — turul 2 prezidențiale.

![SRM Simion Chart](data_simion/SRM_simion_chart.png)

Paper: [SRM_Simion_Validation.docx](SRM_Simion_Validation.docx) | Data: [data_simion/](data_simion/)

### Case Study 8 — Viktor Orbán (Hungary, 2022–2026)

Data: Media Cloud US National + US State & Local + European | 6,268 daily observations  
Baseline: Jan 1, 2010 – Dec 31, 2022 (4,748 obs.) | Analysis: Jan 1, 2022 – Feb 28, 2026 (1,520 obs.)

| V | A | D | N | SRM | Interpretation |
|---|---|---|---|-----|----------------|
| 0.168 | 0.236 | 0.798 | 0.812 | 0.0065 | LOW RESONANCE |

**Longevity Paradox:** 15+ years of media presence produces V=0.168 — structurally equivalent to Putin's acute pre-saturation. Chronic baseline dominance prevents symbolic emergence. **Peak:** April 3, 2022 — Hungarian parliamentary elections (4th consecutive victory, 2/3 majority).
![SRM Orban Chart](data_orban/SRM_Orban_chart.png)

Paper: [SRM_Orban_Validation.docx](SRM_Orban_Validation.docx) | Data: [data_orban/](data_orban/)

---

### Case Study 9 — Nelson Mandela (South Africa, 2013)

Data: Media Cloud US National + US State & Local | 1,096 daily observations  
Baseline: Jan 1, 2010 – Jan 1, 2012 (731 obs.) | avg 3.63 articles/day | avg ratio 0.000639  
Analysis: Jan 1, 2013 – Dec 31, 2013 (365 obs.) | avg 23.14 articles/day | avg ratio 0.002679  
VADER corpus: 4,070 English titles containing "mandela" | Total articles: 11,102

| V | A | D | N | SRM | Interpretation |
|---|---|---|---|-----|----------------|
| 0.311 | 0.246 | 0.742 | 0.510 | 0.0088 | LOW RESONANCE |

**Legacy Paradox:** Mandela's death (December 5, 2013) generated the highest single-day ratio in the dataset (0.08618 on Dec 6) — yet annual SRM=0.0088 due to semantic coherence compression (e⁻ᵏᴰ=0.2267). Near-universal positive consensus (D=0.742, lowest after Zelensky) prevents discourse fragmentation. **Seventh typology identified: Legacy Resonance Symbol.**

**Peak events:**
- Dec 6, 2013 — ratio=0.08618 (death announced, 373 articles)
- Dec 10, 2013 — ratio=0.05247 (Memorial at FNB Stadium, 100+ world leaders)
- Dec 5, 2013 — ratio=0.05037 (breaking news of passing)
- Jun 2013 — avg ratio=0.005329 (hospitalization coverage peak)

![SRM Mandela Chart](data_mandela/SRM_Mandela_chart.png)

Paper: [SRM_Mandela_Validation.docx](SRM_Mandela_Validation.docx) | Data: [data_mandela/](data_mandela/)

---

### Case Study 10 — Emmanuel Macron (France, 2017)

Data: Media Cloud US National + Europe Media Monitor | 1,096 daily observations  
Baseline: Jan 1, 2015 – Dec 31, 2016 (731 obs.) | avg 54.7 articles/day | avg ratio 0.000438  
Analysis: Jan 1, 2017 – Dec 31, 2017 (365 obs.) | avg 866.5 articles/day | avg ratio 0.006027  
VADER corpus: 1,304 English titles containing "macron" | Total articles: 79,964

| V | A | D | N | SRM | Interpretation |
|---|---|---|---|-----|----------------|
| 0.507 | 0.168 | 0.810 | 1.000 | 0.0169 | LOW RESONANCE |

**Rapid Emergence Paradox:** 13.75x escalation (highest V in Low Resonance cohort, V=0.5074) offset by low A=0.1681 (analytical framing of complex political project) and high D=0.810 (5 contradictory frames). **Peak:** May 7, 2017 — presidential election victory (ratio=0.072, 7,542 articles). **Eighth typology: Rapid Emergence Symbol.**

**Peak events:**
- May 7, 2017 — ratio=0.07227 (election victory, 7,542 articles)
- May 8, 2017 — ratio=0.05278 (post-victory reactions, 8,639 articles — highest single day)
- Apr 24, 2017 — ratio=0.04950 (first round results confirmed, 8,166 articles)
- Apr 23, 2017 — ratio=0.04912 (election day first round)
- May 14, 2017 — ratio=0.02809 (presidential inauguration)

![SRM Macron Chart](data_macron/SRM_Macron_chart.png)

Paper: [SRM_Macron_Validation.docx](SRM_Macron_Validation.docx) | Data: [data_macron/](data_macron/)

---

## Repository Structure

```
politomorphism/
├── .github/workflows/
│   ├── srm_ciolacu_validation.yml
│   ├── srm_zelensky_validation.yml
│   ├── srm_putin_validation.yml
│   ├── srm_simion_validation.yml
│   └── srm_orban_validation.yml
├── srm_pipeline/
│   ├── mandela_collect.py
│   ├── pas2_A_sentiment.py
│   ├── pas2_A_simion.py
│   ├── pas2_A_orban.py
│   ├── pas3_D_semantic_drift.py
│   ├── pas4_N_gdelt.py
│   ├── pas4_N_simion.py
│   ├── pas4_N_orban.py
│   ├── pas5_SRM_final.py
│   ├── pas5_SRM_mandela.py
│   ├── pas5_SRM_simion.py
│   └── pas5_SRM_orban.py
├── data_macron/
│   ├── macron_baseline.csv
│   ├── macron_analysis.csv
│   ├── macron_titles.csv
│   └── SRM_Macron_chart.png
├── data_mandela/
│   ├── mandela_baseline.csv
│   ├── mandela_analysis.csv
│   ├── mandela_titles.csv
│   └── mandela_counts_combined.csv
├── data_ciolacu/
├── data_sunflower/
├── data_zelensky/
├── data_putin/
├── data_simion/
└── data_orban/
```

---

## Reproducibility

All data, code, and results are open source and publicly available.  
Data source: [mediacloud.org](https://mediacloud.org)  
Licence: CC BY 4.0
