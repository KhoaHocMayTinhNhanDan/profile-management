# =========================================================
# File:
# observer/modular_mode/observer_pattern/publisher/
# publisher_interface.py
# =========================================================

"""
Publisher Interface
--------------------------------------------------------

Khai báo các method:

- attach()
- detach()
- notify()

để quản lý subscribers.
"""

from abc import (
    ABC,
    abstractmethod,
)


class PublisherInterface(ABC):

    @abstractmethod
    def attach(self, subscriber):
        pass

    @abstractmethod
    def detach(self, subscriber):
        pass

    @abstractmethod
    def notify(self):
        pass