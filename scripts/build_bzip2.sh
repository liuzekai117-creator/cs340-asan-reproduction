#!/usr/bin/env bash
# Build and test baseline and ASan variants separately.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
source "$ROOT/scripts/common.sh"

CLANG_BIN="$(clang_bin)"

bash scripts/fetch_bzip2.sh
mkdir -p build results

COMMON="-Wall -Winline -O2 -g -fno-omit-frame-pointer -D_FILE_OFFSET_BITS=64"

for variant in baseline asan; do
  DIR="build/bzip2-$variant"
  LOG="results/bzip2-build-$variant.log"
  mkdir -p "$DIR"
  cp -a third_party/bzip2-1.0.8/. "$DIR/"

  FLAGS="$COMMON"
  if [[ "$variant" == "asan" ]]; then
    FLAGS="$FLAGS -fsanitize=address"
  fi

  echo "Building and testing: $variant"

  (
    set -e
    echo "Compiler: $CLANG_BIN"
    "$CLANG_BIN" --version
    echo "CFLAGS: $FLAGS"
    make -C "$DIR" clean
    make -C "$DIR" -j2 CC="$CLANG_BIN" CFLAGS="$FLAGS" bzip2
    make -C "$DIR" CC="$CLANG_BIN" CFLAGS="$FLAGS" test
  ) > "$LOG" 2>&1 || {
    echo "FAIL: $variant; see $LOG"
    tail -n 40 "$LOG"
    exit 1
  }

  echo "PASS: $variant build and upstream tests."
done
