# CS340 Reproduction: AddressSanitizer (USENIX ATC'12)

Reproduction of *AddressSanitizer: A Fast Address Sanity Checker*
(Serebryany, Bruening, Potapenko, Vyukov; USENIX ATC 2012) for CS340
Operating Systems, Academic Year 2026-2027.

Paper: https://www.usenix.org/system/files/conference/atc12/atc12-final39.pdf

## Report and evidence

See the [independent replay task](docs/independent-replay.md) for the proposed release check.
Read the [English report (PDF)](report/CS340-ASan-report.pdf) or its
[editable Word document](report/CS340-ASan-report.docx). The report compares elapsed
time and peak resident memory, explains two unusually slow observations,
and tests whether changing the compression level affects ASan overhead.

## Claims under test

| ID | Paper result | Local test |
|---|---|---|
| C1 | Figure 2, 1.73× average elapsed time on SPEC CPU2006 | Four batches of standalone bzip2 compression |
| C2 | Table 1, 3.37× suite memory overhead, 2.12× for 401.bzip2, measured using VmPeak | GNU time peak RSS on standalone bzip2 |

## Results at a glance

Four bzip2 1.0.8 batches on a 32 MiB deterministic input, four measured runs
per variant in alternating order. Every observation is retained, including
the ones that remain unexplained.

| Batch | Baseline elapsed (s) | ASan elapsed (s) | Runtime ratio | Peak RSS ratio |
|---|---:|---:|---:|---:|
| bzip2-run-jGdCjfol | 1.9900 +/- 0.0082 | 3.2000 +/- 0.0231 | 1.61x | 1.93x |
| bzip2-diagnostic-MDul3KA8 | 2.0000 +/- 0.0216 | 3.2475 +/- 0.0450 | 1.62x | 1.93x |
| bzip2-run-0lXaeOE4 | 1.9975 +/- 0.0222 | 3.9625 +/- 1.4721 | 1.98x | 1.92x |
| bzip2-run-NVdQw6zH | 1.9900 +/- 0.0283 | 4.2950 +/- 2.1701 | 2.16x | 1.95x |

Deviations are sample standard deviation over four runs.

Claim status:

- **C1, partially supported.** ASan increased elapsed time in all four
  batches. Ratios ranged from 1.61× to 2.16×. Two batches each had one
  slow ASan run (6.17 s and 7.55 s). Two follow-up batches did not show
  a similar delay. The cause and the suite-wide mean remain unresolved.
- **C2, inconclusive.** Peak RSS rose by a factor of 1.92–1.95. RSS counts
  resident pages, including resident shadow pages. The paper measured peak
  virtual address space, so its ratio cannot be validated by this metric.

A separate environment smoke test detected an intentional error. See
[experiment details](docs/bzip2-experiment.md) and [deviations](docs/deviations.md).

## Requirements

- Linux. This reproduction used Ubuntu 24.04 under WSL2.
- clang 18 or newer, with the AddressSanitizer runtime for that version.
- make, python3, GNU time, curl.

The scripts call `clang-18` when it is on PATH and otherwise fall back to
`clang`, so any 18-or-newer installation works without editing them. To pin
a different binary, set `CLANG`:

    CLANG=clang-19 bash scripts/run_experiment.sh

The ASan runtime package is versioned with the compiler. For clang 18 on
Ubuntu 24.04:

    sudo apt update
    sudo apt install -y clang-18 libclang-rt-18-dev llvm-18 \
      build-essential curl python3 time

## Quick start

    bash scripts/setup_env.sh        # record toolchain and hardware versions
    bash scripts/run_experiment.sh   # bzip2 baseline vs ASan, 4 runs per variant

## Team and contributions

