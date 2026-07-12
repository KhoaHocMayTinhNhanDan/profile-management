from dataclasses import dataclass
from typing import Optional


@dataclass
class CheckoutDocumentInput:
    profile_id: str
    document_id: str
    user_id: str


@dataclass
class CheckoutDocumentOutput:
    status: str
    message: str
    document_url: Optional[str] = None
    local_filename: Optional[str] = None
