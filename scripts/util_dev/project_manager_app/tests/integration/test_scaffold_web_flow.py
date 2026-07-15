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


class TestScaffoldWebFlow(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.workspace_dir = self.test_dir.name
        self.app_ctx = AppContextCLI(self.workspace_dir)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_scaffold_web_files(self):
        project_name = "WebScaffoldProject"
        success_config = write_project_name(self.workspace_dir, project_name)
        self.assertTrue(success_config)

        # Configure custom branding accent color (Orange accent)
        import json

        config_path = os.path.join(
            self.workspace_dir,
            "scripts",
            "util_dev",
            "project_manager_app",
            "appdata",
            "project_config.json",
        )
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        config_data = {
            "project_name": project_name,
            "branding": {
                "accent_color_dark": "#FF5500",
                "accent_hover_dark": "#FF7733",
            },
        }
        with open(config_path, "w", encoding="utf-8") as f_cfg:
            json.dump(config_data, f_cfg, indent=4)

        # Also write to active project config path .projects/project_config.json
        active_config_path = os.path.join(
            self.workspace_dir, ".projects", "project_config.json"
        )
        os.makedirs(os.path.dirname(active_config_path), exist_ok=True)
        with open(active_config_path, "w", encoding="utf-8") as f_cfg:
            json.dump(config_data, f_cfg, indent=4)

        # Generate Web FastAPI feature with Office_Navy color palette
        args = argparse.Namespace(
            name="WebFeature",
            platforms="web_fastapi",
            db="sqlite",
            color_palette="Office_Navy",
        )
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            self.app_ctx.generate_feature_controller.execute(
                args, self.workspace_dir, project_name
            )

        # Verify welcome.html page has colors replaced matching Office_Navy
        welcome_file = os.path.join(
            self.workspace_dir,
            "src",
            "layer_04_infrastructure",
            "ui",
            "web_fastapi",
            "frontend",
            "level_05_pages",
            "welcome.html",
        )
        self.assertTrue(os.path.exists(welcome_file))
        with open(welcome_file, "r", encoding="utf-8") as file:
            html_content = file.read()
            self.assertIn("background-color: #0f172a;", html_content)
            self.assertIn("color: #f1f5f9;", html_content)
            self.assertIn("color: #FF5500;", html_content)

        # Verify Web UI Inspector, main.py, and debug router
        web_inspector_file = os.path.join(
            self.workspace_dir,
            "src",
            "layer_04_infrastructure",
            "ui",
            "web_fastapi",
            "frontend",
            "level_02_molecules",
            "ui_inspector",
            "ui_inspector.js",
        )
        self.assertTrue(os.path.exists(web_inspector_file))

        web_main_file = os.path.join(
            self.workspace_dir,
            "src",
            "layer_04_infrastructure",
            "ui",
            "web_fastapi",
            "fastapi",
            "main.py",
        )
        self.assertTrue(os.path.exists(web_main_file))

        web_debug_router = os.path.join(
            self.workspace_dir,
            "src",
            "layer_04_infrastructure",
            "ui",
            "web_fastapi",
            "fastapi",
            "routers",
            "debug.py",
        )
        self.assertTrue(os.path.exists(web_debug_router))

        # Verify runner script exists for web
        project_snake = "webscaffoldproject"
        web_runner = os.path.join(
            self.workspace_dir,
            "scripts",
            "run",
            "web_fastapi",
            f"run_{project_snake}.py",
        )
        self.assertTrue(os.path.exists(web_runner))

        # Verify buttons.js has border-radius dynamically set to the theme's RADIUS (8px)
        buttons_file = os.path.join(
            self.workspace_dir,
            "src",
            "layer_04_infrastructure",
            "ui",
            "web_fastapi",
            "frontend",
            "level_01_atoms",
            "buttons.js",
        )
        self.assertTrue(os.path.exists(buttons_file))
        with open(buttons_file, "r", encoding="utf-8") as file:
            buttons_content = file.read()
            self.assertIn("border-radius: 8px;", buttons_content)


if __name__ == "__main__":
    unittest.main()
