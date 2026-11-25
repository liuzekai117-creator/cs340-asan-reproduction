# Verification of Table 2

Reviewer: Lin Xiyao (1240001933)
Report version: v1.0

I used AI-assisted Python commands to recalculate Table 2 from the four
archived measurements.csv files. Each batch contained four baseline runs
and four ASan runs. All 32 recorded exit codes were zero.

Elapsed times below are means and sample standard deviations in seconds.
Both ratios divide the ASan mean by the baseline mean. The memory ratio
uses max_rss_KiB.

| Batch | Baseline time (s) | ASan time (s) | Time ratio | Peak RSS ratio |
|---|---:|---:|---:|---:|
| First | 1.9975 ± 0.0222 | 3.9625 ± 1.4721 | 1.9837 | 1.9245 |
| Repeat | 1.9900 ± 0.0283 | 4.2950 ± 2.1701 | 2.1583 | 1.9460 |
| Diagnostic | 2.0000 ± 0.0216 | 3.2475 ± 0.0450 | 1.6238 | 1.9312 |
| End-to-end | 1.9900 ± 0.0082 | 3.2000 ± 0.0231 | 1.6080 | 1.9317 |

All four rows agree with Table 2 at the precision shown in the report.
This check verifies the published calculations using the archived runs.
