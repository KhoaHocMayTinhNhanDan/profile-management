from src.layer_02_usecases.gateways_interface.i_create_profile_template_repository import ICreateProfileTemplateRepository
from src.layer_01_entities.profile_template import ProfileTemplate
from .create_profile_template_dto import CreateProfileTemplateInput, CreateProfileTemplateOutput

class CreateProfileTemplateInteractor:
    def __init__(self, repository: ICreateProfileTemplateRepository):
        self._repository = repository

    async def execute(self, input_data: CreateProfileTemplateInput) -> CreateProfileTemplateOutput:
        if not input_data.template_id:
            return CreateProfileTemplateOutput(status="error", message="Template ID cannot be empty.")
            
        existing = await self._repository.get_by_id(input_data.template_id)
        if existing:
            return CreateProfileTemplateOutput(status="error", message=f"Template with ID '{input_data.template_id}' already exists.")

        # Create ProfileTemplate Entity
        template = ProfileTemplate(
            template_id=input_data.template_id,
            name=input_data.name,
            fields_schema=input_data.fields_schema
        )
        
        await self._repository.save_db(template)
        return CreateProfileTemplateOutput(status="success", message=f"Template '{input_data.name}' created successfully.")
