import re
from datetime import datetime, date


class ProfileTemplate:
    def __init__(
        self, template_id: str, name: str, fields_schema: list, template_dir: str = ""
    ):
        self.template_id = template_id
        self.name = name
        self.fields_schema = fields_schema  # list of dict, e.g., [{"name": "age", "type": "number", "required": True}]
        self.template_dir = template_dir

    def validate_data(self, data: dict) -> tuple[bool, list[str]]:
        errors = []
        schema_dict = {field["name"]: field for field in self.fields_schema}

        # Check required fields
        for field_name, field_def in schema_dict.items():
            if field_def.get("required", False) and field_name not in data:
                errors.append(
                    f"Field '{field_name}' ({field_def.get('label', field_name)}) is required."
                )

        # Validate field types
        for key, value in data.items():
            if key not in schema_dict:
                # Allow extra fields or raise error? Usually DMS allows only defined fields.
                errors.append(
                    f"Field '{key}' is not defined in template '{self.name}'."
                )
                continue

            field_def = schema_dict[key]
            expected_type = field_def.get("type", "string")

            if value is None or value == "":
                if field_def.get("required", False):
                    errors.append(f"Field '{key}' cannot be empty.")
                continue

            if expected_type == "number":
                try:
                    float(value)
                except (ValueError, TypeError):
                    errors.append(f"Field '{key}' must be a number.")
            elif expected_type == "boolean":
                if not isinstance(value, bool) and str(value).lower() not in (
                    "true",
                    "false",
                    "1",
                    "0",
                ):
                    errors.append(f"Field '{key}' must be a boolean.")
            elif expected_type == "date":
                # Check simple YYYY-MM-DD
                if isinstance(value, str):
                    if not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
                        errors.append(
                            f"Field '{key}' must be a date in YYYY-MM-DD format."
                        )
                    else:
                        try:
                            datetime.strptime(value, "%Y-%m-%d")
                        except ValueError:
                            errors.append(f"Field '{key}' contains an invalid date.")
                elif not isinstance(value, (datetime, date)):
                    errors.append(f"Field '{key}' must be a date.")

        return len(errors) == 0, errors

    def to_dict(self) -> dict:
        return {
            "template_id": self.template_id,
            "name": self.name,
            "fields_schema": self.fields_schema,
            "template_dir": self.template_dir,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ProfileTemplate":
        return cls(
            template_id=data.get("template_id", ""),
            name=data.get("name", ""),
            fields_schema=data.get("fields_schema", []),
            template_dir=data.get("template_dir", ""),
        )
