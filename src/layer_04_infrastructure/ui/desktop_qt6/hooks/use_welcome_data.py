import os
import shutil
from PyQt6.QtCore import QObject, pyqtSignal
from src.layer_04_infrastructure.databases.sqlite.sqlite_document_store import (
    SqliteDocumentStore,
)
from .use_async import UseAsync


class UseWelcomeData(QObject):
    """
    Custom Hook quản lý dữ liệu hiển thị và tác vụ ngầm cho WelcomePage.
    """

    data_loaded = pyqtSignal(list, list)  # Emit (profiles, templates)
    template_deleted = pyqtSignal(str)  # Emit template_id
    loading = pyqtSignal(bool)
    error = pyqtSignal(str)

    def __init__(self, context, parent=None):
        super().__init__(parent)
        self.store = SqliteDocumentStore()
        self._async_helper = UseAsync(self)
        self._async_helper.loading.connect(self.loading.emit)
        self._async_helper.finished.connect(self._on_async_finished)
        self._action = ""

    def load_data(self):
        self._action = "load_data"
        self._async_helper.execute(self._run_load_data)

    def delete_template(self, template_id: str):
        self._action = "delete_template"
        self._async_helper.execute(self._run_delete_template, template_id)

    def _run_load_data(self) -> tuple[list, list]:
        profiles = self.store.list_documents("profiles") or []
        templates = self.store.list_documents("profile_templates") or []
        return profiles, templates

    def _run_delete_template(self, template_id: str) -> str:
        # Delete from DB
        self.store.delete_document("profile_templates", template_id)

        # Clean up local templates folder
        t_dir = os.path.join("appdata", "templates", template_id)
        if os.path.exists(t_dir):
            try:
                shutil.rmtree(t_dir)
            except Exception:
                # We can log this but still succeed
                pass
        return template_id

    def _on_async_finished(self, success: bool, result: object, error_msg: str):
        if not success:
            self.error.emit(error_msg)
            return

        if self._action == "load_data":
            if isinstance(result, tuple) and len(result) == 2:
                self.data_loaded.emit(result[0], result[1])
        elif self._action == "delete_template":
            self.template_deleted.emit(str(result))
