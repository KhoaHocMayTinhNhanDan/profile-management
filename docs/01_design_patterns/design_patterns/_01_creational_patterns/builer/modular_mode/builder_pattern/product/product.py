# =========================================================
# File:
# builder/modular_mode/builder_pattern/product/product.py
# =========================================================


class Product:
    """
    Role: Product
    Description: Core participant in the Builder Pattern structure.
    """

    def __init__(self):

        # Các thành phần được build dần dần.
        self.parts = []

    def add_part(self, part: str):

        self.parts.append(part)

    def show_product(self):

        return f"Product parts: {', '.join(self.parts)}"