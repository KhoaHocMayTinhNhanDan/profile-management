from src.layer_02_usecases.gateways_interface.i_create_profile_template_repository import (
    ICreateProfileTemplateRepository,
)
from src.layer_03_interface_adapters.gateways.outbound.i_create_profile_template_data_source import (
    ICreateProfileTemplateDataSource,
)
from src.layer_01_entities.profile_template import ProfileTemplate
from typing import Optional


class CreateProfileTemplateRepository(ICreateProfileTemplateRepository):
    def __init__(self, data_source: ICreateProfileTemplateDataSource):
        self._data_source = data_source

    async def get_by_id(self, template_id: str) -> Optional[ProfileTemplate]:
        data = await self._data_source.get_by_id(template_id)
        if data:
            return ProfileTemplate.from_dict(data)
        return None

    async def save_db(self, template: ProfileTemplate) -> None:
        await self._data_source.save(template.to_dict())
