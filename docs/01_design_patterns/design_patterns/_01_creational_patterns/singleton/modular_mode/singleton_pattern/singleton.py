# =========================================================
# File:
# singleton/modular_mode/singleton_pattern/singleton/singleton.py
# =========================================================


class Singleton:
    """
    Role: Singleton
    Description: Core participant in the Singleton Pattern structure.
    """

    # =====================================================
    # Static variable lưu singleton instance
    # =====================================================

    _instance = None

    def __new__(cls):

        # =================================================
        # Nếu chưa có instance
        # => tạo mới
        # =================================================

        if cls._instance is None:

            print("Creating singleton instance...")

            cls._instance = super().__new__(cls)

        # =================================================
        # Nếu đã có instance
        # => trả lại instance cũ
        # =================================================

        return cls._instance

    def __init__(self):

        self.config = {
            "exchange": "binance",
            "risk_limit": 0.02,
        }

    def show_state(self):

        return (
            f"Singleton id={id(self)}, "
            f"config={self.config}"
        )