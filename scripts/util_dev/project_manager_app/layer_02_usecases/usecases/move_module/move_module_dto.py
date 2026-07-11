from dataclasses import dataclass


@dataclass
class MoveModuleInput:
    source_path: str
    destination_dir: str


@dataclass
class MoveModuleOutput:
    success: bool
    message: str
