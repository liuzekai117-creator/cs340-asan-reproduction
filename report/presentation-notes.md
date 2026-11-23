# AddressSanitizer overhead in bzip2 — speaking notes

These notes use the four tables and figure in the report. Adapt the timing
and speaker assignments to the course Presentation Instruction.

## What did we try to reproduce?

The original paper reports 73% average slowdown on SPEC CPU2006. We could
run the open-source bzip2 encoder on an input anyone can regenerate. Ask the
audience what a 73% increase would mean for a two-second run: about 3.46 s.
Our end-to-end batch measured 3.20 s from a 1.99 s baseline.

## How did we make the comparison fair?

Show the input digest and the two build commands. Both binaries used the same
source and optimization flags. Only the ASan binary enabled instrumentation.
Explain the warmup, alternating order, four timed repetitions and round-trip
check. The main test was on Ubuntu under WSL2.

## Why show individual runs?

Show Figure 1. Point to round two of the first and repeat batches: 6.17 s and
7.55 s. In the next two batches, the same round took 3.18 s and 3.22 s.
Means alone hide this difference. The diagnostic counters were collected
later, so we cannot assign a cause to the earlier delays.

## What does the memory result mean?

In the end-to-end batch, peak RSS rose by 7,173 KiB. Explain the distinction
with an untouched virtual mapping: reserving addresses can raise virtual
size without bringing the same number of pages into RAM. That is why the
paper's 2.12× VmPeak figure for 401.bzip2 and our 1.93× RSS are different
measurements.

## What did changing one factor teach us?

Show Table 4. On the extension host, switching from level 1 to level 9 raised
the baseline time by 0.202 s and the ASan time by 0.091 s. A smaller relative
overhead can accompany a longer absolute runtime. Compare the levels within
the Debian/GCC experiment.

## What would we test next?

Give the overall verdict, partially reproduced at reduced scale. A stronger
comparison would use the paper's workload and memory accounting method.
If an independent replay is completed, show its actual batch, environment
difference and review commit. Credit the person who performed it.
