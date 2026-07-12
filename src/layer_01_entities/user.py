class User:
    def __init__(self, user_id: str, email: str, display_name: str, role: str):
        self.user_id = user_id
        self.email = email
        self.display_name = display_name
        self.role = role  # admin, staff, viewer

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "email": self.email,
            "display_name": self.display_name,
            "role": self.role,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(
            user_id=data.get("user_id", ""),
            email=data.get("email", ""),
            display_name=data.get("display_name", ""),
            role=data.get("role", "viewer"),
        )
