from abc import ABC, abstractmethod
from typing import Optional
from src.layer_01_entities.profile import Profile

class IGenerateDocumentFromTemplateRepository(ABC):
    @abstractmethod
    async def get_profile(self, profile_id: str) -> Optional[Profile]:
        pass

    @abstractmethod
    async def save_db(self, profile: Profile) -> None:
        pass

    @abstractmethod
    async def generate_document(self, template_doc_path: str, data: dict, output_path: str) -> str:
        pass
