"""HotkeyDriver — registers global hotkeys via win32 RegisterHotKey."""
from __future__ import annotations

import ctypes
import logging
import threading

from ..config import TrainerConfig
from ..utils.job_queue import JobQueue

log = logging.getLogger("hellraiser.drivers.hotkey")

MOD_NOREPEAT = 0x4000
VK_MAP = {
    "F1": 0x70, "F2": 0x71, "F3": 0x72, "F4": 0x73,
    "F5": 0x74, "F6": 0x75, "INSERT": 0x2D, "DELETE": 0x2E,
}


class HotkeyDriver:
    def __init__(self, config: TrainerConfig, queue: JobQueue) -> None:
        self.config = config
        self.queue = queue

    def listen(self) -> None:
        user32 = ctypes.windll.user32
        registered = {}
        for job_name, key in self.config.hotkeys.items():
            vk = VK_MAP.get(key.upper())
            if vk and user32.RegisterHotKey(None, hash(job_name) & 0xFFFF, MOD_NOREPEAT, vk):
                registered[hash(job_name) & 0xFFFF] = job_name
                log.info("hotkey %s -> %s", key, job_name)
        threading.Thread(target=self._pump, args=(registered,), daemon=True).start()

    def _pump(self, registered: dict[int, str]) -> None:
        msg = ctypes.wintypes.MSG() if hasattr(ctypes, "wintypes") else None
        import ctypes.wintypes as wt
        msg = wt.MSG()
        while ctypes.windll.user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
            if msg.message == 0x0312 and msg.wParam in registered:
                self.queue.dispatch(registered[msg.wParam])