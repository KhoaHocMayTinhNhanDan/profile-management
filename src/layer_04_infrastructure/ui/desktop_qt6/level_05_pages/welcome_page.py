from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QLabel,
    QMessageBox,
    QFrame,
    QAbstractItemView,
    QWidget,
)
from PyQt6.QtCore import Qt
from typing import Any
import os
import shutil
from src.shared.logger.app_logger import get_logger
from ..level_01_atoms.labels import HeaderLabel, BodyLabel
from ..level_04_templates.page_template import BasePageTemplate
from src.layer_04_infrastructure.databases.sqlite.sqlite_document_store import (
    SqliteDocumentStore,
)

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

        self.total_profiles_card = StatCard(
            self.i18n_manager.translate("total_profiles"), "0"
        )
        self.total_templates_card = StatCard(
            self.i18n_manager.translate("active_templates"), "0"
        )

        self.stats_layout.addWidget(self.total_profiles_card)
        self.stats_layout.addWidget(self.total_templates_card)
        self.content_layout.addLayout(self.stats_layout)

        # Action Buttons Layout
        self.actions_layout = QHBoxLayout()
        from ..level_01_atoms.buttons import PrimaryButton, SecondaryButton

        self.btn_create_template = PrimaryButton(
            self.i18n_manager.translate("btn_create_template")
        )
        self.btn_create_profile = SecondaryButton(
            self.i18n_manager.translate("btn_create_profile")
        )

        self.btn_create_template.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_create_profile.setCursor(Qt.CursorShape.PointingHandCursor)

        self.actions_layout.addWidget(self.btn_create_template)
        self.actions_layout.addWidget(self.btn_create_profile)
        self.actions_layout.addStretch()
        self.content_layout.addLayout(self.actions_layout)

        # Split Layout for List of Profiles and List of Templates (Vertical stacking)
        # 1. Profiles Section
        self.table_label = QLabel(self.i18n_manager.translate("lbl_profiles_list"))
        self.table_label.setObjectName("table_title_lbl")
        self.content_layout.addWidget(self.table_label)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            [
                self.i18n_manager.translate("tbl_profile_id"),
                self.i18n_manager.translate("tbl_profile_type"),
                self.i18n_manager.translate("tbl_status"),
                self.i18n_manager.translate("tbl_created_at"),
                self.i18n_manager.translate("tbl_docs_count"),
            ]
        )
        p_header = self.table.horizontalHeader()
        if p_header is not None:
            p_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.itemDoubleClicked.connect(self._on_row_double_clicked)
        self.content_layout.addWidget(self.table)

        # 2. Templates Section
        self.templates_label = QLabel("Danh sách mẫu hồ sơ trong hệ thống:")
        self.templates_label.setObjectName("table_title_lbl")
        self.content_layout.addWidget(self.templates_label)

        self.templates_table = QTableWidget()
        self.templates_table.setColumnCount(5)
        self.templates_table.setHorizontalHeaderLabels(
            [
                "Mã mẫu",
                "Tên mẫu hồ sơ",
                "Số thuộc tính",
                "Số tệp mẫu (.docx)",
                "Thao tác",
            ]
        )
        t_header = self.templates_table.horizontalHeader()
        if t_header is not None:
            t_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            t_header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.templates_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.templates_table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        v_hdr = self.templates_table.verticalHeader()
        if v_hdr is not None:
            v_hdr.setDefaultSectionSize(38)
            v_hdr.setVisible(False)
        self.content_layout.addWidget(self.templates_table)

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

        # Update Profiles table
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

        # Update Templates table
        self.templates_table.setRowCount(0)
        for t in templates:
            row = self.templates_table.rowCount()
            self.templates_table.insertRow(row)

            t_id = t.get("template_id", "")
            t_name = t.get("name", "")
            fields_count = str(len(t.get("fields_schema", [])))

            # Count docx files in imported templates folder
            t_dir = t.get("template_dir", "")
            docx_count = 0
            if t_dir and os.path.exists(t_dir):
                docx_count = len(
                    [
                        f
                        for f in os.listdir(t_dir)
                        if f.endswith(".docx") and not f.startswith("~$")
                    ]
                )

            self.templates_table.setItem(row, 0, QTableWidgetItem(t_id))
            self.templates_table.setItem(row, 1, QTableWidgetItem(t_name))
            self.templates_table.setItem(row, 2, QTableWidgetItem(fields_count))
            self.templates_table.setItem(row, 3, QTableWidgetItem(str(docx_count)))

            # Action buttons: Edit, Open folder & Delete template
            actions_widget = QWidget()
            actions_lay = QHBoxLayout(actions_widget)
            actions_lay.setContentsMargins(4, 2, 4, 2)
            actions_lay.setSpacing(6)

            from ..level_01_atoms.buttons import SecondaryButton, DangerButton

            btn_edit = SecondaryButton("Sửa")
            btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_edit.clicked.connect(lambda checked, tid=t_id: self._edit_template(tid))

            btn_open = SecondaryButton("Thư mục mẫu")
            btn_open.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_open.clicked.connect(
                lambda checked, path=t_dir: self._open_template_dir(path)
            )

            btn_delete = DangerButton("Xóa")
            btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_delete.clicked.connect(
                lambda checked, tid=t_id, name=t_name: self._delete_template(tid, name)
            )

            actions_lay.addWidget(btn_edit)
            actions_lay.addWidget(btn_open)
            actions_lay.addWidget(btn_delete)
            self.templates_table.setCellWidget(row, 4, actions_widget)

    def _edit_template(self, template_id: str):
        main_win: Any = self.window()
        if main_win is not None and hasattr(main_win, "switch_to_edit_template"):
            main_win.switch_to_edit_template(template_id)

    def _open_template_dir(self, t_dir: str):
        if t_dir and os.path.exists(t_dir):
            os.startfile(os.path.abspath(t_dir))
        else:
            QMessageBox.warning(
                self,
                "Cảnh báo",
                "Thư mục lưu trữ mẫu của ứng dụng không tồn tại hoặc chưa được import!",
            )

    def _delete_template(self, template_id: str, template_name: str):
        reply = QMessageBox.question(
            self,
            "Xác nhận xóa mẫu",
            f"Bạn có chắc chắn muốn xóa mẫu hồ sơ '{template_name}' ({template_id}) khỏi hệ thống?\nHành động này cũng sẽ xóa toàn bộ các tệp Word mẫu đã import của nó.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            # Delete from DB
            self.store.delete_document("profile_templates", template_id)

            # Clean up local templates folder
            t_dir = os.path.join("appdata", "templates", template_id)
            if os.path.exists(t_dir):
                try:
                    shutil.rmtree(t_dir)
                except Exception as e:
                    logger.error(f"Failed to delete templates folder {t_dir}: {e}")

            msg = f"✓ Đã xóa mẫu hồ sơ '{template_name}' khỏi hệ thống thành công!"
            main_win: Any = self.window()
            if main_win and hasattr(main_win, "statusBar") and main_win.statusBar():
                main_win.statusBar().showMessage(msg, 5000)
            self.refresh_data()

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
        self.total_profiles_card.title_label.setText(
            self.i18n_manager.translate("total_profiles")
        )
        self.total_templates_card.title_label.setText(
            self.i18n_manager.translate("active_templates")
        )
        self.btn_create_template.setText(
            self.i18n_manager.translate("btn_create_template")
        )
        self.btn_create_profile.setText(
            self.i18n_manager.translate("btn_create_profile")
        )
        self.table_label.setText(self.i18n_manager.translate("lbl_profiles_list"))
        self.table.setHorizontalHeaderLabels(
            [
                self.i18n_manager.translate("tbl_profile_id"),
                self.i18n_manager.translate("tbl_profile_type"),
                self.i18n_manager.translate("tbl_status"),
                self.i18n_manager.translate("tbl_created_at"),
                self.i18n_manager.translate("tbl_docs_count"),
            ]
        )

        # Translate templates section label
        self.templates_label.setText("Danh sách mẫu hồ sơ trong hệ thống:")
        self.templates_table.setHorizontalHeaderLabels(
            [
                "Mã mẫu",
                "Tên mẫu hồ sơ",
                "Số thuộc tính",
                "Số tệp mẫu (.docx)",
                "Thao tác",
            ]
        )
