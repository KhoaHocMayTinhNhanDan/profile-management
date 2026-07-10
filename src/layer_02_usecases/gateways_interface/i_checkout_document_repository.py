from abc import ABC, abstractmethod
from typing import Optional
from src.layer_01_entities.profile import Profile

class ICheckoutDocumentRepository(ABC):
    @abstractmethod
    async def get_profile(self, profile_id: str) -> Optional[Profile]:
        pass

    @abstractmethod
    async def save_db(self, profile: Profile) -> None:
        pass
