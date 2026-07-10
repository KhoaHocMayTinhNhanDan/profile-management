from src.layer_02_usecases.gateways_interface.i_generate_document_from_template_repository import IGenerateDocumentFromTemplateRepository
from src.layer_01_entities.document import Document
from .generate_document_from_template_dto import GenerateDocumentFromTemplateInput, GenerateDocumentFromTemplateOutput
import uuid
import os

class GenerateDocumentFromTemplateInteractor:
    def __init__(self, repository: IGenerateDocumentFromTemplateRepository):
        self._repository = repository

    async def execute(self, input_data: GenerateDocumentFromTemplateInput) -> GenerateDocumentFromTemplateOutput:
        profile = await self._repository.get_profile(input_data.profile_id)
        if not profile:
            return GenerateDocumentFromTemplateOutput(status="error", message=f"Profile '{input_data.profile_id}' not found.")

        # Prepare local output path
        output_dir = os.path.join("appdata", "generated_docs", input_data.profile_id)
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, input_data.output_doc_name)

        # Call data source to replace placeholders with dynamic_data using python-docx
        try:
            generated_url = await self._repository.generate_document(
                template_doc_path=input_data.template_doc_path,
                data=profile.dynamic_data,
                output_path=output_path
            )
        except Exception as e:
            return GenerateDocumentFromTemplateOutput(status="error", message=f"Failed to generate docx: {e}")

        # Create new Document Entity
        doc_id = str(uuid.uuid4())
        # Calculate size
        size = os.path.getsize(output_path) if os.path.exists(output_path) else 0

        # Calculate a simple checksum
        import hashlib
        checksum = ""
        if os.path.exists(output_path):
            with open(output_path, "rb") as f:
                checksum = hashlib.sha256(f.read()).hexdigest()

        new_doc = Document(
            document_id=doc_id,
            name=input_data.output_doc_name,
            url=generated_url,
            file_type="docx",
            size=size,
            version="1.0",
            is_locked=False,
            locked_by="",
            checksum=checksum
        )

        profile.documents.append(new_doc)
        await self._repository.save_db(profile)

        return GenerateDocumentFromTemplateOutput(
            status="success",
            message="Document generated from template successfully.",
            document_id=doc_id,
            document_url=generated_url
        )
