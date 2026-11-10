# CS340 Reproduction: AddressSanitizer (USENIX ATC'12)

Reproduction of *AddressSanitizer: A Fast Address Sanity Checker*
(Serebryany, Bruening, Potapenko, Vyukov; USENIX ATC 2012) for CS340
Operating Systems, Academic Year 2026-2027.

Paper: https://www.usenix.org/system/files/conference/atc12/atc12-final39.pdf

## Claims under test

| ID | Claim | Paper evidence |
|----|-------|----------------|
| C1 | Average runtime overhead is about 2x | evaluation table on SPEC CPU2006 |
| C2 | Average memory overhead is about 3x | evaluation table on SPEC CPU2006 |
| C3 | Memory errors are found in real programs | case studies |

## Status

Environment smoke test and initial bzip2 measurement pipeline implemented. Three measurement batches and one diagnostic batch recorded; timing variability remains under investigation.

## Requirements

- Linux (Ubuntu 24.04 under WSL2 is used for this reproduction)
- clang >= 18, make, cmake, python3

## Quick start

    bash scripts/setup_env.sh        # record toolchain and hardware versions
    bash scripts/run_experiment.sh   # bzip2 baseline vs ASan, 4 repetitions per variant

## Repository layout

| Path | Contents |
|------|----------|
| scripts/ | environment setup, benchmark download, experiment runner |
| results/ | measurement logs and aggregated tables |
| docs/ | environment, deviations, experiment notes |

## Environment

See docs/environment.md.

## Deviations from the paper

See docs/deviations.md. Every change from the paper setup is listed there with
the original setting, the setting used, and the reason.

## Credits and license

- Paper: Serebryany et al., AddressSanitizer: A Fast Address Sanity Checker, USENIX ATC 2012.
- Implementation under test: LLVM/Clang AddressSanitizer (Apache-2.0 with LLVM exceptions).
- Benchmarks: downloaded by script and not redistributed in this repository.

## Team
| Name      | Student ID  | GitHub Account      |
|-----------|-------------|---------------------|
| Liu Zekai | 1240002302  | liuzekai117-creator |
| Lin Xiyao |  1240001933 | linxiyao111         |
| Liu Fangzhuo|1240002384 | liufangzhuo272      |

## ASan environment smoke test

Verified on Ubuntu 24.04.5 under WSL2 with Clang 18.1.3.
See results/environment.txt for the recorded environment.

Install dependencies:

```bash
sudo apt update
sudo apt install -y clang-18 libclang-rt-18-dev llvm-18 \
  build-essential cmake git python3 time
```

Run from the repository root:

```bash
bash scripts/check_asan.sh
```

Expected output:

```text
PASS: ASan detected the intentional heap-use-after-free.
Log: results/asan_check.log
```

The script compiles tests/asan_check.c and verifies that ASan reports
the intentional heap-use-after-free with a nonzero exit status.
The full diagnostic is saved to results/asan_check.log.
The check normally takes a few seconds after dependencies are installed.

This is an environment smoke test, not a performance benchmark or
evidence that the paper's quantitative claims have been reproduced.
The main experiment runner executes the initial bzip2 workload.

The smoke-test source, script, and documentation were prepared with
ChatGPT assistance and executed and checked by a team member.

## Initial bzip2 performance experiment

Prerequisites: the dependencies listed in the ASan smoke-test section,
plus curl for downloading the upstream source:

```bash
sudo apt install -y curl
```

From the repository root, run:

```bash
bash scripts/run_experiment.sh
```

This downloads and verifies bzip2 1.0.8, builds baseline and ASan
variants, runs upstream tests, generates a deterministic 32 MiB input,
warms up both variants, and measures four runs per variant in
alternating order. Compression uses -9; timed output goes to /dev/null.

Allow a few minutes, excluding dependency installation and download.
Each measurement invocation creates a new results/bzip2-run-* directory.
It contains settings.txt, measurements.csv, stderr logs, and summary.md.
Summary tables report mean and sample standard deviation.

To collect additional diagnostic counters:

```bash
bash scripts/diagnose_bzip2.sh
python3 scripts/summarize_bzip2.py results/bzip2-diagnostic-*/measurements.csv
```

See docs/bzip2-experiment.md for methodology and limitations.
All batches, including unusually slow observations, are retained.
This workload is not SPEC CPU2006, and maximum RSS is not VmPeak.

Source archives, generated inputs and compiled binaries remain in
ignored third_party/ and build/ directories. The source download
retains the upstream LICENSE; no upstream source files are modified.
