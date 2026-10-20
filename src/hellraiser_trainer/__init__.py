"""Clive Barker's Hellraiser: Revival Trainer — memory pipeline core."""

__version__ = "0.9.3"
__author__ = "revival-trainer contributors"

from .bootstrap import TrainerBootstrap
from .config import TrainerConfig

__all__ = ["TrainerBootstrap", "TrainerConfig", "__version__"]