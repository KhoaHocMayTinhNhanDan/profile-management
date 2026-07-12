from src.layer_02_usecases.gateways_interface.i_create_profile_template_repository import (
    ICreateProfileTemplateRepository,
)
from src.layer_01_entities.profile_template import ProfileTemplate
from .create_profile_template_dto import (
    CreateProfileTemplateInput,
    CreateProfileTemplateOutput,
)
import os
import shutil
from src.shared.logger.app_logger import get_logger

logger = get_logger(__name__)


class CreateProfileTemplateInteractor:
    def __init__(self, repository: ICreateProfileTemplateRepository):
        self._repository = repository

    async def execute(
        self, input_data: CreateProfileTemplateInput
    ) -> CreateProfileTemplateOutput:
        if not input_data.template_id:
            return CreateProfileTemplateOutput(
                status="error", message="Template ID cannot be empty."
            )

        existing = await self._repository.get_by_id(input_data.template_id)
        if existing and not input_data.is_update:
            return CreateProfileTemplateOutput(
                status="error",
                message=f"Template with ID '{input_data.template_id}' already exists.",
            )

        dest_dir = os.path.join("appdata", "templates", input_data.template_id)
        os.makedirs(dest_dir, exist_ok=True)
        saved_template_dir = dest_dir

        if input_data.selected_files is not None:
            # Mode A: User selected specific files (could be from different paths)
            import tempfile
            import re

            # 1. Staging: copy files to a temporary directory with their new prefix indices
            with tempfile.TemporaryDirectory() as tmp_dir:
                for idx, fpath in enumerate(input_data.selected_files, start=1):
                    if not fpath or not os.path.exists(fpath):
                        continue
                    filename = os.path.basename(fpath)

                    # Clean any existing numeric prefix to avoid duplication (e.g. "03 - 01 - BB.docx")
                    # Matches "01 - ", "02-", "3. ", "04_ ", etc.
                    cleaned = re.sub(r"^[\d\s\-\.\_]+", "", filename)
                    new_filename = f"{idx:02d} - {cleaned}"

                    try:
                        shutil.copy2(fpath, os.path.join(tmp_dir, new_filename))
                    except Exception as e:
                        logger.error(
                            f"Failed to copy template file {fpath} to temp staging: {e}"
                        )

                # 2. Clear target dest_dir safely
                if os.path.exists(dest_dir):
                    try:
                        shutil.rmtree(dest_dir)
                    except Exception as e:
                        logger.error(
                            f"Failed to clear target directory {dest_dir}: {e}"
                        )
                os.makedirs(dest_dir, exist_ok=True)

                # 3. Move all staged files from temp directory to dest_dir
                for f in os.listdir(tmp_dir):
                    try:
                        shutil.move(os.path.join(tmp_dir, f), os.path.join(dest_dir, f))
                    except Exception as e:
                        logger.error(
                            f"Failed to move staged file {f} to target {dest_dir}: {e}"
                        )
        elif input_data.template_dir:
            # Mode B: Folder-driven import (fallback/backward-compatible mode)
            src_dir = input_data.template_dir
            if os.path.exists(src_dir) and os.path.isdir(src_dir):
                # Copy all docx files
                docx_files = [
                    f
                    for f in os.listdir(src_dir)
                    if f.endswith(".docx") and not f.startswith("~$")
                ]
                for f in docx_files:
                    src_file = os.path.join(src_dir, f)
                    dest_file = os.path.join(dest_dir, f)
                    if os.path.abspath(src_file) != os.path.abspath(dest_file):
                        shutil.copy2(src_file, dest_file)
            else:
                saved_template_dir = input_data.template_dir
        else:
            # If no files selected and no folder, keep whatever is in dest_dir (or empty)
            pass

        # Upgrade all text placeholders to Content Controls inside the copied template files
        fields = [field["name"] for field in input_data.fields_schema]
        if fields and os.path.exists(dest_dir):
            from src.shared.utils.docx_helper import upgrade_docx_placeholders

            for f in os.listdir(dest_dir):
                if f.endswith(".docx") and not f.startswith("~$"):
                    fpath = os.path.join(dest_dir, f)
                    try:
                        upgrade_docx_placeholders(fpath, fields, fpath)
                    except Exception as e:
                        logger.error(
                            f"Failed to auto-upgrade placeholders in {fpath}: {e}"
                        )

        # Create ProfileTemplate Entity
        template = ProfileTemplate(
            template_id=input_data.template_id,
            name=input_data.name,
            fields_schema=input_data.fields_schema,
            template_dir=saved_template_dir,
        )

        await self._repository.save_db(template)

        msg = (
            f"Mẫu hồ sơ '{input_data.name}' đã được cập nhật thành công."
            if input_data.is_update
            else f"Mẫu hồ sơ '{input_data.name}' đã được tạo thành công."
        )
        return CreateProfileTemplateOutput(status="success", message=msg)
