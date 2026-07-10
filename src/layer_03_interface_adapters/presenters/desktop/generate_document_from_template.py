from src.layer_02_usecases.usecases.generate_document_from_template.generate_document_from_template_dto import GenerateDocumentFromTemplateOutput

class GenerateDocumentFromTemplatePresenter:
    def present(self, output: GenerateDocumentFromTemplateOutput) -> dict:
        return {"status": output.status, "message": output.message}
