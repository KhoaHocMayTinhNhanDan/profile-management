class KivyMainWindow:
    def get_template(self, project_name: str) -> str:
        return f'''from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import importlib
import os

class KivyMainWindow(BoxLayout):
    """
    Cửa sổ chính của ứng dụng Mobile Kivy với Sidebar Menu và ScreenManager động.
    """
    def __init__(self, context, **kwargs):
        super().__init__(orientation='horizontal', **kwargs)
        self.context = context

        # 1. Sidebar Left
        self.sidebar = BoxLayout(orientation='vertical', size_hint=(0.25, 1), padding=10, spacing=10)
        with self.sidebar.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color({{ SIDEBAR_BG_KIVY_FLOAT }})
            self.rect = Rectangle(size=self.sidebar.size, pos=self.sidebar.pos)
        self.sidebar.bind(size=self._update_rect, pos=self._update_rect)

        # Title
        title = Label(text="{project_name}", font_size=18, bold=True, size_hint_y=None, height=40)
        self.sidebar.add_widget(title)

        # 2. Main Page Content (ScreenManager)
        self.screen_manager = ScreenManager(size_hint=(0.75, 1))

        # Dynamic Page Discovery
        pages_dir = os.path.join(os.path.dirname(__file__), "level_05_pages")
        page_modules = []
        if os.path.exists(pages_dir):
            for f in os.listdir(pages_dir):
                if f.endswith("_page.py") and f != "__init__.py":
                    page_modules.append(f[:-3])

        # Sắp xếp welcome_page lên đầu tiên
        page_modules.sort(key=lambda x: 0 if x == "welcome_page" else 1)

        for p_mod in page_modules:
            try:
                module = importlib.import_module(
                    f".level_05_pages.{{p_mod}}",
                    package="src.layer_04_infrastructure.ui.mobile_kivy"
                )
                words = p_mod.split("_")
                class_name = "".join(w.capitalize() for w in words)

                if hasattr(module, class_name):
                    page_class = getattr(module, class_name)
                    page_inst = page_class(self.context)

                    # Wrap page in a Screen
                    screen = Screen(name=p_mod)
                    screen.add_widget(page_inst)
                    self.screen_manager.add_widget(screen)

                    # Add navigation button
                    display_name = "Welcome" if p_mod == "welcome_page" else p_mod.replace("_page", "").replace("_", " ").title()
                    btn = Button(text=display_name, size_hint_y=None, height=40)
                    btn.bind(on_release=lambda instance, name=p_mod: self.switch_screen(name))
                    self.sidebar.add_widget(btn)
            except Exception as e:
                print(f"Error loading page module {{p_mod}}: {{e}}")

        self.sidebar.add_widget(Widget()) # Spacer

        self.add_widget(self.sidebar)
        self.add_widget(self.screen_manager)

        # Load Kivy UI Inspector (F9-F12)
        from src import config
        if getattr(config, "DEBUG_UI", True):
            from .level_02_molecules.ui_inspector.ui_inspector import UIInspector
            self.inspector = UIInspector()
        else:
            self.inspector = None

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def switch_screen(self, screen_name):
        self.screen_manager.current = screen_name


class KivyApp(App):
    def __init__(self, context, **kwargs):
        super().__init__(**kwargs)
        self.context = context

    def build(self):
        self.title = "{project_name}"
        Window.size = (380, 680)
        return KivyMainWindow(self.context)
'''
