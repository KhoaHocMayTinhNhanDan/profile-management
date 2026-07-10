from src.layer_03_interface_adapters.gateways.outbound.i_update_profile_data_source import IUpdateProfileDataSource
from src.layer_04_infrastructure.databases.sqlite.sqlite_document_store import SqliteDocumentStore
from typing import Optional

class SqliteUpdateProfileDataSource(IUpdateProfileDataSource):
    def __init__(self, store: Optional[SqliteDocumentStore] = None):
        self._store = store if store is not None else SqliteDocumentStore()

    async def get_template(self, template_id: str) -> Optional[dict]:
        return self._store.get_document("profile_templates", template_id)

    async def get_profile(self, profile_id: str) -> Optional[dict]:
        return self._store.get_document("profiles", profile_id)

    async def save(self, data: dict) -> None:
        profile_id = data.get("profile_id", "")
        self._store.set_document("profiles", profile_id, data)
