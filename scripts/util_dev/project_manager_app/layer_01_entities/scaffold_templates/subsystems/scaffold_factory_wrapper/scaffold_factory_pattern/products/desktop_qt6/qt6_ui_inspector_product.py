class Qt6UiInspector:
    """
    GoF Role: ConcreteProduct
    """

    def get_template(self) -> str:
        return '''from PyQt6.QtCore import QObject, QEvent, Qt, QTimer, QPropertyAnimation, QPoint
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QLabel, QGraphicsOpacityEffect
from PyQt6.QtGui import QPainter, QPen, QColor
import os

class HoverOverlay(QWidget):
    """
    Khung vẽ đường viền bo ngoài (outline) của phần tử đang rà chuột.
    Tránh can thiệp hay thay đổi stylesheet gốc của các widget.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.Tool | 
            Qt.WindowType.WindowTransparentForInput |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.border_color = QColor("{{ ACCENT_COLOR }}") # Mặc định màu tím pastel
        
    def set_target(self, widget: QWidget, color_hex: str = "{{ ACCENT_COLOR }}"):
        if not widget or not widget.isVisible():
            self.hide()
            return
        
        self.border_color = QColor(color_hex)
        geo = widget.geometry()
        global_pos = widget.mapToGlobal(QPoint(0, 0))
        
        self.setGeometry(
            global_pos.x() - 2,
            global_pos.y() - 2,
            geo.width() + 4,
            geo.height() + 4
        )
        self.show()
        self.raise_()
        
    def paintEvent(self, a0):
        painter = QPainter(self)
        border_w = int("{{ BORDER_WIDTH }}".replace("px", "")) if "{{ BORDER_WIDTH }}".replace("px", "").isdigit() else 2
        pen = QPen(self.border_color, border_w, Qt.PenStyle.DashLine)
        painter.setPen(pen)
        painter.drawRect(1, 1, self.width() - 2, self.height() - 2)


class UIInspector(QObject):
    """
    UIInspector - Phân tích, debug phần tử PyQt6 (F12) và chụp ảnh màn hình (F11).
    F10: Chụp ảnh phần tử liên tiếp (lưu vào artifacts/snapshots/).
    F9: Chụp ảnh phần tử liên tiếp, ghi đè (lưu vào artifacts/widget_screenshot.png).
    Hỗ trợ rà chuột hiện rõ đường bo (Hover Outline) cho F9, F10 và F12.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.active = False
        self.screenshot_mode = False
        self.single_screenshot_mode = False
        self.hover_overlay = None

    def eventFilter(self, a0: QObject | None, a1: QEvent | None) -> bool:
        if a0 is None or a1 is None:
            return super().eventFilter(a0, a1)

        # 1. Chụp ảnh màn hình toàn bộ App bằng phím F11
        if a1.type() == QEvent.Type.KeyPress:
            from PyQt6.QtGui import QKeyEvent
            if isinstance(a1, QKeyEvent) and a1.key() == Qt.Key.Key_F11:
                if isinstance(a0, QWidget):
                    self.capture_screenshot(a0)
                    return True

        # 2. Hiển thị đường bo viền khi di chuột qua phần tử (Hover Outline)
        is_hover_active = (self.active or self.screenshot_mode or self.single_screenshot_mode)
        if is_hover_active and a1.type() == QEvent.Type.Enter:
            if isinstance(a0, QWidget):
                cls_name = a0.__class__.__name__
                if cls_name not in ("HoverOverlay", "ToastNotification", "QToolTip", "QMessageBox"):
                    if not self.hover_overlay:
                        self.hover_overlay = HoverOverlay()
                    color = "{{ SUCCESS_COLOR }}" if (self.screenshot_mode or self.single_screenshot_mode) else "{{ ACCENT_COLOR }}"
                    self.hover_overlay.set_target(a0, color)

        if is_hover_active and a1.type() == QEvent.Type.Leave:
            if self.hover_overlay:
                self.hover_overlay.hide()

        # 3. Xử lý sự kiện click chuột
        if a1.type() == QEvent.Type.MouseButtonPress:
            if isinstance(a0, QWidget):
                # Bỏ qua click vào QMessageBox hoặc Toast
                cls_name = a0.__class__.__name__
                curr = a0
                is_dialog = False
                while curr:
                    if curr.__class__.__name__ in ("QMessageBox", "ToastNotification"):
                        is_dialog = True
                        break
                    curr = curr.parentWidget()
                
                if is_dialog:
                    return False

                # Chế độ F9: Chụp ảnh liên tiếp, ghi đè widget_screenshot.png
                if self.single_screenshot_mode:
                    self.capture_widget_screenshot(a0, overwrite=True)
                    return True

                # Chế độ F10: Chụp ảnh liên tiếp lưu vào artifacts/snapshots/
                if self.screenshot_mode:
                    self.capture_widget_screenshot(a0, overwrite=False)
                    return True

                # Chế độ F12: Phân tích widget lấy giá trị
                if self.active:
                    info = self.get_widget_info(a0)
                    clipboard = QApplication.clipboard()
                    if clipboard:
                        clipboard.setText(info)
                    
                    self.highlight_widget(a0)
                    
                    win = a0.window()
                    if win:
                        toast = ToastNotification(
                            f"📋 Đã copy thông tin widget {a0.__class__.__name__} vào Clipboard!",
                            parent=win
                        )
                        geo = win.geometry()
                        global_pos = win.mapToGlobal(QPoint(0, 0))
                        toast_x = global_pos.x() + (geo.width() - toast.width()) // 2
                        toast_y = global_pos.y() + geo.height() - toast.height() - 40
                        toast.show_toast(QPoint(toast_x, toast_y))
                    return True

        return super().eventFilter(a0, a1)

    def capture_screenshot(self, widget: QWidget | None):
        if not widget:
            return
        
        curr: QWidget | None = widget
        top_window: QWidget = widget
        while curr:
            top_window = curr
            curr = curr.parentWidget()
        
        screen = top_window.screen()
        if screen:
            frame_geo = top_window.frameGeometry()
            pixmap = screen.grabWindow(
                0,  # type: ignore
                frame_geo.x(), 
                frame_geo.y(), 
                frame_geo.width(), 
                frame_geo.height()
            )
        else:
            pixmap = top_window.grab()
        
        os.makedirs("artifacts", exist_ok=True)
        
        # F11: CHỈ ghi đè vào file artifacts/ui_screenshot.png để AI đọc trực tiếp
        output_path = os.path.abspath("artifacts/ui_screenshot.png")
        success = pixmap.save(output_path, "PNG")
        
        if success:
            toast = ToastNotification(
                "📸 Đã chụp màn hình và ghi đè: ui_screenshot.png",
                parent=top_window
            )
            geo = top_window.geometry()
            global_pos = top_window.mapToGlobal(QPoint(0, 0))
            toast_x = global_pos.x() + (geo.width() - toast.width()) // 2
            toast_y = global_pos.y() + geo.height() - toast.height() - 40
            toast.show_toast(QPoint(toast_x, toast_y))

    def capture_widget_screenshot(self, widget: QWidget, overwrite: bool = False):
        if not widget:
            return
            
        pixmap = widget.grab()
        
        curr: QWidget | None = widget
        top_window: QWidget = widget
        while curr:
            top_window = curr
            curr = curr.parentWidget()
            
        project_name = "App"
        if hasattr(top_window, "windowTitle"):
            title = top_window.windowTitle()
            import re
            cleaned_title = re.sub(r'[^a-zA-Z0-9_]', '', title)
            if cleaned_title:
                project_name = cleaned_title
                
        mode_str = "mode"
        ctx = getattr(top_window, "context", None)
        if ctx and hasattr(ctx, "mode_manager"):
            mode_str = ctx.mode_manager.get_current_mode()
            
        widget_class = widget.__class__.__name__
        
        if overwrite:
            # F9: CHỈ ghi đè vào file artifacts/widget_screenshot.png để AI đọc trực tiếp
            os.makedirs("artifacts", exist_ok=True)
            output_path = os.path.abspath("artifacts/widget_screenshot.png")
            success = pixmap.save(output_path, "PNG")
            msg = "📸 Đã chụp và ghi đè: widget_screenshot.png"
        else:
            # F10: CHỈ lưu bản sao đánh số vào artifacts/snapshots/
            os.makedirs("artifacts/snapshots", exist_ok=True)
            idx = 1
            while True:
                filename = f"{project_name}_{mode_str}_{widget_class}_{idx}.png"
                output_path = os.path.abspath(os.path.join("artifacts/snapshots", filename))
                if not os.path.exists(output_path):
                    break
                idx += 1
            success = pixmap.save(output_path, "PNG")
            msg = f"📸 Đã chụp phần tử {widget_class}!\\nSnapshot: snapshots/{filename}"
        
        if success:
            toast = ToastNotification(
                msg,
                parent=top_window
            )
            geo = top_window.geometry()
            global_pos = top_window.mapToGlobal(QPoint(0, 0))
            toast_x = global_pos.x() + (geo.width() - toast.width()) // 2
            toast_y = global_pos.y() + geo.height() - toast.height() - 40
            toast.show_toast(QPoint(toast_x, toast_y))

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
            layout = curr.layout()
            if layout is not None:
                m = layout.contentsMargins()
                margins = f", margins=L:{m.left()} T:{m.top()} R:{m.right()} B:{m.bottom()}"
            
            hierarchy.append(f"{class_name}(name={obj_name}, class={class_prop}, {geometry}{margins})")
            curr = curr.parentWidget()
            
        hierarchy_str = " \\n └── ".join(reversed(hierarchy))
        stylesheet = w.styleSheet() or "(Inherited/No Sheet)"
        
        return (
            f"=== TARGET WIDGET ===\\n"
            f"Class: {target_class}\\n"
            f"ObjectName: {target_name}\\n"
            f"Class Property: {target_class_prop}\\n"
            f"Size: {target_geom}\\n\\n"
            f"=== FULL HIERARCHY ===\\n"
            f"{hierarchy_str}\\n\\n"
            f"=== STYLESHEET ===\\n"
            f"{stylesheet}"
        )

    def highlight_widget(self, w: QWidget):
        old_style = w.styleSheet()
        border_color = "{{ ACCENT_HOVER }}"
        flash_style = f"border: {{ BORDER_WIDTH }} dashed {border_color}; background-color: rgba({{ ACCENT_HOVER_RGB }}, 0.1);"
        w.setStyleSheet(flash_style)
        
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(300, lambda: w.setStyleSheet(old_style))


class ToastNotification(QLabel):
    def __init__(self, message: str, parent: QWidget | None = None):
        super().__init__(message, parent)
        self.setWindowFlags(Qt.WindowType.ToolTip | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        
        self.setStyleSheet("""
            QLabel {
                background-color: rgba({{ DARK_BG_RGB }}, 0.95);
                color: {{ SUCCESS_COLOR }};
                border: {{ BORDER_WIDTH }} solid {{ ACCENT_COLOR }};
                border-radius: {{ RADIUS }};
                padding: {{ INPUT_PADDING }};
                font-size: {{ STATUS_FONT_SIZE }};
                font-weight: bold;
                font-family: sans-serif;
            }
        """)
        
        self.adjustSize()
        
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.fade_out)
        
    def show_toast(self, pos: QPoint):
        self.move(pos)
        self.show()
        
        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim.setDuration(200)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.start()
        
        self.timer.start(2500)
        
    def fade_out(self):
        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim.setDuration(300)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.finished.connect(self.close)
        self.anim.start()
'''

    def get_qss_template(self) -> str:
        return ""
