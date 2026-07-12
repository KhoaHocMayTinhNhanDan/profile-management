from src.layer_03_interface_adapters.gateways.outbound.i_create_profile_template_data_source import (
    ICreateProfileTemplateDataSource,
)
from src.layer_04_infrastructure.databases.sqlite.sqlite_document_store import (
    SqliteDocumentStore,
)
from typing import Optional


class SqliteCreateProfileTemplateDataSource(ICreateProfileTemplateDataSource):
    def __init__(self, store: Optional[SqliteDocumentStore] = None):
        self._store = store if store is not None else SqliteDocumentStore()

    async def get_by_id(self, template_id: str) -> Optional[dict]:
        return self._store.get_document("profile_templates", template_id)

    async def save(self, data: dict) -> None:
        template_id = data.get("template_id", "")
        self._store.set_document("profile_templates", template_id, data)
