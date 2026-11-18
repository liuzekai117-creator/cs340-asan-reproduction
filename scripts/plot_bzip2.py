"""Rebuild the figure and table for the four batches archived at a56781d."""
import csv
from pathlib import Path
from statistics import mean, stdev

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/figures"
OUT.mkdir(parents=True, exist_ok=True)
batches = {
    "First": "bzip2-run-0lXaeOE4",
    "Repeat": "bzip2-run-NVdQw6zH",
    "Diagnostic": "bzip2-diagnostic-MDul3KA8",
    "End-to-end": "bzip2-run-jGdCjfol",
}
fig, axes = plt.subplots(2, 4, figsize=(10, 5.4), sharey="row", sharex=True)
header = ["batch", "metric", "unit", "n_per_variant", "baseline_mean",
          "baseline_sample_sd", "asan_mean", "asan_sample_sd", "ratio_of_means"]
table = [header]
for col, (label, directory) in enumerate(batches.items()):
    path = ROOT / "results" / directory / "measurements.csv"
    with path.open() as stream:
        rows = list(csv.DictReader(stream))
    axes[0, col].set_title(label)
    for row, (metric, unit) in enumerate([("elapsed_seconds", "s"), ("max_rss_KiB", "KiB")]):
        ax = axes[row, col]
        stats = []
        for variant, color, marker in [("baseline", "#285579", "o"), ("asan", "#AE432D", "s")]:
            runs = sorted((r for r in rows if r["variant"] == variant), key=lambda r: int(r["run"]))
            if len(rows) != 8 or [r["run"] for r in runs] != list("1234") or any(r["exit_status"] != "0" for r in runs):
                raise ValueError(f"Check run IDs and exit codes in {path}")
            values = [float(r[metric]) for r in runs]
            stats.extend([mean(values), stdev(values)])
            ax.plot(range(1, 5), values, color=color, marker=marker, label=variant, linewidth=1.4)
            if metric == "elapsed_seconds" and max(values) > 5:
                ax.annotate(f"{max(values):.2f} s", (values.index(max(values))+1, max(values)),
                            xytext=(6, 4), textcoords="offset points", fontsize=9)
        table.append([directory, metric, unit, 4, *[f"{v:.4f}" for v in stats + [stats[2]/stats[0]]]])
        ax.grid(axis="y", alpha=.22)
        ax.set_xticks(range(1, 5))
        ax.set_ylim(0, 8.7 if row == 0 else 16500)
        ax.spines[["top", "right"]].set_visible(False)
axes[0, 0].set_ylabel("Elapsed time (s)")
axes[1, 0].set_ylabel("Peak RSS (KiB)")
fig.legend(*axes[0, 0].get_legend_handles_labels(), loc="upper center", ncol=2, frameon=False)
fig.supxlabel("Measured round within batch", fontsize=11)
fig.tight_layout(rect=(0, .04, 1, .91))
fig.savefig(OUT / "bzip2-runs.png", dpi=170)
with (OUT / "bzip2-batch-stats.csv").open("w", newline="") as stream:
    csv.writer(stream).writerows(table)
