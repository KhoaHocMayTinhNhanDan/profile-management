import unittest
import asyncio
from unittest.mock import Mock
from src.layer_02_usecases.usecases.checkout_document.checkout_document_interactor import CheckoutDocumentInteractor
from src.layer_03_interface_adapters.controllers.desktop.checkout_document import CheckoutDocumentController
from src.layer_02_usecases.gateways_interface.i_checkout_document_repository import ICheckoutDocumentRepository
from src.layer_01_entities.profile import Profile
from src.layer_01_entities.document import Document

class TestCheckoutDocumentIntegrationFlow(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock(spec=ICheckoutDocumentRepository)
        async def mock_get_profile(profile_id):
            return Profile(
                profile_id="profile_1",
                template_id="nhan_su",
                status="Draft",
                dynamic_data={},
                documents=[Document(
                    document_id="doc_123",
                    name="HD.docx",
                    url="file://tmp/HD.docx",
                    file_type="docx",
                    size=1024,
                    is_locked=False,
                    locked_by=""
                )]
            )
        async def mock_save(*args, **kwargs):
            pass
        self.mock_repo.get_profile = mock_get_profile
        self.mock_repo.save_db = mock_save
        
        self.interactor = CheckoutDocumentInteractor(self.mock_repo)
        self.controller = CheckoutDocumentController(self.interactor)

    def test_integration_flow_success(self):
        output_dict = asyncio.run(self.controller.handle_request({
            "profile_id": "profile_1",
            "document_id": "doc_123",
            "user_id": "user_dong"
        }))
        
        self.assertIsInstance(output_dict, dict)
        self.assertEqual(output_dict.get("status"), "success")
