from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class CreateProfileInput:
    profile_id: str
    template_id: str
    dynamic_data: Dict[str, Any]
    documents: List[dict] = field(default_factory=list)


@dataclass
class CreateProfileOutput:
    status: str
    message: str
    errors: List[str] = field(default_factory=list)
