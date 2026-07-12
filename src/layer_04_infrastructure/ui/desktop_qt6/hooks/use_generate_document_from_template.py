import asyncio
from PyQt6.QtCore import QObject, pyqtSignal
from src.layer_03_interface_adapters.controllers.desktop.generate_document_from_template import (
    GenerateDocumentFromTemplateController,
)
from .use_async import UseAsync


class UseGenerateDocumentFromTemplate(QObject):
    """
    Custom Hook quản lý trạng thái hiển thị và luồng công việc cho tính năng GenerateDocumentFromTemplate.
    """

    finished = pyqtSignal(int, int)  # (success_count, total_count)
    loading = pyqtSignal(bool)
    error = pyqtSignal(str)

    def __init__(self, context, parent=None):
        super().__init__(parent)
        self._controller = context.container.resolve(
            GenerateDocumentFromTemplateController
        )
        self._async_helper = UseAsync(self)
        self._async_helper.loading.connect(self.loading.emit)
        self._async_helper.finished.connect(self._on_async_finished)

    def generate_documents(self, reqs: list):
        self._async_helper.execute(self._run_generate, reqs)

    def _run_generate(self, reqs: list) -> tuple[int, int]:
        success_count = 0
        for req in reqs:
            res = asyncio.run(self._controller.handle_request(req))
            if res.get("status") == "success":
                success_count += 1
        return success_count, len(reqs)

    def _on_async_finished(self, success: bool, result: object, error_msg: str):
        if not success:
            self.error.emit(error_msg)
            return

        if isinstance(result, tuple) and len(result) == 2:
            success_count, total_count = result
            self.finished.emit(success_count, total_count)
