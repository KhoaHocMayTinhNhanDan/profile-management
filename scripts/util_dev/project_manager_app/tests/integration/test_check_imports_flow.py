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


class TestCheckImportsFlow(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.workspace_dir = self.test_dir.name
        self.app_ctx = AppContextCLI(self.workspace_dir)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_end_to_end_generation_and_check_imports_flow(self):
        project_name = "SpaceShipProject"
        success_config = write_project_name(self.workspace_dir, project_name)
        self.assertTrue(success_config)

        # Generate a simple feature
        args = argparse.Namespace(
            name="EngineControl", platforms="desktop_qt6", db="sqlite"
        )
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            self.app_ctx.generate_feature_controller.execute(
                args, self.workspace_dir, project_name
            )

        # Run imports rule check on the clean generated project
        output = self.app_ctx.check_imports_controller.execute(self.workspace_dir)
        self.assertEqual(output.status, "ok")
        self.assertIsNotNone(output.violations)
        if output.violations is not None:
            self.assertEqual(len(output.violations), 0)

        # Inject an artificial architecture rule violation (Layer 1 imports Layer 2)
        entity_file = os.path.join(
            self.workspace_dir, "src", "layer_01_entities", "__init__.py"
        )
        with open(entity_file, "a", encoding="utf-8") as f:
            f.write("\nimport src.layer_02_usecases.something\n")

        # Re-run import rules check and verify it detects the violation
        output_violation = self.app_ctx.check_imports_controller.execute(
            self.workspace_dir
        )
        self.assertEqual(output_violation.status, "error")
        self.assertIsNotNone(output_violation.violations)
        if output_violation.violations is not None:
            self.assertEqual(len(output_violation.violations), 1)
            violation = output_violation.violations[0]
            self.assertEqual(violation[0], "__init__.py")
            self.assertEqual(violation[1], 1)  # Layer 1
            self.assertEqual(violation[2], 2)  # Layer 2


if __name__ == "__main__":
    unittest.main()
