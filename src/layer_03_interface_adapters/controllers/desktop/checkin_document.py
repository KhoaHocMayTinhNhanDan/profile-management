from src.layer_02_usecases.usecases.checkin_document.checkin_document_dto import (
    CheckinDocumentInput,
)
from src.layer_02_usecases.usecases.checkin_document.checkin_document_interactor import (
    CheckinDocumentInteractor,
)
from src.layer_03_interface_adapters.presenters.desktop.checkin_document import (
    CheckinDocumentPresenter,
)


class CheckinDocumentController:
    def __init__(self, interactor: CheckinDocumentInteractor):
        self._interactor = interactor
        self._presenter = CheckinDocumentPresenter()

    async def handle_request(self, request_data: dict) -> dict:
        input_data = CheckinDocumentInput(
            profile_id=request_data.get("profile_id", ""),
            document_id=request_data.get("document_id", ""),
            user_id=request_data.get("user_id", ""),
            new_url=request_data.get("new_url", ""),
            new_size=request_data.get("new_size", 0),
            new_checksum=request_data.get("new_checksum", ""),
        )
        output_data = await self._interactor.execute(input_data)
        return self._presenter.present(output_data)
