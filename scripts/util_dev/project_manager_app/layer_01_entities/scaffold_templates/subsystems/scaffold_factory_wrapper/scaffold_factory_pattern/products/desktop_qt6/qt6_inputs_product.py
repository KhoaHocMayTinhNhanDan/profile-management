from ..abstract.i_inputs_product import AbstractInputs


class Qt6Inputs(AbstractInputs):
    """
    GoF Role: ConcreteProduct
    """

    def get_template(self) -> str:
        return '''from PyQt6.QtWidgets import QLineEdit, QComboBox


class FormLineEdit(QLineEdit):
    """
    FormLineEdit - Ô nhập liệu biểu mẫu.
    """
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setProperty("class", "FormLineEdit")


class FormComboBox(QComboBox):
    """
    FormComboBox - Hộp chọn biểu mẫu.
    """
    def __init__(self, items=None, parent=None):
        super().__init__(parent)
        if items:
            self.addItems(items)
        self.setProperty("class", "FormComboBox")
'''

    def get_qss_template(self) -> str:
        return """/* --- Atom Inputs --- */
QLineEdit[class="FormLineEdit"] {
    background-color: {DARK_BG};
    color: {TEXT_COLOR};
    border: {BORDER_WIDTH} solid {BORDER_COLOR};
    border-radius: {RADIUS};
    padding: {INPUT_PADDING};
    font-size: {INPUT_FONT_SIZE};
}
QLineEdit[class="FormLineEdit"]:focus {
    border: {BORDER_WIDTH} solid {ACCENT_COLOR};
}

QComboBox[class="FormComboBox"] {
    background-color: {SIDEBAR_BG};
    border: {BORDER_WIDTH} solid {BORDER_COLOR};
    color: {TEXT_COLOR};
    padding: {INPUT_PADDING};
    font-size: {INPUT_FONT_SIZE};
    border-radius: {RADIUS};
}
QComboBox[class="FormComboBox"] QAbstractItemView {
    background-color: {SIDEBAR_BG};
    color: {TEXT_COLOR};
    selection-background-color: {ACCENT_COLOR};
    selection-color: {SIDEBAR_BG};
    border: {BORDER_WIDTH} solid {BORDER_COLOR};
}
"""
