# 🎨 Quy chuẩn Thiết kế UI/UX Chung (General UI/UX Guidelines)

Tài liệu này tổng hợp tinh hoa từ các tiêu chuẩn thiết kế hàng đầu thế giới bao gồm **Nielsen Norman Group (NN/g)**, **Google Material Design 3**, và **Apple Human Interface Guidelines** nhằm xây dựng một hệ thống giao diện nhất quán, trực quan và lấy người dùng làm trung tâm.

---

## 🏛️ 1. 10 Nguyên lý Tiện dụng Kinh điển (Nielsen Norman 10 Usability Heuristics)

Mọi giao diện trong hệ thống bắt buộc phải tuân thủ 10 quy tắc vàng này:

1.  **Trạng thái hệ thống luôn rõ ràng (Visibility of system status):** Hệ thống phải luôn phản hồi cho người dùng biết chuyện gì đang xảy ra bằng các thông báo hoặc loading indicators thích hợp trong thời gian thực.
2.  **Khớp nối thế thực (Match between system and the real world):** Sử dụng ngôn từ, biểu tượng quen thuộc với cuộc sống hàng ngày thay vì các thuật ngữ lập trình chuyên ngành phức tạp.
3.  **Quyền kiểm soát của người dùng (User control and freedom):** Luôn cung cấp lối thoát an toàn khi người dùng bấm nhầm (nút "Hủy bỏ", "Hoàn tác - Undo", "Quay lại").
4.  **Nhất quán và Tiêu chuẩn (Consistency and standards):** Sử dụng đồng bộ nút bấm, biểu tượng, thuật ngữ trên tất cả các màn hình (không dùng "Delete" ở trang này và "Remove" ở trang khác).
5.  **Phòng tránh lỗi (Error prevention):** Thiết kế giao diện để người dùng không thể nhập sai (ví dụ: vô hiệu hóa nút submit nếu form chưa hợp lệ, chọn ngày qua bộ chọn thay vì gõ tay).
6.  **Nhận diện thay vì ghi nhớ (Recognition rather than recall):** Giảm tải bộ nhớ cho người dùng bằng cách hiển thị các tùy chọn trực quan thay vì bắt họ phải nhớ thông tin từ các bước trước.
7.  **Linh hoạt và hiệu quả (Flexibility and efficiency of use):** Thiết kế giao diện đơn giản cho người mới, nhưng cung cấp phím tắt nhanh (Shortcuts), macro xử lý cho người dùng chuyên nghiệp.
8.  **Thẩm mỹ tối giản (Aesthetic and minimalist design):** Loại bỏ các thông tin rác, màu sắc lòe loẹt không cần thiết. Tập trung không gian hiển thị cho nội dung cốt lõi của tác vụ.
9.  **Giúp người dùng nhận biết, chẩn đoán và sửa lỗi (Help users recognize, diagnose, and recover from errors):** Các thông báo lỗi phải viết bằng ngôn ngữ con người, chỉ rõ nguyên nhân và hướng dẫn cụ thể cách sửa, tránh hiển thị mã lỗi thô (ví dụ: *Exception Code 500*).
10. **Trợ giúp và tài liệu (Help and documentation):** Cung cấp các tooltip hướng dẫn ngắn tại chỗ hoặc mục trợ giúp dễ tìm khi người dùng gặp khó khăn.

---

## 🧬 2. Phân Cấp Thiết Kế Hệ Thống (Atomic Design System)

Mọi thành phần giao diện trong tầng Infrastructure UI (`layer_04_infrastructure/ui/`) phải được phân loại và sắp xếp nghiêm ngặt theo mô hình Atomic:

```
[Atoms] ──> [Molecules] ──> [Organisms] ──> [Templates] ──> [Pages]
```

### A. Level 01: Atoms (Nguyên tử - Phần tử cơ bản nhất)
*   **Đặc điểm:** Không thể chia nhỏ hơn mà vẫn giữ nguyên ý nghĩa UI.
*   **Thành phần:** Nút bấm (`Button`), Nhãn (`Label/Text`), Hộp nhập liệu (`TextInput/TextField`), Biểu tượng (`Icon`), Thanh tiến trình (`ProgressBar`), Công tắc (`Switch/Checkbox/RadioButton`).
*   **Quy định:** Không chứa logic nghiệp vụ. Chỉ nhận cấu hình style (color, font, size) và sự kiện click thô.

### B. Level 02: Molecules (Phân tử - Tổ hợp đơn giản)
*   **Đặc điểm:** Kết hợp từ 2 hoặc nhiều Atoms để tạo ra một thành phần có chức năng cụ thể.
*   **Thành phần:** Cụm nhập liệu (`Form Field` = Label + TextInput + ErrorText), Hộp thoại thông báo (`MessageBox` = Label + Button), Thanh tìm kiếm (`SearchBar` = TextInput + Icon).
*   **Quy định:** Có thể chứa logic kiểm tra dữ liệu đầu vào thô (Validation).

### C. Level 03: Organisms (Thực thể phức tạp - Khối chức năng tự vận hành)
*   **Đặc điểm:** Tổ hợp các Molecules và Atoms để tạo thành một khu vực giao diện hoàn chỉnh, có thể tái sử dụng độc lập.
*   **Thành phần:** Thanh điều hướng (`Sidebar/NavigationBar`), Bảng dữ liệu (`DataTable` = Table Headers + Rows + Pagination), Khung biểu đồ (`ChartCard`).
*   **Quy định:** Có thể kết nối trực tiếp với Custom Hook để tự lấy và hiển thị dữ liệu của chính nó.

