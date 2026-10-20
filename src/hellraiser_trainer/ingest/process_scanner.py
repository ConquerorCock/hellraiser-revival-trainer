"""Locate HellraiserRevival.exe and resolve its base module address."""
from __future__ import annotations

import ctypes
import ctypes.wintypes as wt
import logging

log = logging.getLogger("hellraiser.ingest.scanner")

TH32CS_SNAPPROCESS = 0x00000002


class PROCESSENTRY32W(ctypes.Structure):
    _fields_ = [
        ("dwSize", wt.DWORD),
        ("cntUsage", wt.DWORD),
        ("th32ProcessID", wt.DWORD),
        ("th32DefaultHeapID", ctypes.c_void_p),
        ("th32ModuleID", wt.DWORD),
        ("cntThreads", wt.DWORD),
        ("th32ParentProcessID", wt.DWORD),
        ("pcPriClassBase", ctypes.c_long),
        ("dwFlags", wt.DWORD),
        ("szExeFile", wt.WCHAR * 260),
    ]


class ProcessScanner:
    def __init__(self, target: str) -> None:
        self.target = target
        self.pid: int | None = None

    def scan(self) -> int | None:
        k32 = ctypes.windll.kernel32
        snap = k32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
        entry = PROCESSENTRY32W()
        entry.dwSize = ctypes.sizeof(PROCESSENTRY32W)
        try:
            if not k32.Process32FirstW(snap, ctypes.byref(entry)):
                return None
            while True:
                if entry.szExeFile.lower() == self.target.lower():
                    self.pid = entry.th32ProcessID
                    log.info("found %s pid=%d", self.target, self.pid)
                    return self.pid
                if not k32.Process32NextW(snap, ctypes.byref(entry)):
                    return None
        finally:
            k32.CloseHandle(snap)