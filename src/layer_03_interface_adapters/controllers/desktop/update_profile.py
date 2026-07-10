from src.layer_02_usecases.usecases.update_profile.update_profile_dto import UpdateProfileInput
from src.layer_02_usecases.usecases.update_profile.update_profile_interactor import UpdateProfileInteractor
from src.layer_03_interface_adapters.presenters.desktop.update_profile import UpdateProfilePresenter

class UpdateProfileController:
    def __init__(self, interactor: UpdateProfileInteractor):
        self._interactor = interactor
        self._presenter = UpdateProfilePresenter()

    async def handle_request(self, request_data: dict) -> dict:
        input_data = UpdateProfileInput(
            profile_id=request_data.get("profile_id", ""),
            dynamic_data=request_data.get("dynamic_data", {}),
            status=request_data.get("status", None)
        )
        output_data = await self._interactor.execute(input_data)
        return self._presenter.present(output_data)
