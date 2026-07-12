from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QComboBox,
    QCheckBox,
    QLabel,
    QMessageBox,
    QWidget,
    QGridLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFileDialog,
    QApplication,
    QFrame,
    QScrollArea,
)
from PyQt6.QtCore import Qt, QTimer, QEvent, QObject, pyqtSlot
from src.shared.logger.app_logger import get_logger
from ..level_04_templates.page_template import BasePageTemplate
from ..hooks.use_create_profile_template import UseCreateProfileTemplate
import os
import re
from typing import Any

logger = get_logger(__name__)


class ClickableLabel(QLabel):
    """Custom QLabel that executes a callback on left click, styled as an interactive link."""

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.callback: Any = None
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, ev):
        if (
            ev is not None
            and ev.button() == Qt.MouseButton.LeftButton
            and self.callback
        ):
            self.callback()
        super().mousePressEvent(ev)


class RowSelectorFilter(QObject):
    """Custom event filter that dynamically manages focus policy on cell widgets to prevent hover focus selection while allowing click-based focus and row selection."""

    def __init__(self, table: QTableWidget, parent=None):
        super().__init__(parent)
        self.table = table

    def eventFilter(self, a0: QObject | None, a1: QEvent | None) -> bool:
        if a0 is not None and a1 is not None:
            if a1.type() == QEvent.Type.MouseButtonPress:
                # User clicked explicitly: temporarily enable ClickFocus and request focus
                if isinstance(a0, QWidget):
                    a0.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
                    a0.setFocus()
                    # Select corresponding table row
                    for r in range(self.table.rowCount()):
                        for c in range(self.table.columnCount()):
                            cell_w = self.table.cellWidget(r, c)
                            if cell_w == a0 or (
                                cell_w is not None and cell_w.isAncestorOf(a0)
                            ):
                                if self.table.currentRow() != r:
                                    self.table.setCurrentCell(r, 0)
                                break
                    return False

            elif a1.type() == QEvent.Type.FocusOut:
                # Widget lost focus: revert focus policy back to NoFocus to block hover activation
                if isinstance(a0, QWidget):
                    a0.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        return super().eventFilter(a0, a1)


