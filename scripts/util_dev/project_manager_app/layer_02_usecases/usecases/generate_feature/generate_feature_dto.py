from dataclasses import dataclass
from typing import List


@dataclass
class GenerateFeatureInput:
    feature_name: str
    platforms: List[str]
    db_techs: List[str]
    project_root_dir: str
    project_name: str


@dataclass
class GenerateFeatureOutput:
    status: str
    message: str
