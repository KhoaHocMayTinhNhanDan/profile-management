# =========================================================
# File:
# observer/modular_mode/observer_pattern/publisher/
# concrete_publisher.py
# =========================================================

"""
Concrete Publisher
--------------------------------------------------------

Concrete Publisher
(Publisher cụ thể)

Quản lý:
- subscriber list
- state changes
- event notifications
"""

import random

from .publisher_interface import (
    PublisherInterface,
)


class ConcretePublisher(
    PublisherInterface
):

    def __init__(self):

        self._subscribers = []

        self._state = None

    def attach(self, subscriber):

        print(
            f"Attach subscriber: "
            f"{subscriber.__class__.__name__}"
        )

        self._subscribers.append(
            subscriber
        )

    def detach(self, subscriber):

        print(
            f"Detach subscriber: "
            f"{subscriber.__class__.__name__}"
        )

        self._subscribers.remove(
            subscriber
        )

    def notify(self):

        print(
            "\nPublisher notifying subscribers...\n"
        )

        for subscriber in self._subscribers:

            subscriber.update(self)

    def some_business_logic(self):

        print(
            "Publisher performing business logic..."
        )

        self._state = random.randint(
            1,
            100,
        )

        print(
            f"Publisher state changed to: "
            f"{self._state}"
        )

        self.notify()

    @property
    def state(self):

        return self._state