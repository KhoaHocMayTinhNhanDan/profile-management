from dataclasses import dataclass

@dataclass
class CreateProfileTemplateInput:
    template_id: str
    name: str
    fields_schema: list

@dataclass
class CreateProfileTemplateOutput:
    status: str
    message: str
