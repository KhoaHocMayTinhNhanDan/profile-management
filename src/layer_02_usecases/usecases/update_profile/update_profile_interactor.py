from src.layer_02_usecases.gateways_interface.i_update_profile_repository import (
    IUpdateProfileRepository,
)
from src.layer_01_entities.profile import Profile
from .update_profile_dto import UpdateProfileInput, UpdateProfileOutput


class UpdateProfileInteractor:
    def __init__(self, repository: IUpdateProfileRepository):
        self._repository = repository

    async def execute(self, input_data: UpdateProfileInput) -> UpdateProfileOutput:
        if not input_data.profile_id:
            return UpdateProfileOutput(
                status="error", message="Profile ID cannot be empty."
            )

        profile = await self._repository.get_profile(input_data.profile_id)
        if not profile:
            return UpdateProfileOutput(
                status="error",
                message=f"Profile with ID '{input_data.profile_id}' not found.",
            )

        # Load Template to validate updated dynamic_data
        template = await self._repository.get_template(profile.template_id)
        if not template:
            return UpdateProfileOutput(
                status="error",
                message=f"Template '{profile.template_id}' associated with profile not found.",
            )

        # Validate dynamic data
        is_valid, validation_errors = template.validate_data(input_data.dynamic_data)
        if not is_valid:
            return UpdateProfileOutput(
                status="error", message="Validation failed.", errors=validation_errors
            )

        # Apply updates
        profile.dynamic_data = input_data.dynamic_data
        if input_data.status:
            profile.status = input_data.status

        await self._repository.save_db(profile)
        return UpdateProfileOutput(
            status="success",
            message=f"Profile '{input_data.profile_id}' updated successfully.",
        )
