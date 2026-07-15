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


class TestGroupedFeatureFlow(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.workspace_dir = self.test_dir.name
        self.app_ctx = AppContextCLI(self.workspace_dir)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_end_to_end_grouped_generation_flow(self):
        project_name = "GroupedProject"
        success_config = write_project_name(self.workspace_dir, project_name)
        self.assertTrue(success_config)

        # Execute feature generation with group "auth"
        args = argparse.Namespace(
            name="LoginUser", platforms="desktop_qt6", db="sqlite", group="auth"
        )
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            self.app_ctx.generate_feature_controller.execute(
                args, self.workspace_dir, project_name
            )

        # Verify grouped files exist on disk
        interactor_file = os.path.join(
            self.workspace_dir,
            "src",
            "layer_02_usecases",
            "usecases",
            "auth",
            "login_user",
            "login_user_interactor.py",
        )
        self.assertTrue(os.path.exists(interactor_file))

        # Verify unit test file is grouped too
        test_file = os.path.join(
            self.workspace_dir,
            "tests",
            "unit",
            "layer_02_usecases",
            "usecases",
            "auth",
            "test_login_user.py",
        )
        self.assertTrue(os.path.exists(test_file))

        # Verify imports run and are clean
        output = self.app_ctx.check_imports_controller.execute(self.workspace_dir)
        self.assertEqual(output.status, "ok")
        self.assertIsNotNone(output.violations)
        if output.violations is not None:
            self.assertEqual(len(output.violations), 0)


if __name__ == "__main__":
    unittest.main()
