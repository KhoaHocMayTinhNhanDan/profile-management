from abc import ABC, abstractmethod
from typing import Optional

class IGenerateDocumentFromTemplateDataSource(ABC):
    @abstractmethod
    async def get_profile(self, profile_id: str) -> Optional[dict]:
        pass

    @abstractmethod
    async def save(self, data: dict) -> None:
        pass

    @abstractmethod
    async def generate_docx(self, template_doc_path: str, data: dict, output_path: str) -> str:
        """
        Loads the template docx, replaces placeholders with data, and saves to output_path.
        Returns the path/url of the generated file.
        """
        pass
