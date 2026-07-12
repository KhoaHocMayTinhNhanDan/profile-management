from src.layer_02_usecases.usecases.checkout_document.checkout_document_dto import (
    CheckoutDocumentOutput,
)


class CheckoutDocumentPresenter:
    def present(self, output: CheckoutDocumentOutput) -> dict:
        return {
            "status": output.status,
            "message": output.message,
            "document_url": output.document_url,
            "local_filename": output.local_filename,
        }
