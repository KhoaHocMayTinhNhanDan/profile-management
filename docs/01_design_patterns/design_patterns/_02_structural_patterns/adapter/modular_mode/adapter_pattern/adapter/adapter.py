# =========================================================
# File:
# adapter/modular_mode/adapter_pattern/adapter/adapter.py
# =========================================================

from ..target.target_interface import (
    TargetInterface,
)

from ..adaptee.adaptee import Adaptee


class Adapter(TargetInterface):
    """
    Role: Adapter
    Description: Core participant in the Adapter Pattern structure.
    """

    def __init__(
        self,
        adaptee: Adaptee,
    ):

        self.adaptee = adaptee

    def request(self):

        result = (
            self.adaptee.specific_request()
        )

        return (
            f"Adapter translated:\n"
            f"{result}"
        )