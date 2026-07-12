from PyQt6.QtWidgets import QFrame, QVBoxLayout
from ..level_01_atoms.labels import HeaderLabel, BodyLabel


class StatCard(QFrame):
    """
    StatCard - Molecule hiển thị số liệu thống kê nhanh trong dự án.
    Ghép từ 2 Atoms: BodyLabel (tiêu đề) và HeaderLabel (giá trị số).
    """

    def __init__(self, title: str, val: str, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setProperty("class", "StatCard")
        self.setObjectName("stat_card")
        lay = QVBoxLayout(self)

        self.title_label = BodyLabel(title)
        self.value_label = HeaderLabel(val)

        lay.addWidget(self.title_label)
        lay.addWidget(self.value_label)
