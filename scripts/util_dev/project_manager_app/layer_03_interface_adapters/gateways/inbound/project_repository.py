from typing import List
from scripts.util_dev.project_manager_app.layer_02_usecases.gateways_interface.i_project_repository import IProjectRepository
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.gateways.outbound.i_project_data_source import IProjectDataSource

class ProjectRepository(IProjectRepository):
    def __init__(self, data_source: IProjectDataSource):
        self._data_source = data_source
        
    def save_project(self, project_name: str, src_path: str, tests_path: str) -> bool:
        import os
        root_dir = os.path.dirname(src_path)
        run_path = os.path.join(root_dir, "scripts", "run")
        
        src_ok = self._data_source.backup_folder(src_path, f"{project_name}/src")
        tests_ok = self._data_source.backup_folder(tests_path, f"{project_name}/tests")
        run_ok = self._data_source.backup_folder(run_path, f"{project_name}/run")
        return src_ok and tests_ok and run_ok
        
    def load_project(self, project_name: str, dest_src_path: str, dest_tests_path: str) -> bool:
        import os
        root_dir = os.path.dirname(dest_src_path)
        run_path = os.path.join(root_dir, "scripts", "run")
        
        self._data_source.clear_folder(dest_src_path)
        self._data_source.clear_folder(dest_tests_path)
        self._data_source.clear_folder(run_path)
        
        src_ok = self._data_source.restore_folder(f"{project_name}/src", dest_src_path)
        tests_ok = self._data_source.restore_folder(f"{project_name}/tests", dest_tests_path)
        run_ok = self._data_source.restore_folder(f"{project_name}/run", run_path)
        return src_ok and tests_ok and run_ok
        
    def list_projects(self) -> List[str]:
        return self._data_source.get_backup_list()
        
    def reset_workspace(self, root_dir: str) -> bool:
        import os
        src_ok = self._data_source.clear_folder(os.path.join(root_dir, "src"))
        tests_ok = self._data_source.clear_folder(os.path.join(root_dir, "tests"))
        run_ok = self._data_source.clear_folder(os.path.join(root_dir, "scripts", "run"))
        return src_ok and tests_ok and run_ok
