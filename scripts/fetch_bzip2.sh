#!/usr/bin/env bash
# Download a fixed upstream release and verify its SHA-256.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p third_party results

ARCHIVE="third_party/bzip2-1.0.8.tar.gz"
URL="https://sourceware.org/pub/bzip2/bzip2-1.0.8.tar.gz"
SHA="ab5a03176ee106d3f0fa90e381da478ddae405918153cca248e682cd0c4a2269"

if [[ ! -f "$ARCHIVE" ]]; then
  curl --fail --location --retry 3 \
    --connect-timeout 15 --max-time 180 \
    "$URL" -o "$ARCHIVE.part"
  mv "$ARCHIVE.part" "$ARCHIVE"
fi

printf '%s  %s\n' "$SHA" "$ARCHIVE" | sha256sum -c -

if [[ ! -d third_party/bzip2-1.0.8 ]]; then
  tar -xzf "$ARCHIVE" -C third_party
fi

{
  printf 'Source URL: %s\n' "$URL"
  printf 'Version: 1.0.8\n'
  printf 'SHA256: %s\n' "$SHA"
  printf 'Upstream source modifications: none\n'
} > results/bzip2-source.txt

echo "PASS: bzip2 source is ready."
