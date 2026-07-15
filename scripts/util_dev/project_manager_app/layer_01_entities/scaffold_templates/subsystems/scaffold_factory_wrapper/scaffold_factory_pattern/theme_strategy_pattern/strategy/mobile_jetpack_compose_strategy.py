from .theme_strategy_interface import register_strategy
from .default_strategy import DefaultCompilationStrategy
from .mobile_kivy_strategy import MobileCompilationStrategy


@register_strategy("ui/mobile_jetpack_compose")
class ComposeCompilationStrategy(MobileCompilationStrategy):
    """
    GoF Role: ConcreteStrategy
    Concrete strategy for Mobile Jetpack Compose platform.
    """

    def is_matching(self, file_path: str) -> bool:
        return "ui/mobile_jetpack_compose" in file_path.replace("\\", "/")

    def compile(
        self, content: str, theme_data: dict, palette_data: dict, tokens: dict
    ) -> str:
        return DefaultCompilationStrategy().compile(
            content, theme_data, palette_data, tokens
        )
