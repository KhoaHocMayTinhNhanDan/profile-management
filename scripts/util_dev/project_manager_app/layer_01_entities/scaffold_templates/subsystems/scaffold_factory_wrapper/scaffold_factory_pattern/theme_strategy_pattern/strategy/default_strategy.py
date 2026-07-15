import re
from .theme_strategy_interface import ThemeCompilationStrategy, register_strategy


@register_strategy("default")
class DefaultCompilationStrategy(ThemeCompilationStrategy):
    """
    GoF Role: ConcreteStrategy
    Default strategy that performs placeholder replacement and legacy HEX replacements.
    """

    def is_matching(self, file_path: str) -> bool:
        return "default" in file_path.replace("\\", "/")

    def compile(
        self, content: str, theme_data: dict, palette_data: dict, tokens: dict
    ) -> str:
        # 1. Replace Design Token Placeholders: e.g. {{ DARK_BG }} and f-string escaped { DARK_BG }
        for k, v in tokens.items():
            if k != "_color_map":
                val_str = str(v)
                content = content.replace(f"{{{{ {k} }}}}", val_str)
                content = content.replace(f"{{{{{k}}}}}", val_str)
                content = content.replace(f"{{ {k} }}", val_str)
                content = content.replace(f"{{{k}}}", val_str)

        # 2. Replace legacy HEX colors for backward compatibility
        color_map = tokens.get("_color_map", {})
        for src_hex, dest_hex in color_map.items():
            content = re.sub(re.escape(src_hex), dest_hex, content, flags=re.IGNORECASE)

        return content
