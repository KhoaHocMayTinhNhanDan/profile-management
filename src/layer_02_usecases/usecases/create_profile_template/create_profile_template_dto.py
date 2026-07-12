from dataclasses import dataclass


@dataclass
class CreateProfileTemplateInput:
    template_id: str
    name: str
    fields_schema: list
    template_dir: str = ""
    is_update: bool = False
    selected_files: list | None = None


@dataclass
class CreateProfileTemplateOutput:
    status: str
    message: str
