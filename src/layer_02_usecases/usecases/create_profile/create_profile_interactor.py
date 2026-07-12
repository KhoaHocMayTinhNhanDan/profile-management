from src.layer_02_usecases.gateways_interface.i_create_profile_repository import (
    ICreateProfileRepository,
)
from src.layer_01_entities.profile import Profile
from src.layer_01_entities.document import Document
from .create_profile_dto import CreateProfileInput, CreateProfileOutput
from datetime import datetime


class CreateProfileInteractor:
    def __init__(self, repository: ICreateProfileRepository):
        self._repository = repository

    async def execute(self, input_data: CreateProfileInput) -> CreateProfileOutput:
        if not input_data.profile_id:
            return CreateProfileOutput(
                status="error", message="Profile ID cannot be empty."
            )

        existing_profile = await self._repository.get_profile(input_data.profile_id)
        if existing_profile:
            return CreateProfileOutput(
                status="error",
                message=f"Profile with ID '{input_data.profile_id}' already exists.",
            )

        template = await self._repository.get_template(input_data.template_id)
        if not template:
            return CreateProfileOutput(
                status="error",
                message=f"Profile template '{input_data.template_id}' not found.",
            )

        # Validate dynamic data using template validation engine
        is_valid, validation_errors = template.validate_data(input_data.dynamic_data)
        if not is_valid:
            return CreateProfileOutput(
                status="error", message="Validation failed.", errors=validation_errors
            )

        # Map list of doc dicts to Document Entities
        docs = [Document.from_dict(d) for d in input_data.documents]

        # Create Profile Entity
        profile = Profile(
            profile_id=input_data.profile_id,
            template_id=input_data.template_id,
            status="Draft",
            dynamic_data=input_data.dynamic_data,
            documents=docs,
            created_at=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        )

        await self._repository.save_db(profile)
        return CreateProfileOutput(
            status="success",
            message=f"Profile '{input_data.profile_id}' created successfully as Draft.",
        )
