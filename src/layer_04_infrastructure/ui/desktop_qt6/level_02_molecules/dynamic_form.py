from PyQt6.QtWidgets import (
    QWidget,
    QFormLayout,
    QLabel,
    QCheckBox,
    QDateEdit,
    QMessageBox,
)
from PyQt6.QtCore import QDate
from ..level_01_atoms.inputs import FormLineEdit


class DynamicForm(QWidget):
    """
    DynamicForm (Level 2: Molecules): Thành phần biểu mẫu động dùng chung.
    Tự động sinh ra các trường nhập liệu từ lược đồ cấu hình (schema) và
    hỗ trợ trích xuất dữ liệu kèm kiểm tra hợp lệ (validation).
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.form_layout = QFormLayout(self)
        self.form_layout.setSpacing(12)
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        self.widgets_map = {}  # f_name -> (widget, f_type, required, f_label)

    def render_fields(self, schema: list, values: dict | None = None):
        """
        Xóa các trường cũ và tạo các trường nhập liệu mới từ schema.
        Hỗ trợ nạp sẵn các giá trị values (nếu có).
        """
        # Clear layout
        while self.form_layout.count() > 0:
            item = self.form_layout.takeAt(0)
            if item is not None:
                w = item.widget()
                if w is not None:
                    w.setParent(None)
                    w.deleteLater()
        self.widgets_map.clear()

        if not values:
            values = {}

        for field in schema:
            f_name = field["name"]
            f_label = field.get("label", f_name)
            f_type = field.get("type", "string")
            req = field.get("required", False)

            label_text = f"{f_label}:"
            if req:
                label_text = f"{f_label} (*):"
            lbl = QLabel(label_text)

            val = values.get(f_name, None)

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
                if f_type == "number":
                    widget.setPlaceholderText("Nhập số")
                if val is not None:
                    widget.setText(str(val))

            self.form_layout.addRow(lbl, widget)
            self.widgets_map[f_name] = (widget, f_type, req, f_label)

    def get_values(self) -> dict | None:
        """
        Trích xuất và kiểm tra tính hợp lệ của dữ liệu nhập.
        Trả về dict dữ liệu nếu hợp lệ, hoặc None nếu không hợp lệ.
        """
        dynamic_data = {}
        for f_name, (widget, f_type, req, f_label) in self.widgets_map.items():
            if f_type == "boolean":
                val = widget.isChecked()
            elif f_type == "date":
                val = widget.date().toString("yyyy-MM-dd")
            else:
                val = widget.text().strip()
                if req and not val:
                    QMessageBox.warning(
                        self,
                        "Cảnh báo",
                        f"Vui lòng nhập trường bắt buộc: '{f_label}'!",
                    )
                    return None
                if f_type == "number" and val:
                    try:
                        val = float(val)
                    except ValueError:
                        QMessageBox.warning(
                            self, "Cảnh báo", f"Trường '{f_label}' phải nhập kiểu số!"
                        )
                        return None
            dynamic_data[f_name] = val
        return dynamic_data
