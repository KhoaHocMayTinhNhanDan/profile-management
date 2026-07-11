# 📐 Spacing, Typography & Accessibility Rules

*   **Hệ số 8 (8pt Grid System):** Mọi kích thước padding, margin phải là bội số của 8 (8px, 16px, 24px) để tạo sự cân đối thị giác tự nhiên.
*   **Độ tương phản (Contrast Ratio - Chuẩn WCAG 2.1 AA):**
    *   *Chữ thông thường (Normal Text):* Độ tương phản giữa chữ và nền bắt buộc đạt tối thiểu **4.5:1** (ví dụ: cấm dùng chữ xám mờ trên nền đen).
    *   *Chữ lớn (Large Text, từ 18pt trở lên):* Độ tương phản đạt tối thiểu **3:1**.
    *   *Đường viền & Icon tương tác (Borders/Graphical Objects):* Các đường viền của ô nhập liệu (input borders), icon tương tác so với màu nền xung quanh phải đạt tối thiểu **3:1** để đảm bảo người dùng nhận diện được vùng nhập liệu.
*   **Không phụ thuộc duy nhất vào màu sắc để truyền tải thông tin (Color Accessibility):**
    *   Tuyệt đối không được dùng duy nhất màu sắc để thông báo trạng thái. Mọi thông báo lỗi (Error), thành công (Success) hay cảnh báo (Warning) bắt buộc phải đi kèm biểu tượng (Icon) hoặc văn bản mô tả cụ thể (ví dụ: đi kèm icon dấu `[x]` hoặc chữ `[Lỗi]`), giúp người dùng bị mù màu vẫn hiểu được thông tin.
    *   Mỗi hệ Theme (Dark Mode / Light Mode) phải được xây dựng trên một bảng màu Palette độc lập được kiểm thử tương phản riêng biệt, tránh việc tự động đảo ngược màu (Color Inversion) cơ học.
