import pytest
import asyncio
from unittest.mock import Mock
from src.layer_02_usecases.usecases.generate_document_from_template.generate_document_from_template_dto import GenerateDocumentFromTemplateInput, GenerateDocumentFromTemplateOutput
from src.layer_02_usecases.usecases.generate_document_from_template.generate_document_from_template_interactor import GenerateDocumentFromTemplateInteractor
from src.layer_02_usecases.gateways_interface.i_generate_document_from_template_repository import IGenerateDocumentFromTemplateRepository
from src.layer_01_entities.profile import Profile

def test_generate_document_from_template_success():
    mock_repo = Mock(spec=IGenerateDocumentFromTemplateRepository)
    async def mock_get_profile(profile_id):
        return Profile(
            profile_id="profile_1",
            template_id="nhan_su",
            status="Draft",
            dynamic_data={"full_name": "Nguyen Van A"}
        )
    async def mock_generate_document(*args, **kwargs):
        return "file:///tmp/generated.docx"
    async def mock_save(*args, **kwargs):
        pass

    mock_repo.get_profile = mock_get_profile
    mock_repo.generate_document = mock_generate_document
    mock_repo.save_db = mock_save

    usecase = GenerateDocumentFromTemplateInteractor(mock_repo)
    input_dto = GenerateDocumentFromTemplateInput(
        profile_id="profile_1",
        template_doc_path="D:\\DEV\\python\\profile-management\\tests\\unit\\layer_02_usecases\\usecases\\test_create_profile.py", # exists
        output_doc_name="generated.docx"
    )

    output_dto = asyncio.run(usecase.execute(input_dto))

    assert isinstance(output_dto, GenerateDocumentFromTemplateOutput)
    assert output_dto.status == "success"
