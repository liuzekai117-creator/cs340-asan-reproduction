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

Week 1: repository setup, environment pinning, benchmark selection.

## Requirements

- Linux (Ubuntu 24.04 under WSL2 is used for this reproduction)
- clang >= 18, make, cmake, python3

## Quick start

    bash scripts/setup_env.sh        # record toolchain and hardware versions
    bash scripts/run_experiment.sh   # baseline vs ASan, 3 repetitions

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

| Name | Student ID | GitHub |
|------|------------|--------|
| Liu Zekai | 1240002302 | TBD |