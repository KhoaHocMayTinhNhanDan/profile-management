from .product_interface import ProductInterface


class ConcreteProductB(ProductInterface):

    def operation(self) -> str:
        return "Result from ConcreteProductB"