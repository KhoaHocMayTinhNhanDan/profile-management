from src.layer_02_usecases.usecases.generate_document_from_template.generate_document_from_template_dto import GenerateDocumentFromTemplateInput
from src.layer_02_usecases.usecases.generate_document_from_template.generate_document_from_template_interactor import GenerateDocumentFromTemplateInteractor
from src.layer_03_interface_adapters.presenters.web.generate_document_from_template import GenerateDocumentFromTemplatePresenter

class GenerateDocumentFromTemplateController:
    def __init__(self, interactor: GenerateDocumentFromTemplateInteractor):
        self._interactor = interactor
        self._presenter = GenerateDocumentFromTemplatePresenter()

    async def handle_request(self, request_data: dict) -> dict:
        input_data = GenerateDocumentFromTemplateInput(
            profile_id=request_data.get("profile_id", ""),
            template_doc_path=request_data.get("template_doc_path", ""),
            output_doc_name=request_data.get("output_doc_name", "")
        )
        output_data = await self._interactor.execute(input_data)
        return self._presenter.present(output_data)
