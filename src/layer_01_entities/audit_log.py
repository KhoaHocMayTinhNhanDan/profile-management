class AuditLog:
    def __init__(self, log_id: str, user_id: str, action: str, timestamp: str, details: str):
        self.log_id = log_id
        self.user_id = user_id
        self.action = action
        self.timestamp = timestamp
        self.details = details

    def to_dict(self) -> dict:
        return {
            "log_id": self.log_id,
            "user_id": self.user_id,
            "action": self.action,
            "timestamp": self.timestamp,
            "details": self.details
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'AuditLog':
        return cls(
            log_id=data.get("log_id", ""),
            user_id=data.get("user_id", ""),
            action=data.get("action", ""),
            timestamp=data.get("timestamp", ""),
            details=data.get("details", "")
        )
