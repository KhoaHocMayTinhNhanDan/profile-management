from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QComboBox, QCheckBox,
    QLabel, QMessageBox, QScrollArea, QWidget, QGridLayout
)
from PyQt6.QtCore import Qt
from src.shared.logger.app_logger import get_logger
from ..level_04_templates.page_template import BasePageTemplate
from src.layer_03_interface_adapters.controllers.desktop.create_profile_template import CreateProfileTemplateController
import asyncio
from typing import Any

logger = get_logger(__name__)

class CreateProfileTemplatePage(BasePageTemplate):
    def __init__(self, context):
        super().__init__("create_profile_template", context)
        self.controller = context.container.resolve(CreateProfileTemplateController)
        
        # Form Layout
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        
        # ID Template
        self.grid.addWidget(QLabel("Mã Mẫu Hồ Sơ (Không dấu, e.g. nhan_su):"), 0, 0)
        self.txt_id = QLineEdit()
        self.grid.addWidget(self.txt_id, 0, 1)
        
        # Name Template
        self.grid.addWidget(QLabel("Tên Mẫu Hồ Sơ (e.g. Hồ sơ nhân sự):"), 1, 0)
        self.txt_name = QLineEdit()
        self.grid.addWidget(self.txt_name, 1, 1)
        
        self.content_layout.addLayout(self.grid)
        
        # Dynamic Fields Title & Button
        self.fields_header = QHBoxLayout()
        self.fields_header.addWidget(QLabel("<b>Cấu hình thuộc tính động:</b>"))
        self.btn_add_field = QPushButton("+ Thêm Thuộc Tính")
        self.btn_add_field.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add_field.clicked.connect(self._add_field_row)
        self.fields_header.addWidget(self.btn_add_field)
        self.content_layout.addLayout(self.fields_header)
        
        # Scroll Area for dynamic fields rows
        self.fields_widget = QWidget()
        self.fields_layout = QVBoxLayout(self.fields_widget)
        self.fields_layout.setSpacing(10)
        self.fields_layout.addStretch()
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.fields_widget)
        self.content_layout.addWidget(self.scroll_area)
        
        # Save & Cancel buttons
        self.buttons_layout = QHBoxLayout()
        self.btn_save = QPushButton("Lưu Cấu Hình Mẫu")
        self.btn_cancel = QPushButton("Quay Lại")
        self.btn_save.setStyleSheet("background-color: #2ecc71; color: white; padding: 8px 16px; font-weight: bold; border-radius: 4px;")
        self.btn_cancel.setStyleSheet("background-color: #e74c3c; color: white; padding: 8px 16px; font-weight: bold; border-radius: 4px;")
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.buttons_layout.addWidget(self.btn_save)
        self.buttons_layout.addWidget(self.btn_cancel)
        self.buttons_layout.addStretch()
        self.content_layout.addLayout(self.buttons_layout)
        
        # Connect actions
        self.btn_save.clicked.connect(self._save_template)
        self.btn_cancel.clicked.connect(self._go_back)
        
        self.field_rows = []
        # Add first row default
        self._add_field_row()

    def _add_field_row(self):
        row_widget = QWidget()
        row_lay = QHBoxLayout(row_widget)
        row_lay.setContentsMargins(0, 0, 0, 0)
        
        name_input = QLineEdit()
        name_input.setPlaceholderText("Mã trường (e.g. email)")
        
        label_input = QLineEdit()
        label_input.setPlaceholderText("Nhãn hiển thị (e.g. Email liên hệ)")
        
        type_combo = QComboBox()
        type_combo.addItems(["string", "number", "boolean", "date"])
        
        req_check = QCheckBox("Bắt buộc")
        
        btn_del = QPushButton("Xóa")
        btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_del.clicked.connect(lambda: self._remove_field_row(row_widget))
        
        row_lay.addWidget(name_input)
        row_lay.addWidget(label_input)
        row_lay.addWidget(type_combo)
        row_lay.addWidget(req_check)
        row_lay.addWidget(btn_del)
        
        # Insert row before the stretch item
        self.fields_layout.insertWidget(self.fields_layout.count() - 1, row_widget)
        self.field_rows.append({
            "widget": row_widget,
            "name": name_input,
            "label": label_input,
            "type": type_combo,
            "required": req_check
        })

    def _remove_field_row(self, widget):
        self.field_rows = [r for r in self.field_rows if r["widget"] != widget]
        widget.deleteLater()

    def _save_template(self):
        t_id = self.txt_id.text().strip()
        t_name = self.txt_name.text().strip()
        
        if not t_id or not t_name:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập đầy đủ Mã mẫu và Tên mẫu!")
            return
            
        fields_schema = []
        for r in self.field_rows:
            f_name = r["name"].text().strip()
            f_label = r["label"].text().strip()
            if not f_name or not f_label:
                continue
            fields_schema.append({
                "name": f_name,
                "label": f_label,
                "type": r["type"].currentText(),
                "required": r["required"].isChecked()
            })
            
        req = {
            "template_id": t_id,
            "name": t_name,
            "fields_schema": fields_schema
        }
        
        # Execute asynchronously using asyncio.run since Controller is async
        loop = asyncio.get_event_loop()
        res = loop.run_until_complete(self.controller.handle_request(req))
        
        if res.get("status") == "success":
            QMessageBox.information(self, "Thành công", f"Đã lưu mẫu hồ sơ '{t_name}' thành công!")
            self._go_back()
        else:
            QMessageBox.critical(self, "Lỗi", f"Không thể lưu mẫu: {res.get('message')}")

    def _go_back(self):
        main_win: Any = self.window()
        if main_win is not None and hasattr(main_win, "switch_page"):
            # Refresh welcome page first
            welcome = main_win.pages_map.get("welcome")
            if welcome is not None and hasattr(welcome, "refresh_data"):
                welcome.refresh_data()
            main_win.switch_page("welcome")

    def retranslate_ui(self, lang_code: str):
        pass
