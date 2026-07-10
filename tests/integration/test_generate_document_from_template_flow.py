import unittest
import asyncio
from unittest.mock import Mock
from src.layer_02_usecases.usecases.generate_document_from_template.generate_document_from_template_interactor import GenerateDocumentFromTemplateInteractor
from src.layer_03_interface_adapters.controllers.desktop.generate_document_from_template import GenerateDocumentFromTemplateController
from src.layer_02_usecases.gateways_interface.i_generate_document_from_template_repository import IGenerateDocumentFromTemplateRepository
from src.layer_01_entities.profile import Profile

class TestGenerateDocumentFromTemplateIntegrationFlow(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock(spec=IGenerateDocumentFromTemplateRepository)
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
        self.mock_repo.get_profile = mock_get_profile
        self.mock_repo.generate_document = mock_generate_document
        self.mock_repo.save_db = mock_save
        
        self.interactor = GenerateDocumentFromTemplateInteractor(self.mock_repo)
        self.controller = GenerateDocumentFromTemplateController(self.interactor)

    def test_integration_flow_success(self):
        output_dict = asyncio.run(self.controller.handle_request({
            "profile_id": "profile_1",
            "template_doc_path": "D:\\DEV\\python\\profile-management\\tests\\unit\\layer_02_usecases\\usecases\\test_create_profile.py", # exists
            "output_doc_name": "generated.docx"
        }))
        
        self.assertIsInstance(output_dict, dict)
        self.assertEqual(output_dict.get("status"), "success")
