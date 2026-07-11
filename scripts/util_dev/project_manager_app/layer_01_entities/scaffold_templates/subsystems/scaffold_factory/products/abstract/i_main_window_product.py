from abc import ABC, abstractmethod


class AbstractMainWindow(ABC):
    @abstractmethod
    def get_template(self) -> str:
        pass
