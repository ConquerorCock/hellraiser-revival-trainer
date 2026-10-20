"""StateTracker — polls live state at tick_hz for the overlay driver."""
from __future__ import annotations

import logging
import time

from .cheat_engine import CheatEngine

log = logging.getLogger("hellraiser.processors.tracker")


class StateTracker:
    def __init__(self, engine: CheatEngine, tick_hz: int = 60) -> None:
        self.engine = engine
        self.interval = 1.0 / tick_hz
        self.last: dict[str, int] = {}

    def update(self) -> dict[str, int]:
        start = time.perf_counter()
        try:
            self.last = self.engine.reader.snapshot()
        except OSError as exc:
            log.debug("snapshot failed: %s", exc)
        elapsed = time.perf_counter() - start
        if elapsed < self.interval:
            time.sleep(self.interval - elapsed)
        return self.last