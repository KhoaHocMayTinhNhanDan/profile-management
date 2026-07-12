from abc import ABC, abstractmethod
from src.layer_01_entities.profile_template import ProfileTemplate
from typing import Optional


class ICreateProfileTemplateRepository(ABC):
    @abstractmethod
    async def get_by_id(self, template_id: str) -> Optional[ProfileTemplate]:
        pass

    @abstractmethod
    async def save_db(self, template: ProfileTemplate) -> None:
        pass
