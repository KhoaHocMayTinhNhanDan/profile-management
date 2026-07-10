# =========================================================
# File:
# builder/modular_mode/builder_pattern/director/director.py
# =========================================================

from ..builder.builder_interface import BuilderInterface


class Director:
    """
    Role: Director
    Description: Core participant in the Builder Pattern structure.
    """

    def __init__(self, builder: BuilderInterface):

        self.builder = builder

    def change_builder(self, builder: BuilderInterface):

        self.builder = builder

    def build_minimal_product(self):

        self.builder.build_part_a()

    def build_full_feature_product(self):

        self.builder.build_part_a()

        self.builder.build_part_b()

        self.builder.build_part_c()