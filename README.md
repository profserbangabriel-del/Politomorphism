# Politomorphism — Social Resonance Model (SRM)

**Serban Gabriel Florin** | Independent Researcher  
ORCID: [0009-0000-2266-3356](https://orcid.org/0009-0000-2266-3356) | DOI: [10.17605/OSF.IO/HYDNZ](https://doi.org/10.17605/OSF.IO/HYDNZ)  
GitHub: [profserbangabriel-del/politomorphism](https://github.com/profserbangabriel-del/politomorphism)  
License: CC BY 4.0

---

## What is Politomorphism?

Politomorphism is a theoretical framework that treats political symbols as **morphogenetic agents** — entities that transform power structures through the process of symbolic diffusion. Its computational component, the **Social Resonance Model (SRM)**, provides a quantitative measure of how effectively a political symbol mobilizes public space.

---

## The SRM Formula

**SRM = V × A × e^(−λD) × N**

| Variable | Name | What it measures | Range |
|----------|------|-----------------|-------|
| V | Viral Velocity | Log-normalized escalation ratio between peak media presence and pre-event baseline | 0–1 |
| A | Affective Weight | Emotional intensity of coverage — computed via VADER (English) or DistilBERT (Romanian) sentiment analysis on article titles | 0–1 |
| D | Semantic Drift | Fragmentation of meaning across contexts. **Most impactful variable** (exponential position). Now formally defined as D = 0.5·PE + 0.5·ICI — see Section: D Operationalization | 0–1 |
| N | Network Coverage | Proportion of days where the symbol appears in the corpus | 0–1 |
| **λ** | **Decay Constant** | Controls attenuation speed of the semantic factor. **Empirically derived from Google Trends (Step 0).** Default: λ=7 | 2–105 |

---

## How to Read the SRM Score

```
0.00 ────────────── 0.07 ──────────────── 0.20 ──────── 1.00
 LOW RESONANCE          MEDIUM RESONANCE    HIGH RESONANCE
```

> **Empirical finding (12 case studies):** The HIGH RESONANCE zone (>0.20) remains empirically vacant in open, multi-outlet Western media systems. The observed upper bound is ~0.12. HIGH RESONANCE is a theoretical anchor for perfectly coherent symbols, not a practically attainable zone in democratic media ecosystems.

---

## λ Calibration — Step 0 (Mandatory)

> **Key finding:** λ is not a universal constant. It is a typological variable ranging from **λ=2.31** (Orbán — institutionally durable) to **λ=104.66** (Charlie Hebdo — extreme flash viral). The SRM formula is unchanged; λ is now measured before any computation.

### How λ is determined

Before any SRM computation, extract Google Trends data for the analysis period and solve numerically:

```
avg / peak = (1 − e^(−λT)) / (λT)
```

where T = analysis duration in years. Solve for λ using Brent's method (`scipy.optimize.brentq`).

**Script:** [`scripts/get_trends.py`](scripts/get_trends.py) | **Data:** [`srm_lambda_calibration.json`](srm_lambda_calibration.json)

### λ Typology — Five Categories

| Category | λ range | Examples |
|----------|---------|---------|
| Institutionally Durable | 2–5 | Orbán (2.31), Putin (4.90), Zelensky (5.11) |
| Campaign / Ascension | 6–8 | Ciolacu (6.57), Trump (7.01) |
| Electorally Volatile | 12–20 | Macron (12.53), Simion (12.41), Chávez (16.67), Mandela (19.66) |
| Flash Viral | 50–70 | Georgescu (65.33) |
| Extreme Flash Viral | >70 | Charlie Hebdo (104.66) |

> **Recommended default λ = 7** (empirical median of the two fully pipeline-validated Campaign/Ascension anchors: Trump 7.01 + Ciolacu 6.57).  
> **Flash viral rule:** if λ > 30, retain λ=2 in formula and flag as flash event. SRM point estimate is unreliable at this range — only λ typology carries diagnostic value.

---

## D Operationalization — March 2026 Update

> **Key finding:** Semantic Drift (D) — the most influential SRM variable — lacked a formally documented, reproducible computation method. This has been resolved.

### D = 0.5 · PE + 0.5 · ICI

| Component | Name | Measures | Method |
|-----------|------|----------|--------|
| PE | Polysemy Entropy | Topical breadth across domains | Mean Jensen-Shannon Divergence on LDA topic distributions (K=10) |
| ICI | Intra-contextual Incoherence | Framing divergence across outlets | 1 − mean pairwise cosine similarity on sentence embeddings (`paraphrase-multilingual-MiniLM-L12-v2`) |

**Why this matters:** PE and ICI are sociologically distinct. Georgescu's D=0.881 is ICI-driven (media polarization). Orbán's D=0.798 is PE-driven (15 years of topical breadth). The composite distinguishes these mechanisms — the previous implicit operationalization could not.

**Sensitivity:** A ±0.05 error in D produces SRM intervals ranging from ±6% (λ=2) to ±132% (λ=65). Flash Viral scores cannot be interpreted as point estimates.

**Module:** [`scripts/compute_D.py`](scripts/compute_D.py) | **Preprint:** [`SRM_D_Operationalization_Preprint.docx`](SRM_D_Operationalization_Preprint.docx)

---

## Dual-Mode SRM and Acute Amplification Factor (AAF)

For symbols with identifiable acute crisis windows (deaths, elections, coups), two SRM scores are reported:

- **SUSTAINED SRM** — long-term fragmented presence
- **ACUTE SRM** — short-term mobilization during narrative coherence

**AAF = ACUTE SRM / SUSTAINED SRM**

For Hugo Chávez: AAF = 9.5 (SRM jumped from 0.0121 to 0.1154 as D collapsed from 0.720 to 0.380 during the 11-day death window). This metric is now recommended for all symbols with identifiable acute windows.

---

## The 12 Typological Categories

| # | Category | Example | Mechanism |
|---|----------|---------|-----------|
| 1 | Fragmented Diffusion | Călin Georgescu | High visibility, extreme ICI, politically inert |
| 2 | Post-Executive Symbolic Trap | Marcel Ciolacu | Role transition generates structural semantic fragmentation |
| 3 | High-Velocity Campaign | Donald Trump | Exceptional V, moderate coherence |
| 4 | Sustained Wartime Coherent | Volodymyr Zelensky | Crisis ICI suppression, multi-year presence |
| 5 | Pre-Saturated Contradicted | Vladimir Putin | N=1.000 but V suppressed by saturation baseline |
| 6 | Longevity Saturation | Viktor Orbán | 15+ years prevents symbolic emergence |
| 7 | Legacy Resonance | Nelson Mandela | Death spike + semantic consensus suppresses SRM |
| 8 | Rapid Emergence | Emmanuel Macron | High V offset by low A and high D |
| 9 | Civic Mobilization | Sunflower Movement | Fragmented diffusion, no electoral vector |
| 10 | Flash Viral | Călin Georgescu (λ class) | Explosion + collapse, no sustained diffusion |
| 11 | Revolutionary Legacy | Hugo Chávez | SUSTAINED Low + ACUTE Medium; AAF=9.5 |
| 12 | Extreme Flash Viral | Charlie Hebdo | λ=104.66; unprecedented attention concentration |

---

## Comparative Dataset — 12 Case Studies

| Symbol / Context | V | A | D | N | SRM (λ=2) | λ empiric | SRM (λ_emp) | Typology |
|------------------|---|---|---|---|-----------|----------|------------|---------|
| George Simion (RO, 2024–26) | 0.279 | 0.099 | 0.812 | 0.996 | 0.0054 | 12.41 | — | Fragmented Diffusion |
| Viktor Orbán (HU, 2022–26) | 0.168 | 0.236 | 0.798 | 0.812 | 0.0065 | 2.31 | 0.0051 | Longevity Saturation |
| Nelson Mandela (SA, 2013) | 0.311 | 0.246 | 0.742 | 0.510 | 0.0088 | 19.66 | — | Legacy Resonance |
| Vladimir Putin (2022–26) | 0.217 | 0.259 | 0.847 | 1.000 | 0.0103 | 4.90 | 0.0009 | Pre-Saturated Contradicted |
| Hugo Chávez SUSTAINED (VE, 2012–13) | 0.186 | 0.290 | 0.720 | 0.941 | 0.0121 | 16.67 | — | Revolutionary Legacy |
| Emmanuel Macron (FR, 2017) | 0.507 | 0.168 | 0.810 | 1.000 | 0.0169 | 12.53 | — | Rapid Emergence |
| Călin Georgescu (RO, 2024) | 0.750 | 0.398 | 0.881 | 0.600 | 0.0307 | 65.33 | — | Flash Viral |
| Marcel Ciolacu (RO, 2025–26) | 0.720 | 0.420 | 0.841 | 0.650 | 0.0365 | 6.57 | 0.0008 | Post-Executive Trap |
| Sunflower Movement (TW, 2014) | 0.680 | 0.420 | 0.774 | 0.580 | 0.0376 | — | — | Civic Mobilization |
| Charlie Hebdo (FR, 2014) | TBD | TBD | TBD | TBD | TBD | 104.66 | — | Extreme Flash Viral |
| Donald Trump (US, 2015–16) | 0.958 | 0.580 | 0.734 | 0.720 | 0.0922 | 7.01 | 0.0023 | High-Velocity Campaign |
| Hugo Chávez ACUTE (VE, Mar 2013) | 0.689 | 0.358 | 0.380 | 1.000 | 0.1154 | 16.67 | — | Revolutionary Legacy (Acute) |
| Volodymyr Zelensky (UA, 2022–26) | 0.873 | 0.640 | 0.680 | 0.781 | 0.1121 | 5.11 | 0.0135 | Sustained Wartime Coherent* |

*Zelensky reclassified **LOW RESONANCE** under empirical λ=5.11 (SRM_emp=0.0135). MEDIUM classification applies only at λ=2.  
Charlie Hebdo: V, A, D, N pending full pipeline validation. λ_emp computed from Google Trends (avg=6.82, peak=711, T=0.997 years).

---

## Case Studies

### Case Study 1 — Sunflower Movement (Taiwan, 2014)

Data: Media Cloud | 92 days | λ unavailable (GT global avg=1.1, insufficient resolution)

| V | A | D | N | SRM | λ emp | Interpretation |
|---|---|---|---|-----|-------|---------------|
| 0.680 | 0.420 | 0.774 | 0.580 | 0.0376 | — | LOW RESONANCE |

**Key contribution:** First proof that high visibility does not guarantee resonance; semantic coherence (D) is the decisive suppressor.

Data: [`data_sunflower/`](data_sunflower/)

---

### Case Study 2 — Călin Georgescu (Romania, Oct–Dec 2024)

Data: Media Cloud Romanian National + State & Local | 151 days

| V | A | D | N | SRM | λ emp | Interpretation |
|---|---|---|---|-----|-------|---------------|
| 0.750 | 0.398 | 0.881 | 0.600 | 0.0307 | 65.33 | LOW RESONANCE — Flash Viral |

**Key contribution:** Identification of Flash Viral category. D=0.881 is the highest in the dataset. λ>30 triggers the flash viral rule: use λ=2 in formula.

Results: [`SRM_raport_final.json`](SRM_raport_final.json) | Chart: [`SRM_grafic_final.png`](SRM_grafic_final.png) | EN chart: [`SRM_grafic_final_EN georgescu.png`](SRM_grafic_final_EN%20georgescu.png)

---

### Case Study 3 — Marcel Ciolacu (Romania, Dec 2025 – Mar 2026)

Data: Media Cloud Romania National + State & Local | 339 articles | 91 days

| V | A | D | N | SRM | λ emp | SRM (λ_emp) | Interpretation |
|---|---|---|---|-----|-------|------------|---------------|
| 0.720 | 0.420 | 0.841 | 0.650 | 0.0365 | 6.57 | 0.0008 | LOW RESONANCE |

**Key contribution:** Post-Executive Symbolic Trap. First dual-source validation (Media Cloud vs. GDELT). λ=6.57 is the second calibration anchor for the Campaign/Ascension category.

Paper: [`SRM_Ciolacu_Validation.docx`](SRM_Ciolacu_Validation.docx) | Data: [`data_ciolacu/`](data_ciolacu/)

---

### Case Study 4 — Donald Trump (USA, Jun 2015 – Nov 2016)

Data: Media Cloud US National + State & Local | 548 daily observations

| V | A | D | N | SRM | λ emp | SRM (λ_emp) | Interpretation |
|---|---|---|---|-----|-------|------------|---------------|
| 0.958 | 0.580 | 0.734 | 0.720 | 0.0922 | 7.01 | 0.0023 | MEDIUM RESONANCE |

**Key contribution:** First Medium Resonance case. V=0.958 is the highest in the dataset. λ=7.01 is the primary calibration anchor for the recommended default λ=7.

Results: [`SRM_trump_result.json`](SRM_trump_result.json) | Chart: [`SRM_trump_grafic.png`](SRM_trump_grafic.png) | Temporal: [`SRM_trump_temporal.png`](SRM_trump_temporal.png) | Data: [`TRUMP+DATA.csv`](TRUMP+DATA.csv)

---

### Case Study 5 — Volodymyr Zelensky (UA/EU/US, Feb 2022 – Mar 2026)

Data: Media Cloud US National + Europe | 1,489 daily observations

| V | A | D | N | SRM (λ=2) | λ emp | SRM (λ_emp) | Interpretation |
|---|---|---|---|-----------|-------|------------|---------------|
| 0.873 | 0.640 | 0.680 | 0.781 | 0.1121 | 5.11 | 0.0135 | MEDIUM (λ=2) → **LOW** (λ_emp) |

**Key contribution:** Most consequential λ recalibration — reclassified from Medium to Low. First Antagonistic Symbol Pair with Putin. A=0.640 is the highest in the dataset.

Paper: [`SRM_Zelensky_Validation.docx`](SRM_Zelensky_Validation.docx) | Data: [`data_zelensky/`](data_zelensky/)

---

### Case Study 6 — Vladimir Putin (2022–2026)

Data: Media Cloud US National + US State & Local | 1,489 daily observations

| V | A | D | N | SRM | λ emp | SRM (λ_emp) | Interpretation |
|---|---|---|---|-----|-------|------------|---------------|
| 0.217 | 0.259 | 0.847 | 1.000 | 0.0103 | 4.90 | 0.0009 | LOW RESONANCE |

**Key contribution:** Pre-Saturation Paradox — N=1.000 every day yet SRM=0.0103. Putin-Zelensky gap (0.1018) validates SRM's multidimensional discriminative capacity.

Paper: [`SRM_Putin_Validation.docx`](SRM_Putin_Validation.docx) | Data: [`data_putin/`](data_putin/)

---

### Case Study 7 — George Simion (Romania, Oct 2024 – Mar 2026)

Data: Media Cloud Romanian National + State & Local | 516 daily observations

| V | A | D | N | SRM | λ emp | Interpretation |
|---|---|---|---|-----|-------|---------------|
| 0.279 | 0.099 | 0.812 | 0.996 | 0.0054 | 12.41 | LOW RESONANCE |

**Key contribution:** Lowest SRM (0.0054) and lowest A (0.099) in the dataset. Completes the **Romanian Triad** (Georgescu + Ciolacu + Simion) — first within-country controlled comparison. All three produce Low Resonance despite different trajectories, suggesting a structural ICI ceiling in Romanian media.

Paper: [`SRM_Simion_Validation.docx`](SRM_Simion_Validation.docx) | Data: [`data_simion/`](data_simion/)

---

### Case Study 8 — Viktor Orbán (Hungary, 2022–2026)

Data: Media Cloud US National + US State & Local + European | 1,520 daily observations

| V | A | D | N | SRM | λ emp | SRM (λ_emp) | Interpretation |
|---|---|---|---|-----|-------|------------|---------------|
| 0.168 | 0.236 | 0.798 | 0.812 | 0.0065 | 2.31 | 0.0051 | LOW RESONANCE |

**Key contribution:** Longevity Paradox — lowest V (0.168) from 15+ years of saturation. λ=2.31 is the **only case where the original theoretical default λ=2 was empirically validated**.

Paper: [`SRM_Orban_Validation.docx`](SRM_Orban_Validation.docx) | Data: [`data_orban/`](data_orban/)

---

### Case Study 9 — Nelson Mandela (South Africa, 2013)

Data: Media Cloud US National + US State & Local | 365 daily observations | VADER corpus: 4,070 English titles

| V | A | D | N | SRM | λ emp | Interpretation |
|---|---|---|---|-----|-------|---------------|
| 0.311 | 0.246 | 0.742 | 0.510 | 0.0088 | 19.66 | LOW RESONANCE |

**Key contribution:** Legacy Paradox — highest single-day ratio (0.08618 on Dec 6, 2013, day after death) yet annual SRM=0.0088. λ=19.66 confirms death-spike structure. Introduces **Legacy Resonance** typology.

Paper: [`SRM_Mandela_Validation.docx`](SRM_Mandela_Validation.docx) | Data: [`data_mandela/`](data_mandela/)

---

### Case Study 10 — Emmanuel Macron (France, 2017)

Data: Media Cloud US National + Europe Media Monitor | 365 daily observations | VADER corpus: 1,304 English titles

| V | A | D | N | SRM | λ emp | Interpretation |
|---|---|---|---|-----|-------|---------------|
| 0.507 | 0.168 | 0.810 | 1.000 | 0.0169 | 12.53 | LOW RESONANCE |

**Key contribution:** Rapid Emergence Paradox — highest V (0.507) in Low Resonance cohort, yet SRM suppressed by A=0.168 and D=0.810. λ=12.53 ≈ Simion (12.41): single-peak electoral emergence symbols share a common diffusion structure regardless of country.

Paper: [`SRM_Macron_Validation.docx`](SRM_Macron_Validation.docx) | Data: [`data_macron/`](data_macron/)

---

### Case Study 11 — Hugo Chávez (Venezuela, 2012–2013)

Data: Media Cloud US National + Venezuela State & Local | 732 daily observations | VADER corpus: 3,073 English titles  
Baseline: Jan–Oct 2012 | Analysis: Nov 2012–Dec 2013 | Acute Window: Mar 5–15, 2013  
Google Trends: avg=3.0, peak=100 → **λ empiric = 16.67** (Electorally Volatile)

| Mode | V | A | D | N | SRM (λ=2) | Interpretation |
|------|---|---|---|---|-----------|---------------|
| SUSTAINED (Nov 2012–Dec 2013) | 0.186 | 0.290 | 0.720 | 0.941 | 0.0121 | LOW RESONANCE |
| **ACUTE (Mar 5–15, 2013)** | **0.689** | **0.358** | **0.380** | **1.000** | **0.1154** | **MEDIUM RESONANCE** |

**Key contribution:** Introduces **Dual-Mode SRM** framework. AAF = 9.5 (D collapsed from 0.720 → 0.380 during the 11-day death window). Introduces **Acute Amplification Factor (AAF)** as new diagnostic metric. Confirms SRM > 0.20 (HIGH RESONANCE) requires D < 0.09 — theoretically unattainable in open media.

Paper: [`SRM_Chavez_Validation.docx`](SRM_Chavez_Validation.docx) | Data: [`data_chavez/`](data_chavez/)

---

### Case Study 12 — Charlie Hebdo (France, Jan 2015)

Data: Media Cloud | ~14 days | Google Trends: avg=6.82, peak=711, T=0.997 years  
**λ empiric = 104.66** (Extreme Flash Viral — exceeds Flash Viral category upper bound)

| V | A | D | N | SRM (λ=2) | λ emp | Interpretation |
|---|---|---|---|-----------|-------|---------------|
| TBD | TBD | TBD | TBD | TBD | 104.66 | Extreme Flash Viral — V/A/D/N pending |

**Key contribution:** λ=104.66 is the highest value in the dataset, extending the typology beyond the Flash Viral category (50–70) and establishing a new **Extreme Flash Viral** class (>70). Confirms and reinforces the flash viral handling rule.

Raw data: [`charile hebdo counts.csv`](charile%20hebdo%20counts.csv) | [`charile hebdo url.csv`](charile%20hebdo%20url.csv) *(note: full pipeline validation pending)*

---

## Publications and Preprints

| Document | Content | DOI / Link |
|----------|---------|-----------|
| `SRM_Research_Trajectory.docx` | Complete 12-case research trajectory, λ typology, Dual-Mode SRM | [10.17605/OSF.IO/HYDNZ](https://doi.org/10.17605/OSF.IO/HYDNZ) |
| `SRM_D_Operationalization_Preprint.docx` | Formal operationalization of D (PE+ICI), sensitivity analysis, compute_D.py | Pending OSF/Zenodo submission |
| `SRM_Lambda_Calibration_FULL.docx` | λ calibration methodology and full typology | In repo |
| `SRM_Chavez_Validation.docx` | Dual-Mode SRM, AAF metric | In repo |
| `SRM_Ciolacu_Validation.docx` | Post-Executive Symbolic Trap, dual-source validation | In repo |
| `SRM_Zelensky_Validation.docx` | Wartime coherence, λ recalibration | In repo |
| `SRM_Putin_Validation.docx` | Pre-Saturation Paradox, Antagonistic Pair | In repo |
| `SRM_Simion_Validation.docx` | Romanian Triad, media ecosystem ceiling | In repo |
| `SRM_Orban_Validation.docx` | Longevity Saturation, λ=2 validation | In repo |
| `SRM_Mandela_Validation.docx` | Legacy Resonance, death-spike structure | In repo |
| `SRM_Macron_Validation.docx` | Rapid Emergence Paradox | In repo |

---

## Repository Structure

```
politomorphism/
├── .github/workflows/
│   ├── srm_ciolacu_validation.yml
│   ├── srm_zelensky_validation.yml
│   ├── srm_putin_validation.yml
│   ├── srm_simion_validation.yml
│   ├── srm_orban_validation.yml
│   └── fetch_trends.yml
├── scripts/
│   ├── get_trends.py              ← λ calibration (Step 0)
│   ├── compute_D.py               ← D = 0.5·PE + 0.5·ICI (NEW — March 2026)
│   ├── pas2_A_sentiment.py        → moved to srm_pipeline/
│   ├── pas3_D_semantic_drift.py   → moved to srm_pipeline/
│   ├── pas4_N_gdelt.py            → moved to srm_pipeline/
│   └── pas5_SRM_final.py          → moved to srm_pipeline/
├── srm_pipeline/
│   ├── pas2_A_sentiment.py
│   ├── pas3_D_semantic_drift.py
│   ├── pas4_N_gdelt.py
│   └── pas5_SRM_final.py
├── data_chavez/
├── data_ciolacu/
├── data_macron/
├── data_mandela/
├── data_orban/
├── data_putin/
├── data_simion/
├── data_sunflower/
├── data_zelensky/
├── srm_lambda_calibration.json    ← 12-symbol calibration data (updated)
├── SRM_Research_Trajectory.docx
├── SRM_D_Operationalization_Preprint.docx
└── README.md
```

---

## Reproducibility

All data, code, and results are open source.

- **Data sources:** [mediacloud.org](https://mediacloud.org) + [Google Trends](https://trends.google.com) (pytrends)
- **λ calibration:** `scipy.optimize.brentq`, Python 3.11, GitHub Actions ubuntu-latest
- **Sentiment analysis:** VADER (`vaderSentiment 3.3.2`) for English; DistilBERT for Romanian
- **D computation:** `scripts/compute_D.py` — LDA (scikit-learn), sentence-transformers (`paraphrase-multilingual-MiniLM-L12-v2`)
- **Bootstrap CI for D:** n=500 samples, 95% confidence interval
- **GitHub Actions:** workflows trigger on `workflow_dispatch`

---

## Preregistration

OSF Preregistration: [10.17605/OSF.IO/HYDNZ](https://doi.org/10.17605/OSF.IO/HYDNZ)  
Zenodo: [10.5281/zenodo.18962821](https://doi.org/10.5281/zenodo.18962821)

---

*Politomorphism Research Project | Serban Gabriel Florin | Romania / EU | March 2026*
