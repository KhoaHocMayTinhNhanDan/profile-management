from ..abstract.i_page_product import AbstractPage


class KivyPage(AbstractPage):
    def get_template(self, pascal_name: str, snake_name: str) -> str:
        is_welcome = pascal_name == "Welcome"
        is_demo = pascal_name == "ColorPaletteDemo"

        if is_welcome:
            return f"""from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from src.shared.logger.app_logger import get_logger

logger = get_logger(__name__)


class CardWidget(BoxLayout):
    def __init__(self, title, desc, **kwargs):
        super().__init__(orientation='vertical', padding={{ CARD_PADDING_NUM }}, spacing=int(float({{ SPACING_BASE_NUM }}) * 0.6), **kwargs)
        
        with self.canvas.before:
            Color({{ CARD_BG_KIVY_FLOAT }}) # {{ CARD_BG }}
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        lbl_title = Label(
            text=title, 
            font_size={{ HEADER_FONT_SIZE_NUM }}, 
            bold=True, 
            color=({{ ACCENT_HOVER_KIVY_FLOAT }}), # {{ ACCENT_HOVER }}
            size_hint_y=None, 
            height={{ BUTTON_MIN_HEIGHT_NUM }},
            halign='left',
            valign='middle'
        )
        lbl_title.bind(size=lbl_title.setter('text_size'))
        
        lbl_desc = Label(
            text=desc, 
            font_size={{ BODY_FONT_SIZE_NUM }}, 
            color=({{ TEXT_COLOR_KIVY_FLOAT }}), # {{ TEXT_COLOR }}
            halign='left',
            valign='top'
        )
        lbl_desc.bind(size=lbl_desc.setter('text_size'))
        
        self.add_widget(lbl_title)
        self.add_widget(lbl_desc)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class WelcomePage(BoxLayout):
    def __init__(self, context, **kwargs):
        super().__init__(orientation='vertical', padding={{ PAGE_PADDING_NUM }}, spacing={{ CARD_PADDING_NUM }}, **kwargs)
        self.context = context

        # Background color
        with self.canvas.before:
            Color({{ DARK_BG_KIVY_FLOAT }}) # {{ DARK_BG }}
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

        # Title
        lbl_title = Label(
            text="WELCOME TO {pascal_name}", 
            font_size=int(float({{ HEADER_FONT_SIZE_NUM }}) * 1.5), 
            bold=True, 
            color=({{ ACCENT_COLOR_KIVY_FLOAT }}), # {{ ACCENT_COLOR }}
            size_hint_y=None, 
            height=int(float({{ BUTTON_MIN_HEIGHT_NUM }}) * 1.2)
        )
        self.add_widget(lbl_title)

        # Subtitle
        lbl_sub = Label(
            text="Clean Architecture client scaffolded successfully with Kivy Mobile.", 
            font_size={{ STATUS_FONT_SIZE_NUM }}, 
            color=({{ SUBTEXT_COLOR_KIVY_FLOAT }}), # {{ SUBTEXT_COLOR }}
            size_hint_y=None, 
            height={{ BUTTON_MIN_HEIGHT_NUM }}
        )
        self.add_widget(lbl_sub)

        # Grid of Cards
        grid = GridLayout(cols=2, spacing={{ CARD_PADDING_NUM }}, size_hint_y=1.0)
        
        grid.add_widget(CardWidget("🛡️ Layer 01 - Entities", "Pure domain logic, data models, entities and validation rules. Free of framework dependencies."))
        grid.add_widget(CardWidget("⚡ Layer 02 - Use Cases", "Application specific business workflows. Contains interactors, DTOs, and gateway interfaces."))
        grid.add_widget(CardWidget("🔌 Layer 03 - Adapters", "Adapts data models between UI and business layers. Contains presenters, controllers and gateways."))
        grid.add_widget(CardWidget("🌐 Layer 04 - Infrastructure", "All concrete implementations: Kivy layouts, local API routes, and local file storage databases."))
        
        self.add_widget(grid)

        # Footer
        lbl_footer = Label(
            text="👉 Select a feature page from the sidebar menu to run mock simulations.", 
            font_size={{ STATUS_FONT_SIZE_NUM }}, 
            bold=True, 
            color=({{ SUCCESS_COLOR_KIVY_FLOAT }}), # {{ SUCCESS_COLOR }}
            size_hint_y=None, 
            height=int(float({{ BUTTON_MIN_HEIGHT_NUM }}) * 1.2)
        )
        self.add_widget(lbl_footer)

    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
"""

        if is_demo:
            return f"""from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from src.shared.logger.app_logger import get_logger
from ..level_01_atoms.buttons import PrimaryButton, DangerButton, SecondaryButton
import random

logger = get_logger(__name__)


class OptionRow(BoxLayout):
    def __init__(self, text, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height={{ BUTTON_MIN_HEIGHT_NUM }}, spacing={{ SPACING_BASE_NUM }}, **kwargs)
        chk = CheckBox(active=True, size_hint_x=None, width={{ CHECKBOX_INDICATOR_SIZE_NUM }})
        lbl = Label(text=text, font_size={{ STATUS_FONT_SIZE_NUM }}, halign='left', valign='middle')
        lbl.bind(size=lbl.setter('text_size'))
        self.add_widget(chk)
        self.add_widget(lbl)
 
 
class ColorPaletteDemoPage(BoxLayout):
    def __init__(self, context, **kwargs):
        super().__init__(orientation='vertical', padding={{ PAGE_PADDING_NUM }}, spacing={{ CARD_PADDING_NUM }}, **kwargs)
        self.context = context
        self.timer = None
        self.progress_val = 0
        self.log_step = 0
        
        self.logs_pool = [
            "[INFO] Initiating palette rendering context...",
            "[RENDER] Drawing Background nodes with DARK_BG ({{ DARK_BG }})...",
            "[RENDER] Drawing Sidebar panel using SIDEBAR_BG ({{ SIDEBAR_BG }})...",
            "[RENDER] PrimaryButton active state contrast verified (Ratio 4.8:1).",
            "[RENDER] Text element colors loaded cleanly.",
            "[SUCCESS] Color presets rendering simulation complete."
        ]
 
        # Background color
        with self.canvas.before:
            Color({{ DARK_BG_KIVY_FLOAT }}) # {{ DARK_BG }}
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)
 
        # 1. Top Bar
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height={{ INPUT_MIN_HEIGHT_NUM }}, spacing={{ SPACING_BASE_NUM }})
        
        top_bar.add_widget(self.spinner)
        
        self.btn_mode = SecondaryButton(text="🌙 Dark Mode", size_hint_x=0.2)
        self.btn_mode.bind(on_release=self.toggle_theme)
        top_bar.add_widget(self.btn_mode)
        
        top_bar.add_widget(Label(size_hint_x=0.1)) # Spacer
        
        status_box = BoxLayout(orientation='vertical', size_hint_x=0.3)
        self.lbl_status1 = Label(text="● MobileLink: Connected", font_size={{ STATUS_FONT_SIZE_NUM }}, color=({{ SUCCESS_COLOR_KIVY_FLOAT }}))
        self.lbl_status2 = Label(text="● Service: Ready", font_size={{ STATUS_FONT_SIZE_NUM }}, color=({{ SUCCESS_COLOR_KIVY_FLOAT }}))
        status_box.add_widget(self.lbl_status1)
        status_box.add_widget(self.lbl_status2)
        top_bar.add_widget(status_box)
        
        self.add_widget(top_bar)
  
        # 2. Middle Row
        middle_row = BoxLayout(orientation='horizontal', spacing={{ CARD_PADDING_NUM }}, size_hint_y=0.4)
        
        # Spec Card
        spec_card = BoxLayout(orientation='vertical', padding={{ CARD_PADDING_NUM }}, spacing=int(float({{ SPACING_BASE_NUM }}) * 0.6))
        with spec_card.canvas.before:
            Color({{ CARD_BG_KIVY_FLOAT }})
            self.rect1 = Rectangle(size=spec_card.size, pos=spec_card.pos)
        spec_card.bind(size=self._update_rect1, pos=self._update_rect1)
        
        spec_title = Label(text="Design Spec: Color Harmony Verification", font_size={{ HEADER_FONT_SIZE_NUM }}, bold=True, color=({{ ACCENT_COLOR_KIVY_FLOAT }}), size_hint_y=None, height={{ BUTTON_MIN_HEIGHT_NUM }})
        spec_desc = Label(
            text="Verify color harmony across all elements:\\n- Background: Slate Dark ({{ DARK_BG }})\\n- Sidebar: Deep Purple ({{ SIDEBAR_BG }})\\n- Accents: Pink / Mauve ({{ ACCENT_HOVER }} / {{ ACCENT_COLOR }})\\n- Statuses: Green / Yellow / Red",
            font_size={{ BODY_FONT_SIZE_NUM }},
            halign='left',
            valign='top'
        )
        spec_desc.bind(size=spec_desc.setter('text_size'))
        spec_card.add_widget(spec_title)
        spec_card.add_widget(spec_desc)
        middle_row.add_widget(spec_card)
        
        # Options Card
        opt_card = BoxLayout(orientation='vertical', padding={{ CARD_PADDING_NUM }}, spacing=int(float({{ SPACING_BASE_NUM }}) * 0.6))
        with opt_card.canvas.before:
            Color({{ CARD_BG_KIVY_FLOAT }})
            self.rect2 = Rectangle(size=opt_card.size, pos=opt_card.pos)
        opt_card.bind(size=self._update_rect2, pos=self._update_rect2)
        
        opt_title = Label(text="VERIFIABLE ELEMENT STATES", font_size={{ HEADER_FONT_SIZE_NUM }}, bold=True, color=({{ ACCENT_COLOR_KIVY_FLOAT }}), size_hint_y=None, height={{ BUTTON_MIN_HEIGHT_NUM }})
        opt_card.add_widget(opt_title)
        
        grid_opt = GridLayout(cols=2, spacing=int(float({{ SPACING_BASE_NUM }}) * 0.6))
        grid_opt.add_widget(OptionRow("Primary Colors"))
        grid_opt.add_widget(OptionRow("Secondary Accent"))
        grid_opt.add_widget(OptionRow("States Hover/Active"))
        grid_opt.add_widget(OptionRow("Contrast Accessibility"))
        opt_card.add_widget(grid_opt)
        
        middle_row.add_widget(opt_card)
        self.add_widget(middle_row)
 
        # 3. Control & Progress Row
        self.progress_bar = ProgressBar(max=100, size_hint_y=None, height={{ PROGRESS_HEIGHT_NUM }})
        self.add_widget(self.progress_bar)
        
        stats_box = BoxLayout(orientation='horizontal', size_hint_y=None, height={{ STATUS_FONT_SIZE_NUM }} + 4)
        self.lbl_speed = Label(text="Speed: -- MB/s", font_size={{ BODY_FONT_SIZE_NUM }}, halign='left')
        self.lbl_speed.bind(size=self.lbl_speed.setter('text_size'))
        self.lbl_eta = Label(text="Remaining: --", font_size={{ BODY_FONT_SIZE_NUM }}, halign='right')
        self.lbl_eta.bind(size=self.lbl_eta.setter('text_size'))
        stats_box.add_widget(self.lbl_speed)
        stats_box.add_widget(self.lbl_eta)
        self.add_widget(stats_box)
        
        # 4. Buttons
        btn_box = BoxLayout(orientation='horizontal', size_hint_y=None, height={{ INPUT_MIN_HEIGHT_NUM }}, spacing={{ SPACING_BASE_NUM }})
        
        self.btn_start = PrimaryButton(text="Start Palette Test")
        self.btn_start.bind(on_release=self.start_test)
        
        self.btn_pause = SecondaryButton(text="Pause", disabled=True)
        self.btn_pause.bind(on_release=self.pause_test)
        
        self.btn_abort = DangerButton(text="Abort", disabled=True)
        self.btn_abort.bind(on_release=self.abort_test)
        
        btn_box.add_widget(self.btn_start)
        btn_box.add_widget(self.btn_pause)
        btn_box.add_widget(self.btn_abort)
        self.add_widget(btn_box)
 
        # 5. Console Output
        self.add_widget(Label(text="REALTIME PALETTE RENDER LOGS", font_size={{ STATUS_FONT_SIZE_NUM }}, bold=True, size_hint_y=None, height={{ STATUS_FONT_SIZE_NUM }} + 4, halign='left'))
        
        scroll = ScrollView(size_hint_y=None, height={{ CONSOLE_HEIGHT_NUM }})
        self.lbl_console = Label(
            text="[READY] Color presets successfully loaded. Press 'Start Palette Test' to verify render flows...",
            font_size={{ CONSOLE_FONT_SIZE_NUM }},
            color=({{ SUCCESS_COLOR_KIVY_FLOAT }}),
            font_name="Roboto",
            halign='left',
            valign='top',
            size_hint_y=None
        )
        self.lbl_console.bind(size=self._update_console_height)
        scroll.add_widget(self.lbl_console)
        self.add_widget(scroll)

    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def _update_rect1(self, instance, value):
        self.rect1.pos = instance.pos
        self.rect1.size = instance.size

    def _update_rect2(self, instance, value):
        self.rect2.pos = instance.pos
        self.rect2.size = instance.size

    def _update_console_height(self, instance, value):
        self.lbl_console.text_size = (instance.width, None)
        self.lbl_console.height = max(self.lbl_console.texture_size[1], 150)

    def toggle_theme(self, instance):
        is_dark = self.btn_mode.text == "🌙 Dark Mode"
        self.btn_mode.text = "☀️ Light Mode" if is_dark else "🌙 Dark Mode"
        
        with self.canvas.before:
            if is_dark:
                Color({{ LIGHT_BG_KIVY_FLOAT }}) # {{ LIGHT_BG }}
            else:
                Color({{ DARK_BG_KIVY_FLOAT }}) # {{ DARK_BG }}
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)

    def start_test(self, instance):
        self.btn_start.disabled = True
        self.btn_pause.disabled = False
        self.btn_abort.disabled = False
        self.progress_val = 0
        self.log_step = 0
        self.progress_bar.value = 0
        self.lbl_console.text = "[INFO] Starting color palette verification test..."
        
        self.timer = Clock.schedule_interval(self.update_simulation, 0.2)

    def pause_test(self, instance):
        if self.timer:
            Clock.unschedule(self.timer)
            self.timer = None
            self.btn_pause.text = "Resume"
            self.lbl_console.text += "\\n[WARN] Color palette verification test paused."
        else:
            self.timer = Clock.schedule_interval(self.update_simulation, 0.2)
            self.btn_pause.text = "Pause"
            self.lbl_console.text += "\\n[INFO] Color palette verification test resumed."

    def abort_test(self, instance):
        if self.timer:
            Clock.unschedule(self.timer)
            self.timer = None
        self.progress_val = 0
        self.progress_bar.value = 0
        self.btn_start.disabled = False
        self.btn_pause.disabled = True
        self.btn_abort.disabled = True
        self.btn_pause.text = "Pause"
        self.lbl_speed.text = "Speed: -- MB/s"
        self.lbl_eta.text = "Remaining: --"
        self.lbl_console.text += "\\n[ERROR] Color palette verification test aborted."

    def update_simulation(self, dt):
        if self.progress_val < 100:
            self.progress_val += 2
            self.progress_bar.value = self.progress_val
            
            speed = round(40.0 + random.uniform(-3.5, 3.5), 1)
            self.lbl_speed.text = f"Speed: {{speed}} MB/s"
            
            rem_sec = int((100 - self.progress_val) * 0.25)
            self.lbl_eta.text = f"Remaining: {{rem_sec}}s"
            
            if self.log_step < len(self.logs_pool):
                if self.progress_val % 16 == 0:
                    self.lbl_console.text += "\\n" + self.logs_pool[self.log_step]
                    self.log_step += 1
        else:
            Clock.unschedule(self.timer)
            self.timer = None
            self.lbl_speed.text = "Speed: 0.0 MB/s"
            self.lbl_eta.text = "Remaining: Done"
            self.btn_pause.disabled = True
            self.btn_abort.disabled = True
            self.btn_start.disabled = False
            self.lbl_console.text += "\\n[SUCCESS] Color presets rendering simulation complete."
"""

        return f"""from kivy.uix.boxlayout import BoxLayout
from src.shared.logger.app_logger import get_logger

logger = get_logger(__name__)

class {pascal_name}Page(BoxLayout):
    def __init__(self, context, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.context = context
        
        # Xây dựng giao diện trang con Kivy tại đây
        # ...
"""
