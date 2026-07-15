import os
import unittest
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.generate_feature.design_token_linter import (
    DesignTokenLinter,
)
from scripts.util_dev.project_manager_app.layer_01_entities.scaffold_templates.subsystems.scaffold_factory_wrapper.scaffold_factory_pattern.products.desktop_qt6.qt6_page_product import (
    Qt6Page,
)
from scripts.util_dev.project_manager_app.layer_01_entities.scaffold_templates.subsystems.scaffold_factory_wrapper.scaffold_factory_pattern.products.desktop_qt6.qt6_main_window_product import (
    Qt6MainWindow,
)
from scripts.util_dev.project_manager_app.layer_01_entities.scaffold_templates.subsystems.scaffold_factory_wrapper.scaffold_factory_pattern.products.mobile_kivy.kivy_page_product import (
    KivyPage,
)


class TestThemeTokensLinter(unittest.TestCase):
    def test_lint_qt6_page_template(self):
        template = Qt6Page().get_template("ColorPaletteDemo", "color_palette_demo")
        errors = DesignTokenLinter.lint_content(template, "qt6_page_product")
        self.assertEqual(
            errors, [], "Qt6Page template contains magic values:\n" + "\n".join(errors)
        )

    def test_lint_qt6_mainwindow_template(self):
        template = Qt6MainWindow().get_template("Application")
        errors = DesignTokenLinter.lint_content(template, "qt6_main_window_product")
        self.assertEqual(
            errors,
            [],
            "Qt6MainWindow template contains magic values:\n" + "\n".join(errors),
        )

    def test_lint_kivy_page_template(self):
        template = KivyPage().get_template("ColorPaletteDemo", "color_palette_demo")
        errors = DesignTokenLinter.lint_content(template, "kivy_page_product")
        self.assertEqual(
            errors, [], "KivyPage template contains magic values:\n" + "\n".join(errors)
        )
