"""Thin ctypes wrappers for token elevation checks."""
from __future__ import annotations

import ctypes
import ctypes.wintypes as wt


def is_elevated() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def open_process_token(pid: int) -> int | None:
    TOKEN_ADJUST_PRIVILEGES = 0x0020
    TOKEN_QUERY = 0x0008
    handle = wt.HANDLE()
    ok = ctypes.windll.advapi32.OpenProcessToken(
        ctypes.windll.kernel32.OpenProcess(0x0400, False, pid),
        TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY,
        ctypes.byref(handle),
    )
    return handle.value if ok else None