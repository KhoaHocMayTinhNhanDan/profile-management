import asyncio
from PyQt6.QtCore import QObject, pyqtSignal
from src.layer_03_interface_adapters.controllers.desktop.update_profile import (
    UpdateProfileController,
)
from src.layer_04_infrastructure.databases.sqlite.sqlite_document_store import (
    SqliteDocumentStore,
)
from .use_async import UseAsync


class UseUpdateProfile(QObject):
    """
    Custom Hook quản lý trạng thái hiển thị và luồng công việc cho tính năng UpdateProfile.
    """

    profile_loaded = pyqtSignal(dict)
    profile_updated = pyqtSignal(dict)
    template_loaded = pyqtSignal(dict)
    loading = pyqtSignal(bool)
    error = pyqtSignal(str)

    def __init__(self, context, parent=None):
        super().__init__(parent)
        self._controller = context.container.resolve(UpdateProfileController)
        self.store = SqliteDocumentStore()
        self._async_helper = UseAsync(self)
        self._async_helper.loading.connect(self.loading.emit)
        self._async_helper.finished.connect(self._on_async_finished)
        self._action = ""

    def load_profile(self, profile_id: str):
        self._action = "load_profile"
        self._async_helper.execute(self._run_load_profile, profile_id)

    def load_template(self, template_id: str):
        self._action = "load_template"
        self._async_helper.execute(self._run_load_template, template_id)

    def update_profile(
        self, profile_id: str, dynamic_data: dict, status: str | None = None
    ):
        self._action = "update_profile"
        req = {
            "profile_id": profile_id,
            "dynamic_data": dynamic_data,
            "status": status,
        }
        self._async_helper.execute(self._run_update_profile, req)

    def _run_load_profile(self, profile_id: str) -> dict:
        profile = self.store.get_document("profiles", profile_id)
        return profile or {}

    def _run_load_template(self, template_id: str) -> dict:
        template = self.store.get_document("profile_templates", template_id)
        return template or {}

    def _run_update_profile(self, req: dict) -> dict:
        return asyncio.run(self._controller.handle_request(req))

    def _on_async_finished(self, success: bool, result: object, error_msg: str):
        if not success:
            self.error.emit(error_msg)
            return

        if self._action == "load_profile":
            self.profile_loaded.emit(result if isinstance(result, dict) else {})
        elif self._action == "load_template":
            self.template_loaded.emit(result if isinstance(result, dict) else {})
        elif self._action == "update_profile":
            if isinstance(result, dict) and result.get("status") == "success":
                self.profile_updated.emit(result)
            else:
                msg = (
                    result.get("message", "Lỗi cập nhật hồ sơ không xác định")
                    if isinstance(result, dict)
                    else "Lỗi cập nhật"
                )
                self.error.emit(msg)
