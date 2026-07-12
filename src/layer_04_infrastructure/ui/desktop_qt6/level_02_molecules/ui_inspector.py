from PyQt6.QtCore import QObject, QEvent, Qt, QPoint
from PyQt6.QtWidgets import QApplication, QWidget, QToolTip, QMessageBox
from PyQt6.QtGui import QColor
from typing import Any


class UIInspector(QObject):
    """
    UIInspector - Phân tích, debug và sao chép cấu trúc thành phần PyQt6 trực tiếp khi click chuột (F12).
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.active = False

    def eventFilter(self, a0: QObject | None, a1: QEvent | None) -> bool:
        if self.active and a1 is not None and a1.type() == QEvent.Type.MouseButtonPress:
            from PyQt6.QtGui import QMouseEvent

            if isinstance(a1, QMouseEvent):
                pos = a1.globalPosition().toPoint()
                widget = QApplication.widgetAt(pos)
                if widget:
                    # Bỏ qua nếu click vào chính cửa sổ cảnh báo debug
                    curr = widget
                    is_debug_window = False
                    while curr:
                        if curr.__class__.__name__ == "QMessageBox":
                            is_debug_window = True
                            break
                        curr = curr.parentWidget()

                    if is_debug_window:
                        return False

                    info = self.get_widget_info(widget)
                    clipboard = QApplication.clipboard()
                    if clipboard:
                        clipboard.setText(info)

                    self.highlight_widget(widget)

                    # Hiển thị thông báo đẹp mắt bằng QMessageBox tiêu chuẩn
                    QMessageBox.information(
                        widget.window(),
                        "UI Element Inspector",
                        f"<b>Đã copy thông tin widget vào Clipboard!</b><br/><br/>"
                        f"<pre>{info}</pre>",
                    )
                    return True
        return super().eventFilter(a0, a1)

    def get_widget_info(self, w: QWidget) -> str:
        target_class = w.__class__.__name__
        target_name = w.objectName() or "NoName"
        target_class_prop = w.property("class") or "NoClass"
        target_geom = f"{w.width()}x{w.height()}"

        hierarchy = []
        curr = w
        while curr:
            class_name = curr.__class__.__name__
            obj_name = curr.objectName() or "NoName"
            class_prop = curr.property("class") or "NoClass"

            geometry = f"size={curr.width()}x{curr.height()}"
            margins = ""
            lay = curr.layout()
            if lay is not None:
                m = lay.contentsMargins()
                margins = (
                    f", margins=L:{m.left()} T:{m.top()} R:{m.right()} B:{m.bottom()}"
                )

            hierarchy.append(
                f"{class_name}(name={obj_name}, class={class_prop}, {geometry}{margins})"
            )
            curr = curr.parentWidget()

        hierarchy_str = " \n └── ".join(reversed(hierarchy))
        stylesheet = w.styleSheet() or "(Inherited/No Sheet)"

        return (
            f"=== TARGET WIDGET ===\n"
            f"Class: {target_class}\n"
            f"ObjectName: {target_name}\n"
            f"Class Property: {target_class_prop}\n"
            f"Size: {target_geom}\n\n"
            f"=== FULL HIERARCHY ===\n"
            f"{hierarchy_str}\n\n"
            f"=== STYLESHEET ===\n"
            f"{stylesheet}"
        )

    def highlight_widget(self, w: QWidget):
        old_style = w.styleSheet()
        border_color = "#f5c2e7"  # Pink neon
        flash_style = f"border: 2px dashed {border_color}; background-color: rgba(245, 194, 231, 0.1);"
        w.setStyleSheet(flash_style)

        from PyQt6.QtCore import QTimer

        QTimer.singleShot(300, lambda: w.setStyleSheet(old_style))
