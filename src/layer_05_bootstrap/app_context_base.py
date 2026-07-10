import os
from .di_container import DIContainer

class AppContextBase:
    def __init__(self):
        self.container = DIContainer()
        self._register_infrastructure()

    def _register_infrastructure(self):
        # <-- BIND_REPOSITORY_HERE -->
        pass
