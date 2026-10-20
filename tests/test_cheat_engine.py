from unittest.mock import MagicMock

from hellraiser_trainer.config import TrainerConfig
from hellraiser_trainer.processors.cheat_engine import CheatEngine, PATCHES


def test_apply_known_cheat_calls_write():
    reader = MagicMock()
    reader.base = 0x1000
    reader.handle = 1
    engine = CheatEngine(reader, TrainerConfig())
    engine._write = MagicMock(return_value=True)

    ok = engine.apply_patch("godmode")
    assert ok is True
    offset, payload = PATCHES["godmode"]
    engine._write.assert_called_once_with(offset, payload)


def test_unknown_cheat_returns_false():
    engine = CheatEngine(MagicMock(), TrainerConfig())
    assert engine.apply_patch("summon_pinhead") is False