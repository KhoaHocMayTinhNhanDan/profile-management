from abc import ABC
from .theme_strategy_interface import ThemeCompilationStrategy, register_strategy
from .default_strategy import DefaultCompilationStrategy


class WebCompilationStrategy(ThemeCompilationStrategy, ABC):
    """
    GoF Role: Strategy
    Base category strategy for all Web-based platforms.
    """

    pass


@register_strategy("ui/web_fastapi")
class WebFastApiStrategy(WebCompilationStrategy):
    """
    GoF Role: ConcreteStrategy
    Concrete strategy for Web FastAPI platform.
    """

    def is_matching(self, file_path: str) -> bool:
        return "ui/web_fastapi" in file_path.replace("\\", "/")

    def compile(
        self, content: str, theme_data: dict, palette_data: dict, tokens: dict
    ) -> str:
        return DefaultCompilationStrategy().compile(
            content, theme_data, palette_data, tokens
        )
