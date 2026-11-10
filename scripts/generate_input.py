#!/usr/bin/env python3
"""Generate a deterministic 32 MiB synthetic benchmark input."""
import hashlib
from pathlib import Path

root = Path(__file__).resolve().parents[1]
target = root / "build" / "input-32MiB.bin"
target.parent.mkdir(parents=True, exist_ok=True)
digest = hashlib.sha256()

with target.open("wb") as output:
    for i in range(512):
        seed = b"cs340-bzip2-input-v1:" + str(i).encode("ascii")
        block = hashlib.shake_256(seed).digest(65536)
        output.write(block)
        digest.update(block)

metadata = (
    "Generator: SHAKE-256, cs340-bzip2-input-v1\n"
    f"Size_bytes: {target.stat().st_size}\n"
    f"SHA256: {digest.hexdigest()}\n"
)
(root / "results").mkdir(exist_ok=True)
(root / "results" / "bzip2-input.txt").write_text(metadata)
print(metadata, end="")
