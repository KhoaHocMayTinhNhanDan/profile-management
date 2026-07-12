from src.layer_02_usecases.gateways_interface.i_update_profile_repository import (
    IUpdateProfileRepository,
)
from src.layer_03_interface_adapters.gateways.outbound.i_update_profile_data_source import (
    IUpdateProfileDataSource,
)
from src.layer_01_entities.profile import Profile
from src.layer_01_entities.profile_template import ProfileTemplate
from typing import Optional


class UpdateProfileRepository(IUpdateProfileRepository):
    def __init__(self, data_source: IUpdateProfileDataSource):
        self._data_source = data_source

    async def get_template(self, template_id: str) -> Optional[ProfileTemplate]:
        data = await self._data_source.get_template(template_id)
        if data:
            return ProfileTemplate.from_dict(data)
        return None

    async def get_profile(self, profile_id: str) -> Optional[Profile]:
        data = await self._data_source.get_profile(profile_id)
        if data:
            return Profile.from_dict(data)
        return None

    async def save_db(self, profile: Profile) -> None:
        await self._data_source.save(profile.to_dict())
