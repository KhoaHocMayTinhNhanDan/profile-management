from src.layer_02_usecases.gateways_interface.i_checkin_document_repository import (
    ICheckinDocumentRepository,
)
from src.layer_03_interface_adapters.gateways.outbound.i_checkin_document_data_source import (
    ICheckinDocumentDataSource,
)
from src.layer_01_entities.profile import Profile
from typing import Optional


class CheckinDocumentRepository(ICheckinDocumentRepository):
    def __init__(self, data_source: ICheckinDocumentDataSource):
        self._data_source = data_source

    async def get_profile(self, profile_id: str) -> Optional[Profile]:
        data = await self._data_source.get_profile(profile_id)
        if data:
            return Profile.from_dict(data)
        return None

    async def save_db(self, profile: Profile) -> None:
        await self._data_source.save(profile.to_dict())
