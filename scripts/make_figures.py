"""Generate Fig. 1 and Fig. 2 for "What Else Gets Repaired?" (PAKDD 2027, LNCS).

Usage:
    python make_figures.py                      # uses CSVs if present, else fallback
    python make_figures.py --repo repo_level.csv --sweep sim_gap_sweep.csv

Fig. 1 needs repository-level data (one row per repository):
    repo, n_sets, marked_rate, control_rate      (rates as proportions 0-1)

Fig. 2 uses the simulation gap sweep if available (one row per gap/scenario/estimator):
    gap_pp, scenario, estimator, bias_pp, reject_pct
      scenario  in {"constant", "post_only"}
      estimator in {"matched", "DiD"}
If the sweep CSV is missing, Fig. 2 is drawn from the closed form (3) plus ONLY the
simulation values reported in the paper text and Table 3 (no values are invented).
"""
import argparse, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# LNCS look: Computer Modern, 8 pt, text width 122 mm
plt.rcParams.update({
    "font.family": "serif", "font.serif": ["cmr10"], "mathtext.fontset": "cm",
    "axes.formatter.use_mathtext": True, "font.size": 8, "axes.labelsize": 8,
    "legend.fontsize": 6.5, "xtick.labelsize": 7, "ytick.labelsize": 7,
    "axes.linewidth": 0.6, "lines.linewidth": 1.0, "axes.unicode_minus": True,
    "pdf.fonttype": 42,
})
TEXTWIDTH_IN = 122 / 25.4
P_CONTROL = 0.480  # set-weighted control rate used in the paper's bound


def fig1(csv_path, out="fig1_repo_differences.pdf"):
    import pandas as pd
    d = pd.read_csv(csv_path)
    x = 100 * d["control_rate"].to_numpy()
    y = 100 * (d["marked_rate"] - d["control_rate"]).to_numpy()
    w = d["n_sets"].to_numpy(dtype=float)
    # weighted least squares line (exploratory meta-regression)
    X = np.column_stack([np.ones_like(x), x])
    W = np.diag(w)
    beta = np.linalg.solve(X.T @ W @ X, X.T @ W @ y)
    fig, ax = plt.subplots(figsize=(0.62 * TEXTWIDTH_IN, 0.235 * TEXTWIDTH_IN))
    ax.scatter(x, y, s=w / w.max() * 60, facecolor="none", edgecolor="0.2", linewidth=0.6)
    xs = np.linspace(x.min(), x.max(), 100)
    ax.plot(xs, beta[0] + beta[1] * xs, color="0.1")
    ax.axhline(0, color="0.6", linewidth=0.5, linestyle=":")
    for name in ("Roslyn", "Open WebUI"):
        m = d["repo"].str.contains(name, case=False, regex=False)
        for xi, yi in zip(x[m], y[m]):
            ax.annotate(name, (xi, yi), xytext=(4, 2), textcoords="offset points", fontsize=6.5)
    ax.set_xlabel("Control rate of $R_{14}$ (%)")
    ax.set_ylabel("Difference (pp)")
    fig.tight_layout(pad=0.3)
    fig.savefig(out)
    print("wrote", out, "slope =", round(beta[1], 3))


def fig2(sweep_csv=None, out="fig2_label_noise.pdf"):
    fig, (a, b) = plt.subplots(1, 2, figsize=(TEXTWIDTH_IN, 0.235 * TEXTWIDTH_IN))
    gaps = np.linspace(0, 5, 101)
    a.plot(gaps, (1 - P_CONTROL) * gaps, color="0.55", linestyle="--", label="Closed form (3)")
    if sweep_csv and os.path.exists(sweep_csv):
        import pandas as pd
        s = pd.read_csv(sweep_csv)
        style = {("matched", "constant"): ("o", "0.1", "Matched"),
                 ("DiD", "constant"): ("s", "0.45", "DiD"),
                 ("DiD", "post_only"): ("^", "0.1", "DiD, post-only gap")}
        for (est, sc), (mk, col, lab) in style.items():
            t = s[(s.estimator == est) & (s.scenario == sc)].sort_values("gap_pp")
            if len(t):
                a.plot(t.gap_pp, t.bias_pp, marker=mk, color=col, ms=3.5, label=lab)
                b.plot(t.gap_pp, t.reject_pct, marker=mk, color=col, ms=3.5, label=lab)
    else:
        # Values reported in the paper only (Table 3 Sim4/Sim5; Sect. 6 text).
        a.plot([0, 3], [0.04, 1.53], "o", color="0.1", ms=3.5, label="Matched")
        a.plot([0, 3], [0.03, -0.02], "s", color="0.45", ms=3.5, label="DiD")
        a.plot([3], [1.53], "^", mfc="none", mec="0.1", ms=6, label="DiD, post-only gap")
        b.plot([0, 5], [2.5, 74], "o", color="0.1", ms=3.5, label="Matched")
        b.plot([3], [23], "^", mfc="none", mec="0.1", ms=6, label="DiD, post-only gap")
    b.axhline(5, color="0.55", linestyle="--", label=r"Nominal $\alpha = 0.05$")
    a.axhline(0, color="0.75", linewidth=0.5, linestyle=":")
    a.set_xlabel(r"Spurious-event gap $\Delta q$ (pp)"); a.set_ylabel("Bias (pp)")
    b.set_xlabel(r"Spurious-event gap $\Delta q$ (pp)"); b.set_ylabel("FPR (%)")
    for ax, nc in ((a, 2), (b, 1)):
        ax.set_xlim(-0.2, 5.2)
        ax.legend(frameon=False, loc="upper left", ncol=nc, handlelength=1.4,
                  columnspacing=0.8, borderaxespad=0.2, fontsize=6, labelspacing=0.25)
    b.set_yticks([0, 25, 50, 75])
    a.set_ylim(-0.4, 4.2)
    b.set_ylim(0, 110)
    fig.tight_layout(pad=0.3, w_pad=1.5)
    fig.savefig(out)
    print("wrote", out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="repo_level.csv")
    ap.add_argument("--sweep", default="sim_gap_sweep.csv")
    args = ap.parse_args()
    if os.path.exists(args.repo):
        fig1(args.repo)
    else:
        print("Fig. 1 skipped: repository-level data not found:", args.repo)
    fig2(args.sweep)
