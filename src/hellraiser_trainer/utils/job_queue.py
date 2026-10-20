"""JobQueue — pipeline worker that fans ingest jobs into processors."""
from __future__ import annotations

import logging
import queue
import threading
from typing import Callable

log = logging.getLogger("hellraiser.utils.queue")


class JobQueue:
    def __init__(self, maxsize: int = 256) -> None:
        self.maxsize = maxsize
        self._jobs: dict[str, Callable[[], object]] = {}
        self._q: queue.Queue[str] = queue.Queue(maxsize=maxsize)
        self._state: dict[str, int] = {}
        self._lock = threading.Lock()

    def register(self, name: str, fn: Callable[[], object]) -> None:
        self._jobs[name] = fn

    def dispatch(self, name: str) -> None:
        if name not in self._jobs:
            log.warning("no job registered for %s", name)
            return
        try:
            self._q.put_nowait(name)
        except queue.Full:
            log.warning("queue full, dropping %s", name)

    def last_state(self) -> dict[str, int]:
        with self._lock:
            return dict(self._state)

    def drain(self) -> None:
        while True:
            try:
                name = self._q.get(timeout=0.5)
            except queue.Empty:
                continue
            try:
                result = self._jobs[name]()
                if isinstance(result, dict):
                    with self._lock:
                        self._state.update(result)
            except Exception as exc:  # noqa: BLE001
                log.exception("job %s failed: %s", name, exc)