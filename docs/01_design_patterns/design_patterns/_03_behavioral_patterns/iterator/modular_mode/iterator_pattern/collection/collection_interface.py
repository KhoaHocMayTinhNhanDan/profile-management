# =========================================================
# File:
# iterator/modular_mode/iterator_pattern/collection/collection_interface.py
# =========================================================

from abc import ABC, abstractmethod


class CollectionInterface(ABC):
    """
    Role: CollectionInterface
    Description: Core participant in the Collection Interface.Py structure.
    """

    @abstractmethod
    def create_iterator(self):
        pass