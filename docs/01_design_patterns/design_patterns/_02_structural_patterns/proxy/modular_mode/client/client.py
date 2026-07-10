# =========================================================
# File:
# proxy/modular_mode/client/client.py
# =========================================================

from ..proxy_pattern.real_subject.real_subject import (
    RealSubject,
)

from ..proxy_pattern.proxy.proxy import (
    Proxy,
)


def run_client():
    """
    Modular Mode: Client Entry Point
    UML Role: Client
    Key Logic: Instantiates concrete subsystems and drives the pattern execution flow.
    """print("=" * 50)
    print("DIRECT REAL SUBJECT")
    print("=" * 50)

    real_subject = RealSubject()

    print(real_subject.request())

    print()

    print("=" * 50)
    print("USING PROXY")
    print("=" * 50)

    proxy = Proxy(real_subject)

    print(proxy.request())