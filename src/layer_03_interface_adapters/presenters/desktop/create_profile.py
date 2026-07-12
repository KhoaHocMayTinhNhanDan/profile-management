from src.layer_02_usecases.usecases.create_profile.create_profile_dto import (
    CreateProfileOutput,
)


class CreateProfilePresenter:
    def present(self, output: CreateProfileOutput) -> dict:
        return {"status": output.status, "message": output.message}
