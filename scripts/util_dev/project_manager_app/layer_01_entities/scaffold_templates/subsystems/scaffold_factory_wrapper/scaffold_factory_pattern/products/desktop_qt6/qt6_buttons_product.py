from ..abstract.i_buttons_product import AbstractButtons


class Qt6Buttons(AbstractButtons):
    """
    GoF Role: ConcreteProduct
    """

    def get_template(self) -> str:
        return '''from PyQt6.QtWidgets import QPushButton


class PrimaryButton(QPushButton):
    """
    PrimaryButton - Nút bấm hành động chính.
    """
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setProperty("class", "PrimaryButton")


class DangerButton(QPushButton):
    """
    DangerButton - Nút bấm nguy hiểm/cảnh báo.
    """
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setProperty("class", "DangerButton")


class SecondaryButton(QPushButton):
    """
    SecondaryButton - Nút bấm phụ.
    """
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setProperty("class", "SecondaryButton")
'''

    def get_qss_template(self) -> str:
        return """/* --- Atom Buttons --- */
QPushButton[class="PrimaryButton"] {
    background-color: {ACCENT_COLOR};
    color: {SIDEBAR_BG};
    font-size: {BUTTON_FONT_SIZE};
    font-weight: bold;
    padding: {BUTTON_PADDING};
    border-radius: {RADIUS};
    border: none;
}
QPushButton[class="PrimaryButton"]:hover {
    background-color: {ACCENT_HOVER};
}

QPushButton[class="DangerButton"] {
    background-color: {ERROR_COLOR};
    color: {SIDEBAR_BG};
    font-size: {BUTTON_FONT_SIZE};
    font-weight: bold;
    padding: {BUTTON_PADDING};
    border-radius: {RADIUS};
    border: none;
}
QPushButton[class="DangerButton"]:hover {
    background-color: {ACCENT_HOVER};
}

QPushButton[class="SecondaryButton"] {
    background-color: transparent;
    color: {ACCENT_COLOR};
    border: {BORDER_WIDTH} solid {ACCENT_COLOR};
    border-radius: {RADIUS};
    padding: {BUTTON_PADDING};
    font-weight: bold;
    font-size: {BUTTON_FONT_SIZE};
}
QPushButton[class="SecondaryButton"]:hover {
    background-color: {ACCENT_COLOR};
    color: {SIDEBAR_BG};
}
"""
