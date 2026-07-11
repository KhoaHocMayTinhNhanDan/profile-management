from dataclasses import dataclass
from typing import List


@dataclass
class MigrateCleanCodeInput:
    project_root: str


@dataclass
class MigrateCleanCodeOutput:
    success: bool
    message: str
    changed_interfaces: List[str]
    changed_prints: List[str]
