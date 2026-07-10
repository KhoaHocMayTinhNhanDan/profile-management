# =========================================================
# File:
# singleton/modular_mode/client/client.py
# =========================================================

from ..singleton_pattern.singleton import (
    Singleton,
)


def run_client():
    """
    Modular Mode: Client Entry Point
    UML Role: Client
    Key Logic: Instantiates concrete subsystems and drives the pattern execution flow.
    """print("=" * 50)
    print("CREATE OBJECT 1")
    print("=" * 50)

    singleton_a = Singleton()

    print(singleton_a.show_state())

    print()

    print("=" * 50)
    print("CREATE OBJECT 2")
    print("=" * 50)

    singleton_b = Singleton()

    print(singleton_b.show_state())

    print()

    print("=" * 50)
    print("CHECK SAME INSTANCE")
    print("=" * 50)

    print(
        singleton_a is singleton_b
    )

    print()

    # =====================================================
    # Modify state từ object A
    # =====================================================

    singleton_a.config["exchange"] = "bybit"

    print("=" * 50)
    print("STATE AFTER MODIFYING OBJECT A")
    print("=" * 50)

    print(singleton_a.show_state())

    print(singleton_b.show_state())

    print()

    # =====================================================
    # Điều này chứng minh:
    # singleton_a và singleton_b
    # là cùng 1 object.
    # =====================================================