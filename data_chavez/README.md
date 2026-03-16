# data_chavez — Hugo Chávez SRM Validation (Venezuela, 2002)

## Case Study 11 — Hugo Chávez (Venezuela, April 2002)

**Event:** April 11–13, 2002 coup attempt against Chávez + counter-coup restoration within 48 hours.

**First SRM validation using λ=7** (empirical GT calibration default, March 2026).

---

## Analysis Design

| Period | Dates | Purpose |
|--------|-------|---------|
| Baseline | Jan 1, 2001 – Mar 31, 2002 | Pre-coup media baseline |
| Analysis | Apr 1, 2002 – Dec 31, 2002 | Coup event + aftermath |

**Media Cloud collections:** US National + US State & Local + Latin America Monitor  
**Search term:** `HUGO CHAVEZ`

---

## Files Required (upload from Media Cloud)

| File | Description |
|------|-------------|
| `chavez_baseline.csv` | Media Cloud counts Jan 2001 – Mar 2002 |
| `chavez_analysis.csv` | Media Cloud counts Apr 2002 – Dec 2002 |
| `chavez_titles.csv` | Article titles containing "chavez" (for VADER) |

**Columns:** `date, count, total_count, ratio`

---

## Theoretical Parameters (pre-pipeline estimate)

| Variable | Estimated value | Rationale |
|----------|----------------|-----------|
| V | ~0.87 | Near-zero baseline → global saturation in 48h (among highest possible escalation) |
| A | ~0.68 | Coup attempt = extreme affective weight; binary hero/victim framing |
| D | ~0.50 | LOW — coup created binary frame (hero vs. traitor), collapsing prior complexity |
| N | ~0.78 | Strong US + Latin American coverage, but 2002 pre-social-media constraint |
| λ | **7** | Empirical GT median (Trump=7.01, Ciolacu=6.57) |

**Estimated SRM (λ=7):** ~0.19–0.24 → boundary MEDIUM/HIGH RESONANCE  
**Estimated SRM (λ=2):** ~0.28–0.35 → HIGH RESONANCE

---

## Why Chávez 2002 Is Expected to Produce HIGH Resonance

The April 2002 coup attempt is structurally unique in the dataset:

1. **D is low** — the coup collapsed semantic complexity into a binary hero/villain structure. Unlike Macron (5 simultaneous contradictory frames) or Georgescu (fragmented viral), the coup produced semantic convergence.

2. **V is extreme** — escalation from obscure South American president (by US media standards) to front-page global story in 48 hours. Comparable to Mandela's death spike, but sustained for months.

3. **A is high** — military coup, civilian counter-coup, dramatic palace restoration: the event structure maximizes affective weight in English-language media.

4. **N is solid** — US media covered the story continuously for months post-coup (oil crisis angle, US involvement allegations, Bolivarian movement framing).

---

## λ=7 — Methodological Note

All prior SRM validations (Cases 1–10) used λ=2 (theoretical default). Chávez is the **first case using λ=7** — the empirical median derived from GT calibration (March 2026). Both SRM values are reported for comparability.

If D=0.50 holds, the difference:
- `e^(-7×0.50)` = 0.0302 → SRM(λ=7) ≈ 0.87 × 0.68 × 0.0302 × 0.78 ≈ **0.014**
- `e^(-2×0.50)` = 0.3679 → SRM(λ=2) ≈ 0.87 × 0.68 × 0.3679 × 0.78 ≈ **0.170**

**Key insight:** the LOW D that makes Chávez theoretically HIGH resonance at λ=2 is severely compressed at λ=7. This case will test whether the empirical λ calibration changes the resonance classification.

---

## How to Run

1. Download Media Cloud data for both periods (search: HUGO CHAVEZ)
2. Upload CSV files to this folder
3. Go to **Actions → SRM Validation Pipeline — Hugo Chávez → Run workflow**
4. Input your VADER-computed A value and estimated D value
5. Download artifact: `srm-chavez-results`
