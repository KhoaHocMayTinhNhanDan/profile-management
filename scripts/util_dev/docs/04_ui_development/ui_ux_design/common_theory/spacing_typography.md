# 📐 Spacing, Alignment, Proximity & Progressive Disclosure

Tài liệu này tích hợp các quy chuẩn vàng về căn chỉnh (Alignment), khoảng cách (Spacing/Proximity), bố cục lũy tiến (Progressive Disclosure) theo tiêu chuẩn thiết kế của **Figma** và khả năng tiếp cận người dùng (**WCAG 2.1 AA**).

---

## 1. Hệ thống Khoảng cách & Quy luật Kề cận (Spacing & Proximity)

Chúng ta sử dụng **Hệ số 8 (8pt Grid System)** để định hình mọi kích thước khoảng đệm (padding) và khoảng lề (margin). Để giao diện có cấu trúc thị giác rõ ràng, khoảng cách phải tuân thủ **Quy luật Kề cận (Gestalt Law of Proximity)**:

*   **Quy tắc chung**: Các phần tử đứng gần nhau được coi là có mối quan hệ chặt chẽ. Khoảng cách càng lớn thể hiện sự phân rã thông tin càng cao.
*   **Hệ thống phân cấp khoảng cách (Spacing Tokens)**:
    *   `4px` - `8px` (Micro Spacing): Dùng cho khoảng cách giữa Icon và Text trong nút bấm, hoặc giữa **Nhãn (Label)** và **Ô nhập liệu (Input)** tương ứng.
    *   `16px` - `24px` (Macro Spacing): Dùng làm khoảng cách giữa các trường dữ liệu (fields) trong cùng một Form, hoặc khoảng cách đệm (padding) bên trong một thẻ Card/Box.
    *   `32px` - `48px` (Section Spacing): Dùng làm khoảng cách giữa các khối nội dung lớn (Sections) trên trang hoặc giữa hai thẻ Card độc lập.

---

## 2. Hệ thống Kiểu chữ & Phân cấp Văn bản (Typography System)

Để đảm bảo thông tin dễ đọc (readability) và có phân cấp thị giác rõ ràng, hệ thống phông chữ phải tuân thủ nghiêm ngặt quy tắc sau:

*   **Phân cấp kích thước chữ (Font Size Scale)**:
    *   `H1 (Tiêu đề trang)`: 24px - 32px (bold/semibold) - dùng cho tiêu đề chính của màn hình.
    *   `H2 (Tiêu đề khối)`: 18px - 20px (semibold) - dùng cho tiêu đề các thẻ Card hoặc Section.
    *   `Body (Nội dung chính)`: 13px - 14px (regular) - dùng cho các nhãn, văn bản hiển thị thông tin chính.
    *   `Caption (Chú thích phụ)`: 11px - 12px (regular) - dùng cho mô tả phụ, nhãn thời gian hoặc thông điệp trợ giúp nhỏ.
*   **Khoảng cách dòng (Line Height)**:
    *   Luôn cấu hình `line-height` tối thiểu từ **1.2 đến 1.5** lần kích thước chữ. Tránh chữ bị dính sát nhau theo chiều dọc gây khó đọc.
*   **Độ đậm nhạt (Font Weight)**:
    *   Chỉ sử dụng tối đa 3 mức độ đậm nhạt trong một màn hình để tránh giao diện bị rối: `Regular (400)` cho văn bản thường, `Medium/Semibold (500/600)` cho các nhãn quan trọng/tiêu đề nhỏ, và `Bold (700)` cho các tiêu đề lớn hoặc nút bấm chính.

---

## 3. Quy chuẩn Căn lề Hành vi (Alignment)

Căn lề chuẩn xác giúp tạo ra các trục căn dọc vô hình (invisible grid lines), tăng tính thẩm mỹ và giảm thời gian quét thông tin (scan) của mắt người dùng:

