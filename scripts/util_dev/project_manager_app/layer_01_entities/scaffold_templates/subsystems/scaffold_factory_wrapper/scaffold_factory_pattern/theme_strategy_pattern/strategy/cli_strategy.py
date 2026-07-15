from .theme_strategy_interface import ThemeCompilationStrategy, register_strategy


@register_strategy("ui/cli")
class CliCompilationStrategy(ThemeCompilationStrategy):
    """
    GoF Role: ConcreteStrategy
    Strategy for CLI platforms. Since CLI does not require UI theme styling,
    this strategy returns the template content unmodified.
    """

    def is_matching(self, file_path: str) -> bool:
        return "ui/cli" in file_path.replace("\\", "/")

    def compile(
        self, content: str, theme_data: dict, palette_data: dict, tokens: dict
    ) -> str:
        # CLI has no UI elements, return content as-is
        return content
