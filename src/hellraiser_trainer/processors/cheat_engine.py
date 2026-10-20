"""CheatEngine — applies memory patches for each enabled Hellraiser cheat."""
from __future__ import annotations

import ctypes
import ctypes.wintypes as wt
import logging

from ..config import TrainerConfig
from ..ingest.memory_reader import MemoryReader

log = logging.getLogger("hellraiser.processors.cheat")

# Offsets resolved for HellraiserRevival.exe build 1.4.2 (2026-01)
PATCHES = {
    "godmode": (0x2A10, b"\x00\x00\x00\x00"),
    "infinite_pins": (0x2A14, b"\x63\x00\x00\x00"),
    "one_hit_cenobite": (0x4C80, b"\x00\x00\x00\x00"),
}


class CheatEngine:
    def __init__(self, reader: MemoryReader, config: TrainerConfig) -> None:
        self.reader = reader
        self.config = config

    def _write(self, offset: int, data: bytes) -> bool:
        written = wt.SIZE_T(0)
        return bool(
            ctypes.windll.kernel32.WriteProcessMemory(
                self.reader.handle,
                ctypes.c_void_p(self.reader.base + offset),
                data,
                len(data),
                ctypes.byref(written),
            )
        )

    def apply_patch(self, name: str) -> bool:
        if name not in PATCHES:
            log.warning("unknown cheat: %s", name)
            return False
        offset, payload = PATCHES[name]
        ok = self._write(offset, payload)
        log.info("patch %s applied=%s", name, ok)
        return ok

    def apply_all_enabled(self) -> dict[str, bool]:
        results = {}
        for name, enabled in self.config.cheats.items():
            if enabled and name in PATCHES:
                results[name] = self.apply_patch(name)
        return results