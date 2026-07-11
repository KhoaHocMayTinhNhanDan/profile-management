import os
from .move_module_dto import MoveModuleInput, MoveModuleOutput


class MoveModuleInteractor:
    def execute(self, input_data: MoveModuleInput) -> MoveModuleOutput:
        try:
            from rope.base.project import Project
            from rope.refactor.move import MoveModule
        except ImportError:
            return MoveModuleOutput(
                success=False,
                message="'rope' library is not installed in the virtual environment. Please run: pip install rope",
            )

        source_path = input_data.source_path
        destination_dir = input_data.destination_dir

        if not os.path.exists(source_path):
            return MoveModuleOutput(
                success=False, message=f"Source path '{source_path}' does not exist."
            )

        if not os.path.exists(destination_dir):
            return MoveModuleOutput(
                success=False,
                message=f"Destination directory '{destination_dir}' does not exist. Please create it first.",
            )

        if not os.path.isdir(destination_dir):
            return MoveModuleOutput(
                success=False,
                message=f"Destination '{destination_dir}' is not a directory.",
            )

        try:
            project = Project(".")
            source_resource = project.get_resource(source_path)
            dest_resource = project.get_resource(destination_dir)

            refactor = MoveModule(project, source_resource)
            changes = refactor.get_changes(dest_resource)
            project.do(changes)

            return MoveModuleOutput(
                success=True,
                message=f"Successfully moved '{source_path}' into '{destination_dir}' and updated all imports!",
            )
        except Exception as e:
            return MoveModuleOutput(
                success=False, message=f"Move refactoring failed: {e}"
            )
