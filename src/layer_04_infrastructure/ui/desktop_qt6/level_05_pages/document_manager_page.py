from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QLabel, QMessageBox, QFileDialog, QInputDialog, QAbstractItemView, QLineEdit
)
from PyQt6.QtCore import Qt, QMetaObject, Q_ARG, pyqtSlot
from typing import Any
from src.shared.logger.app_logger import get_logger
from ..level_04_templates.page_template import BasePageTemplate
from src.layer_04_infrastructure.databases.sqlite.sqlite_document_store import SqliteDocumentStore
from src.layer_03_interface_adapters.controllers.desktop.checkout_document import CheckoutDocumentController
from src.layer_03_interface_adapters.controllers.desktop.checkin_document import CheckinDocumentController
from src.layer_03_interface_adapters.controllers.desktop.generate_document_from_template import GenerateDocumentFromTemplateController
from src.layer_04_infrastructure.services.file_watcher import FileWatcherService
import asyncio
import os
import shutil

logger = get_logger(__name__)

class DocumentManagerPage(BasePageTemplate):
    def __init__(self, context):
        super().__init__("document_manager", context)
        self.store = SqliteDocumentStore()
        self.watcher = FileWatcherService()
        
        self.checkout_controller = context.container.resolve(CheckoutDocumentController)
        self.checkin_controller = context.container.resolve(CheckinDocumentController)
        self.generate_controller = context.container.resolve(GenerateDocumentFromTemplateController)
        
        self.profile_id = ""
        
        # Subtitle
        self.lbl_subtitle = QLabel("Hồ sơ: ")
        self.lbl_subtitle.setStyleSheet("font-size: 14px; font-weight: bold; color: #888;")
        self.content_layout.addWidget(self.lbl_subtitle)
        
        # Buttons layout
        self.actions_layout = QHBoxLayout()
        self.btn_generate = QPushButton("Sinh Tài liệu từ Mẫu .docx")
        self.btn_back = QPushButton("Quay Lại Dashboard")
        
        self.btn_generate.setStyleSheet("background-color: #2a82da; color: white; padding: 8px 16px; font-weight: bold; border-radius: 4px;")
        self.btn_back.setStyleSheet("background-color: #7f8c8d; color: white; padding: 8px 16px; font-weight: bold; border-radius: 4px;")
        self.btn_generate.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.actions_layout.addWidget(self.btn_generate)
        self.actions_layout.addWidget(self.btn_back)
        self.actions_layout.addStretch()
        self.content_layout.addLayout(self.actions_layout)
        
        # Documents Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID Tài liệu", "Tên Tài liệu", "Phiên bản", "Trạng thái Khóa", "Kích thước", "Thao tác"])
        header = self.table.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.content_layout.addWidget(self.table)
        
        # Connect Actions
        self.btn_generate.clicked.connect(self._generate_from_template)
        self.btn_back.clicked.connect(self._go_back)
        
        self.table.itemDoubleClicked.connect(self._on_row_double_clicked)

    def set_profile(self, profile_id: str):
        self.profile_id = profile_id
        self.lbl_subtitle.setText(f"Hồ sơ: {profile_id}")
        self.refresh_documents()

    def refresh_documents(self):
        self.table.setRowCount(0)
        if not self.profile_id:
            return
            
        profile = self.store.get_document("profiles", self.profile_id)
        if not profile:
            return
            
        docs = profile.get("documents", [])
        for doc in docs:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            d_id = doc.get("document_id", "")
            name = doc.get("name", "")
            ver = doc.get("version", "1.0")
            is_locked = doc.get("is_locked", False)
            locked_by = doc.get("locked_by", "")
            size = doc.get("size", 0)
            
            self.table.setItem(row, 0, QTableWidgetItem(d_id))
            self.table.setItem(row, 1, QTableWidgetItem(name))
            self.table.setItem(row, 2, QTableWidgetItem(f"v{ver}"))
            
            lock_status = "Đang chỉnh sửa" if is_locked else "Sẵn sàng"
            lock_item = QTableWidgetItem(lock_status)
            if is_locked:
                lock_item.setForeground(Qt.GlobalColor.red)
                lock_item.setToolTip(f"Bị khóa bởi {locked_by}")
            else:
                lock_item.setForeground(Qt.GlobalColor.green)
            self.table.setItem(row, 3, lock_item)
            
            self.table.setItem(row, 4, QTableWidgetItem(f"{size / 1024:.1f} KB"))
            
            # Action button for edit
            btn_edit = QPushButton("Biên tập")
            btn_edit.setStyleSheet("padding: 2px 8px; background-color: #34495e; color: white; border-radius: 3px;")
            btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_edit.clicked.connect(lambda checked, d=d_id: self._start_editing_doc(d))
            self.table.setCellWidget(row, 5, btn_edit)

    def _on_row_double_clicked(self, item: Any):
        row = item.row()
        item_obj = self.table.item(row, 0)
        doc_id = item_obj.text() if item_obj is not None else ""
        self._start_editing_doc(doc_id)

    def _start_editing_doc(self, doc_id: str):
        # Execute checkout
        req = {
            "profile_id": self.profile_id,
            "document_id": doc_id,
            "user_id": "user_dong" # current user
        }
        
        loop = asyncio.get_event_loop()
        res = loop.run_until_complete(self.checkout_controller.handle_request(req))
        
        if res.get("status") == "success":
            doc_url = res.get("document_url", "")
            local_name = res.get("local_filename", "")
            
            # Since local document store sets file:/// absolute paths:
            if doc_url.startswith("file:///"):
                file_path = doc_url.replace("file:///", "")
            else:
                file_path = doc_url
                
            # Convert Windows slash
            file_path = os.path.abspath(file_path)
            
            if not os.path.exists(file_path):
                QMessageBox.critical(self, "Lỗi", f"Không tìm thấy file tài liệu tại: {file_path}")
                return
                
            # Create a temporary working copy in appdata/temp_editing/
            temp_dir = os.path.join("appdata", "temp_editing", self.profile_id)
            os.makedirs(temp_dir, exist_ok=True)
            temp_file_path = os.path.abspath(os.path.join(temp_dir, local_name))
            
            # Copy to temp path
            shutil.copy2(file_path, temp_file_path)
            
            # Open MS Word
            try:
                os.startfile(temp_file_path)
                QMessageBox.information(
                    self, 
                    "Soạn thảo Word", 
                    f"Đã khóa tài liệu và mở bằng Microsoft Word.\nĐang theo dõi file: {local_name}\n\nHãy lưu và đóng Word khi hoàn thành."
                )
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể mở file bằng Word: {e}")
                return
                
            # Start Watching the temp file
            self.watcher.start_watching(
                temp_file_path,
                lambda path, size, checksum: self._on_document_saved(doc_id, file_path, path, size, checksum)
            )
            self.refresh_documents()
        else:
            QMessageBox.critical(self, "Lỗi Khóa Tài Liệu", res.get("message"))

    def _on_document_saved(self, doc_id: str, original_path: str, temp_path: str, new_size: int, new_checksum: str):
        # When file changes, copy temp copy back to original path
        try:
            shutil.copy2(temp_path, original_path)
        except Exception as e:
            logger.error(f"Failed to copy back changed file: {e}")
            
        new_url = "file:///" + os.path.abspath(original_path).replace("\\", "/")
        
        req = {
            "profile_id": self.profile_id,
            "document_id": doc_id,
            "user_id": "user_dong",
            "new_url": new_url,
            "new_size": new_size,
            "new_checksum": new_checksum
        }
        
        # Run checkin
        loop = asyncio.get_event_loop()
        res = loop.run_until_complete(self.checkin_controller.handle_request(req))
        
        # Stop watching after change detected
        self.watcher.stop_watching(temp_path)
        
        # Use QMetaObject to trigger UI refresh safely from background thread
        QMetaObject.invokeMethod(self, "_on_checkin_completed", Qt.ConnectionType.QueuedConnection, Q_ARG(dict, res))

    @pyqtSlot(dict)
    def _on_checkin_completed(self, res: dict):
        if res.get("status") == "success":
            QMessageBox.information(
                self, 
                "Đồng bộ thành công", 
                f"Tài liệu đã được tự động lưu lại hệ thống.\nPhiên bản mới: {res.get('new_version')}"
            )
        else:
            QMessageBox.critical(self, "Lỗi Đồng Bộ", res.get("message"))
        self.refresh_documents()

    def _generate_from_template(self):
        # Open QFileDialog to select template docx
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file mẫu Word (.docx)", "", "Word Files (*.docx)")
        if not file_path:
            return
            
        out_name, ok = QInputDialog.getText(
            self, "Tên tài liệu đầu ra", 
            "Nhập tên file tài liệu xuất ra (e.g. Hop_Dong_Nhan_Su.docx):", 
            QLineEdit.EchoMode.Normal, "Hop_Dong_Moi.docx"
        )
        if not ok or not out_name.strip():
            return
            
        req = {
            "profile_id": self.profile_id,
            "template_doc_path": file_path,
            "output_doc_name": out_name.strip()
        }
        
        loop = asyncio.get_event_loop()
        res = loop.run_until_complete(self.generate_controller.handle_request(req))
        
        if res.get("status") == "success":
            QMessageBox.information(self, "Thành công", "Đã sinh tài liệu và điền dữ liệu động thành công!")
            self.refresh_documents()
        else:
            QMessageBox.critical(self, "Lỗi", res.get("message"))

    def _go_back(self):
        main_win: Any = self.window()
        if main_win is not None and hasattr(main_win, "switch_page"):
            welcome = main_win.pages_map.get("welcome")
            if welcome is not None and hasattr(welcome, "refresh_data"):
                welcome.refresh_data()
            main_win.switch_page("welcome")

    def retranslate_ui(self, lang_code: str):
        pass
