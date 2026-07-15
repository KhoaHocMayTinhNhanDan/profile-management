from abc import ABC
from .theme_strategy_interface import ThemeCompilationStrategy, register_strategy
from .default_strategy import DefaultCompilationStrategy


class DesktopCompilationStrategy(ThemeCompilationStrategy, ABC):
    """
    GoF Role: Strategy
    Base category strategy for all Desktop platforms.
    """

    pass


@register_strategy("ui/desktop_qt6")
class DesktopQt6Strategy(DesktopCompilationStrategy):
    """
    GoF Role: ConcreteStrategy
    Concrete strategy for Desktop PyQt6 platform.
    """

    def is_matching(self, file_path: str) -> bool:
        norm_path = file_path.replace("\\", "/")
        return "ui/desktop_qt6" in norm_path or "ui/desktop_qt5" in norm_path

    def compile(
        self, content: str, theme_data: dict, palette_data: dict, tokens: dict
    ) -> str:
        return DefaultCompilationStrategy().compile(
            content, theme_data, palette_data, tokens
        )
