from dataclasses import dataclass
from typing import List


@dataclass
class GenerateFeatureInput:
    feature_name: str
    platforms: List[str]
    db_techs: List[str]
    project_root_dir: str
    project_name: str
    group_name: str = ""
    color_palette: str = "Catppuccin_Mocha"
    theme: str = "default_theme"


@dataclass
class GenerateFeatureOutput:
    status: str
    message: str
