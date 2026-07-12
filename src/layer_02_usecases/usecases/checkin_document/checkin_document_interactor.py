from src.layer_02_usecases.gateways_interface.i_checkin_document_repository import (
    ICheckinDocumentRepository,
)
from .checkin_document_dto import CheckinDocumentInput, CheckinDocumentOutput


class CheckinDocumentInteractor:
    def __init__(self, repository: ICheckinDocumentRepository):
        self._repository = repository

    async def execute(self, input_data: CheckinDocumentInput) -> CheckinDocumentOutput:
        profile = await self._repository.get_profile(input_data.profile_id)
        if not profile:
            return CheckinDocumentOutput(
                status="error", message=f"Profile '{input_data.profile_id}' not found."
            )

        target_doc = None
        for doc in profile.documents:
            if doc.document_id == input_data.document_id:
                target_doc = doc
                break

        if not target_doc:
            return CheckinDocumentOutput(
                status="error",
                message=f"Document '{input_data.document_id}' not found in profile.",
            )

        if not target_doc.is_locked:
            return CheckinDocumentOutput(
                status="error", message="Document is not locked."
            )

        if target_doc.locked_by != input_data.user_id:
            return CheckinDocumentOutput(
                status="error",
                message=f"Document is locked by user '{target_doc.locked_by}', not you.",
            )

        # Resolve original and temp file paths
        import os
        import urllib.parse
        import shutil
        import hashlib

        doc_url = target_doc.url or ""
        if doc_url.startswith("file:///"):
            original_path = doc_url.replace("file:///", "")
        else:
            original_path = doc_url
        original_path = os.path.abspath(urllib.parse.unquote(original_path))

        temp_dir = os.path.join("appdata", "temp_editing", input_data.profile_id)
        temp_path = os.path.abspath(os.path.join(temp_dir, target_doc.name))

        # Check if caller passed metadata or if we should auto-sync from temp path
        new_url = input_data.new_url
        new_size = input_data.new_size
        new_checksum = input_data.new_checksum

        if not new_size:
            # Auto-sync flow: copy temp file back, calculate size/checksum
            if os.path.exists(temp_path):
                copied = False
                for attempt in range(5):
                    try:
                        shutil.copy2(temp_path, original_path)
                        copied = True
                        break
                    except Exception:
                        import time

                        time.sleep(0.5)

                if not copied:
                    return CheckinDocumentOutput(
                        status="error",
                        message="Không thể đồng bộ vì tệp đang bị MS Word khóa độc quyền. Vui lòng đóng Word và thử lại!",
                    )

                # Clean up temp file
                try:
                    os.remove(temp_path)
                except Exception:
                    pass

                new_size = os.path.getsize(original_path)
                with open(original_path, "rb") as f:
                    new_checksum = hashlib.sha256(f.read()).hexdigest()
                new_url = "file:///" + os.path.abspath(original_path).replace("\\", "/")
            else:
                # Temp file does not exist, and caller didn't pass new_size -> Force Unlock (Recovery)
                target_doc.is_locked = False
                target_doc.locked_by = ""
                await self._repository.save_db(profile)
                return CheckinDocumentOutput(
                    status="success",
                    message="Document unlocked (force checkout recovery).",
                    new_version=target_doc.version,
                )

        # Check if file has actually changed based on checksum
        if target_doc.checksum == new_checksum:
            # Unlock without version bump if no change occurred
            target_doc.is_locked = False
            target_doc.locked_by = ""
            await self._repository.save_db(profile)
            return CheckinDocumentOutput(
                status="success",
                message="No changes detected in document. Document unlocked.",
                new_version=target_doc.version,
            )

        # Increment version
        try:
            curr_ver = float(target_doc.version)
            next_ver = f"{curr_ver + 0.1:.1f}"
        except ValueError:
            next_ver = target_doc.version + ".1"

        # Update metadata and unlock
        target_doc.version = next_ver
        target_doc.url = new_url
        target_doc.size = new_size
        target_doc.checksum = new_checksum
        target_doc.is_locked = False
        target_doc.locked_by = ""

        # 2-way sync: extract Content Control values from the saved Word file and update profile's dynamic_data
        from src.shared.utils.docx_helper import extract_document_content_controls

        file_path = original_path

        if os.path.isfile(file_path):
            try:
                extracted = extract_document_content_controls(
                    file_path, profile.dynamic_data
                )
                updated_any = False
                for tag, val in extracted.items():
                    if tag in profile.dynamic_data:
                        cleaned_val = val.strip()
                        if profile.dynamic_data[tag] != cleaned_val:
                            profile.dynamic_data[tag] = cleaned_val
                            updated_any = True

                # If any shared fields updated, push the new dynamic_data values
                # into all other documents of the profile to keep them synchronized
                if updated_any:
                    from src.shared.utils.docx_helper import (
                        fill_document_content_controls,
                    )

                    for doc in profile.documents:
                        o_url = doc.url or ""
                        if o_url.startswith("file:///"):
                            o_path = o_url.replace("file:///", "")
                        else:
                            o_path = o_url
                        o_path = os.path.abspath(urllib.parse.unquote(o_path))

                        if os.path.isfile(o_path):
                            try:
                                fill_document_content_controls(
                                    o_path, profile.dynamic_data, o_path
                                )
                                doc.size = os.path.getsize(o_path)
                                import hashlib

                                with open(o_path, "rb") as f:
                                    doc.checksum = hashlib.sha256(f.read()).hexdigest()
                            except Exception as ex:
                                from src.shared.logger.app_logger import (
                                    get_logger,
                                )

                                logger = get_logger(__name__)
                                logger.error(
                                    f"Failed to auto-sync shared fields to {o_path}: {ex}"
                                )
            except Exception as e:
                from src.shared.logger.app_logger import get_logger

                logger = get_logger(__name__)
                logger.error(f"Failed to perform 2-way sync during checkin: {e}")

        await self._repository.save_db(profile)
        return CheckinDocumentOutput(
            status="success",
            message="Document checked in and version bumped successfully.",
            new_version=next_ver,
        )
