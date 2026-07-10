class Document:
    def __init__(
        self,
        document_id: str,
        name: str,
        url: str,
        file_type: str,
        size: int,
        version: str = "1.0",
        is_locked: bool = False,
        locked_by: str = "",
        checksum: str = ""
    ):
        self.document_id = document_id
        self.name = name
        self.url = url
        self.file_type = file_type
        self.size = size
        self.version = version
        self.is_locked = is_locked
        self.locked_by = locked_by
        self.checksum = checksum

    def to_dict(self) -> dict:
        return {
            "document_id": self.document_id,
            "name": self.name,
            "url": self.url,
            "file_type": self.file_type,
            "size": self.size,
            "version": self.version,
            "is_locked": self.is_locked,
            "locked_by": self.locked_by,
            "checksum": self.checksum
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Document':
        return cls(
            document_id=data.get("document_id", ""),
            name=data.get("name", ""),
            url=data.get("url", ""),
            file_type=data.get("file_type", ""),
            size=data.get("size", 0),
            version=data.get("version", "1.0"),
            is_locked=data.get("is_locked", False),
            locked_by=data.get("locked_by", ""),
            checksum=data.get("checksum", "")
        )
