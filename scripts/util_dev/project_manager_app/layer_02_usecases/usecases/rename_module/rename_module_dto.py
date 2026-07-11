from dataclasses import dataclass


@dataclass
class RenameModuleInput:
    target_path: str
    new_name: str


@dataclass
class RenameModuleOutput:
    success: bool
    message: str
