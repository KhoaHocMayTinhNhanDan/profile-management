from abc import ABC, abstractmethod

class IFileDataSource(ABC):
    @abstractmethod
    def read(self, path: str) -> str: pass
    
    @abstractmethod
    def write(self, path: str, content: str) -> None: pass
    
    @abstractmethod
    def exists(self, path: str) -> bool: pass
    
    @abstractmethod
    def delete(self, path: str) -> None: pass
