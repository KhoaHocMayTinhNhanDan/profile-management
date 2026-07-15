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


class TestScaffoldTauriFlow(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.workspace_dir = self.test_dir.name
        self.app_ctx = AppContextCLI(self.workspace_dir)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_scaffold_tauri_files(self):
        project_name = "TauriScaffoldProject"
        success_config = write_project_name(self.workspace_dir, project_name)
        self.assertTrue(success_config)

        # Generate Tauri desktop feature
        args = argparse.Namespace(
            name="TauriFeature", platforms="desktop_tauri", db="sqlite"
        )
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            self.app_ctx.generate_feature_controller.execute(
                args, self.workspace_dir, project_name
            )

        # Verify Tauri desktop platform files exist on disk
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.workspace_dir,
                    "src",
                    "layer_04_infrastructure",
                    "ui",
                    "desktop_tauri",
                    "src-tauri",
                    "Cargo.toml",
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
                    "desktop_tauri",
                    "src-tauri",
                    "tauri.conf.json",
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
                    "desktop_tauri",
                    "src-tauri",
                    "src",
                    "main.rs",
                )
            )
        )
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.workspace_dir,
                    "scripts",
                    "run",
                    "desktop_tauri",
                    "run_tauriscaffoldproject.py",
                )
            )
        )


if __name__ == "__main__":
    unittest.main()
