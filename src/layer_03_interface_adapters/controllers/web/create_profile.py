from src.layer_02_usecases.usecases.create_profile.create_profile_dto import (
    CreateProfileInput,
)
from src.layer_02_usecases.usecases.create_profile.create_profile_interactor import (
    CreateProfileInteractor,
)
from src.layer_03_interface_adapters.presenters.web.create_profile import (
    CreateProfilePresenter,
)


class CreateProfileController:
    def __init__(self, interactor: CreateProfileInteractor):
        self._interactor = interactor
        self._presenter = CreateProfilePresenter()

    async def handle_request(self, request_data: dict) -> dict:
        input_data = CreateProfileInput(
            profile_id=request_data.get("profile_id", ""),
            template_id=request_data.get("template_id", ""),
            dynamic_data=request_data.get("dynamic_data", {}),
        )
        output_data = await self._interactor.execute(input_data)
        return self._presenter.present(output_data)
