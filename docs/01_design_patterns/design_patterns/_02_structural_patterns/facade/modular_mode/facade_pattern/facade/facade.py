# =========================================================
# File:
# facade/modular_mode/facade_pattern/facade/facade.py
# =========================================================

from ..subsystem.subsystem_a import (
    SubsystemA,
)

from ..subsystem.subsystem_b import (
    SubsystemB,
)

from ..subsystem.subsystem_c import (
    SubsystemC,
)

from ..subsystem.subsystem_d import (
    SubsystemD,
)


class Facade:
    """
    Role: Facade
    Description: Core participant in the Facade Pattern structure.
    """

    def __init__(self):

        # ==================================================
        # Facade quản lý subsystem objects
        # ==================================================

        self._subsystem_a = (
            SubsystemA()
        )

        self._subsystem_b = (
            SubsystemB()
        )

        self._subsystem_c = (
            SubsystemC()
        )

        self._subsystem_d = (
            SubsystemD()
        )

    def operation(self):

        results = [
            self._subsystem_a.operation_a(),
            self._subsystem_b.operation_b(),
            self._subsystem_c.operation_c(),
            self._subsystem_d.operation_d(),
        ]

        return "\n".join(results)