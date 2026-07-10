from abc import ABC, abstractmethod

class AbstractInputs(ABC):
    @abstractmethod
    def get_template(self) -> str:
        pass
