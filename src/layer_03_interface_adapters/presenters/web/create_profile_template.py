from src.layer_02_usecases.usecases.create_profile_template.create_profile_template_dto import CreateProfileTemplateOutput

class CreateProfileTemplatePresenter:
    def present(self, output: CreateProfileTemplateOutput) -> dict:
        return {"status": output.status, "message": output.message}
