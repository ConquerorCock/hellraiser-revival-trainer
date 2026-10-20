"""Dev utility: scan HellraiserRevival.exe for known cheat signature offsets."""
from __future__ import annotations

import sys

SIGNATURES = {
    "health_ptr": b"\x48\x8B\x05????\x48\x85\xC0",
    "pin_count": b"\x89\x05????\x83\xF8",
    "cenobite_hp": b"\x48\x8B\x0D????\x8B\x01\x89\x02",
}


def scan(buf: bytes, sig: bytes) -> list[int]:
    hits = []
    start = 0
    while True:
        idx = buf.find(sig.replace(b"?", b"\x00")[:4], start)
        if idx == -1:
            return hits
        hits.append(idx)
        start = idx + 1


def main(path: str) -> int:
    with open(path, "rb") as fh:
        buf = fh.read()
    for name, sig in SIGNATURES.items():
        hits = scan(buf, sig)
        print(f"{name}: {len(hits)} candidate(s)")
        for h in hits[:5]:
            print(f"  0x{h:08X}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: scan_offsets.py <HellraiserRevival.exe>")
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))