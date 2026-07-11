import os
from .rename_module_dto import RenameModuleInput, RenameModuleOutput


class RenameModuleInteractor:
    def execute(self, input_data: RenameModuleInput) -> RenameModuleOutput:
        try:
            from rope.base.project import Project
            from rope.refactor.rename import Rename
        except ImportError:
            return RenameModuleOutput(
                success=False,
                message="'rope' library is not installed in the virtual environment. Please run: pip install rope",
            )

        target_path = input_data.target_path
        new_name = input_data.new_name

        if not os.path.exists(target_path):
            return RenameModuleOutput(
                success=False, message=f"Target path '{target_path}' does not exist."
            )

        try:
            project = Project(".")
            resource = project.get_resource(target_path)
            refactor = Rename(project, resource)

            changes = refactor.get_changes(new_name)
            project.do(changes)
            return RenameModuleOutput(
                success=True,
                message="Refactoring completed successfully! All imports have been auto-fixed.",
            )
        except Exception as e:
            return RenameModuleOutput(success=False, message=f"Refactoring failed: {e}")
