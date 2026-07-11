import os
import shutil
from typing import List
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.gateways.outbound.i_project_data_source import (
    IProjectDataSource,
)


class FileSystemProjectDataSource(IProjectDataSource):
    def __init__(self, backup_root: str = ".projects"):
        self.backup_root = backup_root

    def backup_folder(self, folder_path: str, backup_name: str) -> bool:
        if not os.path.exists(folder_path):
            return True
        dest = os.path.join(self.backup_root, backup_name)
        if os.path.exists(dest):
            shutil.rmtree(dest)
        shutil.copytree(folder_path, dest)
        return True

    def restore_folder(self, backup_name: str, dest_path: str) -> bool:
        src = os.path.join(self.backup_root, backup_name)
        if not os.path.exists(src):
            return False
        if os.path.exists(dest_path):
            shutil.rmtree(dest_path)
        shutil.copytree(src, dest_path)
        return True

    def get_backup_list(self) -> List[str]:
        if not os.path.exists(self.backup_root):
            return []
        projects = []
        for item in os.listdir(self.backup_root):
            if os.path.isdir(os.path.join(self.backup_root, item)):
                projects.append(item)
        return projects

    def clear_folder(self, folder_path: str) -> bool:
        if os.path.exists(folder_path):
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
        else:
            os.makedirs(folder_path, exist_ok=True)
        return True
