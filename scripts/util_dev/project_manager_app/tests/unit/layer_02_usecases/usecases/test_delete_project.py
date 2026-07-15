import unittest
from unittest.mock import Mock
from scripts.util_dev.project_manager_app.layer_02_usecases.gateways_interface.i_project_repository import (
    IProjectRepository,
)
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.delete_project.delete_project_dto import (
    DeleteProjectInput,
)
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.delete_project.delete_project_interactor import (
    DeleteProjectInteractor,
)


class TestDeleteProject(unittest.TestCase):
    def test_execute_calls_repository(self):
        mock_repo = Mock(spec=IProjectRepository)
        mock_repo.delete_project.return_value = True

        interactor = DeleteProjectInteractor(mock_repo)
        input_data = DeleteProjectInput(project_name="MyTestProject")

        result = interactor.execute(input_data)

        self.assertTrue(result)
        mock_repo.delete_project.assert_called_once_with("MyTestProject")


if __name__ == "__main__":
    unittest.main()
