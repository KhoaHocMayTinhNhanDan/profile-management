from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QComboBox, QCheckBox,
    QLabel, QMessageBox, QScrollArea, QWidget, QFormLayout, QDateEdit
)
from PyQt6.QtCore import QDate
from src.shared.logger.app_logger import get_logger
from ..level_04_templates.page_template import BasePageTemplate
from src.layer_04_infrastructure.databases.sqlite.sqlite_document_store import SqliteDocumentStore
from src.layer_03_interface_adapters.controllers.desktop.create_profile import CreateProfileController
import asyncio
from typing import Any

logger = get_logger(__name__)

class CreateProfilePage(BasePageTemplate):
    def __init__(self, context):
        super().__init__("create_profile", context)
        self.store = SqliteDocumentStore()
        self.controller = context.container.resolve(CreateProfileController)
        
        # Header Layout
        self.header_lay = QFormLayout()
        self.header_lay.setSpacing(10)
        
        # Profile ID
        self.txt_profile_id = QLineEdit()
        self.txt_profile_id.setPlaceholderText("e.g. HS_001")
        self.header_lay.addRow(QLabel("Mã Hồ Sơ:"), self.txt_profile_id)
        
        # Template selection
        self.cbo_template = QComboBox()
        self.cbo_template.currentIndexChanged.connect(self._on_template_changed)
        self.header_lay.addRow(QLabel("Chọn mẫu hồ sơ:"), self.cbo_template)
        
        self.content_layout.addLayout(self.header_lay)
        
        # Dynamic inputs area
        self.form_widget = QWidget()
        self.form_layout = QFormLayout(self.form_widget)
        self.form_layout.setSpacing(10)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.form_widget)
        self.content_layout.addWidget(self.scroll_area)
        
        # Buttons
        self.buttons_lay = QHBoxLayout()
        self.btn_save = QPushButton("Tạo Hồ Sơ Mới")
        self.btn_cancel = QPushButton("Quay Lại")
        self.btn_save.setStyleSheet("background-color: #2ecc71; color: white; padding: 8px 16px; font-weight: bold; border-radius: 4px;")
        self.btn_cancel.setStyleSheet("background-color: #e74c3c; color: white; padding: 8px 16px; font-weight: bold; border-radius: 4px;")
        from PyQt6.QtCore import Qt
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.buttons_lay.addWidget(self.btn_save)
        self.buttons_lay.addWidget(self.btn_cancel)
        self.buttons_lay.addStretch()
        self.content_layout.addLayout(self.buttons_lay)
        
        # Connect actions
        self.btn_save.clicked.connect(self._save_profile)
        self.btn_cancel.clicked.connect(self._go_back)
        
        self.widgets_map = {}
        self.current_template = None
        
        # Initial templates loading
        self.refresh_templates()

    def refresh_templates(self):
        self.cbo_template.clear()
        templates = self.store.list_documents("profile_templates")
        self.templates_map = {t["template_id"]: t for t in templates}
        
        self.cbo_template.addItem("--- Chọn mẫu ---", "")
        for t in templates:
            self.cbo_template.addItem(t.get("name", t.get("template_id")), t["template_id"])

    def _on_template_changed(self, idx):
        # Clear previous layout widgets
        for i in reversed(range(self.form_layout.count())):
            item = self.form_layout.itemAt(i)
            if item is not None:
                w = item.widget()
                if w is not None:
                    w.deleteLater()
        self.widgets_map = {}
        
        t_id = self.cbo_template.currentData()
        if not t_id or t_id not in self.templates_map:
            self.current_template = None
            return
            
        self.current_template = self.templates_map[t_id]
        schema = self.current_template.get("fields_schema", [])
        
        for field in schema:
            f_name = field["name"]
            f_label = field.get("label", f_name)
            f_type = field.get("type", "string")
            req = field.get("required", False)
            
            label_text = f"{f_label}:"
            if req:
                label_text = f"{f_label} (*):"
            lbl = QLabel(label_text)
            
            if f_type == "boolean":
                widget = QCheckBox()
            elif f_type == "date":
                widget = QDateEdit()
                widget.setCalendarPopup(True)
                widget.setDate(QDate.currentDate())
            else:
                widget = QLineEdit()
                if f_type == "number":
                    widget.setPlaceholderText("Nhập số")
            
            self.form_layout.addRow(lbl, widget)
            self.widgets_map[f_name] = (widget, f_type, req)

    def _save_profile(self):
        p_id = self.txt_profile_id.text().strip()
        t_id = self.cbo_template.currentData()
        
        if not p_id:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập Mã hồ sơ!")
            return
        if not t_id:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn Mẫu hồ sơ!")
            return
            
        dynamic_data = {}
        for f_name, (widget, f_type, req) in self.widgets_map.items():
            if f_type == "boolean":
                val = widget.isChecked()
            elif f_type == "date":
                val = widget.date().toString("yyyy-MM-dd")
            else:
                val = widget.text().strip()
                if f_type == "number" and val:
                    try:
                        val = float(val)
                    except ValueError:
                        QMessageBox.warning(self, "Cảnh báo", f"Trường '{f_name}' phải nhập kiểu số!")
                        return
            
            dynamic_data[f_name] = val
            
        req_body = {
            "profile_id": p_id,
            "template_id": t_id,
            "dynamic_data": dynamic_data,
            "documents": []
        }
        
        loop = asyncio.get_event_loop()
        res = loop.run_until_complete(self.controller.handle_request(req_body))
        
        if res.get("status") == "success":
            QMessageBox.information(self, "Thành công", f"Đã khởi tạo hồ sơ '{p_id}' thành công dưới dạng bản nháp (Draft)!")
            self._go_back()
        else:
            msg = res.get("message", "Lỗi không xác định")
            if res.get("errors"):
                msg += "\n- " + "\n- ".join(res.get("errors"))
            QMessageBox.critical(self, "Lỗi", f"Không thể lưu hồ sơ: {msg}")

    def _go_back(self):
        main_win: Any = self.window()
        if main_win is not None and hasattr(main_win, "switch_page"):
            welcome = main_win.pages_map.get("welcome")
            if welcome is not None and hasattr(welcome, "refresh_data"):
                welcome.refresh_data()
            main_win.switch_page("welcome")

    def retranslate_ui(self, lang_code: str):
        pass
