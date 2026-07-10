from src.layer_02_usecases.gateways_interface.i_checkin_document_repository import ICheckinDocumentRepository
from .checkin_document_dto import CheckinDocumentInput, CheckinDocumentOutput

class CheckinDocumentInteractor:
    def __init__(self, repository: ICheckinDocumentRepository):
        self._repository = repository

    async def execute(self, input_data: CheckinDocumentInput) -> CheckinDocumentOutput:
        profile = await self._repository.get_profile(input_data.profile_id)
        if not profile:
            return CheckinDocumentOutput(status="error", message=f"Profile '{input_data.profile_id}' not found.")

        target_doc = None
        for doc in profile.documents:
            if doc.document_id == input_data.document_id:
                target_doc = doc
                break

        if not target_doc:
            return CheckinDocumentOutput(status="error", message=f"Document '{input_data.document_id}' not found in profile.")

        if not target_doc.is_locked:
            return CheckinDocumentOutput(status="error", message="Document is not locked.")

        if target_doc.locked_by != input_data.user_id:
            return CheckinDocumentOutput(
                status="error", 
                message=f"Document is locked by user '{target_doc.locked_by}', not you."
            )

        # Check if file has actually changed based on checksum (optional validation but useful)
        if target_doc.checksum == input_data.new_checksum:
            # Unlock without version bump if no change occurred
            target_doc.is_locked = False
            target_doc.locked_by = ""
            await self._repository.save_db(profile)
            return CheckinDocumentOutput(
                status="success", 
                message="No changes detected in document. Document unlocked.", 
                new_version=target_doc.version
            )

        # Increment version
        try:
            curr_ver = float(target_doc.version)
            next_ver = f"{curr_ver + 0.1:.1f}"
        except ValueError:
            next_ver = target_doc.version + ".1"

        # Update metadata and unlock
        target_doc.version = next_ver
        target_doc.url = input_data.new_url
        target_doc.size = input_data.new_size
        target_doc.checksum = input_data.new_checksum
        target_doc.is_locked = False
        target_doc.locked_by = ""

        await self._repository.save_db(profile)
        return CheckinDocumentOutput(
            status="success",
            message="Document checked in and version bumped successfully.",
            new_version=next_ver
        )
