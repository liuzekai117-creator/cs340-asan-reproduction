#!/usr/bin/env bash
# Record hardware and toolchain versions for the current experiment batch.
# The report is written to results/env-<timestamp>.txt and is safe to commit.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STAMP="$(date +%Y%m%d-%H%M%S)"
REPORT="$ROOT/results/env-$STAMP.txt"
mkdir -p "$ROOT/results"

{
  echo "date:         $(date -Is)"
  echo "hostname:     $(hostname)"
  echo "kernel:       $(uname -r)"
  echo "distribution: $(. /etc/os-release 2>/dev/null && echo "${PRETTY_NAME:-unknown}")"
  echo "cpu:          $(grep -m1 'model name' /proc/cpuinfo | cut -d: -f2- | xargs)"
  echo "threads:      $(nproc)"
  echo "memory:       $(free -h | awk '/^Mem:/{print $2}')"
  echo "clang:        $(clang --version | head -n1)"
  echo "gcc:          $(gcc --version | head -n1)"
  echo "glibc:        $(ldd --version | head -n1)"
  echo "governor:     $(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null || echo unknown)"
} > "$REPORT"

echo "environment recorded in ${REPORT#"$ROOT/"}"