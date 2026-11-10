#!/usr/bin/env bash
# Verify that ASan detects the intentional use-after-free.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p build results

clang-18 -O0 -g -fsanitize=address -fno-omit-frame-pointer \
  tests/asan_check.c -o build/asan_check

status=0
./build/asan_check > results/asan_check.log 2>&1 || status=$?

if [[ "$status" -ne 0 ]] &&
   grep -q "ERROR: AddressSanitizer: heap-use-after-free" \
     results/asan_check.log; then
  echo "PASS: ASan detected the intentional heap-use-after-free."
  echo "Log: results/asan_check.log"
else
  echo "FAIL: Expected ASan diagnostic was not found."
  cat results/asan_check.log
  exit 1
fi
