# =========================================================
# File:
# iterator/modular_mode/iterator_pattern/collection/concrete_collection.py
# =========================================================

from .collection_interface import (
    CollectionInterface,
)

from ..iterator.concrete_iterator import (
    ConcreteIterator,
)


class ConcreteCollection(
    CollectionInterface
):
    """
    Role: ConcreteCollection
    Description: Core participant in the Concrete Collection.Py structure.
    """

    def __init__(self):

        self.items = []

    def add_item(self, item):

        self.items.append(item)

    def create_iterator(self):

        return ConcreteIterator(self)