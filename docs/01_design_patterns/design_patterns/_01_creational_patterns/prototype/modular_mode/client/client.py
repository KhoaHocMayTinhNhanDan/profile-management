# =========================================================
# File:
# prototype/modular_mode/client/client.py
# =========================================================

from ..prototype_pattern.prototype.concrete_prototype import (
    ConcretePrototype,
)


def run_client():
    """
    Modular Mode: Client Entry Point
    UML Role: Client
    Key Logic: Instantiates concrete subsystems and drives the pattern execution flow.
    """

    # =====================================================
    # PRE-BUILT PROTOTYPE TEMPLATE
    # =====================================================

    prototype = ConcretePrototype(
        name="AggressiveTemplate",
        config={
            "signal": "momentum",
            "risk_per_trade": 0.02,
            "exchange": "binance",
            "timeframe": "5m",
            "indicators": [
                "EMA",
                "RSI",
            ],
            "execution": {
                "retry_count": 3,
                "use_websocket": True,
            },
        },
    )

    print("=" * 50)
    print("ORIGINAL PROTOTYPE TEMPLATE")
    print("=" * 50)

    print(prototype.show_state())

    # =====================================================
    # CLONE TEMPLATE
    # =====================================================

    clone = prototype.clone()

    # =====================================================
    # CUSTOMIZE RUNTIME CONFIG
    # =====================================================

    clone.name = "CustomizedClone"

    clone.config["risk_per_trade"] = 0.05

    clone.config["exchange"] = "bybit"

    clone.config["indicators"].append(
        "MACD"
    )

    clone.config["execution"][
        "retry_count"
    ] = 10

    print("=" * 50)
    print("CLONED & CUSTOMIZED OBJECT")
    print("=" * 50)

    print(clone.show_state())

    # =====================================================
    # ORIGINAL TEMPLATE VẪN GIỮ NGUYÊN
    # =====================================================

    print("=" * 50)
    print("ORIGINAL TEMPLATE AFTER CLONE")
    print("=" * 50)

    print(prototype.show_state())

    # =====================================================
    # Điều này chứng minh:
    # deepcopy tạo clone hoàn toàn độc lập.
    # =====================================================