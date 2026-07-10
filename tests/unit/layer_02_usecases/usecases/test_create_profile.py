import pytest
import asyncio
from unittest.mock import Mock
from src.layer_02_usecases.usecases.create_profile.create_profile_dto import CreateProfileInput, CreateProfileOutput
from src.layer_02_usecases.usecases.create_profile.create_profile_interactor import CreateProfileInteractor
from src.layer_02_usecases.gateways_interface.i_create_profile_repository import ICreateProfileRepository
from src.layer_01_entities.profile_template import ProfileTemplate

def test_create_profile_success():
    mock_repo = Mock(spec=ICreateProfileRepository)
    async def mock_get_profile(*args, **kwargs):
        return None
    async def mock_get_template(*args, **kwargs):
        # Return a mock template with field schema
        return ProfileTemplate(
            template_id="nhan_su",
            name="Hồ sơ nhân sự",
            fields_schema=[{"name": "full_name", "type": "string", "required": True}]
        )
    async def mock_save(*args, **kwargs):
        pass

    mock_repo.get_profile = mock_get_profile
    mock_repo.get_template = mock_get_template
    mock_repo.save_db = mock_save

    usecase = CreateProfileInteractor(mock_repo)
    input_dto = CreateProfileInput(
        profile_id="profile_1",
        template_id="nhan_su",
        dynamic_data={"full_name": "Nguyen Van A"}
    )

    output_dto = asyncio.run(usecase.execute(input_dto))

    assert isinstance(output_dto, CreateProfileOutput)
    assert output_dto.status == "success"
