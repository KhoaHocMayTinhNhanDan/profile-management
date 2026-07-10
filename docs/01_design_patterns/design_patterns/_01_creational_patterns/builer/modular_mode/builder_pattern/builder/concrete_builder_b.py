# =========================================================
# File:
# builder/modular_mode/builder_pattern/builder/concrete_builder_b.py
# =========================================================

from .builder_interface import BuilderInterface

from ..product.product import Product


class ConcreteBuilderB(BuilderInterface):
    """
    Role: ConcreteBuilderB
    Description: Core participant in the Concrete Builder B.Py structure.
    """

    def __init__(self):

        self.reset()

    def reset(self):

        self.product = Product()

    def build_part_a(self):

        self.product.add_part("BuilderB - PartA")

    def build_part_b(self):

        self.product.add_part("BuilderB - PartB")

    def build_part_c(self):

        self.product.add_part("BuilderB - PartC")

    def get_product(self):

        product = self.product

        self.reset()

        return product