| Member | Student ID | GitHub | Contribution |
|--------|------------|--------|--------------|
| Liu Zekai | 1240002302 | liuzekai117-creator | Repository layout and planning documents; ASan environment smoke test and environment recording; bzip2 baseline/ASan measurement pipeline, batch summaries, deviations log and compression-level extension (with AI assistance) |
| Lin Xiyao | 1240001933 | linxiyao111 | Added the team roster (adf4cb6), benchmarks and results directories (287cef8, 27258f3), and initial experiment-runner skeleton (f9fdcd7) |
| Liu Fangzhuo | 1240002384 | liufangzhuo272 | Raw-data plots, per-batch statistics and analysis of timing variability (PR #1) |

## Repository layout

| Path | Contents |
|------|----------|
| scripts/ | environment setup, benchmark download, experiment runner |
| results/ | measurement logs and aggregated tables |
| docs/ | environment, deviations, experiment notes |

## Environment

The measured configuration is recorded in [the environment log](results/environment.txt).
To check the same Ubuntu packages against an existing installation, run
`bash scripts/check_recorded_env.sh`. The check reports differences and
leaves the machine untouched. For a new measurement, keep any differences
alongside the results. See [environment notes](docs/environment.md).

The starting project commit is `089633c`. The original bzip2 sources are
unmodified. See [source version and digest](results/bzip2-source.txt) and
[upstream license](docs/licenses/bzip2-LICENSE). To list every project file
changed since the start, run `git diff --name-status 089633c HEAD`.

## Deviations from the paper

See docs/deviations.md. Every change from the paper setup is listed there with
the original setting, the setting used, and the reason.

## Provenance and assistance

The team ran the original Ubuntu/Clang benchmarks and published the logs
and analysis. ChatGPT/Codex assisted with scripts, troubleshooting, plotting,
statistics and report drafting. It also executed the compression-level
extension on the hosted Debian/GCC machine. The two hosts have separate
settings and logs. Individual roles are recorded above and in the report.

## Credits and license

- Paper: Serebryany et al., AddressSanitizer: A Fast Address Sanity Checker, USENIX ATC 2012.
- Implementation under test: LLVM/Clang AddressSanitizer (Apache-2.0 with LLVM exceptions).
- Benchmarks: downloaded by script and not redistributed in this repository.

## ASan environment smoke test

Verified on Ubuntu 24.04.5 under WSL2 with Clang 18.1.3.
See results/environment.txt for the recorded environment.

Run from the repository root:

    bash scripts/check_asan.sh

Expected output:

```text
PASS: ASan detected the intentional heap-use-after-free.
Log: results/asan_check.log
```

The script compiles tests/asan_check.c and verifies that ASan reports the
intentional heap-use-after-free with a nonzero exit status. The full
diagnostic is saved to results/asan_check.log.

This is an environment smoke test, not a performance benchmark or evidence
that the paper's quantitative claims have been reproduced. Assistance
disclosure is in Provenance and assistance.

## Initial bzip2 performance experiment

From the repository root:

    bash scripts/run_experiment.sh

This downloads and verifies bzip2 1.0.8, builds baseline and ASan variants,
runs upstream tests, generates a deterministic 32 MiB input, warms up both
variants, and measures four runs per variant in alternating order. Compression
uses -9; timed output goes to /dev/null.

Allow a few minutes, excluding dependency installation and download. Each
measurement invocation creates a new results/bzip2-run-* directory holding
settings.txt, measurements.csv, stderr logs and summary.md.

The runner summarizes only the batch it just produced, whose path it reads
from results/.last-batch. To re-summarize several batches:

    python3 scripts/summarize_bzip2.py results/bzip2-run-*/measurements.csv

To collect additional diagnostic counters:

    bash scripts/diagnose_bzip2.sh
    python3 scripts/summarize_bzip2.py results/bzip2-diagnostic-*/measurements.csv

See docs/bzip2-experiment.md for methodology and limitations. All batches,
including unusually slow observations, are retained. This workload is not
SPEC CPU2006, and maximum RSS is not VmPeak.

Source archives, generated inputs and compiled binaries remain in ignored
third_party/ and build/ directories. The source download retains the upstream
LICENSE; no upstream source files are modified.

## Extension: bzip2 compression level

[Experiment and reproduction instructions](docs/bzip2-level-extension.md)
compare ASan runtime overhead at levels 1 and 9 on the same input.
The extension uses its own host and toolchain. Its raw timings, build logs
and summary are stored under `results/extension-levels/`.
