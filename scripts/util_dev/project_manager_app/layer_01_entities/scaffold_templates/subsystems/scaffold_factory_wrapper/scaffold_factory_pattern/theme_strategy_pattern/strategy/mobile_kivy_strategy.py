from abc import ABC
from .theme_strategy_interface import ThemeCompilationStrategy, register_strategy
from .default_strategy import DefaultCompilationStrategy


class MobileCompilationStrategy(ThemeCompilationStrategy, ABC):
    """
    GoF Role: Strategy
    Base category strategy for all Mobile platforms.
    """

    pass


@register_strategy("ui/mobile_kivy")
class KivyCompilationStrategy(MobileCompilationStrategy):
    """
    GoF Role: ConcreteStrategy
    Concrete strategy for Mobile Kivy platform.
    """

    def is_matching(self, file_path: str) -> bool:
        return "ui/mobile_kivy" in file_path.replace("\\", "/")

    def compile(
        self, content: str, theme_data: dict, palette_data: dict, tokens: dict
    ) -> str:
        return DefaultCompilationStrategy().compile(
            content, theme_data, palette_data, tokens
        )
