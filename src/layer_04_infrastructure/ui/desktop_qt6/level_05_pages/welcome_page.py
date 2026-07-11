from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QLabel, QMessageBox, QFrame, QAbstractItemView
)
from PyQt6.QtCore import Qt
from typing import Any
from src.shared.logger.app_logger import get_logger
from ..level_01_atoms.labels import HeaderLabel, BodyLabel
from ..level_04_templates.page_template import BasePageTemplate
from src.layer_04_infrastructure.databases.sqlite.sqlite_document_store import SqliteDocumentStore

logger = get_logger(__name__)

class StatCard(QFrame):
    def __init__(self, title: str, val: str, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setProperty("class", "StatCard")
        self.setObjectName("stat_card")
        lay = QVBoxLayout(self)
        
        self.title_label = BodyLabel(title)
        self.value_label = HeaderLabel(val)
        
        lay.addWidget(self.title_label)
        lay.addWidget(self.value_label)

class WelcomePage(BasePageTemplate):
    def __init__(self, context):
        super().__init__("welcome", context)
        self.store = SqliteDocumentStore()
        
        # Quick stats layout
        self.stats_layout = QHBoxLayout()
        self.stats_layout.setSpacing(24)
        
        self.total_profiles_card = StatCard(self.i18n_manager.translate("total_profiles"), "0")
        self.total_templates_card = StatCard(self.i18n_manager.translate("active_templates"), "0")
        
        self.stats_layout.addWidget(self.total_profiles_card)
        self.stats_layout.addWidget(self.total_templates_card)
        self.content_layout.addLayout(self.stats_layout)
        
        # Action Buttons Layout
        self.actions_layout = QHBoxLayout()
        from ..level_01_atoms.buttons import PrimaryButton, SecondaryButton
        self.btn_create_template = PrimaryButton(self.i18n_manager.translate("btn_create_template"))
        self.btn_create_profile = SecondaryButton(self.i18n_manager.translate("btn_create_profile"))
        
        self.btn_create_template.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_create_profile.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.actions_layout.addWidget(self.btn_create_template)
        self.actions_layout.addWidget(self.btn_create_profile)
        self.actions_layout.addStretch()
        self.content_layout.addLayout(self.actions_layout)
        
        # Profiles Table Label
        self.table_label = QLabel(self.i18n_manager.translate("lbl_profiles_list"))
        self.table_label.setObjectName("table_title_lbl")
        self.content_layout.addWidget(self.table_label)
        
        # Profiles Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            self.i18n_manager.translate("tbl_profile_id"),
            self.i18n_manager.translate("tbl_profile_type"),
            self.i18n_manager.translate("tbl_status"),
            self.i18n_manager.translate("tbl_created_at"),
            self.i18n_manager.translate("tbl_docs_count")
        ])
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
        # Update cards
        profiles = self.store.list_documents("profiles")
        templates = self.store.list_documents("profile_templates")
        
        self.total_profiles_card.value_label.setText(str(len(profiles)))
        self.total_templates_card.value_label.setText(str(len(templates)))
        
        # Update table
        self.table.setRowCount(0)
        for p in profiles:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            p_id = p.get("profile_id", "")
            p_type = p.get("template_id", "")
            status = p.get("status", "Active")
            created_at = p.get("created_at", "")
            docs_count = str(len(p.get("documents", [])))
            
            self.table.setItem(row, 0, QTableWidgetItem(p_id))
            self.table.setItem(row, 1, QTableWidgetItem(p_type))
            self.table.setItem(row, 2, QTableWidgetItem(status))
            self.table.setItem(row, 3, QTableWidgetItem(created_at))
            self.table.setItem(row, 4, QTableWidgetItem(docs_count))

    def _on_row_double_clicked(self, item: Any):
        row = item.row()
        id_item = self.table.item(row, 0)
        if id_item is not None:
            profile_id = id_item.text()
            self._open_document_manager(profile_id)

    def _open_document_manager(self, profile_id: str):
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
        self.total_profiles_card.title_label.setText(self.i18n_manager.translate("total_profiles"))
        self.total_templates_card.title_label.setText(self.i18n_manager.translate("active_templates"))
        self.btn_create_template.setText(self.i18n_manager.translate("btn_create_template"))
        self.btn_create_profile.setText(self.i18n_manager.translate("btn_create_profile"))
        self.table_label.setText(self.i18n_manager.translate("lbl_profiles_list"))
        self.table.setHorizontalHeaderLabels([
            self.i18n_manager.translate("tbl_profile_id"),
            self.i18n_manager.translate("tbl_profile_type"),
            self.i18n_manager.translate("tbl_status"),
            self.i18n_manager.translate("tbl_created_at"),
            self.i18n_manager.translate("tbl_docs_count")
        ])
