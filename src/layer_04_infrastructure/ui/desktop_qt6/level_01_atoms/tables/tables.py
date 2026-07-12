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

    def adjust_height_to_contents(self):
        """
        Tự động điều chỉnh chiều cao tối thiểu của bảng dựa trên số lượng dòng hiện có
        để tránh hiện tượng thanh cuộn dọc xuất hiện bên trong bảng.
        """
        # Header height
        h_hdr = self.horizontalHeader()
        h_height = h_hdr.height() if h_hdr is not None else 40
        if h_height < 30:
            h_height = 40

        # Row heights
        r_height = 0
        r_count = self.rowCount()
        for i in range(r_count):
            r_height += self.rowHeight(i) or 40

        if r_count > 0 and r_height == 0:
            r_height = r_count * 40

        if r_count == 0:
            total_height = 100
        else:
            total_height = h_height + r_height + 2 * self.frameWidth() + 4

        self.setMinimumHeight(total_height)
        self.setMaximumHeight(total_height)
