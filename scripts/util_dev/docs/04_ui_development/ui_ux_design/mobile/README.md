# 📱 Quy chuẩn Thiết kế Mobile UX (Kivy / Mobile Viewports)

Tài liệu này định nghĩa các nguyên tắc thiết kế giao diện và tối ưu hóa trải nghiệm người dùng trên thiết bị di động (Mobile App) dựa trên **Google Material Design 3** và **Apple iOS Human Interface Guidelines (HIG)**.

---

## 👆 1. Vùng chạm Tương tác (Touch Target Size)
Kích thước ngón tay người dùng lớn hơn rất nhiều so với con trỏ chuột desktop, do đó giao diện cần được thiết kế rộng rãi:

*   **Kích thước tối thiểu (Touch Target):** Mọi nút bấm, checkbox, biểu tượng click được phải có vùng chạm tối thiểu là **48 x 48 dp** (đối với Android Material 3) hoặc **44 x 44 pt** (đối với iOS HIG) để tránh bấm trượt.
*   **Khoảng giãn cách (Spacing):** Khoảng cách tối thiểu giữa các nút bấm cạnh nhau phải là **8dp** để tránh hiện tượng bấm nhầm nút bên cạnh.

---

## 📐 2. Bố cục và Vùng An toàn (Layout & Safe Area)
*   **Vùng an toàn (Safe Area Insets):** Khi thiết kế giao diện tràn viền, bắt buộc phải chừa khoảng đệm (padding) ở phía trên và phía dưới màn hình để giao diện không bị đè bởi camera tai thỏ (Notch), camera nốt ruồi hoặc thanh vuốt chuyển ứng dụng của hệ điều hành.
*   **Bố cục dọc cuộn (Vertical Scrollable):** Màn hình điện thoại có chiều dọc dài. Mọi layout trang phải đặt trong một bộ cuộn (`ScrollView` trong Kivy) để khi bàn phím ảo (Virtual Keyboard) hiện lên, giao diện tự động cuộn lên và không bị lỗi tràn khung hiển thị.

---

## 🖲️ 3. Tương tác Cử chỉ (Gestures & Touch Feedback)
*   **Phản hồi ngay lập tức (Visual Touch Feedback):** Khi người dùng chạm ngón tay vào nút, nút đó phải thay đổi trạng thái ngay lập tức (ví dụ: chuyển sang màu tối hơn hoặc có hiệu ứng gợn sóng - Ripple Effect) để xác nhận thao tác chạm thành công.
*   **Cử chỉ tự nhiên:**
    *   *Vuốt để cuộn (Swipe to scroll):* Hỗ trợ cuộn mượt mà có gia tốc lực vuốt.
    *   *Kéo để làm mới (Pull-to-refresh):* Áp dụng cho các trang danh sách dữ liệu trực tuyến.
    *   *Vuốt từ cạnh (Edge swipe):* Hỗ trợ vuốt từ cạnh trái màn hình để quay lại trang trước (Back Navigation).

---

## 🧭 4. Điều hướng ứng dụng di động (Mobile Navigation)
*   **Thanh điều hướng dưới cùng (Bottom Navigation Bar):** Chỉ đặt tối đa từ 3 đến 5 chức năng chính của ứng dụng ở thanh dưới cùng. Đây là vùng ngón tay cái dễ chạm tới nhất khi cầm điện thoại bằng một tay.
*   **Ngăn kéo điều hướng (Navigation Drawer/Hamburger Menu):** Dùng để chứa các chức năng cấu hình phụ, lịch sử hoặc thông tin tài khoản.
*   **Nút hành động nổi (Floating Action Button - FAB):** Đặt một nút tròn nổi ở góc dưới bên phải cho hành động quan trọng nhất của màn hình (ví dụ: nút "Tạo mới", nút "Gửi tin nhắn").
