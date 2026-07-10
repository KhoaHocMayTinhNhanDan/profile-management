from src.layer_02_usecases.gateways_interface.i_generate_document_from_template_repository import IGenerateDocumentFromTemplateRepository
from src.layer_03_interface_adapters.gateways.outbound.i_generate_document_from_template_data_source import IGenerateDocumentFromTemplateDataSource
from src.layer_01_entities.profile import Profile
from typing import Optional

class GenerateDocumentFromTemplateRepository(IGenerateDocumentFromTemplateRepository):
    def __init__(self, data_source: IGenerateDocumentFromTemplateDataSource):
        self._data_source = data_source

    async def get_profile(self, profile_id: str) -> Optional[Profile]:
        data = await self._data_source.get_profile(profile_id)
        if data:
            return Profile.from_dict(data)
        return None

    async def save_db(self, profile: Profile) -> None:
        await self._data_source.save(profile.to_dict())

    async def generate_document(self, template_doc_path: str, data: dict, output_path: str) -> str:
        return await self._data_source.generate_docx(template_doc_path, data, output_path)
