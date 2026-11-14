#!/usr/bin/env python3
"""Summarize every supplied batch without excluding observations."""
import csv
import math
import statistics as stats
import sys
from pathlib import Path

REQUIRED_COLUMNS = (
    "run",
    "variant",
    "elapsed_seconds",
    "max_rss_KiB",
    "exit_status",
)
VARIANTS = ("baseline", "asan")
METRICS = ("elapsed_seconds", "max_rss_KiB")
MIN_RUNS_PER_VARIANT = 3


def fail(message):
    raise SystemExit(message)


def read_rows(path):
    """Return the CSV rows of one batch, rejecting unusable headers and files."""
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        header = reader.fieldnames or []
        missing = [name for name in REQUIRED_COLUMNS if name not in header]
        if missing:
            fail(f"{path}: missing column(s): {', '.join(missing)}")
        rows = list(reader)
    if not rows:
        fail(f"{path}: no measurement rows")
    return rows


def parse_finite(value, path, column, row_number):
    """Return value as a finite float, rejecting blanks, text, nan and inf."""
    if value is None or not value.strip():
        fail(f"{path}: row {row_number}: {column} is empty")
    try:
        number = float(value)
    except ValueError:
        fail(f"{path}: row {row_number}: {column}={value!r} is not a number")
    if not math.isfinite(number):
        fail(f"{path}: row {row_number}: {column}={value!r} is not finite")
    return number


def validate(rows, path):
    """Reject rows whose variant, exit status or metrics cannot be summarized."""
    for row_number, row in enumerate(rows, start=2):
        variant = (row.get("variant") or "").strip()
        if variant not in VARIANTS:
            fail(
                f"{path}: row {row_number}: variant={variant!r} is not one of "
                f"{', '.join(VARIANTS)}"
            )
        status = parse_finite(row["exit_status"], path, "exit_status", row_number)
        if status != 0:
            fail(f"{path}: row {row_number}: run failed with exit_status={status:g}")
        for metric in METRICS:
            parse_finite(row[metric], path, metric, row_number)

    counts = {variant: 0 for variant in VARIANTS}
    for row in rows:
        counts[row["variant"]] += 1
    short = [
        f"{variant}={counts[variant]}"
        for variant in VARIANTS
        if counts[variant] < MIN_RUNS_PER_VARIANT
    ]
    if short:
        fail(
            f"{path}: need at least {MIN_RUNS_PER_VARIANT} runs per variant, "
            f"found {', '.join(short)}"
        )


def summarize(path):
    """Write summary.md next to the batch CSV and return its text."""
    rows = read_rows(path)
    validate(rows, path)

    groups = {
        variant: [row for row in rows if row["variant"] == variant]
        for variant in VARIANTS
    }

    lines = [
        f"Source: {path.name}",
        "All observations included; sample standard deviation (n-1).",
        f"Runs: baseline={len(groups['baseline'])}, asan={len(groups['asan'])}",
        "",
        "| Metric | Baseline mean +/- SD | ASan mean +/- SD | Ratio of means |",
        "|---|---:|---:|---:|",
    ]
    for metric in METRICS:
        baseline = [float(row[metric]) for row in groups["baseline"]]
        asan = [float(row[metric]) for row in groups["asan"]]
        baseline_mean = stats.mean(baseline)
        if baseline_mean == 0:
            fail(f"{path}: baseline mean of {metric} is zero; ratio undefined")
        lines.append(
            f"| {metric} | {baseline_mean:.4f} +/- {stats.stdev(baseline):.4f} "
            f"| {stats.mean(asan):.4f} +/- {stats.stdev(asan):.4f} "
            f"| {stats.mean(asan) / baseline_mean:.4f} |"
        )

    text = "\n".join(lines) + "\n"
    path.with_name("summary.md").write_text(text)
    return text


def main():
    if len(sys.argv) < 2:
        fail("Usage: summarize_bzip2.py measurements.csv [...]")
    for name in sys.argv[1:]:
        path = Path(name)
        if not path.is_file():
            fail(f"{path}: no such file")
        print(f"\nBatch: {path.parent}")
        print(summarize(path), end="")


if __name__ == "__main__":
    main()
