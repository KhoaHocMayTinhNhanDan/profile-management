# =========================================================
# File:
# observer/modular_mode/observer_pattern/subscriber/
# subscriber_interface.py
# =========================================================

"""
Subscriber Interface
--------------------------------------------------------

Mọi subscriber phải implement:

    update()

để nhận notification từ publisher.
"""

from abc import (
    ABC,
    abstractmethod,
)


class SubscriberInterface(ABC):

    @abstractmethod
    def update(
        self,
        publisher,
    ):
        pass