class CreateProfileTemplatePage(BasePageTemplate):
    def __init__(self, context):
        super().__init__("create_profile_template", context)
        self.use_create_profile_template = UseCreateProfileTemplate(context, self)
        self.use_create_profile_template.template_loaded.connect(
            self._on_template_loaded
        )
        self.use_create_profile_template.template_saved.connect(self._on_template_saved)
        self.use_create_profile_template.loading.connect(self._set_loading)
        self.use_create_profile_template.error.connect(self._on_error)

        # State variables
        self.edit_mode = False
        self.selected_files = []  # Stores full paths of selected template .docx files

        # Split Layout (Horizontal: Left column for configs & fields, Right column for template files)
        split_layout = QHBoxLayout()
        split_layout.setSpacing(20)

        # --- LEFT COLUMN (Configs & Fields table) ---
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(15)

        # Config Form Grid
        self.grid = QGridLayout()
        self.grid.setSpacing(8)
        self.grid.setColumnStretch(1, 1)  # Ensure inputs stretch

        from ..level_01_atoms.buttons import PrimaryButton, SecondaryButton
        from ..level_01_atoms.inputs import FormLineEdit

        # ID Template
        self.lbl_id = QLabel(self.i18n_manager.translate("lbl_template_id_input"))
        self.txt_id = FormLineEdit()
        self.grid.addWidget(self.lbl_id, 0, 0)
        self.grid.addWidget(self.txt_id, 0, 1)

        # Name Template
        self.lbl_name = QLabel(self.i18n_manager.translate("lbl_template_name_input"))
        self.txt_name = FormLineEdit()
        self.grid.addWidget(self.lbl_name, 1, 0)
        self.grid.addWidget(self.txt_name, 1, 1)

        left_layout.addLayout(self.grid)

        # Header layout for fields
        self.fields_header = QHBoxLayout()
        self.lbl_dynamic = QLabel(self.i18n_manager.translate("lbl_dynamic_fields"))
        self.lbl_dynamic.setObjectName("subtitle_lbl")
        self.fields_header.addWidget(self.lbl_dynamic)

        self.btn_add_field = SecondaryButton("+ Thêm thuộc tính")
        self.btn_add_field.setCursor(Qt.CursorShape.PointingHandCursor)
        self.fields_header.addWidget(self.btn_add_field)

        self.btn_move_up = SecondaryButton("▲ Lên")
        self.btn_move_up.setToolTip("Di chuyển dòng đang chọn lên trên")
        self.btn_move_up.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_move_up.clicked.connect(self._move_selected_row_up)
        self.fields_header.addWidget(self.btn_move_up)

        self.btn_move_down = SecondaryButton("▼ Xuống")
        self.btn_move_down.setToolTip("Di chuyển dòng đang chọn xuống dưới")
        self.btn_move_down.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_move_down.clicked.connect(self._move_selected_row_down)
        self.fields_header.addWidget(self.btn_move_down)

        self.fields_header.addStretch()
        left_layout.addLayout(self.fields_header)

        # Table of fields (placeholders)
        self.table = QTableWidget()
        self.table.setColumnCount(6)  # STT + 5 columns
        self.table.setHorizontalHeaderLabels(
            [
                "STT",
                "Tên nhãn hiển thị",
                "Mã Placeholder (Click để copy)",
                "Kiểu dữ liệu",
                "Bắt buộc",
                "Thao tác",
            ]
        )

        # Configure Table Columns to be Interactive with fixed minimum widths to prevent squishing
        hdr = self.table.horizontalHeader()
        if hdr is not None:
            hdr.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        self.table.setColumnWidth(0, 50)  # STT
        self.table.setColumnWidth(1, 180)  # Tên nhãn hiển thị
        self.table.setColumnWidth(2, 220)  # Mã Placeholder
        self.table.setColumnWidth(3, 110)  # Kiểu dữ liệu
        self.table.setColumnWidth(4, 90)  # Bắt buộc
        self.table.setColumnWidth(5, 100)  # Thao tác (Delete button only)

        v_hdr = self.table.verticalHeader()
        if v_hdr is not None:
            v_hdr.setDefaultSectionSize(42)
            v_hdr.setVisible(False)  # Hide default raw vertical row headers

        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        left_layout.addWidget(self.table)

        # --- RIGHT COLUMN (Template files management) ---
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(10)

        # Scanned files list title & action button
        self.files_header_layout = QHBoxLayout()
        self.lbl_files_title = QLabel("Tài liệu mẫu (.docx):")
        self.lbl_files_title.setObjectName("subtitle_lbl")
        self.files_header_layout.addWidget(self.lbl_files_title)

        self.btn_select_files = SecondaryButton("+ Chọn file Word")
        self.btn_select_files.setCursor(Qt.CursorShape.PointingHandCursor)
        self.files_header_layout.addWidget(self.btn_select_files)

        self.btn_file_up = SecondaryButton("▲ Lên")
        self.btn_file_up.setToolTip("Di chuyển file đang chọn lên trên")
        self.btn_file_up.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_file_up.clicked.connect(self._move_selected_file_up)
        self.files_header_layout.addWidget(self.btn_file_up)

        self.btn_file_down = SecondaryButton("▼ Xuống")
        self.btn_file_down.setToolTip("Di chuyển file đang chọn xuống dưới")
        self.btn_file_down.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_file_down.clicked.connect(self._move_selected_file_down)
        self.files_header_layout.addWidget(self.btn_file_down)

        right_layout.addLayout(self.files_header_layout)

        # Scanned files table
        self.files_table = QTableWidget()
        self.files_table.setColumnCount(2)
        self.files_table.setHorizontalHeaderLabels(["Tên file mẫu", "Thao tác"])

        f_hdr = self.files_table.horizontalHeader()
        if f_hdr is not None:
            f_hdr.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            f_hdr.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)

        f_v_hdr = self.files_table.verticalHeader()
        if f_v_hdr is not None:
            f_v_hdr.setDefaultSectionSize(42)

        self.files_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        right_layout.addWidget(self.files_table)

        split_layout.addWidget(left_widget, stretch=3)
        split_layout.addWidget(right_widget, stretch=2)

        # Wrap split_layout inside a QScrollArea to prevent squishing on small windows
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.scroll_content = QWidget()
        self.scroll_content.setMinimumWidth(
            1150
        )  # Maintain readable minimum size for 6-column fields table + 2-column files table
        self.scroll_content.setLayout(split_layout)
        self.scroll_area.setWidget(self.scroll_content)

        self.content_layout.addWidget(self.scroll_area)

        # Save & Cancel buttons at bottom
        self.buttons_layout = QHBoxLayout()
        self.btn_save = PrimaryButton("Lưu cấu hình mẫu")
        self.btn_cancel = SecondaryButton(self.i18n_manager.translate("btn_back"))
        self.btn_save.setShortcut("Ctrl+S")
        self.btn_cancel.setShortcut("Esc")
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)

        self.buttons_layout.addWidget(self.btn_save)
        self.buttons_layout.addWidget(self.btn_cancel)
        self.buttons_layout.addStretch()
        self.content_layout.addLayout(self.buttons_layout)

        # Connect actions
        self.btn_select_files.clicked.connect(self._select_template_files)
        self.btn_add_field.clicked.connect(self._add_empty_field_row)
        self.btn_save.clicked.connect(self._save_template)
        self.btn_cancel.clicked.connect(self._go_back)

        # Row selector event filter to allow select on click/focus of cell widgets
        self.row_selector_filter = RowSelectorFilter(self.table, self)

        # Initialize
        self.set_template_id_for_editing(None)

    def set_template_id_for_editing(self, template_id: str | None = None):
        """Pre-populate page data if template_id is passed (Edit Mode), else clear fields (Create Mode)."""
        self.table.setRowCount(0)
        self.files_table.setRowCount(0)

        if template_id:
            # EDIT MODE
            self.edit_mode = True
            self.header.setText("Cấu hình Mẫu Hồ Sơ")
            self.btn_save.setText("Cập nhật mẫu")
            self.txt_id.setText(template_id)
            self.txt_id.setReadOnly(True)

            self.use_create_profile_template.load_template(template_id)
        else:
            # CREATE MODE
            self.edit_mode = False
            self.header.setText("Tạo Mới Mẫu Hồ Sơ")
            self.btn_save.setText("Lưu cấu hình mẫu")
            self.txt_id.setText("")
            self.txt_id.setReadOnly(False)
            self.txt_name.setText("")
            self.selected_files = []

            self._add_empty_field_row()
            self._refresh_files_list_table()

    def _select_template_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Chọn các file tài liệu mẫu (.docx)", "", "Word Files (*.docx)"
        )
        if not files:
            return

        # Add to selected list if not already there
        for f in files:
            norm_path = os.path.abspath(f)
            # Avoid duplicate paths
            if norm_path not in [os.path.abspath(x) for x in self.selected_files]:
                self.selected_files.append(f)

        self._refresh_files_list_table()

    def _refresh_files_list_table(self):
        self.files_table.setRowCount(0)
        for idx, fpath in enumerate(self.selected_files, start=1):
            row = self.files_table.rowCount()
            self.files_table.insertRow(row)

            filename = os.path.basename(fpath)
            # Clean any existing numeric prefix (e.g., "01 - ", "02.", etc.)
            cleaned = re.sub(r"^[\d\s\-\.\_]+", "", filename)
            # Format filename with the correct current index prefix
            display_name = f"{idx:02d} - {cleaned}"

            self.files_table.setItem(row, 0, QTableWidgetItem(display_name))

            # Action buttons widget
            actions_widget = QWidget()
            actions_lay = QHBoxLayout(actions_widget)
            actions_lay.setContentsMargins(4, 2, 4, 2)
            actions_lay.setSpacing(6)

            from ..level_01_atoms.buttons import SecondaryButton, DangerButton

            btn_open = SecondaryButton("Mở file")
            btn_open.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_open.clicked.connect(
                lambda checked, path=fpath: self._open_template_file(path)
            )

            btn_remove = DangerButton("Xóa")
            btn_remove.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_remove.clicked.connect(
                lambda checked, path=fpath: self._remove_selected_file(path)
            )

            actions_lay.addWidget(btn_open)
            actions_lay.addWidget(btn_remove)
            self.files_table.setCellWidget(row, 1, actions_widget)

    def _open_template_file(self, fpath: str):
        if os.path.exists(fpath):
            os.startfile(fpath)
        else:
            QMessageBox.warning(self, "Cảnh báo", f"Tệp tin không tồn tại: {fpath}")

    def _remove_selected_file(self, fpath: str):
        if fpath in self.selected_files:
            self.selected_files.remove(fpath)
        self._refresh_files_list_table()

    def _move_selected_file_up(self):
        row = self.files_table.currentRow()
        if row > 0 and row < len(self.selected_files):
            self.selected_files[row], self.selected_files[row - 1] = (
                self.selected_files[row - 1],
                self.selected_files[row],
            )
            self._refresh_files_list_table()
            self.files_table.setCurrentCell(row - 1, 0)

    def _move_selected_file_down(self):
        row = self.files_table.currentRow()
        if row >= 0 and row < len(self.selected_files) - 1:
            self.selected_files[row], self.selected_files[row + 1] = (
                self.selected_files[row + 1],
                self.selected_files[row],
            )
            self._refresh_files_list_table()
            self.files_table.setCurrentCell(row + 1, 0)

    def _update_stt_numbers(self):
        # Update STT column text dynamically
        for row in range(self.table.rowCount()):
            lbl = self.table.cellWidget(row, 0)
            if isinstance(lbl, QLabel):
                lbl.setText(str(row + 1))

    def _add_empty_field_row(self):
        self._add_field_row_with_data("", "", "string", True)

    def _add_field_row_with_data(
        self, label: str, key: str, field_type: str, required: bool
    ):
        row = self.table.rowCount()
        self.table.insertRow(row)

        # 0. STT Label
        lbl_stt = QLabel(str(row + 1))
        lbl_stt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_stt.setObjectName("body_lbl")
        lbl_stt.setStyleSheet("font-weight: bold;")

        # 1. Display Label Input
        txt_label = QLineEdit()
        txt_label.setObjectName("form_input")
        txt_label.setPlaceholderText("e.g. Tên giám định viên")
        txt_label.setText(label)
        txt_label.setProperty(
            "key_name", key
        )  # Store clean key name directly as property
        txt_label.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # 2. Clickable Placeholder Code Label
        initial_placeholder = f"{{{{ {key} }}}}" if key else ""
        lbl_placeholder = ClickableLabel(initial_placeholder)
        lbl_placeholder.setObjectName("body_lbl")
        lbl_placeholder.setStyleSheet("font-weight: bold; color: #38bdf8;")
        lbl_placeholder.setToolTip("Nhấp chuột để sao chép nhanh mã placeholder này")
        lbl_placeholder.callback = lambda lbl=lbl_placeholder: self._copy_placeholder(
            lbl
        )

        # Connect text change to auto-derive key name
        txt_label.textChanged.connect(
            self._create_label_change_handler(txt_label, lbl_placeholder)
        )

        # 3. Type Combo
        cbo_type = QComboBox()
        cbo_type.addItems(["string", "number", "boolean", "date"])
        idx = cbo_type.findText(field_type)
        if idx >= 0:
            cbo_type.setCurrentIndex(idx)
        cbo_type.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # 4. Required Checkbox
        chk_req = QCheckBox()
        chk_req.setChecked(required)
        chk_req.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        chk_widget = QWidget()
        chk_lay = QHBoxLayout(chk_widget)
        chk_lay.setContentsMargins(0, 0, 0, 0)
        chk_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chk_lay.addWidget(chk_req)

        # 5. Actions Layout (Delete button only)
        actions_widget = QWidget()
        actions_lay = QHBoxLayout(actions_widget)
        actions_lay.setContentsMargins(4, 2, 4, 2)
        actions_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)

        from ..level_01_atoms.buttons import DangerButton

        btn_del = DangerButton("Xóa")
        btn_del.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_del.clicked.connect(self._delete_table_row)
        actions_lay.addWidget(btn_del)

        txt_label.installEventFilter(self.row_selector_filter)
        cbo_type.installEventFilter(self.row_selector_filter)
        chk_req.installEventFilter(self.row_selector_filter)
        btn_del.installEventFilter(self.row_selector_filter)

        self.table.setCellWidget(row, 0, lbl_stt)
        self.table.setCellWidget(row, 1, txt_label)
        self.table.setCellWidget(row, 2, lbl_placeholder)
        self.table.setCellWidget(row, 3, cbo_type)
        self.table.setCellWidget(row, 4, chk_widget)
        self.table.setCellWidget(row, 5, actions_widget)

        self._update_stt_numbers()

    def _create_label_change_handler(self, txt_label, lbl_placeholder):
        def handler(text):
            # Lowercase, replace spaces with underscores, strip special characters to create clean python variable name
            import unicodedata

            # Normalize Vietnamese Unicode letters
            normalized = unicodedata.normalize("NFC", text.strip().lower())
            # Replace whitespace/dash with underscore
            key = re.sub(r"[\s\-]+", "_", normalized)
            # Remove characters that are not word characters or letters
            key = "".join(c for c in key if c.isalnum() or c == "_")

            # Fallback if empty
            if key:
                lbl_placeholder.setText(f"{{{{ {key} }}}}")
                txt_label.setProperty("key_name", key)
            else:
                lbl_placeholder.setText("")
                txt_label.setProperty("key_name", "")

        return handler

    def _copy_placeholder(self, lbl):
        if lbl and lbl.text() and not lbl.text().startswith("✓"):
            original_text = lbl.text()
            cb = QApplication.clipboard()
            if cb is not None:
                cb.setText(original_text)

            # Modern micro-interaction feedback: temporarily change label text & color
            lbl.setText("✓ Đã copy!")
            lbl.setStyleSheet("font-weight: bold; color: #10b981;")

            # Revert after 1.2 seconds
            QTimer.singleShot(
                1200, lambda: self._revert_placeholder_label(lbl, original_text)
            )

            # Notify user via status bar of main window
            main_win: Any = self.window()
            if main_win and hasattr(main_win, "statusBar") and main_win.statusBar():
                main_win.statusBar().showMessage(
                    f"Đã sao chép mã placeholder: {original_text}", 3000
                )

    def _revert_placeholder_label(self, lbl, original_text):
        lbl.setText(original_text)
        lbl.setStyleSheet("font-weight: bold; color: #38bdf8;")

    def _get_widget_row(self, widget: QWidget) -> int:
        for r in range(self.table.rowCount()):
            if self.table.cellWidget(r, 5) == widget:
                return r
        return -1

    def _delete_table_row(self):
        button = self.sender()
        if isinstance(button, QWidget):
            parent = button.parentWidget()
            if parent is not None:
                row = self._get_widget_row(parent)
                if row >= 0:
                    self.table.removeRow(row)
                    self._update_stt_numbers()

    def _move_selected_row_up(self):
        row = self.table.currentRow()
        if row > 0:
            self._swap_rows(row, row - 1)
            # Update selection to follow the moved row
            self.table.setCurrentCell(row - 1, self.table.currentColumn())

    def _move_selected_row_down(self):
        row = self.table.currentRow()
        if row >= 0 and row < self.table.rowCount() - 1:
            self._swap_rows(row, row + 1)
            # Update selection to follow the moved row
            self.table.setCurrentCell(row + 1, self.table.currentColumn())

    def _swap_rows(self, row1: int, row2: int):
        if (
            row1 < 0
            or row1 >= self.table.rowCount()
            or row2 < 0
            or row2 >= self.table.rowCount()
        ):
            return

        # Get widgets from row1
        txt_label1 = self.table.cellWidget(row1, 1)
        cbo_type1 = self.table.cellWidget(row1, 3)
        w_chk_container1 = self.table.cellWidget(row1, 4)

        # Get widgets from row2
        txt_label2 = self.table.cellWidget(row2, 1)
        cbo_type2 = self.table.cellWidget(row2, 3)
        w_chk_container2 = self.table.cellWidget(row2, 4)

        # Extract checkboxes from containers
        chk_req1 = None
        if w_chk_container1 is not None:
            lay1 = w_chk_container1.layout()
            if lay1 is not None:
                item1 = lay1.itemAt(0)
                if item1 is not None:
                    chk_req1 = item1.widget()

        chk_req2 = None
        if w_chk_container2 is not None:
            lay2 = w_chk_container2.layout()
            if lay2 is not None:
                item2 = lay2.itemAt(0)
                if item2 is not None:
                    chk_req2 = item2.widget()

        # Perform value swapping (this preserves widgets and triggers their textChanged events to sync labels)
        if isinstance(txt_label1, QLineEdit) and isinstance(txt_label2, QLineEdit):
            val1 = txt_label1.text()
            val2 = txt_label2.text()
            k1 = txt_label1.property("key_name") or ""
            k2 = txt_label2.property("key_name") or ""

            txt_label1.setText(val2)
            txt_label2.setText(val1)
            txt_label1.setProperty("key_name", k2)
            txt_label2.setProperty("key_name", k1)

            # Update labels
            ph1 = self.table.cellWidget(row1, 2)
            ph2 = self.table.cellWidget(row2, 2)
            if isinstance(ph1, QLabel):
                ph1.setText(f"{{{{ {k2} }}}}" if k2 else "")
            if isinstance(ph2, QLabel):
                ph2.setText(f"{{{{ {k1} }}}}" if k1 else "")

        if isinstance(cbo_type1, QComboBox) and isinstance(cbo_type2, QComboBox):
            idx1 = cbo_type1.currentIndex()
            idx2 = cbo_type2.currentIndex()
            cbo_type1.setCurrentIndex(idx2)
            cbo_type2.setCurrentIndex(idx1)

        if isinstance(chk_req1, QCheckBox) and isinstance(chk_req2, QCheckBox):
            state1 = chk_req1.isChecked()
            state2 = chk_req2.isChecked()
            chk_req1.setChecked(state2)
            chk_req2.setChecked(state1)

    def _save_template(self):
        t_id = self.txt_id.text().strip()
        t_name = self.txt_name.text().strip()

        if not t_id or not t_name:
            QMessageBox.warning(
                self, "Cảnh báo", "Vui lòng nhập đầy đủ Mã mẫu và Tên mẫu!"
            )
            return

        if not self.selected_files:
            QMessageBox.warning(
                self, "Cảnh báo", "Vui lòng chọn ít nhất 1 tệp tin Word mẫu (.docx)!"
            )
            return

        fields_schema = []
        for row in range(self.table.rowCount()):
            w_label = self.table.cellWidget(row, 1)  # Display label
            w_type = self.table.cellWidget(row, 3)  # Type combo
            w_chk_container = self.table.cellWidget(
                row, 4
            )  # Required checkbox container

            if (
                isinstance(w_label, QLineEdit)
                and isinstance(w_type, QComboBox)
                and w_chk_container is not None
            ):
                f_name = w_label.property("key_name") or ""
                f_label = w_label.text().strip()
                f_type = w_type.currentText()

                lay = w_chk_container.layout()
                chk = None
                if lay is not None:
                    item = lay.itemAt(0)
                    if item is not None:
                        chk_widget = item.widget()
                        if isinstance(chk_widget, QCheckBox):
                            chk = chk_widget

                f_req = chk.isChecked() if chk is not None else False

                if not f_name or not f_label:
                    continue

                fields_schema.append(
                    {
                        "name": f_name,
                        "label": f_label,
                        "type": f_type,
                        "required": f_req,
                    }
                )

        self.use_create_profile_template.save_template(
            t_id, t_name, fields_schema, self.selected_files, self.edit_mode
        )

    @pyqtSlot(dict)
    def _on_template_loaded(self, t_data: dict):
        if t_data:
            self.txt_name.setText(t_data.get("name", ""))

            # Load fields schema
            fields = t_data.get("fields_schema", [])
            for f in fields:
                self._add_field_row_with_data(
                    label=f.get("label", ""),
                    key=f.get("name", ""),
                    field_type=f.get("type", "string"),
                    required=f.get("required", True),
                )

            # Load imported files
            t_dir = t_data.get("template_dir", "")
            self.selected_files = []
            if t_dir and os.path.exists(t_dir):
                docx_files = [
                    os.path.join(t_dir, f)
                    for f in os.listdir(t_dir)
                    if f.endswith(".docx") and not f.startswith("~$")
                ]
                self.selected_files = sorted(docx_files)

            self._refresh_files_list_table()

    @pyqtSlot(str)
    def _on_template_saved(self, t_name: str):
        msg = f"✓ Đã lưu mẫu hồ sơ '{t_name}' thành công!"
        main_win: Any = self.window()
        if main_win and hasattr(main_win, "show_status_message"):
            main_win.show_status_message(msg, "success", 5000)
        self._go_back()

    @pyqtSlot(bool)
    def _set_loading(self, is_loading: bool):
        main_win: Any = self.window()
        if is_loading:
            self.setCursor(Qt.CursorShape.WaitCursor)
            self.btn_save.setEnabled(False)
            self.btn_cancel.setEnabled(False)
            if main_win and hasattr(main_win, "set_loading"):
                main_win.set_loading(True)
        else:
            self.unsetCursor()
            self.btn_save.setEnabled(True)
            self.btn_cancel.setEnabled(True)
            if main_win and hasattr(main_win, "set_loading"):
                main_win.set_loading(False)

    @pyqtSlot(str)
    def _on_error(self, err_msg: str):
        QMessageBox.critical(self, "Lỗi hệ thống", f"Không thể lưu mẫu: {err_msg}")

    def _go_back(self):
        main_win: Any = self.window()
        if main_win is not None and hasattr(main_win, "switch_page"):
            welcome = main_win.pages_map.get("welcome")
            if welcome is not None and hasattr(welcome, "use_welcome_data"):
                welcome.use_welcome_data.load_data()
            main_win.switch_page("welcome")

    def retranslate_ui(self, lang_code: str):
        self.lbl_id.setText(self.i18n_manager.translate("lbl_template_id_input"))
        self.lbl_name.setText(self.i18n_manager.translate("lbl_template_name_input"))
        self.lbl_dynamic.setText(self.i18n_manager.translate("lbl_dynamic_fields"))
        self.btn_add_field.setText("+ Thêm thuộc tính")
        self.btn_cancel.setText(self.i18n_manager.translate("btn_back"))
        self.lbl_files_title.setText("Tài liệu mẫu (.docx):")
        self.btn_select_files.setText("+ Chọn file Word")
        if self.edit_mode:
            self.header.setText("Cấu hình Mẫu Hồ Sơ")
            self.btn_save.setText("Cập nhật mẫu")
        else:
            self.header.setText("Tạo Mới Mẫu Hồ Sơ")
            self.btn_save.setText("Lưu cấu hình mẫu")
