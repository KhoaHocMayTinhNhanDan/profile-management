from src.layer_02_usecases.usecases.checkout_document.checkout_document_dto import CheckoutDocumentInput
from src.layer_02_usecases.usecases.checkout_document.checkout_document_interactor import CheckoutDocumentInteractor
from src.layer_03_interface_adapters.presenters.web.checkout_document import CheckoutDocumentPresenter

class CheckoutDocumentController:
    def __init__(self, interactor: CheckoutDocumentInteractor):
        self._interactor = interactor
        self._presenter = CheckoutDocumentPresenter()

    async def handle_request(self, request_data: dict) -> dict:
        input_data = CheckoutDocumentInput(
            profile_id=request_data.get("profile_id", ""),
            document_id=request_data.get("document_id", ""),
            user_id=request_data.get("user_id", "")
        )
        output_data = await self._interactor.execute(input_data)
        return self._presenter.present(output_data)
