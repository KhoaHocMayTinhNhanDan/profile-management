import os
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.gateways.outbound.i_file_data_source import IFileDataSource

class FileDataSource(IFileDataSource):
    def read(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
            
    def write(self, path: str, content: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
            
    def exists(self, path: str) -> bool:
        return os.path.exists(path)
        
    def delete(self, path: str) -> None:
        if os.path.exists(path):
            os.remove(path)
