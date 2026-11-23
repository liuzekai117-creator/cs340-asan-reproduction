#!/usr/bin/env bash
# Compare a clean replay host to the versions recorded for the WSL batch.
set -eu
root=$(cd "$(dirname "$0")/.." && pwd)
record="$root/results/environment.txt"
differences=0
compare() {
  if [[ "$2" == "$3" ]]; then
    printf 'match  %s  %s\n' "$1" "$2"
  else
    printf 'differ %s  recorded=%s  observed=%s\n' "$1" "$2" "$3"
    differences=1
  fi
}
source /etc/os-release
compare distribution 'Ubuntu 24.04.5 LTS' "$PRETTY_NAME"
compare kernel '6.18.58.1-microsoft-standard-WSL2' "$(uname -r)"
while read -r package version; do
  actual=$(dpkg-query -W -f='${Version}' "$package" 2>/dev/null) || actual=missing
  compare "$package" "$version" "$actual"
done < <(awk '/^=== C library ===/{exit} seen{print} /^=== Installed tool versions ===/{seen=1}' "$record")
exit "$differences"
