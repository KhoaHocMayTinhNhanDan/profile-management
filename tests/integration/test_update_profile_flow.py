import unittest
import asyncio
from unittest.mock import Mock
from src.layer_02_usecases.usecases.update_profile.update_profile_interactor import UpdateProfileInteractor
from src.layer_03_interface_adapters.controllers.desktop.update_profile import UpdateProfileController
from src.layer_02_usecases.gateways_interface.i_update_profile_repository import IUpdateProfileRepository
from src.layer_01_entities.profile import Profile
from src.layer_01_entities.profile_template import ProfileTemplate

class TestUpdateProfileIntegrationFlow(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock(spec=IUpdateProfileRepository)
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
        self.mock_repo.get_profile = mock_get_profile
        self.mock_repo.get_template = mock_get_template
        self.mock_repo.save_db = mock_save
        
        self.interactor = UpdateProfileInteractor(self.mock_repo)
        self.controller = UpdateProfileController(self.interactor)

    def test_integration_flow_success(self):
        output_dict = asyncio.run(self.controller.handle_request({
            "profile_id": "profile_1",
            "dynamic_data": {"full_name": "New Name"}
        }))
        
        self.assertIsInstance(output_dict, dict)
        self.assertEqual(output_dict.get("status"), "success")
