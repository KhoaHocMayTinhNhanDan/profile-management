from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class UpdateProfileInput:
    profile_id: str
    dynamic_data: Dict[str, Any]
    status: Optional[str] = None  # Optional status update (Draft, Pending, Approved)


@dataclass
class UpdateProfileOutput:
    status: str
    message: str
    errors: List[str] = field(default_factory=list)
