import os
import tempfile
import json
import pytest
from scripts.util_dev.project_manager_app.layer_01_entities.scaffold_templates.subsystems.scaffold_factory_wrapper.scaffold_factory_pattern.theme_strategy_pattern.context.theme_context import (
    ThemeContext,
)
from scripts.util_dev.project_manager_app.layer_01_entities.scaffold_templates.subsystems.scaffold_factory_wrapper.scaffold_factory_pattern.theme_strategy_pattern.strategy.mobile_kivy_strategy import (
    KivyCompilationStrategy,
)
from scripts.util_dev.project_manager_app.layer_01_entities.scaffold_templates.subsystems.scaffold_factory_wrapper.scaffold_factory_pattern.theme_strategy_pattern.strategy.web_fastapi_strategy import (
    WebFastApiStrategy,
)


def test_kivy_compilation_strategy():
    """
    Asserts KivyCompilationStrategy translates placeholders and Kivy radius list correctly.
    """
    strategy = KivyCompilationStrategy()
    assert strategy.is_matching("src/ui/mobile_kivy/buttons.py") is True
    assert strategy.is_matching("src/ui/web_fastapi/index.html") is False

    raw_content = """
    self.background_color = ({{ ACCENT_COLOR_KIVY_FLOAT }})  # #89b4fa
    radius: [{{ RADIUS_NUM }}]
    """

    tokens = {
        "ACCENT_COLOR_KIVY_FLOAT": "1.0, 0.47, 0.78, 1",
        "RADIUS_NUM": "12",
    }

    compiled = strategy.compile(raw_content, {}, {}, tokens)

    assert "self.background_color = (1.0, 0.47, 0.78, 1)" in compiled
    assert "radius: [12]" in compiled


def test_web_compilation_strategy():
    """
    Asserts WebFastApiStrategy replaces placeholders for border-radius and font families.
    """
    strategy = WebFastApiStrategy()
    assert strategy.is_matching("src/ui/web_fastapi/index.html") is True

    raw_content = """
    border-radius: {{ RADIUS }};
    font-family: '{{ FONT_FAMILY }}';
    background-color: {{ DARK_BG }};
    """

    tokens = {
        "RADIUS": "12px",
        "FONT_FAMILY": "Arial",
        "DARK_BG": "#282a36",
    }

    compiled = strategy.compile(raw_content, {}, {}, tokens)

    assert "border-radius: 12px;" in compiled
    assert "font-family: 'Arial';" in compiled
    assert "background-color: #282a36;" in compiled


def test_theme_context_polymorphic_dispatch():
    """
    Asserts ThemeContext loads preset and correctly delegates compile
    to the matched strategy using polymorphism.
    """
    # Create a mock project root with project_config.json
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = os.path.join(temp_dir, "project_config.json")
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump({"branding": {"font_family": "CustomFont"}}, f)

        # Instantiate ThemeContext
        context = ThemeContext(temp_dir, "modern_round", "Catppuccin_Mocha")

        # Test Web compilation delegation
        web_code = """
        border-radius: {{ RADIUS }};
        background-color: {{ DARK_BG }};
        """
        compiled_web = context.compile("src/ui/web_fastapi/welcome.css", web_code)
        # Should apply Web radius and Catppuccin color replacement
        assert "border-radius: 12px;" in compiled_web

        # Test default compilation delegation (for other files)
        other_code = "color: {{ DARK_BG }};"
        compiled_other = context.compile("src/layer_05_bootstrap/main.py", other_code)
        # Should replace placeholder
        assert compiled_other.strip() == f"color: {context.dark_theme['DARK_BG']};"
