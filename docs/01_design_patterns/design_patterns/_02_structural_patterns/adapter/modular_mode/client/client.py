# =========================================================
# File:
# adapter/modular_mode/client/client.py
# =========================================================

from ..adapter_pattern.target.target_interface import (
    TargetInterface,
)

from ..adapter_pattern.adaptee.adaptee import (
    Adaptee,
)

from ..adapter_pattern.adapter.adapter import (
    Adapter,
)


class Client:
    """
    Role: Client
    Description: Core participant in the structure.
    """

    @staticmethod
    def execute(
        target: TargetInterface,
    ):

        print(target.request())


def run_client():
    """
    Modular Mode: Client Entry Point
    UML Role: Client
    Key Logic: Instantiates concrete subsystems and drives the pattern execution flow.
    """print("=" * 50)
    print("USING ADAPTER")
    print("=" * 50)

    # =====================================================
    # Legacy / third-party object
    # =====================================================

    adaptee = Adaptee()

    # =====================================================
    # Wrap bằng adapter
    # =====================================================

    adapter = Adapter(adaptee)

    # =====================================================
    # Client dùng adapter như TargetInterface
    # =====================================================

    Client.execute(adapter)