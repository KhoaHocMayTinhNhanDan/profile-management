from scripts.util_dev.project_manager_app.layer_02_usecases.gateways_interface.i_file_repository import (
    IFileRepository,
)
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.gateways.outbound.i_file_data_source import (
    IFileDataSource,
)


class FileRepository(IFileRepository):
    def __init__(self, data_source: IFileDataSource):
        self._data_source = data_source

    def read_file(self, path: str) -> str:
        return self._data_source.read(path)

    def write_file(self, path: str, content: str) -> None:
        self._data_source.write(path, content)

    def file_exists(self, path: str) -> bool:
        return self._data_source.exists(path)

    def delete_file(self, path: str) -> None:
        self._data_source.delete(path)
