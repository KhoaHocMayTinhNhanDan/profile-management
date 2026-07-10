from abc import ABC, abstractmethod
from typing import Optional
from src.layer_01_entities.profile import Profile
from src.layer_01_entities.profile_template import ProfileTemplate

class IUpdateProfileRepository(ABC):
    @abstractmethod
    async def get_template(self, template_id: str) -> Optional[ProfileTemplate]:
        pass

    @abstractmethod
    async def get_profile(self, profile_id: str) -> Optional[Profile]:
        pass

    @abstractmethod
    async def save_db(self, profile: Profile) -> None:
        pass
