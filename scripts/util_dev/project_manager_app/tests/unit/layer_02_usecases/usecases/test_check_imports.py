import unittest
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.check_imports.check_imports_dto import (
    CheckImportsInput,
)
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.check_imports.check_imports_interactor import (
    CheckImportsInteractor,
)
from scripts.util_dev.project_manager_app.tests.unit.mocks.mock_file_repository import (
    MockFileRepository,
)


class TestCheckImports(unittest.TestCase):
    def setUp(self):
        self.file_repo = MockFileRepository()
        self.interactor = CheckImportsInteractor(self.file_repo)

    def test_directory_not_found(self):
        input_data = CheckImportsInput(project_root_dir="/workspace")
        output = self.interactor.execute(input_data)
        self.assertEqual(output.status, "error")
        self.assertIn("src directory not found!", output.message)

    def test_no_violations(self):
        self.file_repo.make_dir("/workspace/src")

        # layer_02_usecases importing layer_01_entities is allowed (2 -> 1)
        usecase_content = "import src.layer_01_entities.something"
        self.file_repo.write_file(
            "/workspace/src/layer_02_usecases/usecase_file.py", usecase_content
        )

        input_data = CheckImportsInput(project_root_dir="/workspace")
        output = self.interactor.execute(input_data)
        self.assertEqual(output.status, "ok")
        self.assertIsNotNone(output.violations)
        if output.violations is not None:
            self.assertEqual(len(output.violations), 0)

    def test_with_violations(self):
        self.file_repo.make_dir("/workspace/src")

        # layer_01_entities importing layer_02_usecases is NOT allowed (1 -> 2)
        entity_content = "from src.layer_02_usecases.something import Class"
        self.file_repo.write_file(
            "/workspace/src/layer_01_entities/entity_file.py", entity_content
        )

        input_data = CheckImportsInput(project_root_dir="/workspace")
        output = self.interactor.execute(input_data)
        self.assertEqual(output.status, "error")
        self.assertIsNotNone(output.violations)
        if output.violations is not None:
            self.assertEqual(len(output.violations), 1)
            violation = output.violations[0]
            self.assertEqual(violation[0], "entity_file.py")
            self.assertEqual(violation[1], 1)
            self.assertEqual(violation[2], 2)


if __name__ == "__main__":
    unittest.main()
