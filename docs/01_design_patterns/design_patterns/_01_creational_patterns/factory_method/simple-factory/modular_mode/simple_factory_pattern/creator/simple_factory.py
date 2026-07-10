from ..product.concrete_product_a import ConcreteProductA
from ..product.concrete_product_b  import ConcreteProductB


class SimpleFactory:

    @staticmethod
    def create_product(product_type: str):

        if product_type == "A":
            return ConcreteProductA()

        elif product_type == "B":
            return ConcreteProductB()

        else:
            raise ValueError(
                f"Unknown product type: {product_type}"
            )