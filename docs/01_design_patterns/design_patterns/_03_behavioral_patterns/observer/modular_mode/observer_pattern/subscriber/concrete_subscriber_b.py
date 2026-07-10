# =========================================================
# File:
# observer/modular_mode/observer_pattern/subscriber/
# concrete_subscriber_b.py
# =========================================================

"""
Concrete Subscriber B
--------------------------------------------------------

React với event theo logic khác.
"""

from .subscriber_interface import (
    SubscriberInterface,
)


class ConcreteSubscriberB(
    SubscriberInterface
):

    def update(
        self,
        publisher,
    ):

        if publisher.state >= 50:

            print(
                "ConcreteSubscriberB reacted "
                "to state >= 50"
            )