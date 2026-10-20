"""Command-line entry: python -m hellraiser_trainer.cli [--cheat NAME]"""
from __future__ import annotations

import argparse
import logging
import sys

from .bootstrap import TrainerBootstrap
from .utils.winapi import is_elevated

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(message)s")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="hellraiser-trainer")
    parser.add_argument("--cheat", action="append", default=[],
                        help="cheat to enable at launch (repeatable)")
    parser.add_argument("--no-overlay", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    if not is_elevated() and not args.dry_run:
        print("warning: not running elevated; WriteProcessMemory will fail", file=sys.stderr)

    boot = TrainerBootstrap()
    boot.config.overlay_enabled = not args.no_overlay
    for name in args.cheat:
        boot.config.cheats[name] = True

    if args.dry_run:
        print("dry-run config:", boot.config)
        return 0

    boot.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())