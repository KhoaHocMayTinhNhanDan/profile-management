from src.layer_02_usecases.gateways_interface.i_checkout_document_repository import (
    ICheckoutDocumentRepository,
)
from .checkout_document_dto import CheckoutDocumentInput, CheckoutDocumentOutput


class CheckoutDocumentInteractor:
    def __init__(self, repository: ICheckoutDocumentRepository):
        self._repository = repository

    async def execute(
        self, input_data: CheckoutDocumentInput
    ) -> CheckoutDocumentOutput:
        profile = await self._repository.get_profile(input_data.profile_id)
        if not profile:
            return CheckoutDocumentOutput(
                status="error", message=f"Profile '{input_data.profile_id}' not found."
            )

        target_doc = None
        for doc in profile.documents:
            if doc.document_id == input_data.document_id:
                target_doc = doc
                break

        if not target_doc:
            return CheckoutDocumentOutput(
                status="error",
                message=f"Document '{input_data.document_id}' not found in profile.",
            )

        if target_doc.is_locked and target_doc.locked_by != input_data.user_id:
            return CheckoutDocumentOutput(
                status="error",
                message=f"Document is currently locked by user '{target_doc.locked_by}'.",
            )

        # Lock the document for the current user
        target_doc.is_locked = True
        target_doc.locked_by = input_data.user_id

        await self._repository.save_db(profile)
        return CheckoutDocumentOutput(
            status="success",
            message="Document checked out successfully. Locked for editing.",
            document_url=target_doc.url,
            local_filename=target_doc.name,
        )
