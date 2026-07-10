# =========================================================
# File:
# proxy/modular_mode/proxy_pattern/proxy/proxy.py
# =========================================================

from ..subject.subject import (
    Subject,
)


class Proxy(Subject):
    """
    Role: Proxy
    Description: Core participant in the Proxy Pattern structure.
    """

    def __init__(
        self,
        real_subject: Subject,
    ):

        self._real_subject = (
            real_subject
        )

    def request(self) -> str:

        if self._check_access():

            result = (
                self._real_subject.request()
            )

            self._log_access()

            return result

        return "Proxy: access denied."

    def _check_access(self) -> bool:

        print(
            "Proxy: checking access before request..."
        )

        return True

    def _log_access(self):

        print(
            "Proxy: logging request."
        )