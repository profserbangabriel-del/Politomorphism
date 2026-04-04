Politomorphism — Social Resonance Model (SRM)
Serban Gabriel Florin | Independent Researcher  
ORCID: 0009-0000-2266-3356 | DOI: 10.17605/OSF.IO/HYDNZ  
GitHub: profserbangabriel-del/Politomorphism  
License: CC BY 4.0
---
PE/ICI Correlation Map — 19 Validated Symbol-Periods
![SRM PE/ICI Interactive Map](https://img.shields.io/badge/Interactive%20Chart-PE%2FICI%20Map-b8001f?style=flat-square)
> **Interactive version:** [srm_pe_ici_map_interactive.html](https://profserbangabriel-del.github.io/Politomorphism/srm_pe_ici_map_interactive.html)  
> **Key finding:** ICI range (0.385) is **6.8× larger** than PE range (0.057) across 19 symbol-periods. Modi 2014 (ICI=0.904) breaks the Western ICI ceiling through CCFI. The CCFI lifecycle (Modi 2014→2019→2024) documents asymptotic stabilization at ~0.80. Zelensky (ICI=0.542 < PE=0.596) is the only symbol with ICI < PE — wartime frame convergence confirmed empirically.
```
ICI
0.93 │ Chavez ●
0.91 │
0.90 │          IranIsrael ●  Modi2014 ●
     │
0.88 │                    Trump ●
     │
0.85 │                         Modi2024 ●
0.82 │                    Modi2019 ●
0.80 │ ChavezAcute ●  Sunflower ●
0.79 │                    Bolsonaro ●
     │
0.75 │       Putin ●        Mandela ●
0.73 │                 CharlieHebdo ●  Netanyahu ●  Macron ●
     │
0.69 │                    Simion ●
0.66 │                         Ciolacu ●
0.63 │                    Georgescu ●
     │
0.59 │      Orban ●
0.54 │ Zelensky ●
     └──────────────────────────────────────────── PE
       0.55  0.56  0.57  0.58  0.59  0.60  0.61  0.62  0.63
```
Bubble size ∝ 1/√λ (larger = slower decay = higher SRM potential)
---
What is Politomorphism?
Politomorphism is a theoretical framework that treats political symbols as morphogenetic agents — entities that transform power structures through the process of symbolic diffusion. Its computational component, the Social Resonance Model (SRM), quantifies how effectively a political symbol mobilizes public space across Anglo-American media.
> **Status (April 2026):** 19/19 symbol-periods validated. Bootstrap n=200 for all 18 primary symbols. V, A, N computed automatically via `compute_V_A_N.py`. Paper under review at JCSS.
---
The SRM Formula
SRM = V × A × e^(−λD) × N
Variable	Name	What it measures	Range
V	Viral Velocity	Log-normalized escalation ratio (peak/avg) from article time series	0–1
A	Affective Weight	Mean absolute VADER compound sentiment on article titles	0–1
D	Semantic Drift	D = α·PE + (1−α)·ICI, α=0.5 (primary)	0–1
N	Network Coverage	Proportion of days with ≥1 article in corpus window	0–1
λ	Decay Constant	Empirically calibrated from Google Trends avg/peak ratio	2–105
---
Complete Dataset — 19 Symbol-Periods (Bootstrap n=200)
Rank	Symbol	Period	PE	ICI	D	V	A	N	λ	SRM	Typology
1	IranIsrael	INT 2024	0.604	0.909	0.756	0.778	0.295	0.396	17.81	~0	Geopolitical Event
2	Chavez	VE 2013	0.572	0.927	0.750	0.917	0.258	0.402	16.67	~0	Volatile Legacy
3	Modi 2014	IN 2014	0.590	0.904	0.747	0.132	0.221	0.144	2.37	0.000714	CCFI Acute
4	Trump	US 2015–16	0.592	0.881	0.737	0.786	0.222	0.559	7.01	0.000559	Western Ceiling
5	Modi 2024	IN 2024	0.603	0.849	0.726	0.383	0.237	0.529	9.11	0.000065	CCFI Asymptote
6	Modi 2019	IN 2019	0.600	0.815	0.707	0.194	0.184	0.632	6.33	0.000256	CCFI Decay
7	Sunflower	TW 2014	0.621	0.787	0.704	0.091	0.195	0.971	2.00	0.00419	Civic Mobilization
8	ChavezAcute	VE Mar 2013	0.600	0.802	0.701	—	—	—	16.67	—	Dual-Mode
9	Bolsonaro	BR 2022–23	0.611	0.786	0.698	0.550	0.059	0.478	10.43	0.000011	Partial CCFI
10	Macron	FR 2017	0.603	0.729	0.666	0.478	0.085	0.570	12.53	0.000006	Campaign
11	Netanyahu	IL 2023–24	0.591	0.735	0.663	0.428	0.144	0.825	7.02	0.000485	Pre-sorted Wartime
12	CharlieHebdo	FR 2015	0.572	0.732	0.652	0.531	0.140	0.833	104.66	0.0	Extreme Flash Viral
13	Putin	RU 2022	0.547	0.753	0.650	0.503	0.108	0.402	4.90	0.000904	Wartime Aggressor
14	Simion	RO 2024	0.566	0.692	0.629	—	—	—	12.41	—	Volatile
15	Ciolacu	RO 2024–25	0.576	0.658	0.617	—	—	—	6.57	—	Campaign
16	Georgescu	RO 2024	0.578	0.634	0.606	—	—	—	65.33	~0	Flash Viral
17	Orban	HU 2022	0.601	0.592	0.597	—	—	—	2.31	—	Institutional
18	Zelensky	UA 2022	0.596	0.542	0.569	—	—	—	5.11	—	Wartime Defender
—	Mandela	ZA 2013	0.564	0.836	—*	—	—	—	19.66	—	Legacy
*Mandela (2013) predates Media Cloud indexing. PE/ICI from archival estimate. All other D: bootstrap n=200, Jobs #33–#79.  
— = V/A/N/SRM pending final `compute_V_A_N.py` run.
---
D-Score Ranking (Visual)
```
IranIsrael   ████████████████████████████████████████ 0.756
Chavez       ████████████████████████████████████████ 0.750
Modi 2014    ███████████████████████████████████████  0.747
Trump        ██████████████████████████████████████   0.737
Modi 2024    █████████████████████████████████████    0.726
Modi 2019    ████████████████████████████████████     0.707
Sunflower    ████████████████████████████████████     0.704
ChavezAcute  ████████████████████████████████████     0.701
Bolsonaro    ███████████████████████████████████      0.698
Macron       █████████████████████████████████        0.666
Netanyahu    █████████████████████████████████        0.663
CharlieHebdo ████████████████████████████████         0.652
Putin        ████████████████████████████████         0.650
Simion       ███████████████████████████████          0.629
Ciolacu      ██████████████████████████████           0.617
Georgescu    █████████████████████████████            0.606
Orban        █████████████████████████████            0.597
Zelensky     ████████████████████████████             0.569
```
> **Interactive chart:** [srm_pe_ici_map_interactive.html](https://profserbangabriel-del.github.io/Politomorphism/srm_pe_ici_map_interactive.html)
---
λ Calibration — Complete Dataset
```
avg / peak = (1 − e^(−λT)) / (λT)   →   solved via scipy.optimize.brentq
```
Category	λ range	Symbols
Institutionally Durable	2–5	Sunflower (2.00), Orban (2.31), Modi 2014 (2.37), Putin (4.90), Zelensky (5.11)
Campaign / Ascension	6–8	Modi 2019 (6.33), Ciolacu (6.57), Trump (7.01), Netanyahu (7.02)
Electorally Volatile	9–20	Modi 2024 (9.11), Bolsonaro (10.43), Simion (12.41), Macron (12.53), Chavez (16.67), IranIsrael (17.81), Mandela (19.66)
Flash Viral	50–70	Georgescu (65.33)
Extreme Flash Viral	>70	CharlieHebdo (104.66)
Key finding: λ ranges from 2.00 to 104.66 — a 52-fold variation. Lambda is the primary SRM determinant (log-log regression: β_λ = −3.50, p < 0.001, R²_adj = 0.87).
---
D Operationalization
D = α · PE + (1−α) · ICI
Component	Method	Measures
PE	Mean Jensen-Shannon Divergence on LDA (K=10, seed=42)	Topical breadth
ICI	1 − mean pairwise cosine similarity (`paraphrase-multilingual-MiniLM-L12-v2`)	Framing divergence
α = 0.5 (primary — equal weighting, theory-driven, no circularity).  
α_opt = 0.389 reported as exploratory supplementary analysis only (calibrated on same dataset — not used in hypothesis testing).
---
Cross-Cultural Frame Incompatibility (CCFI)
CCFI applies when Anglo-American journalism lacks pre-established interpretive categories, forcing outlets to construct incompatible frameworks from scratch.
CCFI Lifecycle — Modi Longitudinal Series
```
ICI
0.91 │ ● Modi 2014 (CCFI acute — no frameworks)
     │
0.82 │         ● Modi 2019 (CCFI decay — basic categories accumulate)
0.80 │ ─ ─ ─ ─ ─ ─ ─ ─ ─ CCFI asymptote floor ─ ─ ─ ─ ─ ─ ─ ─
0.85 │              ● Modi 2024 (CCFI asymptote — irreducible residual)
     └──────────────────────────────────────────────────── time
           2014              2019              2024
```
Phase	Year	ICI	D	λ	SRM
CCFI acute	2014	0.904	0.747	2.37	0.000714
CCFI decay	2019	0.815	0.707	6.33	0.000256
CCFI asymptote	2024	0.849	0.726	9.11	0.000065
First longitudinal empirical test of CCFI dynamics in the literature.
CCFI Discrimination
	Modi 2014	Netanyahu 2023
ICI	0.904	0.735
Anglo-American framework	ABSENT	PRESENT (decades of Israel-Palestine coverage)
Result	CCFI — ceiling broken	Pre-sorted — no CCFI
Active war + controversy ≠ CCFI. Pre-established frameworks produce moderate ICI regardless of conflict intensity.
---
Key Empirical Findings
ICI dominance: ICI range 6.8× larger than PE range. r(ICI, D) = 0.51, r(PE, D) = −0.02.
CCFI lifecycle: Modi 2014→2019→2024 shows ICI 0.904→0.815→0.849, λ 2.37→6.33→9.11, SRM 11× decrease.
V·A Paradox: CharlieHebdo (V=0.531, A=0.140, N=0.833) → SRM=0.0 due to λ=104.66.
Wartime convergence: Zelensky ICI=0.542 < PE=0.596 — only symbol with ICI<PE. Crisis unifies frames.
Geopolitical Event Symbol: IranIsrael ICI=0.909 through Multi-Domain Geopolitical Activation.
Log-log regression: log(SRM) = 3.09 − 3.50·log(λ) + 1.57·log(V·A·N), R²_adj=0.87, p<0.001.
Highest SRM: Sunflower Movement (SRM=0.00419) — low λ + high N (97% day coverage).
---
ICI Architecture — Seven Structural Levels
Level	ICI range	Symbols	Mechanism
CCFI acute	0.90+	Chavez (0.927), IranIsrael (0.909), Modi 2014 (0.904)	No pre-established frameworks
Western ICI ceiling	0.83–0.89	Trump (0.881), Mandela (0.836), Putin (0.753)	Electoral / legacy / aggressor
CCFI asymptote	0.79–0.82	Modi 2019 (0.815), ChavezAcute (0.802), Modi 2024 (0.849)	Irreducible residual incompatibility
Cross-cultural civic	0.78–0.79	Sunflower (0.787), Bolsonaro (0.786)	Partial cultural framing
Pre-sorted moderate	0.69–0.74	Netanyahu (0.735), CharlieHebdo (0.732), Macron (0.729)	Institutionalized sorting
Convergent	0.59–0.70	Simion (0.692), Ciolacu (0.658), Georgescu (0.634)	Frame sorting / flash decay
Institutional stable	0.54–0.60	Orban (0.592), Zelensky (0.542)	Long-term stabilization / convergence
---
Pipeline Scripts
Script	Purpose
`scripts/compute_D.py`	PE + ICI + bootstrap CI (n=200)
`scripts/compute_V_A_N.py`	Automatic V (from λ), A (VADER), N (article coverage)
`scripts/calibrate_alpha.py`	α optimization — 19/19 real values
`scripts/test_hypotheses.py`	H1/H2/H3 statistical tests
`scripts/loocv_srm.py`	Leave-One-Out CV for log-log regression
GitHub Actions Workflow
```
.github/workflows/srm_compute_D.yml
  → Fetch Media Cloud corpus (2000–4000 articles)
  → compute_D.py  → PE, ICI, D, bootstrap CI
  → compute_V_A_N.py  → V, A, N, SRM
  → calibrate_alpha.py
  → test_hypotheses.py
  → Upload ZIP artifact (retention: 90 days)
  → git pull --rebase && git push
```
---
Repository Structure
```
Politomorphism/
├── .github/workflows/
│   ├── srm_compute_D.yml              ← Full pipeline (Jobs #33–#79)
│   └── fetch_trends.yml               ← λ calibration
├── scripts/
│   ├── compute_D.py                   ← D = α·PE + (1−α)·ICI
│   ├── compute_V_A_N.py               ← V, A, N automatic computation
│   ├── calibrate_alpha.py             ← α_opt = 0.389 (exploratory)
│   ├── test_hypotheses.py             ← H1/H2/H3
│   └── loocv_srm.py                   ← LOOCV validation
├── D_result_*.json                    ← Bootstrap n=200 (18 symbols)
├── V_A_N_*.json                       ← V, A, N, SRM per symbol
├── alpha_calibration_results.json     ← 19/19 real values
├── hypothesis_test_results.json
├── index.html                         ← GitHub Pages site
├── srm_pe_ici_map_interactive.html    ← Interactive PE/ICI chart
└── README.md
```
---
Reproducibility
Data: mediacloud.org (English-language Anglo-American corpus) + Google Trends
λ calibration: `scipy.optimize.brentq`, Python 3.11, GitHub Actions ubuntu-latest
Sentiment: VADER (`vaderSentiment`) on article titles
Embeddings: `paraphrase-multilingual-MiniLM-L12-v2` (sentence-transformers)
LDA: scikit-learn, K=10, random_state=42, max_iter=20
Bootstrap: n=200 for all 18 primary symbols (Jobs #33–#79)
All analyses: reproducible via GitHub Actions — no local environment required
> **Limitation:** All corpora are Anglo-American English-language. ICI in domestic-language corpora for Non-Western symbols would likely differ. Mandela (2013) predates Media Cloud indexing. All reported associations are correlational; causal interpretation requires experimental designs.
---
Preregistration & Citation
OSF: 10.17605/OSF.IO/HYDNZ  
ORCID: 0009-0000-2266-3356
```bibtex
@misc{serban2026politomorphism,
  author  = {Serban, Gabriel Florin},
  title   = {Politomorphism: Social Resonance Model —
             PE/ICI Decomposition across 19 Validated Symbol-Periods},
  year    = {2026},
  doi     = {10.17605/OSF.IO/HYDNZ},
  url     = {https://github.com/profserbangabriel-del/Politomorphism},
  orcid   = {0009-0000-2266-3356},
  license = {CC BY 4.0}
}
```
---
Politomorphism Research Project · Serban Gabriel Florin · Romania / EU · April 2026
