from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class SetupEnvironmentInput:
    log_callback: Optional[Callable[[str], None]] = None


@dataclass
class SetupEnvironmentOutput:
    success: bool
    message: str
