# =========================================================
# File:
# prototype/modular_mode/prototype_pattern/prototype/concrete_prototype.py
# =========================================================

import copy

from .prototype_interface import PrototypeInterface


class ConcretePrototype(PrototypeInterface):
    """
    Role: ConcretePrototype
    Description: Core participant in the Concrete Prototype.Py structure.
    """

    def __init__(
        self,
        name: str,
        config: dict,
    ):

        self.name = name

        self.config = config

    def clone(self):

        return copy.deepcopy(self)

    def show_state(self):

        return (
            f"\n"
            f"name   : {self.name}\n"
            f"config : {self.config}\n"
        )