# Deviations from the paper

Every difference between this reproduction and the paper setup.

| # | Item | Paper setting | Setting used | Reason |
|---|------|---------------|--------------|--------|
| 1 | Benchmark suite | SPEC CPU2006 | TBD (open benchmark suite) | SPEC CPU2006 requires a commercial license |
| 2 | Compiler | LLVM/Clang 3.0 (2012) | clang >= 18 | Current toolchain; the 2012 version is unmaintained |
| 3 | Machine | 2012 x86-64 server | Intel i7-14700KF, 32 GB, Ubuntu 24.04 on WSL2 | Available hardware |
| 4 | Repetitions | Averages as reported | 3 repetitions per configuration | Course requirement |

Runtime and memory numbers are reported as ratios (ASan / baseline), which are
less sensitive to the machine than absolute values.