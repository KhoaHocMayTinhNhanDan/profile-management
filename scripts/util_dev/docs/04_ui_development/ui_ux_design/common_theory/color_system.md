# 🎨 3. Quy chuẩn Theme & Thiết kế Màu sắc (Design Tokens)

Màu sắc trong toàn bộ hệ thống phải được định nghĩa dưới dạng **Design Tokens** (vai trò ngữ nghĩa) thay vì sử dụng mã màu HEX trực tiếp, cho phép ứng dụng dễ dàng thay đổi bộ nhận diện thương hiệu (Brand Palette) và đồng bộ trạng thái Dark/Light Mode.

### ⚖️ Quy tắc Phân bổ và Nhất quán Màu sắc (Quy tắc 60-30-10)

Để giao diện cân bằng thị giác, nhất quán và không bị rối mắt, màu sắc trên bất kỳ màn hình nào cũng phải được phân bổ theo tỷ lệ vàng sau:

*   **60% Màu chủ đạo (Nền - Background):** Chiếm diện tích lớn nhất, sử dụng các tông màu trung tính (như xanh đen tối `#121212` cho Dark Mode). Thiết lập không gian thư giãn cho mắt.
*   **30% Màu bổ trợ (Cấu trúc - Surface/Secondary):** Sử dụng các tông màu sáng hơn nền một chút để dựng khung cấu trúc (như `Sidebar`, các thẻ `Card`, bảng phân chia thông tin).
*   **10% Màu nhấn (Accent - Primary/Error):** Tông màu nổi bật nhất của thương hiệu, **chỉ dùng hạn chế** cho các nút bấm hành động chính (CTA), tiêu điểm tập trung, hoặc cảnh báo quan trọng. Tránh việc tô màu nhấn lan man gây loãng giao diện.

| Token màu | Bản chất ở Light Mode | Bản chất ở Dark Mode | Trách nhiệm áp dụng |
| :--- | :--- | :--- | :--- |
| **`Primary`** | Tông màu thương hiệu chủ đạo (độ tương phản cao) | Tông màu thương hiệu chủ đạo (sáng hơn, bớt bão hòa) | Nút bấm chính, trạng thái active, viền focus |
| **`OnPrimary`** | Tông màu tương phản cao với nền Primary | Tông màu tương phản cao với nền Primary | Màu chữ hoặc biểu tượng nằm TRÊN nền Primary |
| **`Secondary`** | Tông màu phụ để phân nhóm thông tin | Tông màu phụ (sáng nhẹ) | Nút phụ, thẻ phân loại, viền phân cách nhẹ |
| **`Background`** | Tông màu nền sáng chủ đạo | Tông màu nền tối (cấm dùng đen tuyền `#000000` - do gây lóa chữ/Halation Effect và triệt tiêu khả năng hiển thị chiều sâu z-axis) | Nền của toàn bộ cửa sổ ứng dụng |
| **`Surface`** | Tông màu nền của các khối nội dung | Tông màu nền của các khối nội dung (sáng hơn nền Background) | Nền của thẻ Card, bảng dữ liệu, hộp thoại |
| **`OnSurface`** | Tông màu tối có độ tương phản cao với Surface | Tông màu sáng có độ tương phản cao với Surface | Màu chữ hiển thị chính của nội dung văn bản |
| **`OnSurfaceVariant`** | Tông màu trung tính (ví dụ: xám vừa) | Tông màu trung tính (ví dụ: xám sáng dịu) | Chữ phụ, placeholder, icon trang trí, helper text |
| **`Error`** | Tông màu đỏ/cam có độ tương phản cao | Tông màu đỏ/cam sáng | Màu cảnh báo lỗi, nút hành động nguy hiểm |

### ⚡ Quy tắc Trạng thái Tương tác (State Tokens - Chuẩn Material Design 3)

Để giao diện sống động và phản hồi chính xác hành động của người dùng, các thành phần tương tác (nút bấm, ô nhập liệu, menu) phải thay đổi màu sắc theo các trạng thái sau:

