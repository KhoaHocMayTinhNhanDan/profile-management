# =========================================================
# File:
# state/modular_mode/state_pattern/state/
# state_interface.py
# =========================================================

"""
State Interface
--------------------------------------------------------

Mọi concrete state phải implement:

    handle()

để xử lý behavior theo state.
"""

from abc import (
    ABC,
    abstractmethod,
)


class StateInterface(ABC):

    def __init__(self):

        self._context = None

    @property
    def context(self):

        return self._context

    @context.setter
    def context(self, context):

        self._context = context

    @abstractmethod
    def handle(self):
        pass