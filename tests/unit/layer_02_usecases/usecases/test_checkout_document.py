import pytest
import asyncio
from unittest.mock import Mock
from src.layer_02_usecases.usecases.checkout_document.checkout_document_dto import CheckoutDocumentInput, CheckoutDocumentOutput
from src.layer_02_usecases.usecases.checkout_document.checkout_document_interactor import CheckoutDocumentInteractor
from src.layer_02_usecases.gateways_interface.i_checkout_document_repository import ICheckoutDocumentRepository
from src.layer_01_entities.profile import Profile
from src.layer_01_entities.document import Document

def test_checkout_document_success():
    mock_repo = Mock(spec=ICheckoutDocumentRepository)
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

    mock_repo.get_profile = mock_get_profile
    mock_repo.save_db = mock_save

    usecase = CheckoutDocumentInteractor(mock_repo)
    input_dto = CheckoutDocumentInput(
        profile_id="profile_1",
        document_id="doc_123",
        user_id="user_dong"
    )

    output_dto = asyncio.run(usecase.execute(input_dto))

    assert isinstance(output_dto, CheckoutDocumentOutput)
    assert output_dto.status == "success"
