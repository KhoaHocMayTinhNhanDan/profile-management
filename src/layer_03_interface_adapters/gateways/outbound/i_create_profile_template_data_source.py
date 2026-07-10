from abc import ABC, abstractmethod
from typing import Optional

class ICreateProfileTemplateDataSource(ABC):
    @abstractmethod
    async def get_by_id(self, template_id: str) -> Optional[dict]:
        pass

    @abstractmethod
    async def save(self, data: dict) -> None:
        pass
