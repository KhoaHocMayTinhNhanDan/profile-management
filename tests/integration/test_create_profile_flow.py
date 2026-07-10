import unittest
import asyncio
from unittest.mock import Mock
from src.layer_02_usecases.usecases.create_profile.create_profile_interactor import CreateProfileInteractor
from src.layer_03_interface_adapters.controllers.desktop.create_profile import CreateProfileController
from src.layer_02_usecases.gateways_interface.i_create_profile_repository import ICreateProfileRepository
from src.layer_01_entities.profile_template import ProfileTemplate

class TestCreateProfileIntegrationFlow(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock(spec=ICreateProfileRepository)
        async def mock_get_profile(*args, **kwargs):
            return None
        async def mock_get_template(*args, **kwargs):
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
        
        self.interactor = CreateProfileInteractor(self.mock_repo)
        self.controller = CreateProfileController(self.interactor)

    def test_integration_flow_success(self):
        output_dict = asyncio.run(self.controller.handle_request({
            "profile_id": "profile_1",
            "template_id": "nhan_su",
            "dynamic_data": {"full_name": "Nguyen Van A"}
        }))
        
        self.assertIsInstance(output_dict, dict)
        self.assertEqual(output_dict.get("status"), "success")
