from src.layer_02_usecases.usecases.checkin_document.checkin_document_dto import (
    CheckinDocumentOutput,
)


class CheckinDocumentPresenter:
    def present(self, output: CheckinDocumentOutput) -> dict:
        return {"status": output.status, "message": output.message}
