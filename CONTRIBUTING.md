# Contributing to hellraiser-revival-trainer

Thanks for helping keep the Revival trainer alive. This project is a
community-built external trainer for **Clive Barker's Hellraiser: Revival**
(2026). It does not modify game files — it reads and patches process memory
at runtime, exactly like Cheat Engine tables you may already be used to.

## Ground rules

- Keep PRs scoped to a single cheat, driver, or processor.
- Every new memory offset must include a `scripts/scan_offsets.py` signature.
- New cheats go in `src/hellraiser_trainer/processors/cheat_engine.py` under
  the `PATCHES` dict and must be hotkey-bindable via `TrainerConfig.hotkeys`.
- Do not commit game binaries, dumps, or offsets for builds you do not own.

## Local dev

```
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
pytest -q
python -m hellraiser_trainer.cli --dry-run
```

## Reporting offset breakage

When a game patch invalidates offsets:
1. Run `python scripts/scan_offsets.py "C:\...\HellraiserRevival.exe"`.
2. Post the candidate RVA list in an issue tagged `offsets:broken`.
3. Include your game build number from the main menu.

## For educational use

This repo exists for reverse-engineering practice and single-player modding.
Do not use it in multiplayer sessions.