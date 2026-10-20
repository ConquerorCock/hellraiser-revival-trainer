"""OverlayDriver — external WPF-less overlay via tkinter for trainer HUD."""
from __future__ import annotations

import logging
import threading
import tkinter as tk

from ..config import TrainerConfig
from ..utils.job_queue import JobQueue

log = logging.getLogger("hellraiser.drivers.overlay")


class OverlayDriver:
    def __init__(self, config: TrainerConfig, queue: JobQueue) -> None:
        self.config = config
        self.queue = queue
        self._thread: threading.Thread | None = None

    def _render(self) -> None:
        root = tk.Tk()
        root.overrideredirect(True)
        root.attributes("-topmost", True, "-alpha", 0.85)
        root.configure(bg="#0b0000")
        root.geometry("+20+20")
        label = tk.Label(
            root,
            text="HELLRAISER :: REVIVAL TRAINER\nF1 godmode  F2 pins  F3 esp  F4 puzzle",
            fg="#c02020",
            bg="#0b0000",
            font=("Consolas", 10, "bold"),
        )
        label.pack(padx=12, pady=10)
        root.after(200, self._refresh, root, label)
        root.mainloop()

    def _refresh(self, root: tk.Tk, label: tk.Label) -> None:
        state = self.queue.last_state()
        if state:
            text = (
                f"HELLRAISER :: REVIVAL TRAINER\n"
                f"HP {state.get('health', 0)}  PINS {state.get('pins', 0)}  "
                f"CENO {state.get('cenobite_hp', 0)}"
            )
            label.config(text=text)
        root.after(200, self._refresh, root, label)

    def attach(self) -> None:
        if not self.config.overlay_enabled:
            return
        self._thread = threading.Thread(target=self._render, daemon=True)
        self._thread.start()