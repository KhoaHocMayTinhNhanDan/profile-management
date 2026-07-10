import pytest
import asyncio
from unittest.mock import Mock
from src.layer_02_usecases.usecases.update_profile.update_profile_dto import UpdateProfileInput, UpdateProfileOutput
from src.layer_02_usecases.usecases.update_profile.update_profile_interactor import UpdateProfileInteractor
from src.layer_02_usecases.gateways_interface.i_update_profile_repository import IUpdateProfileRepository
from src.layer_01_entities.profile import Profile
from src.layer_01_entities.profile_template import ProfileTemplate

def test_update_profile_success():
    mock_repo = Mock(spec=IUpdateProfileRepository)
    async def mock_get_profile(profile_id):
        return Profile(
            profile_id="profile_1",
            template_id="nhan_su",
            status="Draft",
            dynamic_data={"full_name": "Old Name"}
        )
    async def mock_get_template(template_id):
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

    usecase = UpdateProfileInteractor(mock_repo)
    input_dto = UpdateProfileInput(
        profile_id="profile_1",
        dynamic_data={"full_name": "New Name"}
    )

    output_dto = asyncio.run(usecase.execute(input_dto))

    assert isinstance(output_dto, UpdateProfileOutput)
    assert output_dto.status == "success"
