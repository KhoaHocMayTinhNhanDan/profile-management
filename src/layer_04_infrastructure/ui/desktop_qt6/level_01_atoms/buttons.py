from PyQt6.QtWidgets import QPushButton


class PrimaryButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setProperty("class", "PrimaryButton")
        self.setObjectName("primary_btn")


class DangerButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setProperty("class", "DangerButton")
        self.setObjectName("danger_btn")


class SecondaryButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setProperty("class", "SecondaryButton")
        self.setObjectName("secondary_btn")
