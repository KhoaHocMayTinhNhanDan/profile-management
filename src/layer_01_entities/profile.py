from typing import List, Dict, Any, Optional
from .document import Document


class Profile:
    def __init__(
        self,
        profile_id: str,
        template_id: str,
        status: str,
        dynamic_data: Dict[str, Any],
        documents: Optional[List[Document]] = None,
        created_at: Optional[str] = None,
    ):
        self.profile_id = profile_id
        self.template_id = template_id
        self.status = status  # Draft, Pending, Approved
        self.dynamic_data = dynamic_data
        self.documents = documents if documents is not None else []
        self.created_at = created_at

    def to_dict(self) -> dict:
        return {
            "profile_id": self.profile_id,
            "template_id": self.template_id,
            "status": self.status,
            "dynamic_data": self.dynamic_data,
            "documents": [doc.to_dict() for doc in self.documents],
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Profile":
        raw_docs = data.get("documents", [])
        documents = [
            Document.from_dict(d) if isinstance(d, dict) else d for d in raw_docs
        ]
        return cls(
            profile_id=data.get("profile_id", ""),
            template_id=data.get("template_id", ""),
            status=data.get("status", "Draft"),
            dynamic_data=data.get("dynamic_data", {}),
            documents=documents,
            created_at=data.get("created_at", None),
        )
