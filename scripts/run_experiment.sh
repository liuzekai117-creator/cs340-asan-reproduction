#!/usr/bin/env bash
# Build, generate input, measure, and summarize the batch just produced.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

bash scripts/build_bzip2.sh
python3 scripts/generate_input.py
bash scripts/measure_bzip2.sh

if [[ ! -f results/.last-batch ]]; then
  echo "error: results/.last-batch missing; measure_bzip2.sh recorded no batch" >&2
  exit 1
fi

batch="$(cat results/.last-batch)"
if [[ ! -f "$batch/measurements.csv" ]]; then
  echo "error: $batch/measurements.csv missing" >&2
  exit 1
fi

python3 scripts/summarize_bzip2.py "$batch/measurements.csv"

echo "PASS: experiment completed. See ${batch#"$ROOT/"}/summary.md"
