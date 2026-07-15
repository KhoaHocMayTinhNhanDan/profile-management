from .theme_strategy_interface import ThemeCompilationStrategy, STRATEGY_REGISTRY

# Import all strategies to trigger registration decorators
from .cli_strategy import CliCompilationStrategy
from .web_fastapi_strategy import WebFastApiStrategy
from .desktop_qt6_strategy import DesktopQt6Strategy
from .mobile_kivy_strategy import KivyCompilationStrategy
from .mobile_flutter_strategy import FlutterCompilationStrategy
from .mobile_jetpack_compose_strategy import ComposeCompilationStrategy
from .mobile_react_native_strategy import ReactNativeCompilationStrategy
from .default_strategy import DefaultCompilationStrategy

__all__ = [
    "ThemeCompilationStrategy",
    "STRATEGY_REGISTRY",
    "CliCompilationStrategy",
    "WebFastApiStrategy",
    "DesktopQt6Strategy",
    "KivyCompilationStrategy",
    "FlutterCompilationStrategy",
    "ComposeCompilationStrategy",
    "ReactNativeCompilationStrategy",
    "DefaultCompilationStrategy",
]
