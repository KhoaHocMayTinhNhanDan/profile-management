from abc import ABC, abstractmethod

# Dictionary registry to hold mapping of platform names to Strategy instances
# Excludes static dispatching logic from ThemeContext
STRATEGY_REGISTRY = {}


def register_strategy(platform_key: str):
    """
    Decorator to register a ConcreteStrategy to the STRATEGY_REGISTRY.
    Keeps ThemeCompiler decoupled from concrete strategies.
    """

    def decorator(cls):
        # Instantiate strategy and save to registry
        STRATEGY_REGISTRY[platform_key] = cls()
        return cls

    return decorator


class ThemeCompilationStrategy(ABC):
    """
    GoF Role: Strategy
    Abstract base class for all theme compilation strategies.
    Defines interface for compiling raw templates with theme data.
    """

    @abstractmethod
    def compile(
        self, content: str, theme_data: dict, palette_data: dict, tokens: dict
    ) -> str:
        """
        Compiles the raw template string by replacing color, geometry,
        and other design token placeholders with actual theme variables.
        """
        pass

    @abstractmethod
    def is_matching(self, file_path: str) -> bool:
        """
        Polymorphic check to decide if this strategy is suitable for the
        given file path. Replaces static if/elif matching.
        """
        pass
