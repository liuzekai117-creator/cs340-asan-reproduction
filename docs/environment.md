# Environment

Recorded with scripts/setup_env.sh for every experiment batch.

| Item | Value |
|------|-------|
| CPU | Intel Core i7-14700KF (8 P-cores + 12 E-cores, 28 threads) |
| Memory | 32 GB |
| Host OS | Windows 10 Pro 25H2 (build 26200) |
| Guest OS | Ubuntu 24.04 (WSL2) |
| Kernel | TBD (uname -r) |
| clang | TBD (clang --version) |
| glibc | TBD (ldd --version) |

Notes:

- Experiments are pinned to the P-cores with taskset -c 0-15 so that the hybrid
  core layout does not enter the measurements.
- The CPU governor is set to performance before every measurement batch.