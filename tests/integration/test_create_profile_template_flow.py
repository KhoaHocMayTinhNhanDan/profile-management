import unittest
import asyncio
from unittest.mock import Mock
from src.layer_02_usecases.usecases.create_profile_template.create_profile_template_interactor import CreateProfileTemplateInteractor
from src.layer_03_interface_adapters.controllers.desktop.create_profile_template import CreateProfileTemplateController
from src.layer_02_usecases.gateways_interface.i_create_profile_template_repository import ICreateProfileTemplateRepository

class TestCreateProfileTemplateIntegrationFlow(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock(spec=ICreateProfileTemplateRepository)
        async def mock_get_by_id(*args, **kwargs):
            return None
        async def mock_save(*args, **kwargs):
            pass
        self.mock_repo.get_by_id = mock_get_by_id
        self.mock_repo.save_db = mock_save
        
        self.interactor = CreateProfileTemplateInteractor(self.mock_repo)
        self.controller = CreateProfileTemplateController(self.interactor)

    def test_integration_flow_success(self):
        output_dict = asyncio.run(self.controller.handle_request({
            "template_id": "nhan_su",
            "name": "Hồ sơ nhân sự",
            "fields_schema": []
        }))
        
        self.assertIsInstance(output_dict, dict)
        self.assertEqual(output_dict.get("status"), "success")
