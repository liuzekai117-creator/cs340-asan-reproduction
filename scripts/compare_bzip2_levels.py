"""Compare bzip2 -1 and -9 on the existing baseline and ASan builds."""
import argparse
import csv
import hashlib
import os
from pathlib import Path
import platform
import statistics
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "build/input-32MiB.bin"
LEVELS = ((1, "baseline"), (1, "asan"), (9, "baseline"), (9, "asan"))
# Balanced four-period crossover: each configuration appears in each slot once.
ORDER = ((0, 1, 3, 2), (1, 2, 0, 3), (2, 3, 1, 0), (3, 0, 2, 1))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(out):
    out.mkdir(parents=True, exist_ok=False)
    binaries = {v: ROOT / f"build/bzip2-{v}/bzip2" for _, v in LEVELS}
    settings = [
        platform.platform(), platform.python_version(),
        subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        f"input: {INPUT.stat().st_size} bytes, sha256={sha256(INPUT)}",
        *[f"{v} sha256={sha256(p)}" for v, p in binaries.items()],
        *[f"{k}={os.environ.get(k, '<unset>')}" for k in ("ASAN_OPTIONS", "LSAN_OPTIONS")],
    ]
    (out / "settings.txt").write_text("\n".join(settings) + "\n")
    samples = {cfg: [] for cfg in LEVELS}
    for round_id, order in enumerate((range(4), *ORDER)):
        for slot, i in enumerate(order, 1):
            level, variant = LEVELS[i]
            cmd = [str(binaries[variant]), f"-{level}", "-c", str(INPUT)]
            start = time.perf_counter_ns()
            subprocess.run(cmd, stdout=subprocess.DEVNULL, check=True)
            seconds = (time.perf_counter_ns() - start) / 1e9
            if round_id:
                samples[LEVELS[i]].append(seconds)
            with (out / "runs.csv").open("a", newline="") as f:
                writer = csv.writer(f)
                if f.tell() == 0:
                    writer.writerow(["round_0_is_warmup", "slot", "level", "variant", "elapsed_s"])
                writer.writerow([round_id, slot, level, variant, seconds])
    with (out / "summary.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["level", "variant", "n", "mean_s", "sample_sd_s", "ratio_to_baseline"])
        for (level, variant), values in samples.items():
            avg = statistics.mean(values)
            writer.writerow([level, variant, len(values), avg, statistics.stdev(values),
                             avg / statistics.mean(samples[level, "baseline"])])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="new directory for this batch")
    run(parser.parse_args().output)
