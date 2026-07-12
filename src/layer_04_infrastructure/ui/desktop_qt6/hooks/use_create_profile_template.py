import asyncio
from PyQt6.QtCore import QObject, pyqtSignal
from src.layer_03_interface_adapters.controllers.desktop.create_profile_template import (
    CreateProfileTemplateController,
)
from src.layer_04_infrastructure.databases.sqlite.sqlite_document_store import (
    SqliteDocumentStore,
)
from .use_async import UseAsync


class UseCreateProfileTemplate(QObject):
    """
    Custom Hook quản lý luồng xử lý và dữ liệu ngầm cho CreateProfileTemplatePage.
    """

    template_loaded = pyqtSignal(dict)
    template_saved = pyqtSignal(str)  # Emit template_name
    loading = pyqtSignal(bool)
    error = pyqtSignal(str)

    def __init__(self, context, parent=None):
        super().__init__(parent)
        self.store = SqliteDocumentStore()
        self._controller = context.container.resolve(CreateProfileTemplateController)
        self._async_helper = UseAsync(self)
        self._async_helper.loading.connect(self.loading.emit)
        self._async_helper.finished.connect(self._on_async_finished)
        self._action = ""

    def load_template(self, template_id: str):
        self._action = "load_template"
        self._async_helper.execute(self._run_load_template, template_id)

    def save_template(
        self,
        t_id: str,
        t_name: str,
        fields_schema: list,
        selected_files: list,
        is_update: bool,
    ):
        self._action = "save_template"
        req = {
            "template_id": t_id,
            "name": t_name,
            "fields_schema": fields_schema,
            "selected_files": selected_files,
            "is_update": is_update,
        }
        self._async_helper.execute(self._run_save_template, req)

    def _run_load_template(self, template_id: str) -> dict:
        return self.store.get_document("profile_templates", template_id) or {}

    def _run_save_template(self, req: dict) -> str:
        res = asyncio.run(self._controller.handle_request(req))
        if res.get("status") != "success":
            raise ValueError(res.get("message", "Lỗi lưu mẫu hồ sơ"))
        return req["name"]

    def _on_async_finished(self, success: bool, result: object, error_msg: str):
        if not success:
            self.error.emit(error_msg)
            return

        if self._action == "load_template":
            if isinstance(result, dict):
                self.template_loaded.emit(result)
        elif self._action == "save_template":
            self.template_saved.emit(str(result))
