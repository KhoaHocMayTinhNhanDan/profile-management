# =========================================================
# File:
# facade/modular_mode/client/client.py
# =========================================================

from ..facade_pattern.facade.facade import (
    Facade,
)


def run_client():
    """
    Modular Mode: Client Entry Point
    UML Role: Client
    Key Logic: Instantiates concrete subsystems and drives the pattern execution flow.
    """print("=" * 50)
    print("USING FACADE")
    print("=" * 50)

    # =====================================================
    # Client chỉ làm việc với:
    # Facade
    # =====================================================

    facade = Facade()

    print(
        facade.operation()
    )