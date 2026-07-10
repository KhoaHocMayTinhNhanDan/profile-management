from src.layer_02_usecases.gateways_interface.i_create_profile_repository import ICreateProfileRepository
from src.layer_03_interface_adapters.gateways.outbound.i_create_profile_data_source import ICreateProfileDataSource
from src.layer_01_entities.profile import Profile
from src.layer_01_entities.profile_template import ProfileTemplate
from typing import Optional

class CreateProfileRepository(ICreateProfileRepository):
    def __init__(self, data_source: ICreateProfileDataSource):
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
