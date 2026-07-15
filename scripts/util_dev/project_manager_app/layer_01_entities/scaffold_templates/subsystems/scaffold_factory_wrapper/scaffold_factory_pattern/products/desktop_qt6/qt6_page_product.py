from ..abstract.i_page_product import AbstractPage


class Qt6Page(AbstractPage):
    """
    GoF Role: ConcreteProduct
    """

    def get_template(self, pascal_name: str, snake_name: str) -> str:
        is_welcome = pascal_name == "Welcome"

        if is_welcome:
            template = """from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame
)
from PyQt6.QtCore import Qt
from src.shared.logger.app_logger import get_logger
from ..level_04_templates.page_template import BasePageTemplate

logger = get_logger(__name__)

class WelcomePage(BasePageTemplate):
    def __init__(self, context):
        super().__init__("welcome", context)
        
        # Title Section
        self.lbl_title = QLabel("WELCOME TO {project_name}")
        self.content_layout.addWidget(self.lbl_title)
        
        self.lbl_sub = QLabel("Clean Architecture client scaffolded successfully with PyQt6.")
        self.content_layout.addWidget(self.lbl_sub)
        
        # Grid layout for Clean Architecture layers
        self.grid_layout = QGridLayout()
        
        # Card 1: Entities
        self.card_entities = QFrame()
        ent_layout = QVBoxLayout(self.card_entities)
        ent_title = QLabel("🛡️ Layer 01 - Entities")
        ent_title.setObjectName("CardTitle")
        ent_desc = QLabel("Pure domain logic, data models, entities and validation rules. Free of framework dependencies.")
        ent_desc.setWordWrap(True)
        ent_layout.addWidget(ent_title)
        ent_layout.addWidget(ent_desc)
        self.grid_layout.addWidget(self.card_entities, 0, 0)
        
        # Card 2: Use Cases
        self.card_usecases = QFrame()
        uc_layout = QVBoxLayout(self.card_usecases)
        uc_title = QLabel("⚡ Layer 02 - Use Cases")
        uc_title.setObjectName("CardTitle")
        uc_desc = QLabel("Application specific business workflows. Contains interactors, DTOs, and gateway interfaces.")
        uc_desc.setWordWrap(True)
        uc_layout.addWidget(uc_title)
        uc_layout.addWidget(uc_desc)
        self.grid_layout.addWidget(self.card_usecases, 0, 1)
        
        # Card 3: Interface Adapters
        self.card_adapters = QFrame()
        ad_layout = QVBoxLayout(self.card_adapters)
        ad_title = QLabel("🔌 Layer 03 - Adapters")
        ad_title.setObjectName("CardTitle")
        ad_desc = QLabel("Adapts data models between UI and business layers. Contains presenters, controllers and gateways.")
        ad_desc.setWordWrap(True)
        ad_layout.addWidget(ad_title)
        ad_layout.addWidget(ad_desc)
        self.grid_layout.addWidget(self.card_adapters, 1, 0)
        
        # Card 4: Infrastructure
        self.card_infra = QFrame()
        inf_layout = QVBoxLayout(self.card_infra)
        inf_title = QLabel("🌐 Layer 04 - Infrastructure")
        inf_title.setObjectName("CardTitle")
        inf_desc = QLabel("All concrete implementations: PyQt6 UI screens, settings stores, mock databases, and web drivers.")
        inf_desc.setWordWrap(True)
        inf_layout.addWidget(inf_title)
        inf_layout.addWidget(inf_desc)
        self.grid_layout.addWidget(self.card_infra, 1, 1)
        
        self.content_layout.addLayout(self.grid_layout)
        self.content_layout.addStretch()
        
        # Footer
        self.lbl_footer = QLabel("👉 Select a feature page from the sidebar menu to run mock simulations.")
        self.content_layout.addWidget(self.lbl_footer)
        
        # Subscribe to theme changes
        self.theme_manager.subscribe(self._handle_theme_changed)
        self.apply_dynamic_styles()

    def apply_dynamic_styles(self):
        tm = self.theme_manager
        dark_bg = tm.get_color("DARK_BG")
        sidebar_bg = tm.get_color("SIDEBAR_BG")
        card_bg = tm.get_color("CARD_BG")
        text_color = tm.get_color("TEXT_COLOR")
        accent_color = tm.get_color("ACCENT_COLOR")
        border_color = tm.get_color("BORDER_COLOR")
        success_color = tm.get_color("SUCCESS_COLOR")
        
        # Resolve project name from top level window title dynamically
        proj_name = "Application"
        win = self.window()
        if win and hasattr(win, "windowTitle"):
            title = win.windowTitle()
            if title:
                proj_name = title
                
        h_size = tm.get_token("HEADER_FONT_SIZE")
        s_size = tm.get_token("STATUS_FONT_SIZE")
        margin_b = tm.get_token("LABEL_MARGIN_BOTTOM")
        border_width = tm.get_token("BORDER_WIDTH")
        card_padding = tm.get_token("CARD_PADDING")
        radius = tm.get_token("RADIUS")
        
        # Calculate sub and footer margins dynamically in Python
        margin_val = int(margin_b.replace("px", "")) if margin_b.endswith("px") else 8
        sub_margin = f"{margin_val * 3}px"
        footer_margin = f"{margin_val * 2}px"
        
        spacing_b = tm.get_token("SPACING_BASE")
        spacing_val = int(spacing_b.replace("px", "")) if spacing_b.endswith("px") else 8
        self.grid_layout.setSpacing(spacing_val * 2)
        
        self.lbl_title.setText(f"WELCOME TO {proj_name.upper()}")
        self.lbl_title.setStyleSheet(f"color: {accent_color}; font-size: {h_size}; font-weight: bold; margin-bottom: {margin_b};")
        self.lbl_sub.setStyleSheet(f"color: {text_color}; font-size: {s_size}; opacity: 0.8; margin-bottom: {sub_margin};")
        self.lbl_footer.setStyleSheet(f"color: {success_color}; font-weight: bold; font-size: {s_size}; margin-top: {footer_margin};")
        
        card_qss = f'''
            QFrame {{
                background-color: {card_bg};
                border: {border_width} solid {border_color};
                border-radius: {radius};
                padding: {card_padding};
            }}
            QLabel {{
                color: {text_color};
                border: none;
            }}
            QLabel#CardTitle {{
                font-weight: bold;
                font-size: {h_size};
            }}
        '''
        
        for card in [self.card_entities, self.card_usecases, self.card_adapters, self.card_infra]:
            card.setStyleSheet(card_qss)

    def showEvent(self, a0):
        super().showEvent(a0)
        self.apply_dynamic_styles()

    def _handle_theme_changed(self, theme_name: str, qss: str):
        self.apply_dynamic_styles()

    def retranslate_ui(self, lang_code: str):
        pass
"""
            return template.replace("{pascal_name}", pascal_name).replace(
                "{snake_name}", snake_name
            )

        else:
            specs_title = "COLOR PALETTE PLAYGROUND INFO"
            specs_content = """
            "Color Palette: (Dynamic)\\n"
            "Mode: (Dynamic)\\n"
            "Widget Set: Core PyQt6 Elements\\n"
            "Border Style: Radius (Dynamic)\\n"
            "Typography: Sans-serif (Dynamic)\\n"
            "Design Spec: Color Harmony Verification"
            """
            category_title = "VERIFIABLE ELEMENT STATES"
            chk1_txt, chk2_txt, chk3_txt, chk4_txt = (
                "Primary Colors",
                "Secondary Accent",
                "States Hover/Active",
                "Contrast Accessibility",
            )
            storage_text = "Verify color harmony across all elements:"
            btn_start_txt = "Start Palette Test"
            log_header_txt = "REALTIME PALETTE RENDER LOGS"
            init_console_txt = "[READY] Color presets successfully loaded. Press 'Start Palette Test' to verify render flows..."
            success_msg_title = "Verification Success"
            success_msg_text = "Color palette verification test completed successfully!"
            success_console_log = (
                "[SUCCESS] All rendering processes completed. Connection safely closed."
            )

            template = """from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QComboBox, 
    QCheckBox, QProgressBar, QTextEdit, QPushButton, QFrame, QMessageBox
)
from PyQt6.QtCore import QTimer, Qt
from src.shared.logger.app_logger import get_logger
from ..level_04_templates.page_template import BasePageTemplate
from ..level_01_atoms.buttons.buttons import PrimaryButton, DangerButton, SecondaryButton
from ..level_01_atoms.inputs.inputs import FormLineEdit, FormComboBox

logger = get_logger(__name__)

class {pascal_name}Page(BasePageTemplate):
    def __init__(self, context):
        super().__init__("{snake_name}", context)
        
        # 1. Top Section - Selector, Mode Toggle and Status
        self.top_layout = QHBoxLayout()
        
        self.device_combo = FormComboBox()
        self.device_combo.addItems([
            "Contrast & Color Verification", 
            "Responsive Grid Layout Check", 
            "Widget State Render Test"
        ])
        self.top_layout.addWidget(self.device_combo)
        
        # Light/Dark Mode Switcher Button
        self.btn_mode = SecondaryButton("🌙 Dark Mode")
        self.btn_mode.clicked.connect(self.toggle_mode)
        self.top_layout.addWidget(self.btn_mode)
        
        self.top_layout.addStretch()
        
        # Driver Status Indicators
        status_frame = QFrame()
        self.status_layout = QHBoxLayout(status_frame)
        self.status_layout.setContentsMargins(0, 0, 0, 0)
        
        self.lbl_status_1 = QLabel("● USBLink: Connected")
        self.lbl_status_2 = QLabel("● Service: Ready")
        
        self.status_layout.addWidget(self.lbl_status_1)
        self.status_layout.addWidget(self.lbl_status_2)
        self.top_layout.addWidget(status_frame)
        
        self.content_layout.addLayout(self.top_layout)
        
        # 2. Middle Section - Info & Option Selection
        self.middle_layout = QHBoxLayout()
        
        # Specs Info Card
        self.info_card = QFrame()
        info_layout = QVBoxLayout(self.info_card)
        info_title = QLabel("{specs_title}")
        info_title.setObjectName("CardTitle")
        info_layout.addWidget(info_title)
        
        self.specs_label = QLabel({specs_content})
        info_layout.addWidget(self.specs_label)
        self.middle_layout.addWidget(self.info_card, stretch=1)
        
        # Selection Grid Card
        self.selection_card = QFrame()
        sel_layout = QVBoxLayout(self.selection_card)
        sel_title = QLabel("{category_title}")
        sel_title.setObjectName("CardTitle")
        sel_layout.addWidget(sel_title)
        
        self.grid_layout_demo = QGridLayout()
        
        self.chk_1 = QCheckBox("{chk1_txt}")
        self.chk_2 = QCheckBox("{chk2_txt}")
        self.chk_3 = QCheckBox("{chk3_txt}")
        self.chk_4 = QCheckBox("{chk4_txt}")
        
        checkboxes = [self.chk_1, self.chk_2, self.chk_3, self.chk_4]
        for chk in checkboxes:
            chk.setChecked(True)
        
        self.grid_layout_demo.addWidget(self.chk_1, 0, 0)
        self.grid_layout_demo.addWidget(self.chk_2, 0, 1)
        self.grid_layout_demo.addWidget(self.chk_3, 1, 0)
        self.grid_layout_demo.addWidget(self.chk_4, 1, 1)
        
        sel_layout.addLayout(self.grid_layout_demo)
        sel_layout.addStretch()
        self.middle_layout.addWidget(self.selection_card, stretch=2)
        
        self.content_layout.addLayout(self.middle_layout)
        
        # 3. Lower Section - Progress & Buttons
        progress_card = QFrame()
        self.progress_layout = QVBoxLayout(progress_card)
        
        self.stats_layout = QHBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.stats_layout.addWidget(self.progress_bar, stretch=3)
        
        self.lbl_percent = QLabel("0%")
        self.stats_layout.addWidget(self.lbl_percent)
        
        self.speed_label = QLabel("Speed: -- MB/s")
        self.eta_label = QLabel("Remaining: --")
        
        self.stats_layout.addWidget(self.speed_label)
        self.stats_layout.addWidget(self.eta_label)
        self.progress_layout.addLayout(self.stats_layout)
        
        self.control_layout = QHBoxLayout()
        self.storage_label = QLabel("{storage_text}")
        self.control_layout.addWidget(self.storage_label)
        self.control_layout.addStretch()
        
        self.btn_start = PrimaryButton("{btn_start_txt}")
        self.btn_start.clicked.connect(self.start_test)
        
        self.btn_pause = SecondaryButton("Pause")
        self.btn_pause.setEnabled(False)
        self.btn_pause.clicked.connect(self.pause_test)
        
        self.btn_abort = DangerButton("Abort")
        self.btn_abort.setEnabled(False)
        self.btn_abort.clicked.connect(self.abort_test)
        
        self.control_layout.addWidget(self.btn_start)
        self.control_layout.addWidget(self.btn_pause)
        self.control_layout.addWidget(self.btn_abort)
        self.progress_layout.addLayout(self.control_layout)
        
        self.content_layout.addWidget(progress_card)
        
        # 4. Console Logs Section
        self.log_title = QLabel("{log_header_txt}")
        self.log_title.setObjectName("LogTitle")
        self.content_layout.addWidget(self.log_title)
        
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.append("{init_console_txt}")
        self.content_layout.addWidget(self.console, stretch=2)
        
        # Simulation Timer and variables
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_simulation)
        self.progress_val = 0.0
        self.log_step = 0
        self.tick_count = 0
        self.logs_pool = [
            f"[INFO] Checking color palette configuration: Active ({self.theme_manager.get_current_theme().upper()} preset)",
            "[INFO] Verifying primary color contrast ratios (WCAG AAA)...",
            "[INFO] Checking background color token mappings: DARK_BG, CARD_BG",
            "[INFO] Testing Button state rendering...",
            "[INFO] Button: Hover background contrast checks: OK",
            "[INFO] Button: Pressed background contrast checks: OK",
            "[INFO] Testing Checkbox state rendering...",
            "[INFO] Checkbox: Checked state indicator border checks: OK",
            "[INFO] Checkbox: Unchecked state border checks: OK",
            "[INFO] Testing Progress Bar gradient rendering...",
            "[INFO] Progress Bar: Gradient background rendering: OK",
            "[INFO] Progress Bar: Chunk rounded borders rendering: OK",
            "[INFO] Testing Combo Box dropdown styling...",
            "[INFO] Combo Box: Down-arrow SVG base64 icon parsing: OK",
            "[INFO] Combo Box: List view selection border rendering: OK",
            "[INFO] Testing Console text rendering and font family...",
            "[INFO] Console: Monospace font rendering verified: OK",
            "[INFO] Testing Scroll Bar colors and hover feedback...",
            "[INFO] Scroll Bar: Handle active states contrast verified: OK",
            "[INFO] Finalizing color palette checks...",
            "[INFO] Generating Palette Verification Report...",
            "{success_console_log}"
        ]
        
        # Subscribe to ThemeManager to get reactive styling
        self.theme_manager.subscribe(self._handle_theme_changed)
        
        # Trigger initial style application
        self.apply_dynamic_styles()

    def apply_dynamic_styles(self):
        tm = self.theme_manager
        is_dark = self.app_ctx.mode_manager.is_dark() if hasattr(self.app_ctx, "mode_manager") else True
        
        dark_bg = tm.get_color("DARK_BG")
        sidebar_bg = tm.get_color("SIDEBAR_BG")
        card_bg = tm.get_color("CARD_BG")
        text_color = tm.get_color("TEXT_COLOR")
        accent_color = tm.get_color("ACCENT_COLOR")
        accent_hover = tm.get_color("ACCENT_HOVER")
        border_color = tm.get_color("BORDER_COLOR")
        success_color = tm.get_color("SUCCESS_COLOR")
        error_color = tm.get_color("ERROR_COLOR")
        subtext_color = tm.get_color("SUBTEXT_COLOR")
        
        # Lấy thêm các Design Token phi màu sắc
        radius = tm.get_token("RADIUS")
        border_width = tm.get_token("BORDER_WIDTH")
        margin_b = tm.get_token("LABEL_MARGIN_BOTTOM")
        input_padding = tm.get_token("INPUT_PADDING")
        input_font_size = tm.get_token("INPUT_FONT_SIZE")
        combo_padding = tm.get_token("COMBO_PADDING")
        card_padding = tm.get_token("CARD_PADDING")
        checkbox_radius = tm.get_token("CHECKBOX_RADIUS")
        checkbox_spacing = tm.get_token("CHECKBOX_SPACING")
        progress_radius = tm.get_token("PROGRESS_RADIUS")
        progress_height = tm.get_token("PROGRESS_HEIGHT")
        console_radius = tm.get_token("CONSOLE_RADIUS")
        console_padding = tm.get_token("CONSOLE_PADDING")
        console_font_size = tm.get_token("CONSOLE_FONT_SIZE")
        status_font_size = tm.get_token("STATUS_FONT_SIZE")
        body_font_size = tm.get_token("BODY_FONT_SIZE")
        
        # New layout tokens
        badge_border_width = tm.get_token("BADGE_BORDER_WIDTH")
        badge_border_radius = tm.get_token("BADGE_BORDER_RADIUS")
        badge_padding = tm.get_token("BADGE_PADDING")
        button_min_width = tm.get_token("BUTTON_MIN_WIDTH")
        button_min_height = tm.get_token("BUTTON_MIN_HEIGHT")
        input_min_height = tm.get_token("INPUT_MIN_HEIGHT")
        checkbox_indicator_size = tm.get_token("CHECKBOX_INDICATOR_SIZE")
        button_padding = tm.get_token("BUTTON_PADDING")
        button_border_radius = tm.get_token("BUTTON_BORDER_RADIUS")
        
        # Adjust layout spacing dynamically
        spacing_b = tm.get_token("SPACING_BASE")
        spacing_val = int(spacing_b.replace("px", "")) if spacing_b.endswith("px") else 8
        self.top_layout.setSpacing(spacing_val)
        self.status_layout.setSpacing(spacing_val)
        self.middle_layout.setSpacing(spacing_val * 2)
        self.grid_layout_demo.setSpacing(spacing_val)
        self.progress_layout.setSpacing(spacing_val)
        self.stats_layout.setSpacing(spacing_val)
        self.control_layout.setSpacing(spacing_val)
        
        font_size_val = int(input_font_size.replace("px", "")) if input_font_size.endswith("px") else 12
        combo_min_width = f"{font_size_val * 20}px"
        dropdown_width = f"{font_size_val * 2}px"
        arrow_size = f"{font_size_val}px"
        
        # 1. ComboBox
        qss_combo = '''
            QComboBox[class="FormComboBox"] {
                background-color: {dark_bg};
                color: {text_color};
                border: {border_width} solid {accent_color};
                border-radius: {radius};
                padding: {combo_padding};
                font-size: {input_font_size};
                font-weight: bold;
                min-width: {combo_min_width};
            }
            QComboBox[class="FormComboBox"]::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: {dropdown_width};
                border-left: {border_width} solid {accent_color};
                border-top-right-radius: {radius};
                border-bottom-right-radius: {radius};
                background-color: {sidebar_bg};
            }
            QComboBox[class="FormComboBox"]::down-arrow {
                image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNjYmE2ZjciIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cG9seWxpbmUgcG9pbnRzPSI2IDkgMTIgMTUgMTggOSI+PC9wb2x5bGluZT48L3N2Zz4=");
                width: {arrow_size};
                height: {arrow_size};
            }
        '''.replace("{dark_bg}", dark_bg).replace("{text_color}", text_color).replace("{accent_color}", accent_color).replace("{sidebar_bg}", sidebar_bg).replace("{border_width}", border_width).replace("{radius}", radius).replace("{combo_padding}", combo_padding).replace("{input_font_size}", input_font_size).replace("{combo_min_width}", combo_min_width).replace("{dropdown_width}", dropdown_width).replace("{arrow_size}", arrow_size)
        self.device_combo.setStyleSheet(qss_combo)
        
        # 2. Mode Button
        qss_mode_btn = '''
            QPushButton {
                background-color: {card_bg};
                color: {text_color};
                border: {border_width} solid {border_color};
                border-radius: {button_border_radius};
                padding: {button_padding};
                font-size: {body_font_size};
                font-weight: bold;
                min-width: {button_min_width};
                min-height: {button_min_height};
            }
            QPushButton:hover {
                border-color: {accent_color};
                background-color: {dark_bg};
            }
        '''.replace("{card_bg}", card_bg).replace("{text_color}", text_color).replace("{border_color}", border_color).replace("{border_width}", border_width).replace("{button_border_radius}", button_border_radius).replace("{button_padding}", button_padding).replace("{body_font_size}", body_font_size).replace("{accent_color}", accent_color).replace("{dark_bg}", dark_bg).replace("{button_min_width}", button_min_width).replace("{button_min_height}", button_min_height)
        self.btn_mode.setStyleSheet(qss_mode_btn)
        
        # 3. Status labels (Styled as beautiful capsule badges)
        success_rgb = tm.get_token("SUCCESS_COLOR_RGB")
        badge_bg = f"rgba({success_rgb}, 0.1)" if is_dark else f"rgba({success_rgb}, 0.15)"
        badge_border = f"rgba({success_rgb}, 0.2)" if is_dark else f"rgba({success_rgb}, 0.3)"
        badge_text = success_color
        
        qss_badge = f'''
            QLabel {{
                background-color: {badge_bg};
                color: {badge_text};
                border: {badge_border_width} solid {badge_border};
                border-radius: {badge_border_radius};
                padding: {badge_padding};
                font-weight: bold;
                font-size: {status_font_size};
            }}
        '''
        self.lbl_status_1.setStyleSheet(qss_badge)
        self.lbl_status_2.setStyleSheet(qss_badge)
        
        # 4. Info Spec Card & Category selection card
        qss_info = '''
            QFrame {
                background-color: {card_bg};
                border: {border_width} solid {border_color};
                border-radius: {radius};
                padding: {card_padding};
            }
            QLabel#CardTitle {
                font-weight: bold;
                font-size: {status_font_size};
                color: {accent_color};
                border: none;
                background: transparent;
                margin-bottom: {margin_b};
            }
        '''.replace("{card_bg}", card_bg).replace("{border_color}", border_color).replace("{border_width}", border_width).replace("{radius}", radius).replace("{card_padding}", card_padding).replace("{status_font_size}", status_font_size).replace("{accent_color}", accent_color).replace("{margin_b}", margin_b)
        self.info_card.setStyleSheet(qss_info)
        self.specs_label.setStyleSheet(f"border: none; background: transparent;")
        
        active_theme_text = (
            "<html>"
            f"<body style='font-family: {tm.get_token(\"FONT_FAMILY\")}; font-size: {body_font_size}; color: {text_color};'>"
            "<table style='width: 100%; border-collapse: collapse;'>"
            f"<tr style='height: {button_min_height};'>"
            f"<td style='color: {subtext_color}; font-weight: bold;'>Color Palette:</td>"
            f"<td style='text-align: right; font-weight: bold; color: {accent_color};'>{tm.get_current_theme().upper()}</td>"
            "</tr>"
            f"<tr style='height: {button_min_height};'>"
            f"<td style='color: {subtext_color}; font-weight: bold;'>Mode:</td>"
            f"<td style='text-align: right; font-weight: bold; color: {badge_text};'>{'Dark' if is_dark else 'Light'} Active</td>"
            "</tr>"
            f"<tr style='height: {button_min_height};'>"
            "<td style='color: {subtext_color}; font-weight: bold;'>Widget Set:</td>"
            "<td style='text-align: right; font-weight: bold;'>Core PyQt6 Elements</td>"
            "</tr>"
            f"<tr style='height: {button_min_height};'>"
            f"<td style='color: {subtext_color}; font-weight: bold;'>Border Style:</td>"
            f"<td style='text-align: right; font-weight: bold;'>Radius ({radius})</td>"
            "</tr>"
            f"<tr style='height: {button_min_height};'>"
            f"<td style='color: {subtext_color}; font-weight: bold;'>Typography:</td>"
            f"<td style='text-align: right; font-weight: bold;'>{tm.get_token(\"FONT_FAMILY\")}</td>"
            "</tr>"
            "</table>"
            "</body>"
            "</html>"
        )
        self.specs_label.setText(active_theme_text)
        
        self.selection_card.setStyleSheet(qss_info)
        
        # Resolve path to check.svg icon dynamically
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        check_icon_path = os.path.abspath(os.path.join(current_dir, "..", "assets", "icons", "check.svg")).replace(os.sep, "/")
        
        qss_chk = '''
            QCheckBox {
                color: {text_color};
                font-size: {body_font_size};
                spacing: {checkbox_spacing};
            }
            QCheckBox::indicator {
                width: {checkbox_indicator_size};
                height: {checkbox_indicator_size};
                border: {border_width} solid {border_color};
                border-radius: {checkbox_radius};
                background-color: {dark_bg};
            }
            QCheckBox::indicator:checked {
                background-color: {accent_color};
                border-color: {accent_color};
                image: url("{check_icon_path}");
            }
        '''.replace("{text_color}", text_color).replace("{border_color}", border_color).replace("{dark_bg}", dark_bg).replace("{accent_color}", accent_color).replace("{border_width}", border_width).replace("{body_font_size}", body_font_size).replace("{checkbox_spacing}", checkbox_spacing).replace("{check_icon_path}", check_icon_path).replace("{checkbox_indicator_size}", checkbox_indicator_size).replace("{checkbox_radius}", checkbox_radius)
        
        for chk in [self.chk_1, self.chk_2, self.chk_3, self.chk_4]:
            chk.setStyleSheet(qss_chk)
            
        # 5. Progress bar and statistics
        qss_progress = '''
            QProgressBar {
                background-color: {dark_bg};
                border: {border_width} solid {border_color};
                border-radius: {progress_radius};
                height: {progress_height};
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {accent_color}, stop:1 {accent_hover});
                border-radius: {progress_radius};
            }
        '''.replace("{dark_bg}", dark_bg).replace("{border_color}", border_color).replace("{accent_color}", accent_color).replace("{accent_hover}", accent_hover).replace("{border_width}", border_width).replace("{progress_radius}", progress_radius).replace("{progress_height}", progress_height)
        self.progress_bar.setStyleSheet(qss_progress)
        lbl_percent_w = int(button_min_width.replace("px", "")) // 2 if button_min_width.endswith("px") else 40
        self.lbl_percent.setFixedWidth(lbl_percent_w)
        self.lbl_percent.setStyleSheet(f"color: {accent_color}; font-weight: bold; font-size: {body_font_size}; margin-left: {checkbox_spacing};")
        
        self.speed_label.setStyleSheet(f"color: {text_color}; font-weight: bold; font-size: {body_font_size}; margin-left: {card_padding};")
        self.eta_label.setStyleSheet(f"color: {text_color}; font-weight: bold; font-size: {body_font_size}; margin-left: {card_padding};")
        self.storage_label.setStyleSheet(f"color: {success_color}; font-weight: bold; font-size: {body_font_size};")
        self.log_title.setStyleSheet(f"color: {subtext_color}; font-weight: bold; font-size: {status_font_size}; margin-top: {margin_b};")
        
        # 6. Test Control Buttons Styling
        qss_btn_start = '''
            QPushButton {
                background-color: {accent_color};
                color: white;
                border: none;
                border-radius: {button_border_radius};
                padding: {button_padding};
                font-size: {body_font_size};
                font-weight: bold;
                min-width: {button_min_width};
                min-height: {button_min_height};
            }
            QPushButton:hover {
                background-color: {accent_hover};
            }
            QPushButton:disabled {
                background-color: {border_color};
                color: {subtext_color};
            }
        '''.replace("{accent_color}", accent_color).replace("{accent_hover}", accent_hover).replace("{button_border_radius}", button_border_radius).replace("{button_padding}", button_padding).replace("{body_font_size}", body_font_size).replace("{border_color}", border_color).replace("{subtext_color}", subtext_color).replace("{button_min_width}", button_min_width).replace("{button_min_height}", button_min_height)
        self.btn_start.setStyleSheet(qss_btn_start)
        
        qss_btn_pause = '''
            QPushButton {
                background-color: transparent;
                color: {accent_color};
                border: {border_width} solid {accent_color};
                border-radius: {button_border_radius};
                padding: {button_padding};
                font-size: {body_font_size};
                font-weight: bold;
                min-width: {button_min_width};
                min-height: {button_min_height};
            }
            QPushButton:hover {
                background-color: {accent_color};
                color: {dark_bg};
            }
            QPushButton:disabled {
                border-color: {border_color};
                color: {subtext_color};
            }
        '''.replace("{accent_color}", accent_color).replace("{border_width}", border_width).replace("{button_border_radius}", button_border_radius).replace("{button_padding}", button_padding).replace("{body_font_size}", body_font_size).replace("{dark_bg}", dark_bg).replace("{border_color}", border_color).replace("{subtext_color}", subtext_color).replace("{button_min_width}", button_min_width).replace("{button_min_height}", button_min_height)
        self.btn_pause.setStyleSheet(qss_btn_pause)
        
        qss_btn_abort = '''
            QPushButton {
                background-color: {error_color};
                color: white;
                border: none;
                border-radius: {button_border_radius};
                padding: {button_padding};
                font-size: {body_font_size};
                font-weight: bold;
                min-width: {button_min_width};
                min-height: {button_min_height};
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
            QPushButton:disabled {
                background-color: {border_color};
                color: {subtext_color};
            }
        '''.replace("{error_color}", error_color).replace("{button_border_radius}", button_border_radius).replace("{button_padding}", button_padding).replace("{body_font_size}", body_font_size).replace("{border_color}", border_color).replace("{subtext_color}", subtext_color).replace("{button_min_width}", button_min_width).replace("{button_min_height}", button_min_height)
        self.btn_abort.setStyleSheet(qss_btn_abort)
        
        # 7. Console
        qss_console = '''
            QTextEdit {
                background-color: {sidebar_bg};
                color: {success_color};
                border: {border_width} solid {border_color};
                border-radius: {console_radius};
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: {console_font_size};
                padding: {console_padding};
            }
        '''.replace("{sidebar_bg}", sidebar_bg).replace("{success_color}", success_color).replace("{border_color}", border_color).replace("{border_width}", border_width).replace("{console_radius}", console_radius).replace("{console_font_size}", console_font_size).replace("{console_padding}", console_padding)
        self.console.setStyleSheet(qss_console)

    def toggle_mode(self):
        mode_manager = self.app_ctx.mode_manager
        current = mode_manager.get_current_mode()
        new_mode = "light" if current == "dark" else "dark"
        mode_manager.switch_mode(new_mode)

    def _handle_theme_changed(self, theme_name: str, qss: str):
        is_dark = self.app_ctx.mode_manager.is_dark()
        self.btn_mode.setText("🌙 Dark" if is_dark else "☀️ Light")
        self.apply_dynamic_styles()

    def start_test(self):
        self.btn_start.setEnabled(False)
        self.btn_pause.setEnabled(True)
        self.btn_abort.setEnabled(True)
        self.device_combo.setEnabled(False)
        
        self.console.append("[INFO] Starting color palette verification test...")
        self.progress_val = 0.0
        self.log_step = 0
        self.tick_count = 0
        self.timer.start(30) # 30ms tick for buttery smooth 33 FPS animation

    def pause_test(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn_pause.setText("Resume")
            self.console.append("[WARN] Color palette verification test paused.")
        else:
            self.timer.start(30)
            self.btn_pause.setText("Pause")
            self.console.append("[INFO] Color palette verification test resumed.")

    def abort_test(self):
        self.timer.stop()
        self.progress_val = 0.0
        self.log_step = 0
        self.tick_count = 0
        self.progress_bar.setValue(0)
        self.lbl_percent.setText("0%")
        self.speed_label.setText("Speed: -- MB/s")
        self.eta_label.setText("Remaining: --")
        self.btn_start.setEnabled(True)
        self.btn_pause.setEnabled(False)
        self.btn_abort.setEnabled(False)
        self.btn_pause.setText("Pause")
        self.device_combo.setEnabled(True)
        self.console.append("[ERROR] Color palette verification test aborted.")

    def update_simulation(self):
        if self.progress_val < 100.0:
            self.progress_val += 0.2
            if self.progress_val > 100.0:
                self.progress_val = 100.0
            self.progress_bar.setValue(int(self.progress_val))
            self.lbl_percent.setText(f"{int(self.progress_val)}%")
            
            self.tick_count += 1
            
            # Low-frequency update for text stats every 20 ticks (320ms) to avoid flickering/blur
            if self.tick_count % 20 == 0:
                import random
                speed = round(40.0 + random.uniform(-3.5, 3.5), 1)
                self.speed_label.setText(f"Speed: {speed} MB/s")
                rem_sec = max(0, int((100 - self.progress_val) * 0.12))
                self.eta_label.setText(f"Remaining: {rem_sec}s" if rem_sec > 0 else "Remaining: 1s")
                
            # Append log every 30 ticks (approx 480ms)
            if self.tick_count % 30 == 0 and self.log_step < len(self.logs_pool):
                self.console.append(self.logs_pool[self.log_step])
                self.log_step += 1
        else:
            self.timer.stop()
            self.lbl_percent.setText("100%")
            self.speed_label.setText("Speed: 0.0 MB/s")
            self.eta_label.setText("Remaining: Done")
            self.btn_pause.setEnabled(False)
            self.btn_abort.setEnabled(False)
            self.btn_start.setEnabled(True)
            self.device_combo.setEnabled(True)
            QMessageBox.information(
                self, 
                "{success_msg_title}", 
                "{success_msg_text}"
            )
            self.progress_val = 0.0
            self.log_step = 0
            self.tick_count = 0

    def retranslate_ui(self, lang_code: str):
        pass
"""
            return (
                template.replace("{pascal_name}", pascal_name)
                .replace("{snake_name}", snake_name)
                .replace("{specs_title}", specs_title)
                .replace("{specs_content}", specs_content)
                .replace("{category_title}", category_title)
                .replace("{chk1_txt}", chk1_txt)
                .replace("{chk2_txt}", chk2_txt)
                .replace("{chk3_txt}", chk3_txt)
                .replace("{chk4_txt}", chk4_txt)
                .replace("{storage_text}", storage_text)
                .replace("{btn_start_txt}", btn_start_txt)
                .replace("{log_header_txt}", log_header_txt)
                .replace("{init_console_txt}", init_console_txt)
                .replace("{success_console_log}", success_console_log)
                .replace("{success_msg_title}", success_msg_title)
                .replace("{success_msg_text}", success_msg_text)
            )
