"""Entry bootstrap: wires ingest -> processor -> driver pipeline."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional

from .config import TrainerConfig
from .ingest.process_scanner import ProcessScanner
from .ingest.memory_reader import MemoryReader
from .processors.cheat_engine import CheatEngine
from .processors.state_tracker import StateTracker
from .drivers.overlay_driver import OverlayDriver
from .drivers.hotkey_driver import HotkeyDriver
from .utils.job_queue import JobQueue

log = logging.getLogger("hellraiser.bootstrap")


@dataclass
class TrainerBootstrap:
    config: Optional[TrainerConfig] = None

    def __post_init__(self) -> None:
        self.config = self.config or TrainerConfig.load()
        self.queue = JobQueue(maxsize=self.config.queue_size)

    def build_pipeline(self) -> None:
        scanner = ProcessScanner(target=self.config.process_name)
        reader = MemoryReader(scanner, base=self.config.module_base)
        engine = CheatEngine(reader, config=self.config)
        tracker = StateTracker(engine, tick_hz=self.config.tick_hz)

        self.queue.register("scan", scanner.scan)
        self.queue.register("read", reader.snapshot)
        self.queue.register("apply", engine.apply_patch)
        self.queue.register("track", tracker.update)

        log.info("pipeline built for %s (pid=%s)", self.config.process_name, scanner.pid)

    def run(self) -> None:
        self.build_pipeline()
        OverlayDriver(self.config, self.queue).attach()
        HotkeyDriver(self.config, self.queue).listen()
        self.queue.drain()