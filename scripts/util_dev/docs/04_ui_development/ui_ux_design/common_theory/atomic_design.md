# 🧬 2. Phân Cấp Thiết Kế Hệ Thống (Atomic Design System)

> [!IMPORTANT]
> **QUY TẮC THÉP CHO AI & DEVELOPER (CẤM VI PHẠM):**
> 1. **CẤM TUYỆT ĐỐI** import hoặc sử dụng bất kỳ Custom Hook nghiệp vụ, Controller, hay gọi API/Database trực tiếp bên trong các component từ **Level 1 (Atoms) đến Level 4 (Templates)**.
> 2. **CHỈ CÓ THỂ** sử dụng Custom Hooks, gọi logic nghiệp vụ hoặc đăng ký callback tại **Level 5 (Pages)**.
> 3. Mọi component ở Level 1, 2, 3 phải hoạt động theo cơ chế **Pure UI / Stateless** (chỉ nhận props từ trên xuống và đẩy signal/event ra ngoài).

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
*   **Quy định:** Không tự ý khởi tạo hoặc kết nối trực tiếp với Custom Hook nghiệp vụ để đảm bảo tính tái sử dụng cao nhất. Organisms chỉ nhận dữ liệu được truyền trực tiếp từ Page (Level 5) hoặc tương tác với các UI Services (Theme, i18n, Navigation).

### D. Level 04: Templates (Khung bố cục)
*   **Đặc điểm:** Định nghĩa bộ khung layout của màn hình (hệ thống Grid, vị trí của Sidebar, Header, Content Area).
*   **Thành phần:** `MainLayoutTemplate` (Sidebar bên trái, Content bên phải), `SplitScreenTemplate` (Chia đôi màn hình trái/phải).
*   **Quy định:** Chỉ chứa layout trống, không chứa dữ liệu thật.

### E. Level 05: Pages (Trang màn hình hoàn chỉnh)
*   **Đặc điểm:** Là thực thể cuối cùng người dùng nhìn thấy, lắp ráp các Organisms và Molecules vào các ô trống của Template.
*   **Thành phần:** `DashboardPage`, `SettingsPage`, `UserProfilePage`.
*   **Quy định:** Đây là nơi duy nhất quản lý vòng đời khởi tạo của Custom Hook, phân phối luồng dữ liệu sạch và các callbacks từ Hook xuống các Organisms con.

---

## 🎨 Quy chuẩn tổ chức File và Stylesheet (Component Colocation)

Để đảm bảo khả năng tái sử dụng, dễ bảo trì và mở rộng, toàn bộ các component thuộc từ **Level 1 (Atoms) đến Level 4 (Templates)** phải được thiết kế theo cấu trúc **Component Colocation**:

1. **Một thư mục riêng cho mỗi component**: Mỗi Atom, Molecule, Organism, hay Template cụ thể phải nằm trong một thư mục con riêng biệt đặt tên theo snake_case của thành phần đó.
2. **Đặt file style ngay cạnh file code logic**:
   - File code (ví dụ: `buttons.py`, `sidebar.py`) và file stylesheet tương ứng (ví dụ: `buttons.qss`, `sidebar.qss`) bắt buộc phải nằm chung trong cùng thư mục của component đó.
   - Tránh tuyệt đối việc nhét code CSS/QSS inline vào file Python hoặc gom tất cả vào một file stylesheet dùng chung khổng lồ.
3. **Sử dụng tệp `__init__.py` để facade**:
   - Ở cấp thư mục component (ví dụ `buttons/`): Dùng `__init__.py` để export các class bên trong ra ngoài.
   - Ở cấp thư mục Level (ví dụ `level_01_atoms/`): Dùng `__init__.py` để expose toàn bộ các component con, giúp các tầng khác khi import chỉ cần chỉ định đến thư mục Level mà không cần import sâu vào từng folder vật lý con.
   
*Ví dụ cấu trúc chuẩn:*
```text
level_01_atoms/
├── __init__.py                # from .buttons import PrimaryButton...
└── buttons/
    ├── __init__.py            # from .buttons import PrimaryButton
    ├── buttons.py             # Logic của widget
    └── buttons.qss            # Stylesheet của widget sử dụng biến màu {ACCENT_COLOR}...
```

