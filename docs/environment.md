# Recorded experiment environment

- CPU model: Intel Core i7-14700KF.
- WSL-visible logical CPUs: 28.
- WSL-visible memory: approximately 15 GiB.
- Guest OS: Ubuntu 24.04.5 LTS.
- Kernel: 6.18.58.1-microsoft-standard-WSL2.
- Compiler: Ubuntu Clang 18.1.3.
- glibc: 2.39.

Full package versions and hardware output are in results/environment.txt.
Additional environment snapshots are stored as results/env-*.txt.
Exact Windows edition and version remain to be verified.

Experiments are not CPU-pinned. No performance-governor setting was
applied by the experiment scripts. The virtual CPU topology reported
inside WSL does not establish the mapping to physical P-cores/E-cores.

WSL mirrored networking was enabled for access to the Windows proxy.
The proxy is used for downloads and Git access, not the local
compression workload.

Versions are recorded; a fully pinned installation environment has
not yet been implemented.
