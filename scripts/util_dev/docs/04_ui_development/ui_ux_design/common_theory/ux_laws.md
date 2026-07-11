# 🧠 Các Quy Luật Tâm Lý Học Hành Vi Trong Thiết Kế UI/UX (Laws of UX)

Để xây dựng giao diện trực quan, thân thiện và giảm thiểu tối đa thời gian học cách sử dụng của người dùng, toàn bộ thiết kế giao diện phải tuân thủ nghiêm ngặt các quy luật tâm lý kinh điển sau:

---

## 1. Luật Jakob (Jakob's Law) - Sự quen thuộc
*   **Nguyên lý:** Người dùng dành phần nhóm thời gian của họ để sử dụng các ứng dụng khác. Do đó, họ mong muốn ứng dụng của bạn hoạt động giống hệt các ứng dụng quen thuộc mà họ đã biết.
*   **Ứng dụng:**
    *   Sử dụng các mẫu thiết kế (Design Patterns) tiêu chuẩn: Thanh menu nằm ở góc trên/trái, nút đóng (X) nằm ở góc phải trên (Windows) hoặc trái trên (macOS).
    *   Biểu tượng (Icons) phải có tính phổ quát toàn cầu (Ví dụ: 🔍 cho Tìm kiếm, ⚙️ cho Cấu hình, 🗑️ cho Thùng rác). Tránh tự sáng chế ra các biểu tượng kỳ dị gây khó hiểu.

---

## 2. Luật Fitts (Fitts's Law) - Kích thước & Khoảng cách
*   **Nguyên lý:** Thời gian để người dùng di chuyển chuột/tay chạm vào một mục tiêu phụ thuộc vào **khoảng cách** di chuyển và **kích thước** của mục tiêu đó.
*   **Ứng dụng:**
    *   Làm cho các Call-to-Action (CTA) chính có kích thước lớn và rõ ràng (Ví dụ: Nút "Thanh toán", "Xác nhận" phải có padding tối thiểu 12px - 16px).
    *   Đặt các nút hành động liên quan gần nhau để giảm quãng đường di chuyển của con trỏ chuột.
    *   **Vùng chạm (Target Area):** Đảm bảo vùng click xung quanh các nút nhỏ (như icon button) đủ rộng để người dùng không bị click trượt.

---

## 3. Luật Hick (Hick's Law) - Đơn giản hóa lựa chọn
*   **Nguyên lý:** Thời gian người dùng đưa ra quyết định sẽ tăng lên tỷ lệ thuận với số lượng và độ phức tạp của các lựa chọn trên màn hình.
*   **Ứng dụng:**
    *   **Phân rã luồng phức tạp (Chunking):** Chia nhỏ các form nhập liệu quá dài thành các bước tuần tự (Wizard Flow / Multi-step Form).
    *   Ẩn bớt các chức năng phụ ít dùng dưới các menu thả xuống (Dropdown/More Options).
    *   Tránh hiển thị quá 5 lựa chọn hành động có độ ưu tiên ngang nhau trên cùng một vùng giao diện.

---

## 4. Luật Miller (Miller's Law) - Giới hạn bộ nhớ ngắn hạn
*   **Nguyên lý:** Một người bình thường chỉ có thể lưu giữ tối đa $7 \\pm 2$ thông tin trong bộ nhớ ngắn hạn cùng một lúc.
*   **Ứng dụng:**
    *   Nhóm các phần tử thông tin liên quan thành từng khối riêng biệt (ví dụ: nhóm thông tin cá nhân, nhóm thông tin thẻ thanh toán).
    *   Giới hạn số lượng mục trên thanh menu điều hướng (`Sidebar`) tối đa từ 5 đến 7 mục để người dùng không bị quá tải thông tin.

---

## 5. Ngưỡng Doherty (Doherty Threshold) - Tốc độ phản hồi
*   **Nguyên lý:** Trải nghiệm tương tác giữa người dùng và máy tính sẽ đạt hiệu suất tối đa khi phản hồi xuất hiện trong vòng **dưới 400 mili-giây (ms)**.
*   **Ứng dụng:**
    *   **Trạng thái Chờ (Loading States):** Nếu một tác vụ (gọi API, truy vấn DB) tốn hơn 400ms để hoàn thành, giao diện **bắt buộc phải hiển thị ngay lập tức** hiệu ứng chờ (Spinner, Progress Bar, hoặc Skeleton Screen) để người dùng biết hệ thống đang hoạt động và không bấm nút lặp lại.
    *   Sử dụng hiệu ứng chuyển trang mượt mà (Transitions) để giả lập cảm giác phản hồi tức thì.

---

## 6. Hiệu ứng Cô lập (Von Restorff Effect) - Tiêu điểm chú ý
*   **Nguyên lý:** Trong nhiều đối tượng tương tự nhau, đối tượng nào có sự khác biệt rõ rệt nhất về mặt thị giác sẽ được chú ý và ghi nhớ lâu nhất.
*   **Ứng dụng:**
    *   Thiết kế nút hành động chính (Primary CTA) có màu sắc nổi bật (Primary Color) hoàn toàn so với các nút hành động phụ (Secondary CTA - sử dụng màu trung tính hoặc chỉ có viền outline).
    *   Sử dụng màu cảnh báo (`Error Color`) cho các hành động nguy hiểm (như "Xóa tài khoản") để cảnh báo người dùng.