*   **Văn bản & Nội dung đọc**: Luôn căn lề trái (**Left-aligned**) đối với các ngôn ngữ đọc từ trái qua phải (tiếng Việt, tiếng Anh). Tuyệt đối cấm căn đều hai bên (Justified) vì tạo ra khoảng trống "sông" (rivers of space) gây mỏi mắt.
*   **Số liệu & Tiền tệ**: Luôn căn lề phải (**Right-aligned**) đối với các cột số liệu, số lượng, hoặc số tiền trong các bảng (Table) để người dùng dễ dàng so sánh độ dài hàng đơn vị, hàng chục, hàng trăm theo chiều dọc.
*   **Các nút bấm hành động (Buttons)**:
    *   Trong các cửa sổ Modal/Dialog: Các nút bấm chính (CTA) và phụ nên được nhóm ở góc dưới cùng bên phải (chuẩn Windows/Web) hoặc căn giữa nếu là trang độc lập.
    *   Nút bấm chính (Primary) luôn nằm ở vị trí dễ tiếp cận nhất theo luồng đọc (bên phải ngoài cùng trong cụm nút ngang).

---

## 4. Tiết lộ Thông tin Lũy tiến (Progressive Disclosure)

Để ngăn chặn hiện tượng quá tải nhận thức (Cognitive Overload), giao diện chỉ hiển thị những thông tin tối thiểu cần thiết để người dùng hoàn thành tác vụ hiện tại, ẩn đi các chi tiết nâng cao:

*   **Ẩn/Hiện thông minh**:
    *   Sử dụng *Advanced Settings* (Thiết lập nâng cao) hoặc các khối *Accordion* có thể thu gọn/mở rộng để ẩn các cấu hình ít khi sử dụng.
    *   Sử dụng *Dropdown menu* (`...` hoặc More) để ẩn các hành động phụ (ví dụ: Xóa, Sao chép, Tải về) của một hàng trong bảng.
*   **Luồng chia nhỏ (Multi-step flow)**: Đối với các form nhập liệu phức tạp có trên 7 trường thông tin, bắt buộc phải chia thành các bước tuần tự (Wizard Flow) hoặc sử dụng các Tab chức năng phân loại thay vì đổ tất cả lên một màn hình cuộn dọc dài.

---

## 5. Quy chuẩn Khả năng Tiếp cận (Accessibility - WCAG 2.1 AA)

*   **Độ tương phản màu sắc (Contrast Ratio)**:
    *   *Chữ thông thường (Normal Text)*: Độ tương phản giữa chữ và nền bắt buộc đạt tối thiểu **4.5:1** (cấm dùng chữ xám mờ trên nền đen hoặc trắng).
    *   *Chữ lớn (Large Text, từ 18pt trở lên)*: Độ tương phản đạt tối thiểu **3:1**.
    *   *Đường viền & Icon tương tác (Borders/Graphical Objects)*: Các đường viền của ô nhập liệu (input borders), icon tương tác so với màu nền xung quanh phải đạt tối thiểu **3:1** để đảm bảo người dùng nhận diện được vùng nhập liệu.
*   **Nguyên tắc Phi màu sắc (Non-color dependency)**:
    *   Tuyệt đối không dùng độc nhất màu sắc để truyền tải thông thái. Mọi thông báo lỗi (Error), thành công (Success) hay cảnh báo (Warning) bắt buộc phải đi kèm biểu tượng (Icon) hoặc văn bản mô tả cụ thể (ví dụ: đi kèm icon dấu `[x]` hoặc chữ `[Lỗi]`), giúp người dùng bị mù màu vẫn hiểu được thông tin.
    *   Mỗi hệ Theme (Dark Mode / Light Mode) phải được xây dựng trên một bảng màu Palette độc lập được kiểm thử tương phản riêng biệt, tránh việc tự động đảo ngược màu (Color Inversion) cơ học.

