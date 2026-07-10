from src.layer_02_usecases.usecases.create_profile_template.create_profile_template_dto import CreateProfileTemplateInput
from src.layer_02_usecases.usecases.create_profile_template.create_profile_template_interactor import CreateProfileTemplateInteractor
from src.layer_03_interface_adapters.presenters.desktop.create_profile_template import CreateProfileTemplatePresenter

class CreateProfileTemplateController:
    def __init__(self, interactor: CreateProfileTemplateInteractor):
        self._interactor = interactor
        self._presenter = CreateProfileTemplatePresenter()

    async def handle_request(self, request_data: dict) -> dict:
        input_data = CreateProfileTemplateInput(
            template_id=request_data.get("template_id", ""),
            name=request_data.get("name", ""),
            fields_schema=request_data.get("fields_schema", [])
        )
        output_data = await self._interactor.execute(input_data)
        return self._presenter.present(output_data)
