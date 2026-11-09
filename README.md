# What Else Gets Repaired? — PAKDD 2027 Artifact

Research artifact scaffold for **“What Else Gets Repaired? Mining and Auditing Cross-File Repair after AI-Marked Commits.”**

This repository is based on the manuscript and figure-generation script supplied by the author. It preserves those source files and makes the current evidence and missing inputs explicit.

## Research summary

The manuscript reports a matched comparison of 6,422 AI-marker commits and 30,808 unmarked commits across 45 repositories. Its primary outcome, `R14`, is a fix-like commit within 14 days that touches at least one file changed by the original commit and at least one previously untouched file.

Reported manuscript estimates:
- `R14`: 50.8% for marked commits versus 48.0% for controls (difference +2.8 percentage points; 95% CI 0.6 to 5.3).
- Difference-in-differences estimate: +1.9 percentage points (95% CI 0.3 to 3.5).
- The manuscript discusses sensitivity to differential spurious fix-labeling, repository heterogeneity, and bootstrap interval coverage.

**These are manuscript-reported values, not independently reproduced results in this scaffold.**

## Repository layout

```text
.
├── manuscript/       # Supplied LaTeX sources and PDF previews
├── scripts/          # Supplied figure-generation script
├── data/             # Input data belong here (not included in supplied ZIP)
├── results/          # Reproducible outputs belong here
├── docs/              # Artifact audit and reproduction notes
├── requirements.txt
└── README.md
```

## Current artifact status

The supplied ZIP contained:
- `PAKDD2027_main.tex`
- `PAKDD2027_main_without_Fig1.tex`
- `PAKDD2027_preview.pdf`
- `PAKDD2027_preview_without_Fig1.pdf`
- `fig2_label_noise.pdf`
- `make_figures.py`

It did **not** contain the event-level or repository-level CSV data, the matching table, the original analysis scripts, the simulation implementation, or the prespecification/sensitivity CSV files referenced in the research materials. Consequently, the main empirical estimates and simulation claims cannot yet be rerun from this ZIP alone.

## Setup

Python 3.10+ is recommended.

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Figure generation

The supplied script can generate Figure 2 using the paper's embedded fallback points:

```bash
cd scripts
python make_figures.py
```

Figure 1 requires a repository-level CSV with columns:

```csv
repo,n_sets,marked_rate,control_rate
```

Run it from `scripts/` with:

```bash
python make_figures.py --repo ../data/repo_level.csv
```

The optional simulation sweep CSV for Figure 2 requires:

```csv
gap_pp,scenario,estimator,bias_pp,reject_pct
```

Allowed `scenario` values are `constant` and `post_only`; allowed `estimator` values are `matched` and `DiD`. If no sweep CSV is supplied, the script uses the limited fallback values explicitly described in its source comments. Those points are not a substitute for the full simulation output.

## Reproduction status

| Component | Status |
|---|---|
| Manuscript source and PDF previews | Included in supplied archive |
| Figure 2 source PDF | Included in supplied archive |
| Figure-generation Python script | Included in supplied archive |
| Figure 1 repository-level input | Missing |
| Event-level commit data | Missing |
| Matching / outcome-construction code | Missing |
| Main statistical analysis code | Missing |
| Full simulation code and sweep output | Missing |
| Prespecification and sensitivity result tables | Missing |

See [`docs/ARTIFACT_AUDIT.md`](docs/ARTIFACT_AUDIT.md) before making any reproducibility or artifact-completeness claim.

## Data and privacy

The manuscript states that commit messages and author identities are not redistributed because they are personal data of third parties. Any future data release should preserve that restriction and document the permitted aggregation/de-identification procedure.

## Citation

Use the bibliographic details from the final accepted/submitted manuscript. Do not treat this scaffold as a published or independently validated artifact.
