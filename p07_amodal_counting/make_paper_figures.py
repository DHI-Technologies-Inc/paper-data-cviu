#!/usr/bin/env python3
"""Generate paper 07 figures from committed synthetic table + G1-03 JSON.

Diagrams are drawn with boxes and arrows. No monospace text dumps.
Numbers come from SYNTH (committed bench) and evaluation_result_v1.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_shared"))
from figdraw import FILL_OK, GRAY, INK, NAVY, ORANGE, arrow, box, clean_axes, rc

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "latex_tmlr" / "figures"
G103 = Path("REPO_ROOT/products/amodal-counting/evidence/a4_protocol/evaluation_result_v1.json")

SYNTH = [
    {"crowding": 0.0, "naive": 2.80, "corrected": 2.40, "coverage": 0.90, "z": 6.726},
    {"crowding": 0.3, "naive": 2.60, "corrected": 1.97, "coverage": 0.90, "z": 8.202},
    {"crowding": 0.6, "naive": 2.85, "corrected": 2.34, "coverage": 0.975, "z": 14.463},
    {"crowding": 0.8, "naive": 3.73, "corrected": 2.46, "coverage": 0.975, "z": 7.754},
]

# Alignment study at crowding 0.6 (separate from T1 naive 2.85).
# Means over 10 paired seeds per crowding level (eval/align_multiseed_2026-10-05.json).
ALIGN = {
    0.3: {"naive": 2.350, "truth_fitted": 1.946, "aligned": 1.855},
    0.6: {"naive": 2.960, "truth_fitted": 2.286, "aligned": 2.195},
    0.8: {"naive": 3.702, "truth_fitted": 2.722, "aligned": 2.550},
}


def draw_pipeline() -> None:
    fig, ax = plt.subplots(figsize=(6.7, 2.05))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    b1 = box(ax, 0.01, 0.34, 0.13, 0.36, "Boxes", weight="medium", fontsize=12.5)
    b2 = box(ax, 0.16, 0.34, 0.16, 0.36, r"Visibility" + "\n" + r"$\hat v$", fontsize=12.2)
    b3 = box(
        ax,
        0.34, 0.34, 0.19, 0.36,
        r"$p(\mathrm{detect}$" + "\n" + r"$\mid\hat v)$",
        fontsize=12.0,
    )
    b4 = box(ax, 0.55, 0.34, 0.13, 0.36, "HT\ncount", fontsize=12.2)
    b5 = box(ax, 0.71, 0.34, 0.13, 0.36, r"$z\cdot\hat\sigma$", fontsize=12.2)
    b6 = box(ax, 0.87, 0.34, 0.13, 0.36, "Interval\n+ flag", fill=FILL_OK, weight="medium", fontsize=12.2)
    for a, b in ((b1, b2), (b2, b3), (b3, b4), (b4, b5), (b5, b6)):
        arrow(ax, (a[0] + a[4] / 2, 0.52), (b[0] - b[4] / 2, 0.52))
    fig.savefig(OUT / "f1_pipeline.pdf")
    fig.savefig(OUT / "f1_pipeline.png", dpi=200)
    plt.close(fig)


def draw_detectability() -> None:
    xs = [i / 50.0 for i in range(51)]
    k, v0 = 10.0, 0.35
    ys = [1.0 / (1.0 + pow(2.718281828, -k * (x - v0))) for x in xs]
    fig, ax = plt.subplots(figsize=(5.6, 2.55))
    ax.plot(xs, ys, color=NAVY, lw=1.6)
    ax.axvline(0.05, color=INK, linestyle="--", lw=1.0, label="visibility floor 0.05")
    ax.axhline(0.3, color=GRAY, linestyle=":", lw=1.1, label="min_p default 0.3")
    ax.set_xlabel("visibility")
    ax.set_ylabel(r"$p(\mathrm{detect})$")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.05)
    clean_axes(ax)
    ax.legend(frameon=False, fontsize=7.6)
    fig.savefig(OUT / "f2_detectability.pdf")
    fig.savefig(OUT / "f2_detectability.png", dpi=200)
    plt.close(fig)


def draw_alignment() -> None:
    import numpy as np
    levels = [0.3, 0.6, 0.8]
    series = [("naive", "Naive", GRAY), ("truth_fitted", "Fit on $v$, query $\\hat v$", ORANGE),
              ("aligned", "Fit on $\\hat v$, query $\\hat v$", NAVY)]
    x = np.arange(len(levels))
    w = 0.26
    fig, ax = plt.subplots(figsize=(5.4, 2.65))
    for i, (key, label, color) in enumerate(series):
        vals = [ALIGN[c][key] for c in levels]
        bars = ax.bar(x + (i - 1) * w, vals, width=w, color=color, label=label, zorder=2)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + 0.05, f"{v:.2f}", ha="center", va="bottom", fontsize=6.8)
    ax.set_xticks(x)
    ax.set_xticklabels([f"crowding {c}" for c in levels], fontsize=8)
    ax.set_ylabel("MAE (mean of 10 seeds)")
    ax.set_ylim(0, 4.6)
    clean_axes(ax)
    ax.legend(frameon=False, fontsize=7.2, loc="upper left", ncol=3)
    fig.savefig(OUT / "f3_alignment.pdf")
    fig.savefig(OUT / "f3_alignment.png", dpi=200)
    plt.close(fig)


def draw_coverage() -> None:
    fig, ax = plt.subplots(figsize=(4.8, 2.55))
    ax.bar([0, 1], [0.565, 0.9375], width=0.48, color=[ORANGE, NAVY], zorder=2)
    ax.axhline(0.90, color=INK, linestyle="--", lw=1.0, label="nominal 0.90")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Analytic HT", r"After conformal $z$"])
    ax.set_ylim(0, 1.08)
    ax.set_ylabel("coverage")
    clean_axes(ax)
    ax.legend(frameon=False, loc="upper left")
    fig.savefig(OUT / "f4_coverage.pdf")
    fig.savefig(OUT / "f4_coverage.png", dpi=200)
    plt.close(fig)


def draw_synth_mae() -> None:
    crowd = [r["crowding"] for r in SYNTH]
    fig, ax = plt.subplots(figsize=(5.6, 2.65))
    ax.plot(crowd, [r["naive"] for r in SYNTH], "o-", color=ORANGE, lw=1.4, label="naive MAE")
    ax.plot(crowd, [r["corrected"] for r in SYNTH], "s-", color=NAVY, lw=1.4, label="corrected MAE")
    ax.set_xlabel("crowding")
    ax.set_ylabel("MAE (synthetic)")
    ax.set_xticks(crowd)
    clean_axes(ax)
    ax.legend(frameon=False)
    fig.savefig(OUT / "t1_synth_mae.pdf")
    fig.savefig(OUT / "t1_synth_mae.png", dpi=200)
    plt.close(fig)


def draw_min_p() -> None:
    minp = [0.1, 0.2, 0.3, 0.4]
    fig, ax = plt.subplots(figsize=(5.6, 2.65))
    ax.plot(minp, [2.89, 2.21, 1.71, 1.52], "o-", color=NAVY, lw=1.4, label="crowding 0.6")
    ax.plot(minp, [2.63, 2.60, 2.59, 2.53], "s-", color=ORANGE, lw=1.4, label="crowding 0.8")
    ax.set_xlabel(r"$\mathrm{min\_p}$")
    ax.set_ylabel("MAE")
    ax.set_xticks(minp)
    clean_axes(ax)
    ax.legend(frameon=False)
    fig.savefig(OUT / "t2_min_p.pdf")
    fig.savefig(OUT / "t2_min_p.png", dpi=200)
    plt.close(fig)


def draw_z_scales() -> None:
    crowd = [r["crowding"] for r in SYNTH]
    fig, ax = plt.subplots(figsize=(5.6, 2.55))
    ax.plot(crowd, [r["z"] for r in SYNTH], "o-", color=NAVY, lw=1.4)
    ax.set_xlabel("crowding")
    ax.set_ylabel("conformal $z$-scale")
    ax.set_xticks(crowd)
    ax.set_ylim(0, 16)
    clean_axes(ax)
    fig.savefig(OUT / "t3_z_scales.pdf")
    fig.savefig(OUT / "t3_z_scales.png", dpi=200)
    plt.close(fig)


def draw_g103(agg: dict, support: dict) -> None:
    raw = float(agg["mae_raw"])
    corr = float(agg["mae_corrected"])
    ci = agg["paired_bootstrap"]["ci_95_percentile"]
    fig, ax = plt.subplots(figsize=(5.4, 2.75))
    bars = ax.bar([0, 1], [raw, corr], width=0.48, color=[ORANGE, NAVY], zorder=2)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Raw detections", "Corrected HT"])
    ax.set_ylabel("P3 one-shot MAE")
    ax.set_ylim(0, 15.2)
    clean_axes(ax)
    for b, v in zip(bars, (raw, corr)):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.25, f"{v:.3f}", ha="center", va="bottom", fontsize=8)
    ax.text(
        0.5,
        0.96,
        f"coverage {agg['coverage']:.4f}   "
        f"{agg['extrapolation_count']}/{agg['scenes']} extrapolating   "
        f"bootstrap 95% [{ci[0]:+.4f}, {ci[1]:+.4f}] includes 0",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=6.8,
        color=GRAY,
    )
    ax.text(
        0.5,
        -0.22,
        f"in-support $n={support['scenes']}$: corrected {support['mae_corrected']:.3f} "
        f"vs raw {support['mae_raw']:.3f} (loses)",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=7.2,
        color=INK,
    )
    fig.savefig(OUT / "t4_g1_03.pdf")
    fig.savefig(OUT / "t4_g1_03.png", dpi=200)
    plt.close(fig)


def main() -> None:
    rc()
    OUT.mkdir(parents=True, exist_ok=True)
    g1 = json.loads(G103.read_text())
    agg = g1["aggregate"]
    support = g1["slices"]["within_calibration_support"]

    draw_pipeline()
    draw_detectability()
    draw_alignment()
    draw_coverage()
    draw_synth_mae()
    draw_min_p()
    draw_z_scales()
    draw_g103(agg, support)

    (OUT / "MANIFEST.json").write_text(
        json.dumps(
            {
                "script": "07_amodal_counting/eval/make_paper_figures.py",
                "source_g1_03": str(G103),
                "synth": SYNTH,
                "align_multiseed_means": {str(k): v for k, v in ALIGN.items()},
                "outputs": sorted(p.name for p in OUT.iterdir() if p.name != "MANIFEST.json"),
            },
            indent=2,
        )
        + "\n"
    )


if __name__ == "__main__":
    main()
