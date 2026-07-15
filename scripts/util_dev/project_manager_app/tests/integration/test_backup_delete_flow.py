import unittest
import tempfile
import os
from scripts.util_dev.project_manager_app.layer_05_bootstrap.app_context_cli import (
    AppContextCLI,
)


class TestBackupDeleteFlow(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.workspace_dir = self.test_dir.name
        self.app_ctx = AppContextCLI(self.workspace_dir)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_backup_and_delete_project_flow(self):
        # Prepare dummy folders src/ and tests/
        src_path = os.path.join(self.workspace_dir, "src")
        tests_path = os.path.join(self.workspace_dir, "tests")
        os.makedirs(src_path, exist_ok=True)
        os.makedirs(tests_path, exist_ok=True)

        with open(os.path.join(src_path, "dummy.py"), "w", encoding="utf-8") as f:
            f.write("# dummy")

        # Save/Backup project
        project_name = "BackupToDelete"
        success_save = self.app_ctx.save_controller.execute(
            project_name, src_path, tests_path
        )
        self.assertTrue(success_save)

        # Verify backup folder exists on disk
        backup_dir = os.path.join(self.workspace_dir, ".projects", project_name)
        self.assertTrue(os.path.exists(backup_dir))
        self.assertTrue(project_name in self.app_ctx.list_controller.execute())

        # Delete project using delete controller
        success_delete = self.app_ctx.delete_controller.execute(project_name)
        self.assertTrue(success_delete)

        # Verify backup folder was physically deleted from disk
        self.assertFalse(os.path.exists(backup_dir))
        self.assertFalse(project_name in self.app_ctx.list_controller.execute())


if __name__ == "__main__":
    unittest.main()
