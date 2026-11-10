#!/usr/bin/env python3
"""Summarize every supplied batch without excluding observations."""
import csv
import statistics as stats
import sys
from pathlib import Path

if len(sys.argv) < 2:
    raise SystemExit("Usage: summarize_bzip2.py measurements.csv [...]")

for name in sys.argv[1:]:
    path = Path(name)
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))

    if any(int(r["exit_status"]) != 0 for r in rows):
        raise SystemExit(f"Failed run found: {path}")

    groups = {
        v: [r for r in rows if r["variant"] == v]
        for v in ("baseline", "asan")
    }
    if any(len(group) < 3 for group in groups.values()):
        raise SystemExit(f"Need at least 3 runs per variant: {path}")

    lines = [
        f"Source: {path.name}",
        "All observations included; sample standard deviation (n-1).",
        f"Runs: baseline={len(groups['baseline'])}, asan={len(groups['asan'])}",
        "",
        "| Metric | Baseline mean +/- SD | ASan mean +/- SD | Ratio of means |",
        "|---|---:|---:|---:|",
    ]
    for metric in ("elapsed_seconds", "max_rss_KiB"):
        b = [float(r[metric]) for r in groups["baseline"]]
        a = [float(r[metric]) for r in groups["asan"]]
        lines.append(
            f"| {metric} | {stats.mean(b):.4f} +/- {stats.stdev(b):.4f} "
            f"| {stats.mean(a):.4f} +/- {stats.stdev(a):.4f} "
            f"| {stats.mean(a) / stats.mean(b):.4f} |"
        )

    text = "\n".join(lines) + "\n"
    path.with_name("summary.md").write_text(text)
    print(f"\nBatch: {path.parent}")
    print(text)
