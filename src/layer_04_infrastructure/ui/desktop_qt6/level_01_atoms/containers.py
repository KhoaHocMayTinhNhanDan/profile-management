from PyQt6.QtWidgets import QFrame, QVBoxLayout


class CardContainer(QFrame):
    """
    CardContainer (Level 1: Atoms): Khung chứa sử dụng chung có màu nền,
    viền và bo góc theo thiết kế Card của hệ thống (Design System).
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("class", "CardContainer")
        self.container_layout = QVBoxLayout(self)
        self.container_layout.setContentsMargins(16, 16, 16, 16)
        self.container_layout.setSpacing(12)

    def addWidget(self, widget):
        self.container_layout.addWidget(widget)

    def addLayout(self, layout):
        self.container_layout.addLayout(layout)


class PanelContainer(QFrame):
    """
    PanelContainer (Level 1: Atoms): Khung chứa phụ trợ cho các vùng điều khiển
    hoặc thanh điều hướng con có màu nền tối/chìm đồng bộ.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("class", "PanelContainer")
        self.container_layout = QVBoxLayout(self)
        self.container_layout.setContentsMargins(16, 16, 16, 16)
        self.container_layout.setSpacing(12)

    def addWidget(self, widget):
        self.container_layout.addWidget(widget)

    def addLayout(self, layout):
        self.container_layout.addLayout(layout)