### D. Level 04: Templates (Khung bố cục)
*   **Đặc điểm:** Định nghĩa bộ khung layout của màn hình (hệ thống Grid, vị trí của Sidebar, Header, Content Area).
*   **Thành phần:** `MainLayoutTemplate` (Sidebar bên trái, Content bên phải), `SplitScreenTemplate` (Chia đôi màn hình trái/phải).
*   **Quy định:** Chỉ chứa layout trống, không chứa dữ liệu thật.

### E. Level 05: Pages (Trang màn hình hoàn chỉnh)
*   **Đặc điểm:** Là thực thể cuối cùng người dùng nhìn thấy, lắp ráp các Organisms và Molecules vào các ô trống của Template.
*   **Thành phần:** `DashboardPage`, `SettingsPage`, `UserProfilePage`.
*   **Quy định:** Quản lý vòng đời khởi tạo của Custom Hook, phân phối callback từ Hook xuống các Organisms con.

---

## 🎨 3. Quy chuẩn Theme & Thiết kế Màu sắc (Design Tokens)

Màu sắc trong toàn bộ hệ thống phải được định nghĩa dưới dạng **Design Tokens** (vai trò ngữ nghĩa) thay vì sử dụng mã màu HEX trực tiếp, cho phép ứng dụng dễ dàng thay đổi bộ nhận diện thương hiệu (Brand Palette) và đồng bộ trạng thái Dark/Light Mode:

| Token màu | Bản chất ở Light Mode | Bản chất ở Dark Mode | Trách nhiệm áp dụng |
| :--- | :--- | :--- | :--- |
| **`Primary`** | Tông màu thương hiệu chủ đạo (độ tương phản cao) | Tông màu thương hiệu chủ đạo (sáng hơn, bớt bão hòa) | Nút bấm chính, trạng thái active, viền focus |
| **`OnPrimary`** | Tông màu tương phản cao với nền Primary | Tông màu tương phản cao với nền Primary | Màu chữ hoặc biểu tượng nằm TRÊN nền Primary |
| **`Secondary`** | Tông màu phụ để phân nhóm thông tin | Tông màu phụ (sáng nhẹ) | Nút phụ, thẻ phân loại, viền phân cách nhẹ |
| **`Background`** | Tông màu nền sáng chủ đạo | Tông màu nền tối (cấm dùng đen tuyền `#000` để giảm mỏi mắt) | Nền của toàn bộ cửa sổ ứng dụng |
| **`Surface`** | Tông màu nền của các khối nội dung | Tông màu nền của các khối nội dung (sáng hơn nền Background) | Nền của thẻ Card, bảng dữ liệu, hộp thoại |
| **`OnSurface`** | Tông màu tối có độ tương phản cao với Surface | Tông màu sáng có độ tương phản cao với Surface | Màu chữ hiển thị chính của nội dung văn bản |
| **`Error`** | Tông màu đỏ/cam có độ tương phản cao | Tông màu đỏ/cam sáng | Màu cảnh báo lỗi, nút hành động nguy hiểm |

---

## 🌐 4. Quy chuẩn Quốc tế hóa (i18n - Internationalization)

Để ứng dụng sẵn sàng chạy đa ngôn ngữ (tiếng Việt, tiếng Anh, v.v.), lập trình viên phải tuân thủ:

*   **Không hard-code chuỗi ký tự hiển thị:** Cấm viết text hiển thị trực tiếp lên UI (Ví dụ: `self.button.setText("Lưu lại")` $\rightarrow$ **VI PHẠM**). Bắt buộc phải gọi qua Service ngôn ngữ: `self.button.setText(self.i18n.get("btn_save"))`.
*   **Thiết kế Layout co giãn (Flexible Text Wrapping):**
    *   Độ dài của cùng một từ ở các ngôn ngữ khác nhau có thể chênh lệch đến **30% - 40%** (ví dụ: tiếng Đức dài hơn tiếng Anh).
    *   Mọi nhãn hiển thị text (`Label`) phải cấu hình tự động xuống dòng (`word-wrap / multiline`) và các layout phải co giãn tự động theo kích thước chữ, tránh việc text bị cắt cụt (`...`) hoặc tràn khung.
*   **Định dạng chuẩn địa phương (Locale Formatting):**
    *   *Tiền tệ:* Định dạng đúng ký hiệu (ví dụ: `1.000.000 ₫` tại VN, `$1,000,000` tại Mỹ).
    *   *Thời gian:* Sử dụng hệ thống định dạng ngày tháng theo Locale (ví dụ: `DD/MM/YYYY` hoặc `YYYY-MM-DD`).

---

## Spacing & Typography Rules (Xem chi tiết)
*   **Hệ số 8 (8pt Grid System):** Mọi kích thước padding, margin phải là bội số của 8 (8px, 16px, 24px) để tạo sự cân đối thị giác tự nhiên.
*   **Độ tương phản (Contrast Ratio):** Độ tương phản chữ/nền luôn đạt tối thiểu **4.5:1** (tiêu chuẩn WCAG AA).
