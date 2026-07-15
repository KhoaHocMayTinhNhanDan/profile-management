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


class TestScaffoldMobileFlow(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.workspace_dir = self.test_dir.name
        self.app_ctx = AppContextCLI(self.workspace_dir)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_scaffold_mobile_files(self):
        project_name = "MobileScaffoldProject"
        success_config = write_project_name(self.workspace_dir, project_name)
        self.assertTrue(success_config)

        # Generate Kivy, Flutter, React Native, and Jetpack Compose mobile platforms with Office_Navy color palette
        args = argparse.Namespace(
            name="MobileFeature",
            platforms="mobile_kivy,mobile_flutter,mobile_react_native,mobile_jetpack_compose",
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

        # 1. Kivy verification
        kivy_inspector_file = os.path.join(
            self.workspace_dir,
            "src",
            "layer_04_infrastructure",
            "ui",
            "mobile_kivy",
            "level_02_molecules",
            "ui_inspector",
            "ui_inspector.py",
        )
        self.assertTrue(os.path.exists(kivy_inspector_file))

        kivy_main_window_file = os.path.join(
            self.workspace_dir,
            "src",
            "layer_04_infrastructure",
            "ui",
            "mobile_kivy",
            "main_window.py",
        )
        self.assertTrue(os.path.exists(kivy_main_window_file))

        project_snake = "mobilescaffoldproject"
        mobile_runner = os.path.join(
            self.workspace_dir,
            "scripts",
            "run",
            "mobile_kivy",
            f"run_{project_snake}.py",
        )
        self.assertTrue(os.path.exists(mobile_runner))

        # 2. Flutter verification
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.workspace_dir,
                    "src",
                    "layer_04_infrastructure",
                    "ui",
                    "mobile_flutter",
                    "pubspec.yaml",
                )
            )
        )
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.workspace_dir,
                    "src",
                    "layer_04_infrastructure",
                    "ui",
                    "mobile_flutter",
                    "lib",
                    "main.dart",
                )
            )
        )

        # 3. React Native verification
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.workspace_dir,
                    "src",
                    "layer_04_infrastructure",
                    "ui",
                    "mobile_react_native",
                    "package.json",
                )
            )
        )
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.workspace_dir,
                    "src",
                    "layer_04_infrastructure",
                    "ui",
                    "mobile_react_native",
                    "App.tsx",
                )
            )
        )

        # 4. Jetpack Compose verification
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.workspace_dir,
                    "src",
                    "layer_04_infrastructure",
                    "ui",
                    "mobile_jetpack_compose",
                    "build.gradle.kts",
                )
            )
        )
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.workspace_dir,
                    "src",
                    "layer_04_infrastructure",
                    "ui",
                    "mobile_jetpack_compose",
                    "src",
                    "main",
                    "java",
                    "com",
                    "cleanarch",
                    "app",
                    "MainActivity.kt",
                )
            )
        )

        # Verify color replacements on Mobile platforms matching Office_Navy
        # 1. Kivy check
        kivy_welcome = os.path.join(
            self.workspace_dir,
            "src",
            "layer_04_infrastructure",
            "ui",
            "mobile_kivy",
            "level_05_pages",
            "welcome_page.py",
        )
        self.assertTrue(os.path.exists(kivy_welcome))
        with open(kivy_welcome, "r", encoding="utf-8") as f_kivy:
            kivy_content = f_kivy.read()
            self.assertIn("Color(0.06, 0.09, 0.16, 1.0)", kivy_content)  # #0f172a

        # 2. Flutter check
        flutter_welcome = os.path.join(
            self.workspace_dir,
            "src",
            "layer_04_infrastructure",
            "ui",
            "mobile_flutter",
            "lib",
            "level_05_pages",
            "welcome_page.dart",
        )
        self.assertTrue(os.path.exists(flutter_welcome))
        with open(flutter_welcome, "r", encoding="utf-8") as f_fl:
            fl_content = f_fl.read()
            self.assertIn("Color(0xFF0F172A)", fl_content)

        # 3. React Native check
        rn_app = os.path.join(
            self.workspace_dir,
            "src",
            "layer_04_infrastructure",
            "ui",
            "mobile_react_native",
            "App.tsx",
        )
        self.assertTrue(os.path.exists(rn_app))
        with open(rn_app, "r", encoding="utf-8") as f_rn:
            rn_content = f_rn.read()
            self.assertIn("#0f172a", rn_content)

        # 4. Jetpack Compose check
        compose_welcome = os.path.join(
            self.workspace_dir,
            "src",
            "layer_04_infrastructure",
            "ui",
            "mobile_jetpack_compose",
            "src",
            "main",
            "java",
            "com",
            "cleanarch",
            "app",
            "level_05_pages",
            "WelcomeScreen.kt",
        )
        self.assertTrue(os.path.exists(compose_welcome))
        with open(compose_welcome, "r", encoding="utf-8") as f_compose:
            compose_content = f_compose.read()
            self.assertIn("Color(0xFF0F172A)", compose_content)


if __name__ == "__main__":
    unittest.main()
