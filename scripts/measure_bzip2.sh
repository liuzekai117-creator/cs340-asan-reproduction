#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export LC_ALL=C

BATCH="$(mktemp -d "$ROOT/results/bzip2-run-XXXXXXXX")"
INPUT="build/input-32MiB.bin"

{
  date -Is
  echo "Repository commit: $(git rev-parse HEAD)"
  git status --short
  echo "Command: bzip2 -9 -c INPUT > /dev/null"
  echo "Repetitions: 4 per variant; alternating order"
  echo "Warmup: 1 per variant, excluded from measurements"
  echo "CPU affinity: not pinned"
  echo "ASAN_OPTIONS=${ASAN_OPTIONS-<unset>}"
  echo "LSAN_OPTIONS=${LSAN_OPTIONS-<unset>}"
  uname -r
  clang-18 --version
  sha256sum "$INPUT" build/bzip2-{baseline,asan}/bzip2
} > "$BATCH/settings.txt"

echo "Warming up..."
for variant in baseline asan; do
  "./build/bzip2-$variant/bzip2" -9 -c "$INPUT" \
    > /dev/null 2> "$BATCH/warmup-$variant.stderr"
done

echo "run,variant,elapsed_seconds,max_rss_KiB,exit_status" \
  > "$BATCH/measurements.csv"

for run in 1 2 3 4; do
  if (( run % 2 == 1 )); then
    order=(baseline asan)
  else
    order=(asan baseline)
  fi

  for variant in "${order[@]}"; do
    echo "Run $run/4: $variant"
    /usr/bin/time \
      -f "$run,$variant,%e,%M,%x" \
      -o "$BATCH/measurements.csv" -a \
      "./build/bzip2-$variant/bzip2" -9 -c "$INPUT" \
      > /dev/null 2> "$BATCH/run-$run-$variant.stderr"
  done
done

echo "Completed: $BATCH"
cat "$BATCH/measurements.csv"
