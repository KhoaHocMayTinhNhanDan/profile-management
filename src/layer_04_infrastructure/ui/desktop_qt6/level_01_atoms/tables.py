from PyQt6.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView


class AppTable(QTableWidget):
    """
    AppTable (Level 1: Atoms): Thành phần bảng dữ liệu dùng chung.
    Tự động cấu hình các thuộc tính cơ bản để đồng bộ hóa hành vi và kiểu dáng
    (chọn cả dòng, khóa chỉnh sửa trực tiếp, ẩn tiêu đề dòng).
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("class", "AppTable")

        # Cấu hình hành vi chuẩn cho bảng dữ liệu
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # Ẩn thanh tiêu đề dòng dọc (1, 2, 3...) và tăng nhẹ chiều cao dòng chuẩn
        v_hdr = self.verticalHeader()
        if v_hdr is not None:
            v_hdr.setVisible(False)
            v_hdr.setDefaultSectionSize(40)

        # Mặc định kéo dãn các cột
        h_hdr = self.horizontalHeader()
        if h_hdr is not None:
            h_hdr.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
