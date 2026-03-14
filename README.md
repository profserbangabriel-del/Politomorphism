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
| V | Viral Velocity | How fast the symbol spreads — computed as a log-normalized escalation ratio between peak media presence and pre-event baseline | 0–1 |
| A | Affective Weight | Emotional intensity of coverage — computed via VADER sentiment analysis on article titles | 0–1 |
| D | Semantic Drift | How fragmented the symbol's meaning is across different contexts. **This is the most impactful variable** due to its exponential position in the formula. | 0–1 |
| N | Network Coverage | Proportion of days (or sources) where the symbol appears in the corpus | 0–1 |

> **Key insight:** The formula is not a simple average. Semantic Drift (D) is exponentially penalized — a D of 0.88 compresses the final score by 83%, regardless of how visible or emotional the symbol is. This captures a real phenomenon: a symbol can be everywhere and mean nothing coherent.

---

## How to Read the SRM Score

| 0.00 | 0.07 | 0.20 | 1.00 |
|------|------|------|------|
| LOW RESONANCE | → | MEDIUM RESONANCE | HIGH RESONANCE |

**In plain language:**
- **Low Resonance** does not mean the symbol is unknown or ignored. It means the media talks about it constantly, but in so many contradictory ways that no coherent political force can rally around it.
- **Medium Resonance** means the symbol successfully organizes a political field — people know what it stands for, even if contested.
- **High Resonance** has not yet been observed in the validated dataset.

---

## The 4 Diagnostic Categories

Through six validated case studies, the SRM framework has identified four structurally distinct symbol typologies:

### 1. Fragmented Diffusion Symbol
*High visibility, extreme semantic drift, politically inert*

The symbol circulates widely but simultaneously means too many incompatible things. No single political force can claim it without alienating other audiences. Example: **Călin Georgescu (D=0.881)** — simultaneously framed as sovereignty champion, conspiracy theorist, spiritual leader, and Russian agent.

### 2. Post-Executive Symbolic Trap
*Institutional role transition generates unavoidable semantic fragmentation*

When a political actor moves from executive power to opposition, they inherit contradictory framings: accountability for past decisions, critique of successors, new institutional role. This structural superposition predictably produces high drift. Example: **Marcel Ciolacu (D=0.841)** — simultaneously framed as opposition critic, former premier blamed for recession, county council president, party leader, and judicial target.

### 3. High-Velocity Campaign Symbol
*Exceptional diffusion speed, moderate semantic coherence*

The symbol spreads faster than any other in the dataset but remains semantically contested across multiple frames. Sufficient coherence for national mobilization, not enough for hegemonic dominance. Example: **Donald Trump (V=0.958, D=0.734, SRM=0.0922)**.

### 4. Sustained Wartime Medium-Resonance Symbol
*Multi-year high visibility, cross-cultural presence, coherence through crisis framing*

Wartime conditions simplify the symbolic field: a single dominant frame (resistance/defense) crowds out competing interpretations. The symbol achieves the highest SRM in the dataset not through the highest visibility, but through the lowest semantic drift. Example: **Volodymyr Zelensky (D=0.680, SRM=0.1121)**.

### 5. Pre-Saturated Contradicted Symbol *(new — Case Study 6)*
*Maximum visibility, maximum network coverage, low resonance due to pre-saturation and geopolitical semantic contradiction*

When a symbol is already dominant in media before a triggering event, it cannot generate high Viral Velocity regardless of the event's scale. Combined with geopolitically-induced semantic drift (different actors assign incompatible meanings for strategic reasons), the symbol becomes omnipresent but resonance-poor. Example: **Vladimir Putin (V=0.217, N=1.000, SRM=0.0103)**.

---

## Comparative Dataset — 6 Validated Symbols

