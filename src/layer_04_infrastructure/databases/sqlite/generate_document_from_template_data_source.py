from src.layer_03_interface_adapters.gateways.outbound.i_generate_document_from_template_data_source import (
    IGenerateDocumentFromTemplateDataSource,
)
from src.layer_04_infrastructure.databases.sqlite.sqlite_document_store import (
    SqliteDocumentStore,
)
from src.shared.utils.docx_helper import fill_document_content_controls
from typing import Optional
import os


class SqliteGenerateDocumentFromTemplateDataSource(
    IGenerateDocumentFromTemplateDataSource
):
    def __init__(self, store: Optional[SqliteDocumentStore] = None):
        self._store = store if store is not None else SqliteDocumentStore()

    async def get_profile(self, profile_id: str) -> Optional[dict]:
        return self._store.get_document("profiles", profile_id)

    async def save(self, data: dict) -> None:
        profile_id = data.get("profile_id", "")
        self._store.set_document("profiles", profile_id, data)

    async def generate_docx(
        self, template_doc_path: str, data: dict, output_path: str
    ) -> str:
        # Generate populated document (filling Content Controls and replacing placeholders)
        fill_document_content_controls(template_doc_path, data, output_path)

        # Return file:// absolute path representing the URL
        return "file:///" + os.path.abspath(output_path).replace("\\", "/")
