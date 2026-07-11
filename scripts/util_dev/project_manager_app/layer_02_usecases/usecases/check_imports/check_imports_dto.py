from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class CheckImportsInput:
    project_root_dir: str


@dataclass
class CheckImportsOutput:
    status: str
    message: str
    violations: Optional[List[Tuple[str, int, int]]] = None
