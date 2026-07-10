import unittest
import asyncio
from unittest.mock import Mock
from src.layer_02_usecases.usecases.checkin_document.checkin_document_interactor import CheckinDocumentInteractor
from src.layer_03_interface_adapters.controllers.desktop.checkin_document import CheckinDocumentController
from src.layer_02_usecases.gateways_interface.i_checkin_document_repository import ICheckinDocumentRepository
from src.layer_01_entities.profile import Profile
from src.layer_01_entities.document import Document

class TestCheckinDocumentIntegrationFlow(unittest.TestCase):
    def setUp(self):
        self.mock_repo = Mock(spec=ICheckinDocumentRepository)
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
                    version="1.0",
                    is_locked=True,
                    locked_by="user_dong",
                    checksum="old_hash"
                )]
            )
        async def mock_save(*args, **kwargs):
            pass
        self.mock_repo.get_profile = mock_get_profile
        self.mock_repo.save_db = mock_save
        
        self.interactor = CheckinDocumentInteractor(self.mock_repo)
        self.controller = CheckinDocumentController(self.interactor)

    def test_integration_flow_success(self):
        output_dict = asyncio.run(self.controller.handle_request({
            "profile_id": "profile_1",
            "document_id": "doc_123",
            "user_id": "user_dong",
            "new_url": "file://tmp/HD_new.docx",
            "new_size": 1050,
            "new_checksum": "new_hash"
        }))
        
        self.assertIsInstance(output_dict, dict)
        self.assertEqual(output_dict.get("status"), "success")
