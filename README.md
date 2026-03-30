# Politomorphism — Social Resonance Model (SRM)

**Serban Gabriel Florin** | Independent Researcher  
ORCID: [0009-0000-2266-3356](https://orcid.org/0009-0000-2266-3356) | DOI: [10.17605/OSF.IO/HYDNZ](https://doi.org/10.17605/OSF.IO/HYDNZ)  
GitHub: [profserbangabriel-del/Politomorphism](https://github.com/profserbangabriel-del/Politomorphism)  
License: CC BY 4.0

---

## PE/ICI Correlation Map — 15 Validated Symbols

[![SRM PE/ICI Correlation Map](docs/srm_pe_ici_map.svg)](https://profserbangabriel-del.github.io/Politomorphism/srm_pe_ici_map_interactive.html)

> **Interactive version:** [srm_pe_ici_map_interactive.html](https://profserbangabriel-del.github.io/Politomorphism/srm_pe_ici_map_interactive.html) — hover over any symbol for full PE/ICI values and key findings. Filter by typology.  
> **Key finding (updated):** ICI range (0.311) is **4.0× larger** than PE range (0.078) across 15 symbols. Modi (ICI=0.915) breaks the Western ICI ceiling through Cross-Cultural Frame Incompatibility (CCFI). Netanyahu (ICI=0.698) discriminates CCFI from pre-sorted ideological framing.

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
| D | Semantic Drift | Fragmentation of meaning across contexts. **Most impactful variable** (exponential position). Formally defined as D = α·PE + (1−α)·ICI with α_optimal = **0.338** (updated) — see Section: D Operationalization | 0–1 |
| N | Network Coverage | Proportion of days where the symbol appears in the corpus | 0–1 |
| **λ** | **Decay Constant** | Controls attenuation speed of the semantic factor. **Empirically derived from Google Trends (Step 0).** Default: λ=7 | 2–105 |

---

## How to Read the SRM Score

```
0.00 ────────────── 0.07 ──────────────── 0.20 ──────── 1.00
 LOW RESONANCE          MEDIUM RESONANCE    HIGH RESONANCE
```

> **Empirical finding (15 case studies):** The HIGH RESONANCE zone (>0.20) remains empirically vacant in open, multi-outlet Western media systems. The observed upper bound is ~0.12. For Non-Western symbols, CCFI-generated D suppresses SRM regardless of V and A — a Non-Western correction factor is required for cross-cultural SRM comparison.

---

## λ Calibration — Step 0 (Mandatory)

> **Key finding:** λ is not a universal constant. It is a typological variable ranging from **λ=2.31** (Orbán — institutionally durable) to **λ=104.66** (Charlie Hebdo — extreme flash viral).

### How λ is determined

```
avg / peak = (1 − e^(−λT)) / (λT)
```

Solve for λ using Brent's method (`scipy.optimize.brentq`). **Script:** [`scripts/get_trends.py`](scripts/get_trends.py)

### λ Typology — Five Categories

| Category | λ range | Examples |
|----------|---------|---------|
| Institutionally Durable | 2–5 | Orbán (2.31), Putin (4.90), Zelensky (5.11) |
| Campaign / Ascension | 6–8 | Ciolacu (6.57), Trump (7.01) |
| Electorally Volatile | 12–20 | Macron (12.53), Simion (12.41), Chávez (16.67), Mandela (19.66) |
| Flash Viral | 50–70 | Georgescu (65.33) |
| Extreme Flash Viral | >70 | Charlie Hebdo (104.66) |

> **Recommended default λ = 7.** Flash viral rule: if λ > 30, retain λ=2 and flag as flash event.

---

## D Operationalization — Updated March 2026

### D = α · PE + (1−α) · ICI

| Component | Name | Measures | Method |
|-----------|------|----------|--------|
| PE | Polysemy Entropy | Topical breadth across domains | Mean Jensen-Shannon Divergence on LDA topic distributions (K=10, seed=42) |
| ICI | Intra-contextual Incoherence | Framing divergence across outlets | 1 − mean pairwise cosine similarity on sentence embeddings (`paraphrase-multilingual-MiniLM-L12-v2`) |

### Alpha Calibration Results — Updated (14 real-value entries)

| Parameter | 13-symbol | 15-symbol (updated) | Change |
|-----------|-----------|---------------------|--------|
| α_optimal | 0.351 | **0.338** | ICI weight → 0.662 |
| Pearson r (D_new vs D_legacy) | 0.682 | **0.701** | Stronger validity |
| Mean D_legacy upward bias | −15.6% | **−16.2%** | Slightly larger |
| ICI range / PE range | 2.81× | **4.0×** | CCFI expands ICI dominance |

### Eight Cross-Symbol Findings (updated from six)

1. **ICI drives D variation** — ICI range (0.311) is 4.0× larger than PE range (0.078).
2. **ICI ceiling ~0.83–0.84 is Western-specific** — Trump (0.835), Mandela (0.836), Putin (0.834) define the Western ceiling. Non-Western CCFI symbols can exceed it substantially.
3. **Modi (ICI=0.915) breaks the ceiling** through Cross-Cultural Frame Incompatibility (CCFI): absence of pre-established Anglo-American interpretive frameworks generates extreme framing divergence.
4. **Netanyahu (ICI=0.698) does not exhibit CCFI** despite active war context — pre-established Israel-Palestine frames in Anglo-American media produce pre-sorted moderate ICI, not CCFI.
5. **ICI−PE as typological dimension** — gradient from Modi (+0.339) to Orbán (+0.001) maps coherently onto symbol typologies.
6. **H1 directionally supported** — both Flash Viral symbols (Charlie Hebdo +0.138, Georgescu +0.106) have ICI > PE.
7. **H3 extended** — wartime produces asymmetric ICI: Putin aggressor (+0.267) > Netanyahu contested (+0.087) > Zelensky defender (+0.056).
8. **CCFI is a structural SRM suppressor** — Non-Western symbols require a correction factor for valid cross-cultural SRM comparison.

**Modules:** [`scripts/compute_D.py`](scripts/compute_D.py) | [`scripts/calibrate_alpha.py`](scripts/calibrate_alpha.py)

---

## Complete PE/ICI Dataset — 15 Validated Symbols

| Rank | Symbol | Country | Period | PE | ICI | D_new | ICI−PE | SRM (λ=2) | Typology |
|------|--------|---------|--------|----|-----|-------|--------|-----------|----------|
| 1 | **Modi** | **IN** | **2013–14** | **0.576** | **0.915** | **0.746** | **+0.339** | TBD | **CCFI** |
| 2 | Trump | USA | 2015–16 | 0.542 | 0.835 | 0.689 | +0.293 | 0.0922 | Campaign |
| 3 | Mandela | ZA | 2013 | 0.564 | 0.836 | 0.700 | +0.272 | 0.0088 | Legacy |
| 4 | Putin | RU | 2022 | 0.566 | 0.834 | 0.700 | +0.267 | 0.0103 | Wartime Aggressor |
| 5 | Sunflower Mvt | TW | 2014 | 0.625 | 0.789 | 0.707 | +0.165 | 0.0376 | Civic Mobilization |
| 6 | Charlie Hebdo | FR | 2015 | 0.592 | 0.730 | 0.661 | +0.138 | ~0 | Flash Viral |
| 7 | Chávez | VE | 2013 | 0.594 | 0.720 | 0.657 | +0.126 | 0.0121 | Electorally Volatile |
| 8 | Ciolacu | RO | 2025–26 | 0.622 | 0.745 | 0.683 | +0.123 | 0.0365 | Campaign/Post-exec. |
| 9 | Macron | FR | 2017 | 0.593 | 0.714 | 0.654 | +0.121 | 0.0169 | Campaign |
| 10 | Georgescu | RO | 2024 | 0.595 | 0.700 | 0.648 | +0.106 | 0.0307 | Flash Viral |
| 11 | Netanyahu | IL | 2023–24 | 0.610 | 0.698 | 0.654 | +0.087 | TBD | Pre-Sorted Wartime |
| 12 | Simion | RO | 2024 | 0.598 | 0.685 | 0.641 | +0.087 | 0.0054 | Electorally Volatile |
| 13 | Zelensky | UA | 2022 | 0.604 | 0.660 | 0.632 | +0.056 | 0.1121 | Wartime Defender |
| 14 | Orbán | HU | 2022 | 0.604 | 0.605 | 0.604 | +0.001 | 0.0065 | Institutionally Durable |
| — | Chávez (acute) | VE | Mar 2013 | — | — | 0.380* | — | 0.1154* | Dual-Mode |

*Estimated. All other D_new values are real pipeline outputs (Jobs #10–#26).  
Modi and Netanyahu: V, A, N pending full SRM validation.

---

## ICI Architecture — Three Tiers

| Tier | ICI range | Symbols | Mechanism |
|------|-----------|---------|-----------|
| Non-Western CCFI | **0.90+** | Modi (0.915) | Cross-Cultural Frame Incompatibility |
| Western ICI ceiling | **0.83–0.84** | Trump (0.835), Mandela (0.836), Putin (0.834) | Electoral polarization / legacy contestation / aggressor amplification |
| Moderate ICI | **0.60–0.79** | All other 12 symbols | Pre-sorted / convergent / institutional |

---

## Cross-Cultural Frame Incompatibility (CCFI)

> **New theoretical mechanism (March 2026)** — introduced by the Modi and Netanyahu cases.

CCFI applies when Anglo-American journalism **lacks pre-established interpretive categories** for a political symbol, forcing different outlets to construct incompatible frameworks from scratch. This generates ICI substantially above the Western ceiling.

**CCFI does NOT apply** when pre-established frameworks exist (Israel-Palestine, Russia-West): pre-sorted ideological framing then produces moderate ICI regardless of conflict intensity.

| Condition | Symbol | ICI | Result |
|-----------|--------|-----|--------|
| No Anglo-American framework (Hindu nationalism) | Modi | 0.915 | **CCFI — ceiling broken** |
| Pre-established framework (Israel-Palestine) | Netanyahu | 0.698 | **Pre-sorted — no CCFI** |

**Implication for SRM:** CCFI acts as a structural SRM suppressor for Non-Western symbols. Higher CCFI-generated ICI → higher D → more severe exponential penalty → SRM underestimates actual political resonance. A Non-Western correction factor is required.

---

## Dual-Mode SRM and Acute Amplification Factor (AAF)

- **SUSTAINED SRM** — long-term fragmented presence
- **ACUTE SRM** — short-term mobilization during narrative coherence
- **AAF = ACUTE / SUSTAINED**

For Hugo Chávez: AAF = 9.5 (SRM jumped from 0.0121 → 0.1154 as D collapsed 0.720 → 0.380 during the 11-day death window).

---

## The 15 Typological Categories

| # | Category | Example | ICI−PE | Mechanism |
|---|----------|---------|--------|-----------|
| 1 | **Non-Western CCFI** | **Narendra Modi** | **+0.339** | **Cross-Cultural Frame Incompatibility** |
| 2 | High-Velocity Campaign | Donald Trump | +0.293 | Exceptional V, maximum ICI-dominance |
| 3 | Legacy Resonance | Nelson Mandela | +0.272 | Post-mortem Legacy Contestation ICI |
| 4 | Wartime Aggressor | Vladimir Putin | +0.267 | Moral-political polarization amplifies ICI to ceiling |
| 5 | Civic Mobilization | Sunflower Movement | +0.165 | Cross-cultural framing diversity |
| 6 | Flash Viral / Extreme | Charlie Hebdo | +0.138 | Convergence-then-contestation; λ=104.66 |
| 7 | Revolutionary Legacy | Hugo Chávez | +0.126 | Structured ICI; SUSTAINED Low + ACUTE Medium; AAF=9.5 |
| 8 | Post-Executive Trap | Marcel Ciolacu | +0.123 | Role transition → structural semantic fragmentation |
| 9 | Rapid Emergence | Emmanuel Macron | +0.121 | Contradictory frame coexistence |
| 10 | Fragmented Diffusion | Călin Georgescu | +0.106 | Flash Viral; λ=65.33 |
| 11 | **Pre-Sorted Wartime** | **Benjamin Netanyahu** | **+0.087** | **Institutionalized conflict frames; no CCFI** |
| 12 | Electorally Volatile | George Simion | +0.087 | Affective Deficit (A=0.099) |
| 13 | Sustained Wartime Defender | Volodymyr Zelensky | +0.056 | Crisis frame convergence |
| 14 | Longevity Saturation | Viktor Orbán | +0.001 | 15+ years — perfectly balanced PE/ICI |
| 15 | Revolutionary Legacy (Acute) | Hugo Chávez (acute) | — | D_acute=0.380; Dual-Mode |

---

## Comparative Dataset — Full SRM Variables

| Symbol / Context | V | A | D_new | N | SRM (λ=2) | λ empiric | SRM (λ_emp) | Typology |
|------------------|---|---|-------|---|-----------|----------|------------|---------|
| **Narendra Modi (IN, 2013–14)** | TBD | TBD | **0.746** | TBD | TBD | TBD | TBD | **CCFI** |
| George Simion (RO, 2024–26) | 0.279 | 0.099 | 0.641 | 0.996 | 0.0054 | 12.41 | — | Electorally Volatile |
| Viktor Orbán (HU, 2022–26) | 0.168 | 0.236 | 0.604 | 0.812 | 0.0065 | 2.31 | 0.0051 | Longevity Saturation |
| Nelson Mandela (SA, 2013) | 0.311 | 0.246 | 0.700 | 0.510 | 0.0088 | 19.66 | — | Legacy Resonance |
| Vladimir Putin (2022–26) | 0.217 | 0.259 | 0.700 | 1.000 | 0.0103 | 4.90 | 0.0009 | Wartime Aggressor |
| Hugo Chávez SUSTAINED (VE, 2012–13) | 0.186 | 0.290 | 0.657 | 0.941 | 0.0121 | 16.67 | — | Revolutionary Legacy |
| Emmanuel Macron (FR, 2017) | 0.507 | 0.168 | 0.654 | 1.000 | 0.0169 | 12.53 | — | Rapid Emergence |
| **Benjamin Netanyahu (IL, 2023–24)** | TBD | TBD | **0.654** | TBD | TBD | TBD | TBD | **Pre-Sorted Wartime** |
| Călin Georgescu (RO, 2024) | 0.750 | 0.398 | 0.648 | 0.600 | 0.0307 | 65.33 | — | Flash Viral |
| Marcel Ciolacu (RO, 2025–26) | 0.720 | 0.420 | 0.683 | 0.650 | 0.0365 | 6.57 | 0.0008 | Post-Executive Trap |
| Sunflower Movement (TW, 2014) | 0.680 | 0.420 | 0.707 | 0.580 | 0.0376 | — | — | Civic Mobilization |
| Charlie Hebdo (FR, 2015) | TBD | TBD | 0.661 | TBD | TBD | 104.66 | — | Extreme Flash Viral |
| Donald Trump (US, 2015–16) | 0.958 | 0.580 | 0.689 | 0.720 | 0.0922 | 7.01 | 0.0023 | High-Velocity Campaign |
| Hugo Chávez ACUTE (VE, Mar 2013) | 0.689 | 0.358 | 0.380* | 1.000 | 0.1154 | 16.67 | — | Revolutionary Legacy (Acute) |
| Volodymyr Zelensky (UA, 2022–26) | 0.873 | 0.640 | 0.632 | 0.781 | 0.1121 | 5.11 | 0.0135 | Wartime Defender |

*D_acute = 0.380 expert estimate. All other D_new = real pipeline outputs. Modi/Netanyahu: V, A, N pending.

---

## Case Studies

### Case Study 1 — Sunflower Movement (Taiwan, 2014)

| V | A | D_new | N | SRM | Job |
|---|---|-------|---|-----|-----|
| 0.680 | 0.420 | 0.707 | 0.580 | 0.0376 | #15 |

**Key contribution:** Highest D_new (0.707) in dataset. ICI−PE = +0.165 (rank 5/15). Cross-cultural civic mobilization drives framing diversity.

---

### Case Study 2 — Călin Georgescu (Romania, Oct–Dec 2024)

| V | A | D_new | N | SRM | λ emp | Job |
|---|---|-------|---|-----|-------|-----|
| 0.750 | 0.398 | 0.648 | 0.600 | 0.0307 | 65.33 | #14 |

**Key contribution:** Flash Viral. Largest D discrepancy (D_legacy=0.881 vs D_new=0.648, Δ=−26.5%). Romanian Triad. ICI−PE = +0.106 (rank 10/15).

---

### Case Study 3 — Marcel Ciolacu (Romania, Dec 2025 – Mar 2026)

| V | A | D_new | N | SRM | λ emp | SRM (λ_emp) | Job |
|---|---|-------|---|-----|-------|------------|-----|
| 0.720 | 0.420 | 0.683 | 0.650 | 0.0365 | 6.57 | 0.0008 | #12 |

**Key contribution:** Post-Executive Symbolic Trap. ICI−PE = +0.123 ≈ Macron (+0.121). Romanian Triad.

---

### Case Study 4 — Donald Trump (USA, Jun 2015 – Nov 2016)

| V | A | D_new | N | SRM | λ emp | SRM (λ_emp) | Job |
|---|---|-------|---|-----|-------|------------|-----|
| 0.958 | 0.580 | 0.689 | 0.720 | 0.0922 | 7.01 | 0.0023 | #10 |

**Key contribution:** Highest ICI-dominance among Western symbols (ICI−PE = +0.293, rank 2/15). ICI ceiling co-occupant. Largest corpus: 69,997 articles.

---

### Case Study 5 — Volodymyr Zelensky (UA/EU/US, Feb 2022 – Mar 2026)

| V | A | D_new | N | SRM (λ=2) | λ emp | SRM (λ_emp) | Job |
|---|---|-------|---|-----------|-------|------------|-----|
| 0.873 | 0.640 | 0.632 | 0.781 | 0.1121 | 5.11 | 0.0135 | #17 |

**Key contribution:** H3 reformulated. Wartime Defender. ICI−PE = +0.056 (rank 13/15). A=0.640 highest in dataset.

---

### Case Study 6 — Vladimir Putin (2022–2026)

| V | A | D_new | N | SRM | λ emp | SRM (λ_emp) | Job |
|---|---|-------|---|-----|-------|------------|-----|
| 0.217 | 0.259 | 0.700 | 1.000 | 0.0103 | 4.90 | 0.0009 | #18 |

**Key contribution:** ICI ≈ Trump (0.834). Antagonistic Pair with Zelensky. ICI−PE = +0.267 (rank 4/15).

---

### Case Study 7 — George Simion (Romania, Oct 2024 – Mar 2026)

| V | A | D_new | N | SRM | λ emp | Job |
|---|---|-------|---|-----|-------|-----|
| 0.279 | 0.099 | 0.641 | 0.996 | 0.0054 | 12.41 | #19 |

**Key contribution:** Affective Deficit — A=0.099 is the binding SRM constraint. Completes Romanian Triad. ICI−PE = +0.087 (rank 11/15).

---

### Case Study 8 — Viktor Orbán (Hungary, 2022–2026)

| V | A | D_new | N | SRM | λ emp | SRM (λ_emp) | Job |
|---|---|-------|---|-----|-------|------------|-----|
| 0.168 | 0.236 | 0.604 | 0.812 | 0.0065 | 2.31 | 0.0051 | #16 |

**Key contribution:** ICI−PE ≈ 0 — perfectly balanced. Longevity Paradox. Lowest D_new (0.604) and V (0.168) in dataset.

---

### Case Study 9 — Nelson Mandela (South Africa, 2013)

| V | A | D_new | N | SRM | λ emp | Job |
|---|---|-------|---|-----|-------|-----|
| 0.311 | 0.246 | 0.700 | 0.510 | 0.0088 | 19.66 | #20 |

**Key contribution:** Highest absolute ICI among Western symbols (0.836). Legacy Contestation ICI. ICI−PE = +0.272 (rank 3/15).

---

### Case Study 10 — Emmanuel Macron (France, 2017)

| V | A | D_new | N | SRM | λ emp | Job |
|---|---|-------|---|-----|-------|-----|
| 0.507 | 0.168 | 0.654 | 1.000 | 0.0169 | 12.53 | #21 |

**Key contribution:** Rapid Emergence Paradox. ICI−PE = +0.121 ≈ Ciolacu (+0.123) — structural equivalence across national contexts.

---

### Case Study 11 — Hugo Chávez (Venezuela, 2012–2013)

| Mode | V | A | D | N | SRM (λ=2) | Job |
|------|---|---|---|---|-----------|-----|
| SUSTAINED | 0.186 | 0.290 | 0.657 | 0.941 | 0.0121 | #22 |
| **ACUTE (Mar 5–15, 2013)** | **0.689** | **0.358** | **0.380*** | **1.000** | **0.1154** | est. |

**Key contribution:** Dual-Mode SRM. AAF = 9.5. Structured Revolutionary ICI (+0.126) vs. Unstructured Legacy Contestation ICI (Mandela +0.272).

---

### Case Study 12 — Charlie Hebdo (France, Jan–Feb 2015)

| V | A | D_new | N | λ emp | Job |
|---|---|-------|---|-------|-----|
| TBD | TBD | 0.661 | TBD | 104.66 | #24 |

**Key contribution:** Flash Viral rank 1 (ICI=0.730, ICI−PE=+0.138). λ=104.66 highest in dataset. H1 confirmed.

---

### Case Study 13 — Narendra Modi (India, May 2013 – May 2014) ★ NEW

| V | A | D_new | N | SRM (λ=2) | Job |
|---|---|-------|---|-----------|-----|
| TBD | TBD | **0.746** | TBD | TBD | #25 |

**Key contribution:** **ICI = 0.9151 — breaks the Western ICI ceiling by +0.079.** Introduces Cross-Cultural Frame Incompatibility (CCFI) as a sixth ICI-generating mechanism. Establishes Non-Western Campaign/Ascension as a distinct typological sub-category (ICI−PE = +0.339, rank 1/15). CCFI acts as structural SRM suppressor.

Paper: [`SRM_Modi_SSRN_2026.docx`](SRM_Modi_SSRN_2026.docx)

---

### Case Study 14 — Benjamin Netanyahu (Israel, Oct 2023 – Mar 2024) ★ NEW

| V | A | D_new | N | SRM (λ=2) | Job |
|---|---|-------|---|-----------|-----|
| TBD | TBD | **0.654** | TBD | TBD | #26 |

**Key contribution:** **ICI = 0.6977 — does NOT exhibit CCFI despite active war context.** Pre-established Israel-Palestine frames in Anglo-American media produce pre-sorted moderate ICI. Discriminates CCFI from pre-sorted ideological framing. Introduces Pre-Sorted Wartime Contested typology. ICI−PE = +0.087 (rank 11/15).

Paper: [`SRM_Netanyahu_SSRN_2026.docx`](SRM_Netanyahu_SSRN_2026.docx)

---

## SSRN Publications

All papers available at DOI: [10.17605/OSF.IO/HYDNZ](https://doi.org/10.17605/OSF.IO/HYDNZ)

| Paper | Job | Key finding |
|-------|-----|-------------|
| Trump v2 | #10 | ICI ceiling rank 1 Western (+0.293) · 69,997-article corpus |
| Ciolacu v2 | #12 | Romanian Triad · PE convergence |
| Georgescu v2 | #14 | Largest D discrepancy (−26.5%) · λ-dominance |
| Sunflower v2 | #15 | Highest D_new (0.707) · cross-cultural diversity |
| Orbán v2 | #16 | ICI−PE≈0 · Longevity Paradox |
| Zelensky v2 | #17 | Wartime defender · H3 reformulated |
| Putin v2 | #18 | Antagonistic Pair · ICI≈Trump |
| Simion v2 | #19 | Affective Deficit (A=0.099) |
| Mandela v2 | #20 | Highest Western ICI · Legacy Contestation ICI |
| Macron v2 | #21 | Rapid Emergence Paradox |
| Chávez v2 | #22 | Dual-Mode SRM · Structured vs. Unstructured ICI |
| Charlie Hebdo | #24 | Flash Viral rank 1 · λ=104.66 |
| **Modi** ★ | **#25** | **ICI=0.915 · CCFI · Non-Western ceiling breach** |
| **Netanyahu** ★ | **#26** | **ICI=0.698 · Pre-sorted frames · CCFI discrimination** |
| **Synthetic Comparative v2** ★ | — | **15-symbol synthesis · CCFI · 8 principal findings · α=0.338** |

---

## Repository Structure

```
politomorphism/
├── .github/workflows/
│   ├── srm_compute_D.yml              ← PE/ICI pipeline (Jobs #10–#26)
│   ├── srm_ciolacu_validation.yml
│   ├── srm_zelensky_validation.yml
│   ├── srm_putin_validation.yml
│   ├── srm_simion_validation.yml
│   ├── srm_orban_validation.yml
│   └── fetch_trends.yml
├── scripts/
│   ├── get_trends.py                  ← λ calibration (Step 0)
│   ├── compute_D.py                   ← D = α·PE + (1−α)·ICI
│   ├── calibrate_alpha.py             ← α_optimal = 0.338 (updated)
│   ├── test_hypotheses.py             ← H1/H2/H3/H4 tests
│   └── srm_pipeline/
├── docs/
│   ├── srm_pe_ici_map.svg             ← Static correlation map
│   └── srm_pe_ici_map_interactive.html ← Interactive visualization
├── results/
│   └── D_result_*.json
└── README.md
```

---

## Reproducibility

- **Data:** [mediacloud.org](https://mediacloud.org) + [Google Trends](https://trends.google.com)
- **λ calibration:** `scipy.optimize.brentq`, Python 3.11, GitHub Actions ubuntu-latest
- **Sentiment:** VADER (`vaderSentiment 3.3.2`) English; DistilBERT Romanian
- **D computation:** LDA (scikit-learn K=10 seed=42) + `paraphrase-multilingual-MiniLM-L12-v2`
- **Alpha calibration:** α_optimal = **0.338**, 14 real-value entries (updated)
- **Bootstrap:** n=20 (speed); publication requires n≥200

---

## Preregistration

OSF: [10.17605/OSF.IO/HYDNZ](https://doi.org/10.17605/OSF.IO/HYDNZ)  
Zenodo: [10.5281/zenodo.18962821](https://doi.org/10.5281/zenodo.18962821)

---

## Citation

```bibtex
@misc{serban2026politomorphism,
  author  = {Serban, Gabriel Florin},
  title   = {Politomorphism: Social Resonance Model —
             PE/ICI Decomposition across 15 Validated Political Symbols},
  year    = {2026},
  doi     = {10.17605/OSF.IO/HYDNZ},
  url     = {https://github.com/profserbangabriel-del/Politomorphism},
  license = {CC BY 4.0}
}
```

---

*Politomorphism Research Project · Serban Gabriel Florin · Romania / EU · March 2026*
