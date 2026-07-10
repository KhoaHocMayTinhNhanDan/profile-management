# 🖥️ Quy chuẩn Thiết kế Desktop UX (PyQt6 / Tkinter)

Tài liệu này định nghĩa các quy tắc thiết kế giao diện đồ họa máy tính (Desktop GUI) dựa trên **Apple macOS Human Interface Guidelines (HIG)** và tiêu chuẩn ứng dụng Windows, tập trung vào tối ưu hóa tương tác bằng chuột, bàn phím và không gian màn hình rộng.

---

## ⌨️ 1. Điều hướng Bàn phím & Focus States
Ứng dụng desktop bắt buộc phải sử dụng được 100% bằng bàn phím mà không cần chuột:

*   **Thứ tự Tab (Tab Order):** Phím `Tab` phải di chuyển tiêu điểm (Focus Indicator) qua các widget theo đúng thứ tự logic từ trên xuống dưới, từ trái qua phải.
*   **Trạng thái Focus trực quan:** Trường dữ liệu đang được Focus phải thay đổi viền (ví dụ: viền màu xanh Primary) để người dùng biết họ đang gõ chữ ở đâu.
*   **Phím tắt mặc định (Keyboard Shortcuts):**
    *   `Enter`: Kích hoạt hành động chính của màn hình (ví dụ: nút Submit trong hộp thoại).
    *   `Escape`: Đóng cửa sổ, tắt popup, hủy bỏ tác vụ đang thực thi.
    *   `Ctrl + S` (hoặc `Cmd + S` trên Mac): Lưu dữ liệu.
    *   `Ctrl + F`: Mở ô tìm kiếm.

---

## 🖱️ 2. Trạng thái Tương tác Con trỏ Chuột (Hover & Cursor States)
*   **Hover Effect (Trạng thái rê chuột):** Mọi nút bấm, thẻ thông tin click được, hoặc hàng trong bảng (Table Row) phải đổi màu nền nhẹ (thường sáng lên hoặc tối đi 10%) khi con trỏ chuột di qua.
*   **Thay đổi hình dáng con trỏ (Cursor Shape):**
    *   Chuyển sang con trỏ bàn tay (`Pointing Hand/Grab`) khi di chuột vào phần tử bấm được (Button, Link, Tab).
    *   Chuyển sang con trỏ chữ I (`I-Beam`) khi di chuột vào vùng nhập văn bản.
    *   Chuyển sang con trỏ tải (`Wait/Busy`) khi hệ thống đang xử lý tác vụ đồng bộ khóa giao diện.

---

## 🔲 3. Quản lý Bố cục Cửa sổ & Chia lưới (Window Layout)
*   **Layout đàn hồi (Flexible Layout):** Tuyệt đối không dùng kích thước pixel cứng (hard-coded pixels) cho vị trí các widget. Bắt buộc sử dụng hệ thống layout tự co giãn (`QGridLayout`, `QVBoxLayout`, `QHBoxLayout` trong Qt) để giao diện tự dàn đều khi phóng to/thu nhỏ.
*   **Kích thước tối thiểu (Minimum Size):** Phải set thuộc tính kích thước cửa sổ tối thiểu để giao diện không bị vỡ hoặc che khuất các nút điều hướng quan trọng khi người dùng thu nhỏ cửa sổ hết cỡ.
*   **Tỉ lệ hiển thị (Visual Hierarchy):** Các cột thông tin phụ bên phải hoặc menu điều hướng bên trái nên có cơ chế ẩn/hiện (Splitter/Drawer) để nhường diện tích cho khu vực làm việc chính ở trung tâm.

---

## 📂 4. Phân cấp Menu & Thanh trạng thái (Menus & StatusBar)
*   **Thanh Menu chính (MenuBar):** Nhóm các chức năng hệ thống theo nhóm chuẩn quốc tế: `File` (các tác vụ tệp tin, cài đặt, thoát), `Edit` (sao chép, hoàn tác), `Tools` (các công cụ mở rộng), và `Help`.
*   **Thanh công cụ (ToolBar):** Chỉ đưa các lối tắt của các hành động được sử dụng nhiều nhất (tối đa 5-7 nút kèm tooltip giải thích).
*   **Thanh trạng thái (StatusBar):** Đặt ở dưới cùng cửa sổ để cập nhật thông tin nhanh cho người dùng (ví dụ: "Đang kết nối database...", "Đã lưu 5 phút trước").
