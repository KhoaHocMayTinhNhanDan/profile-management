import os
from PyQt6.QtCore import QObject, pyqtSignal
from src.layer_03_interface_adapters.controllers.desktop.create_profile import (
    CreateProfileController,
)
from src.layer_03_interface_adapters.controllers.desktop.generate_document_from_template import (
    GenerateDocumentFromTemplateController,
)
from src.layer_04_infrastructure.databases.sqlite.sqlite_document_store import (
    SqliteDocumentStore,
)
from .use_async import UseAsync


class UseCreateProfile(QObject):
    """
    Custom Hook quản lý luồng xử lý và dữ liệu ngầm cho CreateProfilePage.
    """

    templates_loaded = pyqtSignal(list)
    profile_created = pyqtSignal(str)  # Emit profile_id
    loading = pyqtSignal(bool)
    error = pyqtSignal(str)

    def __init__(self, context, parent=None):
        super().__init__(parent)
        self.store = SqliteDocumentStore()
        self._controller = context.container.resolve(CreateProfileController)
        self._gen_controller = context.container.resolve(
            GenerateDocumentFromTemplateController
        )
        self._async_helper = UseAsync(self)
        self._async_helper.loading.connect(self.loading.emit)
        self._async_helper.finished.connect(self._on_async_finished)
        self._action = ""

    def load_templates(self):
        self._action = "load_templates"
        self._async_helper.execute(self._run_load_templates)

    def create_profile(self, p_id: str, t_id: str, dynamic_data: dict):
        self._action = "create_profile"
        req = {
            "profile_id": p_id,
            "template_id": t_id,
            "dynamic_data": dynamic_data,
        }
        self._async_helper.execute(self._run_create_profile, req)

    def _run_load_templates(self) -> list:
        return self.store.list_documents("profile_templates") or []

    def _run_create_profile(self, req: dict) -> str:
        import asyncio

        # 1. Create the profile
        req_body = {
            "profile_id": req["profile_id"],
            "template_id": req["template_id"],
            "dynamic_data": req["dynamic_data"],
            "documents": [],
        }
        res = asyncio.run(self._controller.handle_request(req_body))
        if res.get("status") != "success":
            msg = res.get("message", "Lỗi tạo hồ sơ")
            if res.get("errors"):
                msg += "\n- " + "\n- ".join(res.get("errors"))
            raise ValueError(msg)

        # 2. Get the template to auto generate documents
        template = self.store.get_document("profile_templates", req["template_id"])
        if template:
            t_dir = template.get("template_dir", "")
            if t_dir and os.path.exists(t_dir):
                docx_files = sorted(
                    [
                        f
                        for f in os.listdir(t_dir)
                        if f.endswith(".docx") and not f.startswith("~$")
                    ]
                )
                for f in docx_files:
                    gen_req = {
                        "profile_id": req["profile_id"],
                        "template_doc_path": os.path.join(t_dir, f),
                        "output_doc_name": f,
                    }
                    asyncio.run(self._gen_controller.handle_request(gen_req))

        return req["profile_id"]

    def _on_async_finished(self, success: bool, result: object, error_msg: str):
        if not success:
            self.error.emit(error_msg)
            return

        if self._action == "load_templates":
            if isinstance(result, list):
                self.templates_loaded.emit(result)
        elif self._action == "create_profile":
            self.profile_created.emit(str(result))
