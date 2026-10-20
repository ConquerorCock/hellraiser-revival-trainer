"""Config loader — reads trainer.toml from %APPDATA%/HellraiserRevival."""
from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path


CONFIG_DIR = Path(os.getenv("APPDATA", "~")).expanduser() / "HellraiserRevival"
DEFAULT_PATH = CONFIG_DIR / "trainer.toml"


@dataclass
class TrainerConfig:
    process_name: str = "HellraiserRevival.exe"
    module_base: int = 0x7FF6A0000000
    tick_hz: int = 60
    queue_size: int = 256
    overlay_enabled: bool = True
    overlay_theme: str = "lemarchand"
    hotkeys: dict[str, str] = field(default_factory=lambda: {
        "toggle_godmode": "F1",
        "toggle_infinite_pins": "F2",
        "toggle_esp_puzzle": "F3",
        "spawn_puzzle_box": "F4",
    })
    cheats: dict[str, bool] = field(default_factory=lambda: {
        "godmode": False,
        "infinite_pins": False,
        "esp_puzzle": False,
        "one_hit_cenobite": False,
    })

    @classmethod
    def load(cls, path: Path = DEFAULT_PATH) -> "TrainerConfig":
        if not path.exists():
            return cls()
        with path.open("rb") as fh:
            data = tomllib.load(fh)
        cfg = cls()
        for key, val in data.items():
            if hasattr(cfg, key):
                setattr(cfg, key, val)
        return cfg