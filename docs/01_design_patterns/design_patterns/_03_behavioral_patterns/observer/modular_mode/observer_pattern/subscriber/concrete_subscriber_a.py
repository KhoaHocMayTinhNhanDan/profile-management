# =========================================================
# File:
# observer/modular_mode/observer_pattern/subscriber/
# concrete_subscriber_a.py
# =========================================================

"""
Concrete Subscriber A
--------------------------------------------------------

React với event theo logic riêng.
"""

from .subscriber_interface import (
    SubscriberInterface,
)


class ConcreteSubscriberA(
    SubscriberInterface
):

    def update(
        self,
        publisher,
    ):

        if publisher.state < 50:

            print(
                "ConcreteSubscriberA reacted "
                "to state < 50"
            )