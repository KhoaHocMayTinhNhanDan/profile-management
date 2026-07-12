from dataclasses import dataclass


@dataclass
class CheckinDocumentInput:
    profile_id: str
    document_id: str
    user_id: str
    new_url: str
    new_size: int
    new_checksum: str


@dataclass
class CheckinDocumentOutput:
    status: str
    message: str
    new_version: str = ""
