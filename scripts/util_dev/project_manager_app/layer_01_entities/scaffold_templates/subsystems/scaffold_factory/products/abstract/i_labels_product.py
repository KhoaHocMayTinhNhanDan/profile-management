from abc import ABC, abstractmethod


class AbstractLabels(ABC):
    @abstractmethod
    def get_template(self) -> str:
        pass
