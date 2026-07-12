import asyncio
import os
import shutil
from typing import Any
from PyQt6.QtCore import QObject, pyqtSignal
from src.layer_03_interface_adapters.controllers.desktop.checkout_document import (
    CheckoutDocumentController,
)
from .use_async import UseAsync


class UseCheckoutDocument(QObject):
    """
    Custom Hook quản lý trạng thái hiển thị và luồng công việc cho tính năng CheckoutDocument.
    """

    finished = pyqtSignal(dict)
    loading = pyqtSignal(bool)
    error = pyqtSignal(str)

    def __init__(self, context, parent=None):
        super().__init__(parent)
        self._controller = context.container.resolve(CheckoutDocumentController)
        self._async_helper = UseAsync(self)
        self._async_helper.loading.connect(self.loading.emit)
        self._async_helper.finished.connect(self._on_async_finished)
        self._profile_id = ""
        self._document_id = ""

    def checkout(self, profile_id: str, document_id: str):
        self._profile_id = profile_id
        self._document_id = document_id
        req = {
            "profile_id": profile_id,
            "document_id": document_id,
            "user_id": "user_dong",
        }
        self._async_helper.execute(self._run_checkout_and_open, req)

    def _run_checkout_and_open(self, req: dict) -> dict:
        res = asyncio.run(self._controller.handle_request(req))
        if res.get("status") != "success":
            return res

        doc_url = res.get("document_url", "")
        local_name = res.get("local_filename", "")

        if not doc_url:
            return {"status": "error", "message": "Đường dẫn tài liệu (URL) trống."}

        if doc_url.startswith("file:///"):
            file_path = doc_url.replace("file:///", "")
        else:
            file_path = doc_url
        file_path = os.path.abspath(file_path)

        if not os.path.isfile(file_path):
            return {
                "status": "error",
                "message": f"Không tìm thấy file gốc tại: {file_path}",
            }

        # Copy to temp path
        temp_dir = os.path.join("appdata", "temp_editing", self._profile_id)
        os.makedirs(temp_dir, exist_ok=True)
        temp_file_path = os.path.abspath(os.path.join(temp_dir, local_name))

        try:
            shutil.copy2(file_path, temp_file_path)
        except Exception as e:
            return {"status": "error", "message": f"Không thể tạo file tạm: {e}"}

        # Start MS Word
        try:
            os.startfile(temp_file_path)
        except Exception as e:
            return {"status": "error", "message": f"Không thể mở Word: {e}"}

        res["temp_file_path"] = temp_file_path
        res["original_path"] = file_path
        return res

    def _on_async_finished(self, success: bool, result: object, error_msg: str):
        if not success:
            self.error.emit(error_msg)
        elif isinstance(result, dict):
            if result.get("status") == "success":
                # Start file watcher via checkin hook on the parent page
                page: Any = self.parent()
                if page and hasattr(page, "use_checkin"):
                    page.use_checkin.start_watching(
                        self._profile_id,
                        self._document_id,
                        result.get("temp_file_path", ""),
                        result.get("original_path", ""),
                    )
                self.finished.emit(result)
            else:
                self.error.emit(result.get("message", "Lỗi checkout không xác định"))
        else:
            self.error.emit("Kết quả trả về không hợp lệ")
