class KivyUiInspector:
    def get_template(self) -> str:
        return '''from kivy.core.window import Window
from kivy.app import App
from kivy.core.clipboard import Clipboard
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.clock import Clock
import os
import re

class HoverOverlay(Widget):
    """
    Khung vẽ đường viền bo ngoài (outline) của phần tử đang rà chuột trong Kivy.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.border_color = ({{ ACCENT_COLOR_KIVY_FLOAT }})  # {{ ACCENT_COLOR }} in rgba
        self.target = None
        self.bind(size=self._draw_border, pos=self._draw_border)

    def set_target(self, widget, color_rgba=None):
        if color_rgba is None:
            color_rgba = ({{ ACCENT_COLOR_KIVY_FLOAT }})
        self.target = widget
        self.border_color = color_rgba
        if widget:
            wx, wy = widget.to_window(*widget.pos)
            self.pos = (wx - 2, wy - 2)
            self.size = (widget.width + 4, widget.height + 4)
            self._draw_border()
        else:
            self.canvas.clear()

    def _draw_border(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(*self.border_color)
            border_w = float("{{ BORDER_WIDTH }}".replace("px", "")) if "{{ BORDER_WIDTH }}".replace("px", "").replace(".", "", 1).isdigit() else 1.5
            Line(rectangle=(self.x, self.y, self.width, self.height), width=border_w, dash_length=4, dash_offset=2)


class UIInspector:
    """
    UIInspector cho Kivy - Phân tích, debug phần tử (F12), chụp toàn app (F11),
    chụp widget ghi đè (F9) và chụp widget lưu lịch sử (F10).
    """
    def __init__(self):
        self.active = False
        self.screenshot_mode = False
        self.single_screenshot_mode = False
        self.hover_overlay = None

        Window.bind(on_motion=self.on_window_motion)
        Window.bind(on_touch_down=self.on_touch_down)
        Window.bind(on_key_down=self.on_key_down)

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        # Kivy keycodes: F9=290, F10=291, F11=292, F12=293
        if key == 293: # F12
            self.toggle_inspector()
            return True
        elif key == 292: # F11
            self.capture_screenshot()
            return True
        elif key == 291: # F10
            self.toggle_screenshot_mode()
            return True
        elif key == 290: # F9
            self.toggle_single_screenshot_mode()
            return True
        return False

    def toggle_inspector(self):
        self.active = not self.active
        self.screenshot_mode = False
        self.single_screenshot_mode = False
        self._hide_overlay()
        if self.active:
            print("[UI Inspector Mobile] BAT CHE DO DEBUG (F12) - Ra chuot de chon, click de copy thong tin!")
        else:
            print("[UI Inspector Mobile] TAT CHE DO DEBUG.")

    def toggle_screenshot_mode(self):
        self.screenshot_mode = not self.screenshot_mode
        self.single_screenshot_mode = False
        self.active = False
        self._hide_overlay()
        if self.screenshot_mode:
            print("[UI Inspector Mobile] BAT CHE DO CHUP ANH PHAN TU (F10) - Click de luu vao snapshots/!")
        else:
            print("[UI Inspector Mobile] TAT CHE DO CHUP ANH PHAN TU.")

    def toggle_single_screenshot_mode(self):
        self.single_screenshot_mode = not self.single_screenshot_mode
        self.screenshot_mode = False
        self.active = False
        self._hide_overlay()
        if self.single_screenshot_mode:
            print("[UI Inspector Mobile] BAT CHE DO CHUP ANH DON (F9) - Click de ghi de widget_screenshot.png!")
        else:
            print("[UI Inspector Mobile] TAT CHE DO CHUP ANH DON.")

    def _hide_overlay(self):
        if self.hover_overlay and self.hover_overlay.parent:
            Window.remove_widget(self.hover_overlay)
            self.hover_overlay = None

    def _ensure_overlay(self):
        if not self.hover_overlay:
            self.hover_overlay = HoverOverlay()
            Window.add_widget(self.hover_overlay)
        return self.hover_overlay

    def on_window_motion(self, window, etype, motionevent):
        if not (self.active or self.screenshot_mode or self.single_screenshot_mode):
            return
        pos = motionevent.pos
        widget = self._find_smallest_widget_at(pos)
        if widget:
            overlay = self._ensure_overlay()
            color = ({{ SUCCESS_COLOR_KIVY_FLOAT }}) if (self.screenshot_mode or self.single_screenshot_mode) else ({{ ACCENT_COLOR_KIVY_FLOAT }})
            overlay.set_target(widget, color)
        else:
            self._hide_overlay()

    def on_touch_down(self, window, touch):
        if not (self.active or self.screenshot_mode or self.single_screenshot_mode):
            return False

        pos = touch.pos
        widget = self._find_smallest_widget_at(pos)
        if not widget:
            return False

        if self.single_screenshot_mode:
            self.capture_widget_screenshot(widget, overwrite=True)
            return True
        elif self.screenshot_mode:
            self.capture_widget_screenshot(widget, overwrite=False)
            return True
        elif self.active:
            info = self.get_widget_info(widget)
            Clipboard.copy(info)
            self.highlight_widget(widget)
            print(f"[UI Inspector Mobile] Da copy thong tin widget vao Clipboard!\\n{info}")
            return True

        return False

    def _find_smallest_widget_at(self, pos):
        app = App.get_running_app()
        if not app or not app.root:
            return None
        
        colliding = []
        for child in app.root.walk():
            wx, wy = child.to_window(*child.pos)
            if (wx <= pos[0] <= wx + child.width) and (wy <= pos[1] <= wy + child.height):
                if child.__class__.__name__ not in ("HoverOverlay", "Window"):
                    colliding.append(child)
                    
        if not colliding:
            return None
        colliding.sort(key=lambda w: w.width * w.height)
        return colliding[0]

    def capture_screenshot(self):
        os.makedirs("artifacts", exist_ok=True)
        output_path = os.path.abspath("artifacts/ui_screenshot.png")
        app = App.get_running_app()
        if app and app.root:
            app.root.export_to_png(output_path)
            print(f"[UI Inspector Mobile] Da chup toan app ghi de: {output_path}")

    def capture_widget_screenshot(self, widget, overwrite=False):
        project_name = "App"
        app = App.get_running_app()
        if app:
            project_name = app.__class__.__name__.replace("App", "")
            
        mode_str = "mode"
        if hasattr(app, "context") and hasattr(app.context, "mode_manager"):
            mode_str = app.context.mode_manager.get_current_mode()
            
        widget_class = widget.__class__.__name__
        
        if overwrite:
            os.makedirs("artifacts", exist_ok=True)
            output_path = os.path.abspath("artifacts/widget_screenshot.png")
            widget.export_to_png(output_path)
            print(f"[UI Inspector Mobile] Da chup ghi de widget: {output_path}")
        else:
            os.makedirs("artifacts/snapshots", exist_ok=True)
            idx = 1
            while True:
                filename = f"{project_name}_{mode_str}_{widget_class}_{idx}.png"
                output_path = os.path.abspath(os.path.join("artifacts/snapshots", filename))
                if not os.path.exists(output_path):
                    break
                idx += 1
            widget.export_to_png(output_path)
            print(f"[UI Inspector Mobile] Da chup luu widget: {output_path}")

    def get_widget_info(self, w) -> str:
        target_class = w.__class__.__name__
        target_size = f"{w.width}x{w.height}"
        target_pos = f"{w.x},{w.y}"
        
        hierarchy = []
        curr = w
        while curr:
            class_name = curr.__class__.__name__
            geometry = f"pos={curr.x},{curr.y} size={curr.width}x{curr.height}"
            hierarchy.append(f"{class_name}({geometry})")
            curr = curr.parent
            
        hierarchy_str = " \\n └── ".join(reversed(hierarchy))
        return (
            f"=== TARGET WIDGET ===\\n"
            f"Class: {target_class}\\n"
            f"Pos: {target_pos}\\n"
            f"Size: {target_size}\\n\\n"
            f"=== FULL HIERARCHY ===\\n"
            f"{hierarchy_str}"
        )

    def highlight_widget(self, w):
        with w.canvas.after:
            Color(*[{{ ACCENT_COLOR_KIVY_FLOAT }}][:3], 0.5)
            border_w = float("{{ BORDER_WIDTH }}".replace("px", "")) if "{{ BORDER_WIDTH }}".replace("px", "").replace(".", "", 1).isdigit() else 2
            line = Line(rectangle=(w.x, w.y, w.width, w.height), width=border_w)
        def clear_line(dt):
            w.canvas.after.remove(line)
        Clock.schedule_once(clear_line, 0.3)
'''

    def get_qss_template(self) -> str:
        return ""
