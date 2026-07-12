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
)
from PyQt6.QtCore import Qt, QMetaObject, Q_ARG, pyqtSlot
from typing import Any
from src.shared.logger.app_logger import get_logger
from ..level_04_templates.page_template import BasePageTemplate
from src.layer_04_infrastructure.databases.sqlite.sqlite_document_store import (
    SqliteDocumentStore,
)
from src.layer_03_interface_adapters.controllers.desktop.checkout_document import (
    CheckoutDocumentController,
)
from src.layer_03_interface_adapters.controllers.desktop.checkin_document import (
    CheckinDocumentController,
)
from src.layer_03_interface_adapters.controllers.desktop.generate_document_from_template import (
    GenerateDocumentFromTemplateController,
)
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
        self.generate_controller = context.container.resolve(
            GenerateDocumentFromTemplateController
        )

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
        self.lbl_info_title.setStyleSheet("font-weight: bold; font-size: 14px;")
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
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            [
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
        self.current_template = None

    def set_profile(self, profile_id: str):
        self.profile_id = profile_id
        self.lbl_subtitle.setText(f"Hồ sơ: {profile_id}")
        self.refresh_dynamic_inputs()
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
            size = doc.get("size", 0)

            self.table.setItem(row, 0, QTableWidgetItem(d_id))
            self.table.setItem(row, 1, QTableWidgetItem(name))
            self.table.setItem(row, 2, QTableWidgetItem(f"v{ver}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{size / 1024:.1f} KB"))

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
            self.table.setCellWidget(row, 4, btn_edit)

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
            "user_id": "user_dong",  # current user
        }

        res = asyncio.run(self.checkout_controller.handle_request(req))

        if res.get("status") == "success":
            doc_url = res.get("document_url", "")
            local_name = res.get("local_filename", "")

            # Since local document store sets file:/// absolute paths:
            if not doc_url:
                QMessageBox.critical(
                    self, "Lỗi", "Đường dẫn tài liệu (URL) trống hoặc không hợp lệ."
                )
                return

            if doc_url.startswith("file:///"):
                file_path = doc_url.replace("file:///", "")
            else:
                file_path = doc_url

            # Convert Windows slash
            file_path = os.path.abspath(file_path)

            if not os.path.isfile(file_path):
                QMessageBox.critical(
                    self, "Lỗi", f"Không tìm thấy file tài liệu tại: {file_path}"
                )
                return

            # Create a temporary working copy in appdata/temp_editing/
            temp_dir = os.path.join("appdata", "temp_editing", self.profile_id)
            os.makedirs(temp_dir, exist_ok=True)
            temp_file_path = os.path.abspath(os.path.join(temp_dir, local_name))

            # Copy to temp path
            try:
                shutil.copy2(file_path, temp_file_path)
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể tạo file tạm: {e}")
                return

            # Open MS Word
            try:
                os.startfile(temp_file_path)
                main_win: Any = self.window()
                if main_win and hasattr(main_win, "statusBar") and main_win.statusBar():
                    main_win.statusBar().showMessage(
                        f"✓ Đã mở '{local_name}'. Hãy sửa trong Word, bấm Ctrl+S rồi bấm 'Hoàn thành sửa' để lưu.",
                        9000,
                    )
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể mở file bằng Word: {e}")
                return

            self.refresh_documents()
        else:
            QMessageBox.critical(self, "Lỗi Khóa Tài Liệu", res.get("message"))

    def _finish_editing_doc(self, doc_id: str):
        profile = self.store.get_document("profiles", self.profile_id)
        if not profile:
            return

        target_doc = None
        for doc in profile.get("documents", []):
            if doc["document_id"] == doc_id:
                target_doc = doc
                break

        if not target_doc:
            return

        doc_url = target_doc.get("url", "")
        name = target_doc.get("name", "")

        if doc_url.startswith("file:///"):
            original_path = doc_url.replace("file:///", "")
        else:
            original_path = doc_url
        original_path = os.path.abspath(original_path)

        temp_dir = os.path.join("appdata", "temp_editing", self.profile_id)
        temp_path = os.path.abspath(os.path.join(temp_dir, name))

        if not os.path.exists(temp_path):
            QMessageBox.critical(
                self,
                "Lỗi",
                f"Không tìm thấy file tạm để đồng bộ tại: {temp_path}",
            )
            return

        # Attempt to copy file back
        import time

        copied = False
        last_err = None
        for attempt in range(3):
            try:
                shutil.copy2(temp_path, original_path)
                copied = True
                break
            except Exception as e:
                last_err = e
                time.sleep(0.5)

        if not copied:
            QMessageBox.warning(
                self,
                "Lỗi Khóa File",
                "Không thể đồng bộ vì tệp đang bị MS Word khóa độc quyền.\n\n"
                "Vui lòng nhấn Lưu (Ctrl+S) trong Word, đóng Word lại rồi bấm 'Hoàn thành sửa' thử lại!",
            )
            return

        # Calculate new size and checksum
        import hashlib

        new_size = os.path.getsize(original_path)
        with open(original_path, "rb") as f:
            new_checksum = hashlib.sha256(f.read()).hexdigest()

        new_url = "file:///" + os.path.abspath(original_path).replace("\\", "/")

        req = {
            "profile_id": self.profile_id,
            "document_id": doc_id,
            "user_id": "user_dong",
            "new_url": new_url,
            "new_size": new_size,
            "new_checksum": new_checksum,
        }

        # Run checkin
        res = asyncio.run(self.checkin_controller.handle_request(req))

        if res.get("status") == "success":
            msg = f"✓ Đồng bộ thành công: Tài liệu đã được lưu lại hệ thống (Phiên bản mới: {res.get('new_version')})"
            main_win: Any = self.window()
            if main_win and hasattr(main_win, "statusBar") and main_win.statusBar():
                main_win.statusBar().showMessage(msg, 6000)
        else:
            QMessageBox.critical(self, "Lỗi Đồng Bộ", res.get("message"))

        # Clean up temp file
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except Exception:
            pass

        self.refresh_dynamic_inputs()
        self.refresh_documents()

    def _generate_from_template(self):
        # Get profile
        profile = self.store.get_document("profiles", self.profile_id)
        if not profile:
            return

        t_id = profile.get("template_id", "")
        template = self.store.get_document("profile_templates", t_id)
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
                    "Không tìm thấy file Word (.docx) mẫu nào trong thư mục cấu hình!",
                )
                return

            # Generate all docx files in the directory
            reply = QMessageBox.question(
                self,
                "Xác nhận sinh hồ sơ",
                f"Phát hiện {len(docx_files)} file tài liệu mẫu trong thư mục cấu hình.\nBạn có muốn tự động sinh toàn bộ các tài liệu này?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.No:
                return

            reqs = []
            for f in docx_files:
                reqs.append(
                    {
                        "profile_id": self.profile_id,
                        "template_doc_path": os.path.join(t_dir, f),
                        "output_doc_name": f,
                    }
                )

        # Run requests
        success_count = 0
        for req in reqs:
            res = asyncio.run(self.generate_controller.handle_request(req))
            if res.get("status") == "success":
                success_count += 1

        if success_count > 0:
            msg = f"✓ Đã sinh thành công {success_count}/{len(reqs)} tài liệu hồ sơ từ thư mục mẫu!"
            main_win: Any = self.window()
            if main_win and hasattr(main_win, "statusBar") and main_win.statusBar():
                main_win.statusBar().showMessage(msg, 5000)
            self.refresh_documents()
        else:
            QMessageBox.critical(
                self, "Lỗi", "Không thể sinh tài liệu nào từ thư mục mẫu."
            )

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
        self.refresh_documents()

    def refresh_dynamic_inputs(self):
        # Clear previous layout widgets safely
        while self.info_form_layout.count() > 0:
            item = self.info_form_layout.takeAt(0)
            if item is not None:
                w = item.widget()
                if w is not None:
                    w.setParent(None)
                    w.deleteLater()
        self.info_widgets_map = {}

        if not self.profile_id:
            return

        profile = self.store.get_document("profiles", self.profile_id)
        if not profile:
            return

        t_id = profile.get("template_id", "")
        self.current_template = self.store.get_document("profile_templates", t_id)
        if not self.current_template:
            return

        schema = self.current_template.get("fields_schema", [])
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

            val = dynamic_data.get(f_name)

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

        profile = self.store.get_document("profiles", self.profile_id)
        if not profile:
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

        profile["dynamic_data"] = dynamic_data

        # Save to database
        self.store.set_document("profiles", self.profile_id, profile)

        # Regenerate all documents using updated dynamic_data (App -> Doc)
        t_id = profile.get("template_id", "")
        template = self.store.get_document("profile_templates", t_id)
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

                success_count = 0
                for f in docx_files:
                    req = {
                        "profile_id": self.profile_id,
                        "template_doc_path": os.path.join(t_dir, f),
                        "output_doc_name": f,
                    }
                    res = asyncio.run(self.generate_controller.handle_request(req))
                    if res.get("status") == "success":
                        success_count += 1

                msg = f"✓ Đã lưu thông tin và cập nhật thành công {success_count}/{len(docx_files)} tài liệu hồ sơ!"
                main_win: Any = self.window()
                if main_win and hasattr(main_win, "statusBar") and main_win.statusBar():
                    main_win.statusBar().showMessage(msg, 5000)
            else:
                QMessageBox.warning(
                    self,
                    "Thông báo",
                    "Lưu thành công, nhưng không tìm thấy thư mục mẫu để cập nhật tài liệu.",
                )
        else:
            QMessageBox.warning(
                self,
                "Thông báo",
                "Lưu thành công, nhưng mẫu hồ sơ không còn tồn tại để cập nhật tài liệu.",
            )

        self.refresh_documents()
