import os
import json
from ..strategy import STRATEGY_REGISTRY, DefaultCompilationStrategy


class ThemeContext:
    """
    GoF Role: Context
    Manages loading of theme presets (geometry, font) and color palettes.
    Derives platform-specific formats (ARGB, Kivy Float) dynamically and
    coordinates compilation of template placeholders using Strategy Pattern.
    """

    def __init__(self, root_dir: str, theme_name: str, color_preset_name: str):
        self.root_dir = root_dir
        self.theme_name = theme_name
        self.color_preset_name = color_preset_name

        self.theme_data = {}
        self.palette_data = {}
        self.tokens = {}

        self._load_theme_and_palette()
        self.validate_theme_contract()

    def _load_theme_and_palette(self):
        # 1. Resolve paths to appdata/theme_presets and its subdirectories
        appdata_dir = os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "..",
                "..",
                "..",
                "..",
                "..",
                "..",
                "..",
                "appdata",
            )
        )
        themes_dir = os.path.join(appdata_dir, "theme_presets")
        palettes_dir = os.path.join(themes_dir, "07_color_palettes")

        # 2. Load Theme configuration from the 6 pillars subdirectories
        self.theme_data = {}
        theme_clean_name = self.theme_name.lower().replace("_", "")

        # Pillars directories (01 to 05 have JSON configuration, 06 has visual assets)
        pillar_subs = [
            "01_geometry_borders",
            "02_typography",
            "03_spacing",
            "04_shadows_elevation",
            "05_motion_animations",
        ]

        for sub in pillar_subs:
            sub_dir = os.path.join(themes_dir, sub)
            if not os.path.exists(sub_dir):
                continue

            # Search for the requested theme file in this subdirectory
            target_file = None
            for file_name in os.listdir(sub_dir):
                name_without_ext, _ = os.path.splitext(file_name)
                if name_without_ext.lower().replace("_", "") == theme_clean_name:
                    target_file = os.path.join(sub_dir, file_name)
                    break

            # If not found, fallback to default_theme.json
            if not target_file or not os.path.exists(target_file):
                target_file = os.path.join(sub_dir, "default_theme.json")

            if os.path.exists(target_file):
                try:
                    with open(target_file, "r", encoding="utf-8") as f:
                        sub_data = json.load(f)
                    self.theme_data.update(sub_data)
                except Exception:
                    pass

            # Load defaults if target_file wasn't default_theme.json to ensure full fallback
            default_file = os.path.join(sub_dir, "default_theme.json")
            if os.path.exists(default_file) and target_file != default_file:
                try:
                    with open(default_file, "r", encoding="utf-8") as f:
                        defaults = json.load(f)
                    for k, v in defaults.items():
                        if k not in self.theme_data:
                            self.theme_data[k] = v
                except Exception:
                    pass

        # 3. Load Color Palette configuration
        palette_file = None
        palette_clean_name = self.color_preset_name.lower().replace("_", "")
        if os.path.exists(palettes_dir):
            for file_name in os.listdir(palettes_dir):
                name_without_ext, _ = os.path.splitext(file_name)
                if name_without_ext.lower().replace("_", "") == palette_clean_name:
                    palette_file = os.path.join(palettes_dir, file_name)
                    break

        if not palette_file or not os.path.exists(palette_file):
            palette_file = os.path.join(palettes_dir, "Catppuccin_Mocha.json")

        try:
            with open(palette_file, "r", encoding="utf-8") as f:
                self.palette_data = json.load(f)
        except Exception:
            self.palette_data = {}

        # 4. Extract Dark and Light Mode sections
        self.dark_theme = (
            self.palette_data.get("dark", list(self.palette_data.values())[0])
            if self.palette_data
            else {}
        )
        self.light_theme = (
            self.palette_data.get("light", {}) if self.palette_data else {}
        )

        dark_section = self.dark_theme
        light_section = self.light_theme

        # 5. Apply manual branding overrides from project_config.json
        try:
            from scripts.util_dev.project_manager_app.config.project_config import (
                read_project_branding,
            )

            branding = read_project_branding(self.root_dir)
            if branding:
                if dark_section:
                    if "accent_color_dark" in branding:
                        dark_section["ACCENT_COLOR"] = branding["accent_color_dark"]
                    if "accent_hover_dark" in branding:
                        dark_section["ACCENT_HOVER"] = branding["accent_hover_dark"]
                    if "font_family" in branding:
                        self.theme_data["FONT_FAMILY"] = branding["font_family"]
                if light_section:
                    if "accent_color_light" in branding:
                        light_section["ACCENT_COLOR"] = branding["accent_color_light"]
                    if "accent_hover_light" in branding:
                        light_section["ACCENT_HOVER"] = branding["accent_hover_light"]
        except Exception:
            pass

        # 6. Build unified tokens dictionary
        # Add all geometry and typography tokens from the Theme configuration
        for k, v in self.theme_data.items():
            self.tokens[k] = v

        # Add all colors from the Color Palette configuration (defaulting to dark mode)
        for k, v in dark_section.items():
            self.tokens[k] = v

            # Derive ARGB format: e.g. ACCENT_COLOR_ARGB = 0xFF89B4FA
            self.tokens[f"{k}_ARGB"] = "0xFF" + v.replace("#", "").upper()

            # Derive RGB format: e.g. ACCENT_COLOR_RGB = 137, 180, 250
            try:
                h = v.replace("#", "")
                r_int = int(h[0:2], 16)
                g_int = int(h[2:4], 16)
                b_int = int(h[4:6], 16)
                self.tokens[f"{k}_RGB"] = f"{r_int}, {g_int}, {b_int}"
            except Exception:
                self.tokens[f"{k}_RGB"] = "255, 255, 255"

            # Derive Kivy Float format: e.g. ACCENT_COLOR_KIVY_FLOAT = 0.54, 0.71, 0.98, 1.0
            try:
                h = v.replace("#", "")
                r = int(h[0:2], 16) / 255.0
                g = int(h[2:4], 16) / 255.0
                b = int(h[4:6], 16) / 255.0
                self.tokens[f"{k}_KIVY_FLOAT"] = f"{r:.2f}, {g:.2f}, {b:.2f}, 1.0"
            except Exception:
                self.tokens[f"{k}_KIVY_FLOAT"] = "1.0, 1.0, 1.0, 1.0"

        # Derive numeric versions of px-valued tokens for Kivy/numeric layout compatibility
        for k in list(self.tokens.keys()):
            v = self.tokens[k]
            if isinstance(v, str) and v.endswith("px") and k != "_color_map":
                try:
                    num_val = v.replace("px", "").strip()
                    float(num_val)  # Test parseability
                    self.tokens[f"{k}_NUM"] = num_val
                except ValueError:
                    pass

        # Special mapping alias for Dracula/Catppuccin compatibility in test suites
        # (Translate legacy hex matches)
        dark_bg = dark_section.get("DARK_BG", "#1e1e2e")
        card_bg = dark_section.get("CARD_BG", "#181825")
        text_color = dark_section.get("TEXT_COLOR", "#cdd6f4")
        subtext_color = dark_section.get("SUBTEXT_COLOR", "#a6adc8")
        accent_color = dark_section.get("ACCENT_COLOR", "#89b4fa")
        accent_hover = dark_section.get("ACCENT_HOVER", "#b4befe")
        success_color = dark_section.get("SUCCESS_COLOR", "#a6e3a1")
        error_color = dark_section.get("ERROR_COLOR", "#f38ba8")
        border_color = dark_section.get("BORDER_COLOR", "#313244")

        light_bg = light_section.get("DARK_BG", "#eff1f5")
        light_text = light_section.get("TEXT_COLOR", "#4c4f69")
        light_card = light_section.get("CARD_BG", "#e6e9ef")
        light_border = light_section.get("BORDER_COLOR", "#dce0e8")

        self.color_map = {
            "#282a36": dark_bg,
            "#44475a": card_bg,
            "#f8f8f2": text_color,
            "#6272a4": subtext_color,
            "#50fa7b": accent_color,
            "#1e1e2e": dark_bg,
            "#181825": card_bg,
            "#313244": border_color,
            "#cdd6f4": text_color,
            "#a6adc8": subtext_color,
            "#cba6f7": accent_color,
            "#89b4fa": accent_color,
            "#f5c2e7": accent_hover,
            "#a6e3a1": success_color,
            "#f38ba8": error_color,
            "#eff1f5": light_bg,
            "#4c4f69": light_text,
            "#e6e9ef": light_card,
            "#dce0e8": light_border,
        }
        self.tokens["_color_map"] = self.color_map

    def compile(self, file_path: str, content: str) -> str:
        """
        Delegates compilation of template content to the matched strategy.
        Uses dynamic dispatching via polymorphism.
        """
        norm_path = file_path.replace("\\", "/")

        # Preserve placeholders in PyQt6 QSS files for dynamic runtime compiling
        if norm_path.endswith(".qss") and ("ui/desktop_qt" in norm_path):
            return content

        # Match strategy via polymorphic is_matching call
        for platform_key, strategy in STRATEGY_REGISTRY.items():
            if platform_key != "default" and strategy.is_matching(norm_path):
                return strategy.compile(
                    content, self.theme_data, self.palette_data, self.tokens
                )

        # Fallback to default strategy
        default_strat = STRATEGY_REGISTRY.get("default") or DefaultCompilationStrategy()
        return default_strat.compile(
            content, self.theme_data, self.palette_data, self.tokens
        )

    def validate_theme_contract(self):
        """
        Validates that all W3C design tokens required for pixel-perfect layout
        control are defined in the context.
        """
        required_tokens = [
            "RADIUS",
            "BUTTON_BORDER_RADIUS",
            "INPUT_BORDER_RADIUS",
            "CHECKBOX_BORDER_RADIUS",
            "PROGRESS_BORDER_RADIUS",
            "CONSOLE_BORDER_RADIUS",
            "BADGE_BORDER_RADIUS",
            "BORDER_WIDTH",
            "BADGE_BORDER_WIDTH",
            "FONT_FAMILY",
            "BUTTON_FONT_SIZE",
            "INPUT_FONT_SIZE",
            "HEADER_FONT_SIZE",
            "BODY_FONT_SIZE",
            "CONSOLE_FONT_SIZE",
            "STATUS_FONT_SIZE",
            "SPACING_BASE",
            "PAGE_PADDING",
            "BUTTON_PADDING",
            "INPUT_PADDING",
            "COMBO_PADDING",
            "CARD_PADDING",
            "CONSOLE_PADDING",
            "BADGE_PADDING",
            "CHECKBOX_SPACING",
            "BUTTON_MIN_WIDTH",
            "BUTTON_MIN_HEIGHT",
            "INPUT_MIN_HEIGHT",
            "CHECKBOX_INDICATOR_SIZE",
            "PROGRESS_HEIGHT",
            "CONSOLE_HEIGHT",
            "SIDEBAR_WIDTH",
            "CONTAINER_MAX_WIDTH",
            "GRID_MIN_WIDTH",
            "GRID_GAP",
        ]
        missing = [t for t in required_tokens if t not in self.tokens]
        if missing:
            raise ValueError(
                f"Theme '{self.theme_name}' contract validation failed. Missing tokens: {missing}"
            )
