# Experimental differences

| Factor | Published experiment (section 4) | This project | Reason and consequence |
|---|---|---|---|
| Programs and input | SPEC CPU2006 C/C++ suite with reference workloads | Unmodified standalone bzip2 1.0.8, 32 MiB deterministic SHAKE-256 input, compression at level 9 | The licensed suite was unavailable. One encoder input cannot establish a suite mean. |
| Processor and OS | 64-bit Linux on an HP Z600, two Xeon E5620 processors, 24 GB RAM | Ubuntu 24.04.5 on WSL2, Core i7-14700KF, 28 visible CPUs and about 15 GiB guest RAM | Available host. No CPU pinning or governor control. |
| Compiler and instrumentation | Contemporary LLVM/Clang, baseline -O2, 32-byte redzones, allocation stack unwinding disabled, quarantine zero | Clang 18.1.3, both builds -O2 -g with frame pointers, ASan options unset | Maintained runtime and shipped defaults. The cost of each difference was not isolated. |
| Time and repetition | Suite slowdown in Figure 2 | GNU time, four timed runs per variant after warmup, alternating order, compressed output discarded | Exposes run-level variability and limits output I/O. |
| Memory | Table 1 reports VmPeak at termination | GNU time maximum resident set size in KiB | External observation preserves the upstream source. Untouched virtual mappings need not occupy RAM. |
| Extension | Outside the published experiment | Levels 1 and 9 on one Debian 13 host, GCC 14.2, leak detection disabled, four runs per cell | Hosted tracing interfered with LeakSanitizer. Compare levels within this host only. |

[Paper](https://www.usenix.org/system/files/conference/atc12/atc12-final39.pdf) ·
[WSL environment](../results/environment.txt) ·
[Extension settings](../results/extension-levels/batch-01/settings.txt)
