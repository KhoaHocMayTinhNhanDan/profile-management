# =========================================================
# File:
# iterator/modular_mode/iterator_pattern/iterator/concrete_iterator.py
# =========================================================

from .iterator_interface import (
    IteratorInterface,
)


class ConcreteIterator(
    IteratorInterface
):
    """
    Role: ConcreteIterator
    Description: Core participant in the Concrete Iterator.Py structure.
    """

    def __init__(self, collection):

        self._collection = collection

        self._position = 0

    def has_next(self):

        return (
            self._position
            < len(self._collection.items)
        )

    def next(self):

        item = self.current()

        self._position += 1

        return item

    def current(self):

        return self._collection.items[
            self._position
        ]

    def reset(self):

        self._position = 0