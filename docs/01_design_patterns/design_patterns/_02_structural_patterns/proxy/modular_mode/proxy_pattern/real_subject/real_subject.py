# =========================================================
# File:
# proxy/modular_mode/proxy_pattern/real_subject/real_subject.py
# =========================================================

from ..subject.subject import (
    Subject,
)


class RealSubject(Subject):
    """
    Role: RealSubject
    Description: Core participant in the Real Subject.Py structure.
    """

    def request(self) -> str:

        return (
            "RealSubject: handling request."
        )