#!/usr/bin/env bash
# Helpers shared by the experiment scripts. Source this file; do not run it.

# Echo the clang executable to use.
#
# Honours CLANG when it is set. Otherwise prefers clang-18 and falls back to
# clang, so any 18-or-newer installation works without editing the scripts.
# Fails with a message on stderr when no usable compiler is found.
clang_bin() {
  local candidate

  if [[ -n "${CLANG:-}" ]]; then
    if ! command -v "$CLANG" >/dev/null 2>&1; then
      echo "error: CLANG=$CLANG is not executable or not on PATH" >&2
      return 1
    fi
    command -v "$CLANG"
    return 0
  fi

  for candidate in clang-18 clang; do
    if command -v "$candidate" >/dev/null 2>&1; then
      command -v "$candidate"
      return 0
    fi
  done

  echo "error: no clang found; install clang 18 or newer, or set CLANG" >&2
  return 1
}
