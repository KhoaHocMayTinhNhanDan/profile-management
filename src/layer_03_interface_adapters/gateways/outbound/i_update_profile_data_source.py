from abc import ABC, abstractmethod
from typing import Optional


class IUpdateProfileDataSource(ABC):
    @abstractmethod
    async def get_template(self, template_id: str) -> Optional[dict]:
        pass

    @abstractmethod
    async def get_profile(self, profile_id: str) -> Optional[dict]:
        pass

    @abstractmethod
    async def save(self, data: dict) -> None:
        pass
