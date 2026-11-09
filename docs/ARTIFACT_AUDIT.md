# Artifact audit

## Scope

This audit compares the contents of the author-supplied ZIP with the files and reproducibility claims described in the supplied manuscript. It does not validate the underlying empirical data or independently reproduce the paper's results.

## Files received

| File | Present | Notes |
|---|---:|---|
| `PAKDD2027_main.tex` | Yes | Main LaTeX manuscript |
| `PAKDD2027_main_without_Fig1.tex` | Yes | Alternate manuscript source |
| `PAKDD2027_preview.pdf` | Yes | Manuscript preview |
| `PAKDD2027_preview_without_Fig1.pdf` | Yes | Alternate preview |
| `fig2_label_noise.pdf` | Yes | Figure 2 PDF |
| `make_figures.py` | Yes | Figure generation script |

## Inputs and scripts not received

The manuscript/artifact description refers to repository-level data, repository lists, marker rules, a prespecification record, sensitivity results, and analysis/simulation scripts. These were not present in the supplied ZIP. In particular, the ZIP does not contain enough information to reconstruct commit-level outcomes or rerun the matching and inferential analyses.

## Required next inputs

1. The exact anonymized artifact contents or an export of the existing artifact repository.
2. The repository-level CSV used for Figure 1.
3. The event-level or sufficient aggregated data required by the prespecified analysis, with third-party identities and commit messages excluded as described in the manuscript.
4. Matching and outcome-construction scripts.
5. Main analysis and simulation scripts, including fixed seeds and configuration.
6. Prespecification and sensitivity result files.

## Integrity rules for future work

- Do not synthesize missing observations or fabricate repository-level values.
- Do not reverse-engineer raw data from plotted points or manuscript summary statistics.
- Label any newly implemented analysis as a reconstruction until checked against the original protocol and outputs.
- Keep manuscript-reported values distinct from independently regenerated results.
- Respect the manuscript's stated privacy restriction on commit messages and author identities.
