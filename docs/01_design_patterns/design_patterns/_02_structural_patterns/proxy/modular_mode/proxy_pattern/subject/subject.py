# =========================================================
# File:
# proxy/modular_mode/proxy_pattern/subject/subject.py
# =========================================================

from abc import (
    ABC,
    abstractmethod,
)


class Subject(ABC):
    """
    Role: Subject
    Description: Core participant in the Proxy Pattern structure.
    """

    @abstractmethod
    def request(self) -> str:
        pass