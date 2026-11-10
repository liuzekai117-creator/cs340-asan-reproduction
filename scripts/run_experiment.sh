#!/usr/bin/env bash
# Build, generate input, measure, and summarize.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

bash scripts/build_bzip2.sh
python3 scripts/generate_input.py
bash scripts/measure_bzip2.sh

shopt -s nullglob
files=(results/bzip2-run-*/measurements.csv)
python3 scripts/summarize_bzip2.py "${files[@]}"

echo "PASS: experiment completed. See results/bzip2-run-*/summary.md"
