"""OpenProcess + ReadProcessMemory wrapper for trainer ingestion."""
from __future__ import annotations

import ctypes
import ctypes.wintypes as wt
import logging

from .process_scanner import ProcessScanner

log = logging.getLogger("hellraiser.ingest.reader")

PROCESS_ALL_ACCESS = 0x1F0FFF


class MemoryReader:
    def __init__(self, scanner: ProcessScanner, base: int) -> None:
        self.scanner = scanner
        self.base = base
        self.handle: int | None = None

    def _ensure_handle(self) -> int:
        if self.handle:
            return self.handle
        if not self.scanner.pid:
            raise RuntimeError("process not scanned — call scanner.scan() first")
        self.handle = ctypes.windll.kernel32.OpenProcess(
            PROCESS_ALL_ACCESS, False, self.scanner.pid
        )
        if not self.handle:
            raise OSError("OpenProcess failed for pid %s" % self.scanner.pid)
        return self.handle

    def read(self, offset: int, size: int) -> bytes:
        buf = ctypes.create_string_buffer(size)
        read = wt.SIZE_T(0)
        ok = ctypes.windll.kernel32.ReadProcessMemory(
            self._ensure_handle(),
            ctypes.c_void_p(self.base + offset),
            buf,
            size,
            ctypes.byref(read),
        )
        if not ok:
            raise OSError("ReadProcessMemory failed at 0x%X" % (self.base + offset))
        return buf.raw[: read.value]

    def snapshot(self) -> dict[str, int]:
        return {
            "health": int.from_bytes(self.read(0x2A10, 4), "little"),
            "pins": int.from_bytes(self.read(0x2A14, 4), "little"),
            "cenobite_hp": int.from_bytes(self.read(0x4C80, 4), "little"),
        }