*   **Trạng thái Bình thường (Enabled):** Sử dụng các token màu gốc ở bảng trên.
*   **Trạng thái Di chuột (Hover):** Phủ một lớp overlay có độ mờ **8% opacity** sử dụng tông màu của chữ/icon (On-color) lên trên màu nền gốc của component (ví dụ: Hover lên nút Primary màu xanh chữ trắng sẽ phủ thêm 8% màu trắng để nút sáng hơn).
*   **Trạng thái Nhấn chuột (Pressed/Active):** Phủ một lớp overlay có độ mờ **12% opacity** sử dụng tông màu chữ/icon lên trên màu nền gốc.
*   **Trạng thái Vô hiệu hóa (Disabled):** 
    *   *Nội dung (Chữ, Icon):* Thiết lập độ mờ về **38% opacity** so với màu gốc.
    *   *Khung nền (Container):* Thiết lập độ mờ về **12% opacity** (hoặc sử dụng màu xám mờ đồng bộ).
    *   *Hành vi:* Vô hiệu hóa hoàn toàn tương tác chuột, không kích hoạt trạng thái hover hay focus.

### 📐 Quy tắc Độ cao Bề mặt (Surface Elevation - Đặc biệt quan trọng với Dark Mode)

Trong giao diện tối (Dark Mode), bóng đổ (Shadows) rất khó nhìn thấy bằng mắt thường. Do đó, để thể hiện cấu trúc phân lớp chồng đè và chiều sâu không gian (z-axis), hệ thống quy định nguyên lý **Độ sáng theo độ cao (Tonal Lightness)**:

*   **Nguyên tắc xếp lớp:** Bề mặt nào có độ cao z-axis lớn hơn (nổi gần mắt người dùng hơn) thì bắt buộc phải có **màu nền sáng hơn** (Lighter tone).
*   **Hệ thống phân cấp 3 lớp nền mặc định:**
    1.  **Lớp 0 (Tối nhất):** `Background` - Màu nền chính của toàn bộ cửa sổ ứng dụng (ví dụ: xanh đen thẫm hoặc xám đen tối `#121212`).
    2.  **Lớp 1 (Sáng vừa):** `Surface (Level 1)` - Nền của các khu vực chứa nội dung như thẻ Card, bảng dữ liệu, vùng danh sách (màu nền sáng hơn Background từ 3% - 5%).
    3.  **Lớp 2 (Sáng nhất):** `Surface (Level 2)` - Nền của các cửa sổ pop-up, menu thả xuống (dropdown), hộp thoại Modal, hoặc tooltip (màu nền sáng hơn Surface Level 1).
*   **Tránh dùng hiệu ứng phát sáng (Light Glows)** để thay thế cho bóng đổ, hãy luôn dùng sự chuyển đổi tông màu nền sáng/tối để biểu diễn độ cao.

### 🎨 Quy tắc Nhất quán Họ màu (Color Family Consistency)

Màu sắc trên giao diện phải tạo cảm giác đồng đều, liền mạch và chuyên nghiệp:

*   **Không trộn lẫn các họ màu không liên quan:** Toàn bộ hệ màu trung tính (`Background`, `Surface`, `Secondary`) phải có cùng một gốc pha màu (Color Family). 
    *   *Ví dụ:* Nếu nền chính `Background` là màu xám đen pha ánh xanh dương (cool gray), các thẻ `Card` hoặc `Sidebar` bắt buộc phải là xám-xanh dương sáng hơn. Tuyệt đối không được trộn một thẻ Card màu xám pha ánh vàng (warm gray) lên trên nền cool gray.
*   **Đồng bộ thành phần có cùng độ ưu tiên:** Các nút bấm, nhãn trạng thái hoặc biểu tượng có cùng ý nghĩa nghiệp vụ (như nút "Lưu/Xác nhận") phải sử dụng chung **một mã màu Primary duy nhất** trên mọi màn hình của toàn bộ hệ thống.
