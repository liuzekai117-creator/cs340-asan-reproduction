# Independent replay for the release review

Proposed reviewer: Lin Xiyao. This page describes an open task. Add the
reviewer's name, findings and commit only after the reviewer performs the work.

1. Clone the delivery revision in a fresh Ubuntu environment. Record the commit
   with `git rev-parse HEAD`. Follow only the README for dependency installation
   and the main experiment. Note any step that requires outside information.
2. Run `bash scripts/check_recorded_env.sh` and save its output. Differences
   are useful evidence. Record which differences could affect the comparison.
3. Capture the new batch path, input SHA-256 and upstream test results. From
   its measurements.csv, independently compute mean elapsed time for each
   executable and divide the ASan mean by the baseline mean. Compare with
   the historical end-to-end ratio of 1.608 and discuss any difference.
4. Write a short validation note with the commands, environment, raw rows or
   link to them, outcome, and one interpretation. If a step fails, record
   the failing command and diagnose it. Include any verified documentation fix.
5. Review the intended files and open a pull request from your own account.
   Include your student ID and full name in the commit message. Link the
   reviewed commit from the report contribution statement before release.
