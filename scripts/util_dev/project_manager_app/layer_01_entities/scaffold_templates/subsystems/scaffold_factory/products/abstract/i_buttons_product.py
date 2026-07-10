from abc import ABC, abstractmethod

class AbstractButtons(ABC):
    @abstractmethod
    def get_template(self) -> str:
        pass
