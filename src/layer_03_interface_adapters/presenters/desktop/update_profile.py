from src.layer_02_usecases.usecases.update_profile.update_profile_dto import (
    UpdateProfileOutput,
)


class UpdateProfilePresenter:
    def present(self, output: UpdateProfileOutput) -> dict:
        return {"status": output.status, "message": output.message}
