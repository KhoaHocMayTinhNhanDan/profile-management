from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QLabel, QMessageBox, QFrame, QAbstractItemView
)
from PyQt6.QtCore import Qt
from typing import Any
from src.shared.logger.app_logger import get_logger
from ..level_04_templates.page_template import BasePageTemplate
from src.layer_04_infrastructure.databases.sqlite.sqlite_document_store import SqliteDocumentStore

logger = get_logger(__name__)

class StatCard(QFrame):
    def __init__(self, title: str, val: str, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("background-color: #2d2d2d; border-radius: 6px; padding: 15px; border: 1px solid #3d3d3d;")
        lay = QVBoxLayout(self)
        
        t_label = QLabel(title)
        t_label.setStyleSheet("color: #888; font-size: 12px; font-weight: bold;")
        self.value_label = QLabel(val)
        self.value_label.setStyleSheet("color: #fff; font-size: 24px; font-weight: bold; margin-top: 5px;")
        
        lay.addWidget(t_label)
        lay.addWidget(self.value_label)

class WelcomePage(BasePageTemplate):
    def __init__(self, context):
        super().__init__("welcome", context)
        self.store = SqliteDocumentStore()
        
        # Quick stats layout
        self.stats_layout = QHBoxLayout()
        self.stats_layout.setSpacing(20)
        
        self.total_profiles_card = StatCard("Total Profiles", "0")
        self.total_templates_card = StatCard("Active Templates", "0")
        
        self.stats_layout.addWidget(self.total_profiles_card)
        self.stats_layout.addWidget(self.total_templates_card)
        self.content_layout.addLayout(self.stats_layout)
        
        # Action Buttons Layout
        self.actions_layout = QHBoxLayout()
        self.btn_create_template = QPushButton("Tạo Mẫu Hồ Sơ")
        self.btn_create_profile = QPushButton("Tạo Hồ Sơ Mới")
        
        self.btn_create_template.setStyleSheet("background-color: #2a82da; color: white; padding: 8px 16px; font-weight: bold; border-radius: 4px;")
        self.btn_create_profile.setStyleSheet("background-color: #2ecc71; color: white; padding: 8px 16px; font-weight: bold; border-radius: 4px;")
        self.btn_create_template.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_create_profile.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.actions_layout.addWidget(self.btn_create_template)
        self.actions_layout.addWidget(self.btn_create_profile)
        self.actions_layout.addStretch()
        self.content_layout.addLayout(self.actions_layout)
        
        # Profiles Table Label
        self.table_label = QLabel("Danh sách Hồ sơ Đơn vị (Nhấp đúp dòng để xem tài liệu):")
        self.table_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px;")
        self.content_layout.addWidget(self.table_label)
        
        # Profiles Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Mã Hồ sơ", "Loại Hồ sơ", "Trạng thái", "Ngày tạo", "Số tài liệu"])
        header = self.table.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.itemDoubleClicked.connect(self._on_row_double_clicked)
        self.content_layout.addWidget(self.table)
        
        # Connect Actions
        self.btn_create_template.clicked.connect(self._go_to_create_template)
        self.btn_create_profile.clicked.connect(self._go_to_create_profile)
        
        self.refresh_data()

    def refresh_data(self):
        profiles = self.store.list_documents("profiles")
        templates = self.store.list_documents("profile_templates")
        
        self.total_profiles_card.value_label.setText(str(len(profiles)))
        self.total_templates_card.value_label.setText(str(len(templates)))
        
        self.table.setRowCount(0)
        for p in profiles:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            p_id = p.get("profile_id", "")
            t_id = p.get("template_id", "")
            status = p.get("status", "Draft")
            created_at = p.get("created_at", "")
            docs_count = str(len(p.get("documents", [])))
            
            self.table.setItem(row, 0, QTableWidgetItem(p_id))
            self.table.setItem(row, 1, QTableWidgetItem(t_id))
            
            status_item = QTableWidgetItem(status)
            if status == "Approved":
                status_item.setForeground(Qt.GlobalColor.green)
            elif status == "Pending":
                status_item.setForeground(Qt.GlobalColor.yellow)
            self.table.setItem(row, 2, status_item)
            
            self.table.setItem(row, 3, QTableWidgetItem(created_at))
            self.table.setItem(row, 4, QTableWidgetItem(docs_count))

    def _on_row_double_clicked(self, item: Any):
        row = item.row()
        item_obj = self.table.item(row, 0)
        if item_obj is None:
            return
        profile_id = item_obj.text()
        # Switch to document manager view for this profile
        main_win: Any = self.window()
        if main_win is not None and hasattr(main_win, "switch_to_document_manager"):
            main_win.switch_to_document_manager(profile_id)

    def _go_to_create_template(self):
        main_win: Any = self.window()
        if main_win is not None and hasattr(main_win, "switch_page"):
            main_win.switch_page("create_profile_template")

    def _go_to_create_profile(self):
        main_win: Any = self.window()
        if main_win is not None and hasattr(main_win, "switch_page"):
            main_win.switch_page("create_profile")

    def retranslate_ui(self, lang_code: str):
        pass
