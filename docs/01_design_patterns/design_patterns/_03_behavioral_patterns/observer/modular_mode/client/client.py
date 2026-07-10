from ..observer_pattern.publisher.concrete_publisher import (
    ConcretePublisher,
)

from ..observer_pattern.subscriber.concrete_subscriber_a import (
    ConcreteSubscriberA,
)

from ..observer_pattern.subscriber.concrete_subscriber_b import (
    ConcreteSubscriberB,
)
def run_client():
    print("=" * 50)
    print("CREATE PUBLISHER")
    print("=" * 50)

    publisher = ConcretePublisher()

    print()

    print("=" * 50)
    print("CREATE SUBSCRIBERS")
    print("=" * 50)

    subscriber_a = ConcreteSubscriberA()

    subscriber_b = ConcreteSubscriberB()

    print()

    print("=" * 50)
    print("SUBSCRIBE")
    print("=" * 50)

    publisher.attach(subscriber_a)

    publisher.attach(subscriber_b)

    print()

    print("=" * 50)
    print("CHANGE STATE")
    print("=" * 50)

    publisher.some_business_logic()

    print()

    print("=" * 50)
    print("UNSUBSCRIBE SUBSCRIBER B")
    print("=" * 50)

    publisher.detach(subscriber_b)

    print()

    print("=" * 50)
    print("CHANGE STATE AGAIN")
    print("=" * 50)

    publisher.some_business_logic()
    print()