| Symbol / Context | V | A | D | N | SRM | Category |
|-----------------|---|---|---|---|-----|----------|
| Sunflower Mvt (TW, 2014) | 0.680 | 0.420 | 0.7737 | 0.580 | 0.0376 | Low |
| Călin Georgescu (RO, 2024) | 0.750 | 0.398 | 0.8813 | 0.600 | 0.0307 | Low — Fragmented Diffusion |
| Marcel Ciolacu (RO, 2025–26) | 0.720 | 0.420 | 0.8412 | 0.650 | 0.0365 | Low — Post-Executive Trap |
| **Vladimir Putin (2022–26)** | **0.217** | **0.259** | **0.847** | **1.000** | **0.0103** | **Low — Pre-Saturated Contradicted** |
| Donald Trump (US, 2015–16) | 0.958 | 0.580 | 0.7340 | 0.720 | 0.0922 | Medium — High-Velocity Campaign |
| Zelensky (UA/EU/US, 2022–26) | 0.873 | 0.640 | 0.680 | 0.781 | 0.1121 | Medium — Wartime Symbol |

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

Data: Media Cloud Romania National + State & Local | 339 articles | 38 sources | 91 days

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

Baseline: May 2019 – Feb 2022 (1,011 observations). Peak event: Feb 28 – Mar 4, 2025 (Zelensky–Trump White House meeting).

Paper: [SRM_Zelensky_Validation.docx](SRM_Zelensky_Validation.docx) | Results: [SRM_zelensky_result.json](SRM_zelensky_result.json) | Data: [data_zelensky/](data_zelensky/)

### Case Study 6 — Vladimir Putin (2022–2026) *(new)*

Data: Media Cloud US National + US State & Local | 2,472 daily observations  
Baseline: May 20, 2019 – Feb 23, 2022 (1,011 obs.) | Analysis: Feb 24, 2022 – Feb 23, 2026 (1,461 obs.)

| V | A | D | N | SRM | Interpretation |
|---|---|---|---|-----|----------------|
| 0.217 | 0.259 | 0.847 | 1.000 | 0.0103 | LOW RESONANCE |

**Methodological advance:** A=0.2593 computed via VADER on 19,851 article titles — **first automated A computation in the SRM dataset**. All previous validations used expert-estimated A values.

**Pre-Saturation Paradox:** Putin had N=1.000 (present every single day of the 4-year analysis period) yet SRM=0.0103. Omnipresence without semantic coherence or emergence does not generate resonance. Escalation only 2.16x from high baseline (96.6 articles/day) produces V=0.217.

**First Antagonistic Symbol Pair:** Putin vs Zelensky — same corpus, same period, same triggering event. SRM gap of 0.1018 driven by V differential (+0.656), A differential (+0.381), D differential (−0.167).

![SRM Putin Chart](data_putin/SRM_Putin_chart.png)

Paper: [SRM_Putin_Validation.docx](SRM_Putin_Validation_FINAL_V4.docx) | Results: [SRM_putin_result.json](data_putin/SRM_putin_result.json) | Data: [data_putin/](data_putin/)

---

## Repository Structure

```
politomorphism/
├── .github/workflows/
│   ├── srm_ciolacu_validation.yml
│   ├── srm_zelensky_validation.yml
│   └── srm_putin_validation.yml
├── srm_pipeline/
│   ├── pas2_A_sentiment.py
│   ├── pas3_D_semantic_drift.py
│   ├── pas4_N_gdelt.py
│   └── pas5_SRM_final.py
├── data_ciolacu/
├── data_sunflower/
├── data_zelensky/
├── data_putin/
│   ├── PUTIN_DATA_FIRST_PERIOD_ATTENTION.csv
│   ├── PUTIN_DATA_SECOND_PERIOD_ATTENTION.csv
│   ├── PUTIN_DATA_FIRST_PERIOD_TOP_SOURCES.csv
│   ├── PUTIN_SECOND_PERIOD_TOP_SOURCES.csv
│   ├── putin_titles_baseline.csv
│   └── SRM_Putin_chart.png
└── README.md
```

---

## Reproducibility

All data, code, and results are open source and publicly available.  
Data source: [mediacloud.org](https://mediacloud.org)  
Licence: CC BY 4.0
