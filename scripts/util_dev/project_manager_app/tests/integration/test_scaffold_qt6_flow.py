import unittest
import tempfile
import os
import argparse
from scripts.util_dev.project_manager_app.layer_05_bootstrap.app_context_cli import (
    AppContextCLI,
)
from scripts.util_dev.project_manager_app.config.project_config import (
    write_project_name,
)


class TestScaffoldQt6Flow(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.workspace_dir = self.test_dir.name
        self.app_ctx = AppContextCLI(self.workspace_dir)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_scaffold_qt6_assets_and_files(self):
        project_name = "AssetTestProject"
        success_config = write_project_name(self.workspace_dir, project_name)
        self.assertTrue(success_config)

        # Generate PyQt6 desktop feature
        args = argparse.Namespace(
            name="AssetFeature", platforms="desktop_qt6", db="sqlite"
        )
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            self.app_ctx.generate_feature_controller.execute(
                args, self.workspace_dir, project_name
            )

        # Verify assets_loader.py is created
        assets_loader_file = os.path.join(
            self.workspace_dir,
            "src",
            "layer_04_infrastructure",
            "ui",
            "desktop_qt6",
            "services",
            "assets_loader.py",
        )
        self.assertTrue(os.path.exists(assets_loader_file))
        with open(assets_loader_file, "r", encoding="utf-8") as file:
            content = file.read()
            self.assertIn("class AssetsLoader", content)
            self.assertIn("load_theme_icon", content)

        # Verify the dynamically named theme JSON files exist in the 7-pillar subdirectories
        for sub in ["01_geometry_borders", "07_color_palettes"]:
            theme_json_file = os.path.join(
                self.workspace_dir,
                "src",
                "layer_04_infrastructure",
                "ui",
                "desktop_qt6",
                "services",
                "theme",
                "themes",
                "catppuccin_mocha",
                sub,
                "theme.json",
            )
            self.assertTrue(os.path.exists(theme_json_file))

        # Verify colocated assets directories are pre-created for atoms
        for atom_name in ["buttons", "inputs", "labels"]:
            gitkeep_path = os.path.join(
                self.workspace_dir,
                "src",
                "layer_04_infrastructure",
                "ui",
                "desktop_qt6",
                "level_01_atoms",
                atom_name,
                "assets",
                "icons",
                ".gitkeep",
            )
            self.assertTrue(os.path.exists(gitkeep_path))

        # Verify config.py has DEBUG_UI setting
        config_file = os.path.join(self.workspace_dir, "src", "config.py")
        self.assertTrue(os.path.exists(config_file))
        with open(config_file, "r", encoding="utf-8") as file:
            content = file.read()
            self.assertIn("DEBUG_UI", content)

        # Verify main_window.py checks config.DEBUG_UI
        main_window_file = os.path.join(
            self.workspace_dir,
            "src",
            "layer_04_infrastructure",
            "ui",
            "desktop_qt6",
            "main_window.py",
        )
        self.assertTrue(os.path.exists(main_window_file))
        with open(main_window_file, "r", encoding="utf-8") as file:
            content = file.read()
            self.assertIn("config.DEBUG_UI", content)

        # Verify ui_inspector.py has F11 capture_screenshot capability
        ui_inspector_file = os.path.join(
            self.workspace_dir,
            "src",
            "layer_04_infrastructure",
            "ui",
            "desktop_qt6",
            "level_02_molecules",
            "ui_inspector",
            "ui_inspector.py",
        )
        self.assertTrue(os.path.exists(ui_inspector_file))
        with open(ui_inspector_file, "r", encoding="utf-8") as file:
            content = file.read()
            self.assertIn("Key_F11", content)
            self.assertIn("capture_screenshot", content)


if __name__ == "__main__":
    unittest.main()
