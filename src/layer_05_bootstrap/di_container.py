from typing import Any

class DIContainer:
    def __init__(self):
        self._services = {}
        
    def register(self, interface: Any, implementation: Any) -> None:
        self._services[interface] = implementation
        
    def resolve(self, interface: Any) -> Any:
        instance = self._services.get(interface)
        if instance is None:
            raise ValueError(f"Dependency not registered: {interface}")
        return instance
