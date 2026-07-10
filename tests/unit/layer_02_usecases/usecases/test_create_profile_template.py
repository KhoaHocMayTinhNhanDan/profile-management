import pytest
import asyncio
from unittest.mock import Mock
from src.layer_02_usecases.usecases.create_profile_template.create_profile_template_dto import CreateProfileTemplateInput, CreateProfileTemplateOutput
from src.layer_02_usecases.usecases.create_profile_template.create_profile_template_interactor import CreateProfileTemplateInteractor
from src.layer_02_usecases.gateways_interface.i_create_profile_template_repository import ICreateProfileTemplateRepository

def test_create_profile_template_success():
    mock_repo = Mock(spec=ICreateProfileTemplateRepository)
    async def mock_get_by_id(*args, **kwargs):
        return None
    async def mock_save(*args, **kwargs):
        pass
    mock_repo.get_by_id = mock_get_by_id
    mock_repo.save_db = mock_save
    
    usecase = CreateProfileTemplateInteractor(mock_repo)
    input_dto = CreateProfileTemplateInput(
        template_id="nhan_su",
        name="Hồ sơ nhân sự",
        fields_schema=[{"name": "full_name", "type": "string", "required": True}]
    )
    
    output_dto = asyncio.run(usecase.execute(input_dto))
    
    assert isinstance(output_dto, CreateProfileTemplateOutput)
    assert output_dto.status == "success"
