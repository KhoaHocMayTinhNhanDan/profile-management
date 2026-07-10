from .product_interface import ProductInterface


class ConcreteProductA(ProductInterface):

    def operation(self) -> str:
        return "Result from ConcreteProductA"