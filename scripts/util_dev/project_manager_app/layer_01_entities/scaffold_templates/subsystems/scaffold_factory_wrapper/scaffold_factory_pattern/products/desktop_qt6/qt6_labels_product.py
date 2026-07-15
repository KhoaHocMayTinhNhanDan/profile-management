from ..abstract.i_labels_product import AbstractLabels


class Qt6Labels(AbstractLabels):
    """
    GoF Role: ConcreteProduct
    """

    def get_template(self) -> str:
        return """from PyQt6.QtWidgets import QLabel

class HeaderLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setProperty("class", "HeaderLabel")

class BodyLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setProperty("class", "BodyLabel")
"""

    def get_qss_template(self) -> str:
        return """/* --- Atom Labels --- */
QLabel[class="HeaderLabel"] {
    color: {ACCENT_COLOR};
    font-family: {FONT_FAMILY};
    font-size: {HEADER_FONT_SIZE};
    font-weight: bold;
    margin-bottom: {LABEL_MARGIN_BOTTOM};
}

QLabel[class="BodyLabel"] {
    color: {TEXT_COLOR};
    font-family: {FONT_FAMILY};
    font-size: {BODY_FONT_SIZE};
}
"""
