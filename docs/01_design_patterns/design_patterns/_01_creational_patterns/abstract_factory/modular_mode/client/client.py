# =========================================================
# File: abstract_factory/modular_mode/client/client.py
# =========================================================

from ..abstract_factory_pattern.factory.abstract_factory import (
    AbstractFactory,
)

from ..abstract_factory_pattern.factory.concrete_factory_a import (
    ConcreteFactoryA,
)

from ..abstract_factory_pattern.factory.concrete_factory_b import (
    ConcreteFactoryB,
)


class Client:
    """
    Role: Client
    Description: Core participant in the structure.
    """


    @staticmethod
    def execute(factory: AbstractFactory):
        """
        UML Role: Executor
        """
        # Create Product A
        product_a = factory.create_product_a()

        # Create Product B
        product_b = factory.create_product_b()

        # ==================================================
        # Sử dụng Product A
        # ==================================================

        print(product_a.useful_function_a())

        # ==================================================
        # Sử dụng Product B
        # ==================================================

        print(product_b.useful_function_b())

        # ==================================================
        # Product B cộng tác với Product A
        # ==================================================
        #
        # Điểm QUAN TRỌNG của Abstract Factory:
        #
        # Các products cùng family thường:
        # - tương thích
        # - làm việc được với nhau
        #
        # Ví dụ:
        #
        # BinanceExecutionAPI
        #     dùng BinanceMarketDataAPI
        #
        # DarkButton
        #     dùng DarkThemeConfig
        #
        # PostgreSQLQueryBuilder
        #     dùng PostgreSQLConnection
        #
        # ==================================================

        print(
            product_b.another_useful_function_b(product_a)
        )


def run_client():
    """
    Modular Mode: Client Entry Point
    UML Role: Client
    Key Logic: Instantiates concrete subsystems and drives the pattern execution flow.
    """
    # =====================================================
    # Sử dụng Variant / Family A
    # =====================================================

    print("=" * 50)
    print("USING FACTORY A")
    print("=" * 50)

    # Tạo Concrete Factory A
    factory_a = ConcreteFactoryA()

    # Inject factory vào client
    Client.execute(factory_a)

    print()

    # =====================================================
    # Sử dụng Variant / Family B
    # =====================================================

    print("=" * 50)
    print("USING FACTORY B")
    print("=" * 50)

    # Tạo Concrete Factory B
    factory_b = ConcreteFactoryB()

    # Inject factory vào client
    Client.execute(factory_b)