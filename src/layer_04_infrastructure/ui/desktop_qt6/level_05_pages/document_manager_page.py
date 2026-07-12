from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QLabel,
    QMessageBox,
    QFileDialog,
    QInputDialog,
    QAbstractItemView,
    QLineEdit,
    QWidget,
    QProgressBar,
    QFrame,
)
from PyQt6.QtCore import Qt, QMetaObject, Q_ARG, pyqtSlot
from typing import Any
from src.shared.logger.app_logger import get_logger
from ..level_04_templates.page_template import BasePageTemplate
from ..hooks.use_checkout_document import UseCheckoutDocument
from ..hooks.use_checkin_document import UseCheckinDocument
from ..hooks.use_update_profile import UseUpdateProfile
from ..hooks.use_generate_document_from_template import UseGenerateDocumentFromTemplate
import os

logger = get_logger(__name__)


class DocumentManagerPage(BasePageTemplate):
    def __init__(self, context):
        super().__init__("document_manager", context)
        self.use_checkout = UseCheckoutDocument(context, self)
        self.use_checkin = UseCheckinDocument(context, self)
        self.use_update_profile = UseUpdateProfile(context, self)
        self.use_generate = UseGenerateDocumentFromTemplate(context, self)

        self.use_checkout.finished.connect(self._on_checkout_success)
        self.use_checkout.error.connect(self._on_checkout_error)
        self.use_checkin.finished.connect(self._on_checkin_success)
        self.use_checkin.error.connect(self._on_checkin_error)

        self.use_update_profile.profile_loaded.connect(self._on_profile_loaded)
        self.use_update_profile.template_loaded.connect(self._on_template_loaded)
        self.use_update_profile.profile_updated.connect(self._on_profile_updated)
        self.use_update_profile.error.connect(self._on_profile_error)

        self.use_generate.finished.connect(self._on_generate_finished)
        self.use_generate.error.connect(self._on_generate_error)

        self.use_checkout.loading.connect(self._set_loading)
        self.use_checkin.loading.connect(self._set_loading)
        self.use_generate.loading.connect(self._set_loading)

        self.profile_id = ""

        # Main horizontal split layout
        self.main_split_layout = QHBoxLayout()
        self.main_split_layout.setSpacing(15)

        # ----------------- LEFT PANEL: PROFILE INFO & DYNAMIC INPUTS -----------------
        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout(self.left_panel)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(10)

        self.lbl_info_title = QLabel("Thông tin biểu mẫu")
        self.lbl_info_title.setObjectName("table_title_lbl")
        self.left_layout.addWidget(self.lbl_info_title)

        from PyQt6.QtWidgets import QScrollArea, QFormLayout

        self.info_scroll = QScrollArea()
        self.info_scroll.setWidgetResizable(True)
        self.info_scroll.setObjectName("profile_info_scroll")

        self.info_form_widget = QWidget()
        self.info_form_layout = QFormLayout(self.info_form_widget)
        self.info_form_layout.setSpacing(10)
        self.info_scroll.setWidget(self.info_form_widget)
        self.left_layout.addWidget(self.info_scroll)

        from ..level_01_atoms.buttons import PrimaryButton

        self.btn_save_info = PrimaryButton("Lưu thông tin")
        self.btn_save_info.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_save_info.setShortcut("Ctrl+S")
        self.btn_save_info.setToolTip("Lưu thông tin hồ sơ (Ctrl+S)")
        self.btn_save_info.clicked.connect(self._save_profile_info)
        self.left_layout.addWidget(self.btn_save_info)

        # ----------------- RIGHT PANEL: ACTIONS & DOCUMENTS TABLE -----------------
        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout(self.right_panel)
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(10)

        # Subtitle
        self.lbl_subtitle = QLabel(
            self.i18n_manager.translate("lbl_profile_subtitle") + ": "
        )
        self.lbl_subtitle.setObjectName("profile_subtitle_lbl")
        self.right_layout.addWidget(self.lbl_subtitle)

        # Buttons layout
        self.actions_layout = QHBoxLayout()
        from ..level_01_atoms.buttons import SecondaryButton

        self.btn_back = SecondaryButton(
            self.i18n_manager.translate("btn_back_dashboard")
        )
        self.btn_back.setShortcut("Esc")
        self.btn_back.setCursor(Qt.CursorShape.PointingHandCursor)

        self.actions_layout.addWidget(self.btn_back)
        self.actions_layout.addStretch()
        self.right_layout.addLayout(self.actions_layout)

        # Documents Table
        self.table = QTableWidget()
        v_header = self.table.verticalHeader()
        if v_header is not None:
            v_header.setVisible(False)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            [
                "STT",
                self.i18n_manager.translate("tbl_doc_id"),
                self.i18n_manager.translate("tbl_doc_name"),
                self.i18n_manager.translate("tbl_doc_version"),
                self.i18n_manager.translate("tbl_doc_size"),
                self.i18n_manager.translate("tbl_doc_action"),
            ]
        )
        header = self.table.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.right_layout.addWidget(self.table)

        # Assemble main split layout
        self.main_split_layout.addWidget(self.left_panel, 35)
        self.main_split_layout.addWidget(self.right_panel, 65)
        self.content_layout.addLayout(self.main_split_layout)

        # Connect Actions
        self.btn_back.clicked.connect(self._go_back)
        self.table.itemDoubleClicked.connect(self._on_row_double_clicked)

        self.info_widgets_map = {}

    def set_profile(self, profile_id: str):
        self.profile_id = profile_id
        self.lbl_subtitle.setText(f"Hồ sơ: {profile_id}")
        self.use_update_profile.load_profile(profile_id)

    @pyqtSlot(dict)
    def _on_profile_loaded(self, profile: dict):
        self.current_profile = profile
        self._render_documents(profile.get("documents", []))

        t_id = profile.get("template_id", "")
        if t_id:
            self.use_update_profile.load_template(t_id)

    @pyqtSlot(dict)
    def _on_template_loaded(self, template: dict):
        self.current_template = template
        if hasattr(self, "current_profile") and self.current_profile:
            self._render_dynamic_inputs(self.current_profile, template)

    @pyqtSlot(dict)
    def _on_profile_updated(self, res: dict):
        if self.current_template:
            t_dir = self.current_template.get("template_dir", "")
            if t_dir and os.path.exists(t_dir):
                docx_files = sorted(
                    [
                        f
                        for f in os.listdir(t_dir)
                        if f.endswith(".docx") and not f.startswith("~$")
                    ]
                )

                reqs = []
                for f in docx_files:
                    reqs.append(
                        {
                            "profile_id": self.profile_id,
                            "template_doc_path": os.path.join(t_dir, f),
                            "output_doc_name": f,
                        }
                    )
                self.use_generate.generate_documents(reqs)
            else:
                QMessageBox.warning(
                    self,
                    "Thông báo",
                    "Lưu thành công, nhưng không tìm thấy thư mục mẫu để cập nhật tài liệu.",
                )
                self.use_update_profile.load_profile(self.profile_id)
        else:
            self.use_update_profile.load_profile(self.profile_id)

    @pyqtSlot(str)
    def _on_profile_error(self, err_msg: str):
        QMessageBox.critical(self, "Lỗi Nghiệp Vụ", err_msg)

    @pyqtSlot(int, int)
    def _on_generate_finished(self, success_count: int, total_count: int):
        if success_count > 0:
            msg = f"✓ Sinh tài liệu thành công: {success_count}/{total_count} file đã được đồng bộ!"
            main_win: Any = self.window()
            if main_win and hasattr(main_win, "show_status_message"):
                main_win.show_status_message(msg, "success", 5000)
        else:
            QMessageBox.critical(
                self, "Lỗi", "Không thể sinh tài liệu nào từ thư mục mẫu."
            )
        self.use_update_profile.load_profile(self.profile_id)

    @pyqtSlot(str)
    def _on_generate_error(self, err_msg: str):
        QMessageBox.critical(self, "Lỗi Sinh Tài Liệu", err_msg)
        self.use_update_profile.load_profile(self.profile_id)

    @pyqtSlot(bool)
    def _set_loading(self, is_loading: bool):
        main_win: Any = self.window()
        if is_loading:
            self.setCursor(Qt.CursorShape.WaitCursor)
            self.btn_save_info.setEnabled(False)
            self.btn_back.setEnabled(False)
            self.table.setEnabled(False)
            if main_win and hasattr(main_win, "set_loading"):
                main_win.set_loading(True)
        else:
            self.unsetCursor()
            self.btn_save_info.setEnabled(True)
            self.btn_back.setEnabled(True)
            self.table.setEnabled(True)
            if main_win and hasattr(main_win, "set_loading"):
                main_win.set_loading(False)

    def _render_documents(self, docs: list):
        self.table.setRowCount(0)
        for doc in docs:
            row = self.table.rowCount()
            self.table.insertRow(row)

            d_id = doc.get("document_id", "")
            name = doc.get("name", "")
            ver = doc.get("version", "1.0")
            is_locked = doc.get("is_locked", False)
            size = doc.get("size", 0)

            self.table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            self.table.setItem(row, 1, QTableWidgetItem(d_id))
            self.table.setItem(row, 2, QTableWidgetItem(name))
            self.table.setItem(row, 3, QTableWidgetItem(f"v{ver}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{size / 1024:.1f} KB"))

            # Action button for edit
            from ..level_01_atoms.buttons import SecondaryButton

            btn_text = (
                self.i18n_manager.translate("status_editing")
                if is_locked
                else self.i18n_manager.translate("status_viewing")
            )
            btn_edit = SecondaryButton(btn_text)
            btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
            if is_locked:
                btn_edit.clicked.connect(
                    lambda checked, d=d_id: self._finish_editing_doc(d)
                )
            else:
                btn_edit.clicked.connect(
                    lambda checked, d=d_id: self._start_editing_doc(d)
                )
            self.table.setCellWidget(row, 5, btn_edit)

    def _on_row_double_clicked(self, item: Any):
        row = item.row()
        item_obj = self.table.item(row, 1)
        doc_id = item_obj.text() if item_obj is not None else ""
        self._start_editing_doc(doc_id)

    def _start_editing_doc(self, doc_id: str):
        self.use_checkout.checkout(self.profile_id, doc_id)

    def _finish_editing_doc(self, doc_id: str):
        self.use_checkin.force_unlock(self.profile_id, doc_id)

    @pyqtSlot(dict)
    def _on_checkout_success(self, res: dict):
        local_name = res.get("local_filename", "")
        main_win: Any = self.window()
        if main_win and hasattr(main_win, "show_status_message"):
            main_win.show_status_message(
                f"✓ Đã mở '{local_name}'. Tự động đồng bộ khi bạn lưu và đóng Word.",
                "info",
                9000,
            )
        if self.profile_id:
            self.use_update_profile.load_profile(self.profile_id)

    @pyqtSlot(str)
    def _on_checkout_error(self, error_msg: str):
        QMessageBox.critical(self, "Lỗi Khóa Tài Liệu", error_msg)
        if self.profile_id:
            self.use_update_profile.load_profile(self.profile_id)

    @pyqtSlot(dict)
    def _on_checkin_success(self, res: dict):
        msg = f"✓ Tự động đồng bộ thành công: Tài liệu đã được lưu lại hệ thống (Phiên bản mới: {res.get('new_version')})"
        main_win: Any = self.window()
        if main_win and hasattr(main_win, "show_status_message"):
            main_win.show_status_message(msg, "success", 6000)
        if self.profile_id:
            self.use_update_profile.load_profile(self.profile_id)

    @pyqtSlot(str)
    def _on_checkin_error(self, error_msg: str):
        QMessageBox.critical(self, "Lỗi Đồng Bộ", error_msg)
        if self.profile_id:
            self.use_update_profile.load_profile(self.profile_id)

    @pyqtSlot(str)
    def _on_watcher_sync_failed(self, error_msg: str):
        QMessageBox.warning(
            self,
            "Lỗi Khóa File",
            f"{error_msg}\n\nVui lòng nhấn Lưu (Ctrl+S) trong Word, đóng Word lại rồi thử lại!",
        )

    def _generate_from_template(self):
        profile = self.current_profile
        if not profile:
            return

        template = self.current_template
        if not template:
            QMessageBox.warning(self, "Thông báo", "Không tìm thấy cấu hình mẫu hồ sơ!")
            return

        t_dir = template.get("template_dir", "")
        if not t_dir or not os.path.exists(t_dir):
            # Fallback to single file selection if no template folder is configured
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Chọn file mẫu Word (.docx)", "", "Word Files (*.docx)"
            )
            if not file_path:
                return

            out_name, ok = QInputDialog.getText(
                self,
                "Tên tài liệu đầu ra",
                "Nhập tên file tài liệu xuất ra (e.g. Hop_Dong_Nhan_Su.docx):",
                QLineEdit.EchoMode.Normal,
                "Hop_Dong_Moi.docx",
            )
            if not ok or not out_name.strip():
                return

            reqs = [
                {
                    "profile_id": self.profile_id,
                    "template_doc_path": file_path,
                    "output_doc_name": out_name.strip(),
                }
            ]
        else:
            # Scanned from template dir
            docx_files = sorted(
                [
                    f
                    for f in os.listdir(t_dir)
                    if f.endswith(".docx") and not f.startswith("~$")
                ]
            )
            if not docx_files:
                QMessageBox.warning(
                    self,
                    "Thông báo",
                    f"Thư mục mẫu hồ sơ trống! Hãy sao chép các file .docx mẫu vào:\n{t_dir}",
                )
                return

            # Generate all docx files in the directory
            reqs = []
            for f in docx_files:
                reqs.append(
                    {
                        "profile_id": self.profile_id,
                        "template_doc_path": os.path.join(t_dir, f),
                        "output_doc_name": f,
                    }
                )

        # Trigger asynchronous generation via hook!
        self.use_generate.generate_documents(reqs)

    def _go_back(self):
        main_win: Any = self.window()
        if main_win is not None and hasattr(main_win, "switch_page"):
            welcome = main_win.pages_map.get("welcome")
            if welcome is not None and hasattr(welcome, "refresh_data"):
                welcome.refresh_data()
            main_win.switch_page("welcome")

    def retranslate_ui(self, lang_code: str):
        self.lbl_subtitle.setText(
            self.i18n_manager.translate("lbl_profile_subtitle") + f": {self.profile_id}"
        )
        self.btn_back.setText(self.i18n_manager.translate("btn_back_dashboard"))
        self.table.setHorizontalHeaderLabels(
            [
                self.i18n_manager.translate("tbl_doc_id"),
                self.i18n_manager.translate("tbl_doc_name"),
                self.i18n_manager.translate("tbl_doc_version"),
                self.i18n_manager.translate("tbl_doc_size"),
                self.i18n_manager.translate("tbl_doc_action"),
            ]
        )
        if self.profile_id:
            self.use_update_profile.load_profile(self.profile_id)

    def _render_dynamic_inputs(self, profile: dict, template: dict):
        # Clear previous layout widgets safely
        while self.info_form_layout.count() > 0:
            item = self.info_form_layout.takeAt(0)
            if item is not None:
                w = item.widget()
                if w is not None:
                    w.setParent(None)
                    w.deleteLater()
        self.info_widgets_map = {}

        schema = template.get("fields_schema", [])
        dynamic_data = profile.get("dynamic_data", {})

        from PyQt6.QtCore import QDate
        from PyQt6.QtWidgets import QDateEdit, QCheckBox, QLabel
        from ..level_01_atoms.inputs import FormLineEdit

        for field in schema:
            f_name = field["name"]
            f_label = field.get("label", f_name)
            f_type = field.get("type", "string")
            req = field.get("required", False)

            label_text = f"{f_label}:"
            if req:
                label_text = f"{f_label} (*):"
            lbl = QLabel(label_text)

            val = dynamic_data.get(f_name, None)

            if f_type == "boolean":
                widget = QCheckBox()
                widget.setChecked(bool(val) if val is not None else False)
            elif f_type == "date":
                widget = QDateEdit()
                widget.setCalendarPopup(True)
                if val:
                    widget.setDate(QDate.fromString(str(val), "yyyy-MM-dd"))
                else:
                    widget.setDate(QDate.currentDate())
            else:
                widget = FormLineEdit()
                widget.setText(str(val) if val is not None else "")
                if f_type == "number":
                    widget.setPlaceholderText("Nhập số")

            self.info_form_layout.addRow(lbl, widget)
            self.info_widgets_map[f_name] = (widget, f_type, req)

    def _save_profile_info(self):
        if not self.profile_id:
            return

        dynamic_data = {}
        for f_name, (widget, f_type, req) in self.info_widgets_map.items():
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
                        QMessageBox.warning(
                            self, "Cảnh báo", f"Trường '{f_name}' phải nhập kiểu số!"
                        )
                        return

            dynamic_data[f_name] = val

        self.use_update_profile.update_profile(self.profile_id, dynamic_data)
