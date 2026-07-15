# Hướng dẫn Phát triển UI & Kiến trúc Hooks Đa Nền Tảng

Tài liệu này hướng dẫn chi tiết cách phát triển giao diện người dùng (UI) và tổ chức mã nguồn tầng hiển thị (Presentation/Infrastructure UI) theo mô hình **Atomic Design** kết hợp mẫu kiến trúc **Custom Hooks** tổng quát hóa cho mọi nền tảng (Desktop PyQt6/Tauri, Mobile Kivy/Flutter/React Native/Jetpack Compose, Web Frontend).

---

## 1. Cấu trúc Thư mục UI tổng quát (`layer_04_infrastructure/ui/`)

Mã nguồn UI của bất kỳ nền tảng nào đều được tổ chức phân cấp đồng bộ theo mô hình **Component Colocation** (đặt mã nguồn logic và style thiết kế giao diện trong cùng một thư mục thành phần để dễ bảo trì):

```text
desktop_qt6/ (hoặc web_fastapi, desktop_tauri, mobile_kivy, mobile_flutter, mobile_react_native, mobile_jetpack_compose)
│
├── level_01_atoms/        # Phần tử cơ bản nhỏ nhất (nhóm theo thư mục)
│   ├── __init__.py        # File facade để import nhanh gọn
│   ├── buttons/
│   │   ├── __init__.py
│   │   ├── buttons.py     # Code logic Python
│   │   └── buttons.qss    # File stylesheet riêng của buttons
│   └── ...
│
├── level_02_molecules/    # Tổ hợp các atoms đơn giản
│   └── ui_inspector/
│       ├── __init__.py
│       ├── ui_inspector.py
│       └── ui_inspector.qss
│
├── level_03_organisms/    # Khối giao diện phức tạp tự hoàn thiện
│   └── sidebar/
│       ├── __init__.py
│       ├── sidebar.py
│       └── sidebar.qss
│
├── level_04_templates/    # Bộ khung layout bố cục chung của trang
│   └── page_template/
│       ├── __init__.py
│       ├── page_template.py
│       └── page_template.qss
│
├── level_05_pages/        # Các trang màn hình cụ thể ghép từ các component trên
│
├── hooks/                 # Custom Hooks: Nơi quản lý State, Timers, và các luồng tác vụ bất đồng bộ
├── services/              # UI Services: Hệ quản trị Theme, Đa ngôn ngữ (i18n), Định tuyến (Navigation)
└── assets/                # Static Resources: Hình ảnh (images), biểu tượng (icons), phông chữ (fonts)
```

### Định nghĩa & Ranh giới trách nhiệm của 5 tầng UI (Atomic Design)
Để đảm bảo tính tái sử dụng và sạch sẽ, AI và lập trình viên phải tuân thủ nghiêm ngặt ranh giới của từng cấp độ:

1. **Level 1: Atoms (Nguyên tử)**
   * *Định nghĩa:* Các thành phần cơ bản không thể chia nhỏ hơn (ví dụ: Custom Button, Custom Label, Custom Input).
   * *Ranh giới:* **Tuyệt đối không chứa logic nghiệp vụ, không import Custom Hook, Controller hay Services.** Chỉ nhận dữ liệu thô (string, int, bool) qua tham số và phát tín hiệu (emit signals/events) cơ bản khi có tương tác.
2. **Level 2: Molecules (Phân tử)**
   * *Định nghĩa:* Ghép từ nhiều Atoms để thực hiện một vai trò đơn giản (ví dụ: `FormField` gồm Label + Input + ErrorLabel).
   * *Ranh giới:* Có thể chứa logic kiểm tra định dạng giao diện thô (như báo đỏ khi trống), nhưng **vẫn không được phép chứa logic nghiệp vụ hoặc gọi Hook/Controller**.
3. **Level 3: Organisms (Cơ quan)**
   * *Định nghĩa:* Khối giao diện tự hoàn thiện phức tạp lắp ghép từ Atoms và Molecules (ví dụ: `Sidebar` menu, `TaskTable` hiển thị danh sách).
   * *Ranh giới:* Có thể tương tác với các UI Services (như đổi ngôn ngữ i18n, chuyển trang Navigation, đổi Theme) và nhận các data objects phức tạp, nhưng không quản lý trạng thái nghiệp vụ dài hạn.
4. **Level 4: Templates (Bố cục)**
   * *Định nghĩa:* Khung layout phân chia bố cục rỗng (ví dụ: Layout 2 cột Header + Sidebar).
   * *Ranh giới:* Chỉ định nghĩa vị trí hiển thị (layouts) và các khe cắm (slots/layout widgets), không chứa logic hoặc dữ liệu thật.
5. **Level 5: Pages (Trang)**
   * *Định nghĩa:* Điểm lắp ráp hoàn chỉnh (Đưa các Organisms/Molecules vào cắm vào Template).
   * *Ranh giới:* **Đây là nơi duy nhất được phép khởi tạo Custom Hook, đăng ký lắng nghe (subscribe) tín hiệu từ Hook, và gọi Controller để kích hoạt logic nghiệp vụ.**

---

## 2. Nguyên tắc Ranh giới Clean Architecture

* **Tầng 3 (Interface Adapters / Presenters)**: Tuyệt đối không chứa bất kỳ import hoặc tham chiếu nào liên quan đến thư viện đồ họa của nền tảng (như PyQt6, Kivy, Web DOM/HTML). Các lớp Presenter được sinh tự động và chỉ đóng vai trò định dạng dữ liệu thuần Python.
* **Tầng 4 (Infrastructure / UI Hooks & Views)**: Là nơi duy nhất được import thư viện đồ họa GUI.
* **Tách biệt logic hiển thị và logic dữ liệu**: Các trang giao diện (`level_05_pages/`) chỉ làm nhiệm vụ vẽ giao diện, tuyệt đối không được tự khởi tạo luồng chạy nền, bộ hẹn giờ hoặc thực hiện truy vấn cơ sở dữ liệu / API trực tiếp.
* **Nhất quán Styling (Theme Consistency)**: 
  - Tuyệt đối không viết cứng (hardcode) mã màu sắc, kích thước phông chữ cục bộ bằng code Python/JS bên trong các Component UI con.
  - Tất cả các phần tử đồ họa phải áp dụng phong cách động bằng cách kế thừa thông qua hệ quản trị Theme chung của dự án (`base.qss` cho Desktop, các CSS Class cho Web).
  - **Cơ chế nạp stylesheet tự động (Colocated QSS Loader)**: Hệ thống `ThemeManager` sẽ tự động quét đệ quy (recursive scan) toàn bộ các tệp `.qss` đặt cạnh các UI components (từ Level 1 đến Level 4) và ghép chúng thành một chuỗi stylesheet duy nhất để nạp toàn cục lúc khởi chạy. Lập trình viên và AI **chỉ cần đặt thuộc tính class cho widget và viết file `.qss` tương ứng bên cạnh**; tuyệt đối không tự viết code nạp file QSS thủ công.

---

## 3. Bản đồ Ánh xạ mã màu (Design Tokens to QSS/CSS Variables)

Để nhất quán giữa tài liệu lý thuyết thiết kế màu sắc (Design Tokens) và lập trình stylesheet thực tế, lập trình viên và AI bắt buộc phải sử dụng các biến placeholder tương ứng được định nghĩa trong `theme.json` và thay thế tự động bởi `ThemeManager`:

| Token thiết kế (UX Theory) | Biến trong Stylesheet (QSS/CSS) | Mô tả & Cách dùng |
| :--- | :--- | :--- |
| **`Primary`** (Màu nhấn chính) | `{ACCENT_COLOR}` | Nút chính (CTA), tiêu điểm focus, đường viền kích hoạt. |
| **`Primary Hover`** | `{ACCENT_HOVER}` | Trạng thái hover của nút bấm hoặc phần tử nhấn chính. |
| **`Background`** (Mền tổng) | `{DARK_BG}` | Màu nền cửa sổ chính của ứng dụng. |
| **`Surface`** (Bề mặt khối) | `{CARD_BG}` | Nền của các thẻ Card, Sidebar con, danh sách dữ liệu. |
| **`OnSurface`** (Chữ chính) | `{TEXT_COLOR}` | Màu chữ hiển thị chính của nội dung văn bản. |
| **`OnSurfaceVariant`** (Chữ phụ) | `{SUBTEXT_COLOR}` | Chữ phụ, placeholder, chú giải nhỏ, icon trang trí. |
| **`Success`** (Thành công) | `{SUCCESS_COLOR}` | Trạng thái thành công, thông báo hoàn thành. |
| **`Error`** (Cảnh báo lỗi) | `{ERROR_COLOR}` | Màu nền cảnh báo lỗi, nút hành động nguy hiểm. |
| **`Border`** (Đường viền) | `{BORDER_COLOR}` | Màu của các đường phân cách, đường viền của input/card. |
| **`Border Width`** | `{BORDER_WIDTH}` | Độ dày đường viền mặc định (thường là `1px`). |
| **`Border Radius`** | `{RADIUS}` | Độ bo góc bo viền mặc định của các card/input/button (ví dụ: `8px`). |
| **`Typography`** (Họ phông) | `{FONT_FAMILY}` | Định nghĩa font chữ chính (ví dụ: `Inter, Roboto, sans-serif`). |

*Lưu ý: Không tự ý viết mã màu HEX cụ thể vào QSS/CSS của các Component con. Luôn luôn sử dụng các biến QSS đại diện ở trên để đồng bộ màu sắc động theo Theme.*

---

## 4. Quy chuẩn Đóng gói Tài nguyên Cục bộ (Colocated Assets) & Kiểm thử Trực quan

### 4.1 Quy chuẩn Đóng gói Tài nguyên Cục bộ (Colocated Assets)
Để đảm bảo các Component (Atoms, Molecules, Organisms) có tính tự trị cao, dễ di chuyển (Move/Rename Module) và tái sử dụng, mọi tài nguyên đồ họa (icons SVG/PNG, hình ảnh, CSS/QSS riêng biệt) của component **bắt buộc phải được đặt cục bộ** trong thư mục của chính component đó thay vì đặt tập trung ở ngoài.

#### Cấu trúc thư mục Component tự trị:
```text
level_01_atoms/
└── buttons/
    ├── __init__.py
    ├── buttons.py        # Logic Component
    ├── buttons.qss       # QSS của riêng nút này
    └── assets/           # Thư mục chứa tài nguyên cục bộ
        └── icons/
            └── search.svg
```

#### Cách thức nạp tài nguyên đa nền tảng:
*   **Desktop (PyQt6)**: Sử dụng lớp `AssetsLoader` được sinh tự động tại `services/assets_loader.py`.
    ```python
    # Nạp QSS cục bộ
    qss = AssetsLoader.load_qss(__file__, "buttons.qss")
    self.setStyleSheet(ThemeManager.get_instance().compile_qss(qss))

    # Nạp icon SVG tự động đổi màu theo Theme hiện hành (lưu trong RAM Cache)
    theme_accent = ThemeManager.get_instance().get_color("ACCENT_COLOR")
    icon = AssetsLoader.load_theme_icon("assets/icons/search.svg", theme_accent)
    self.setIcon(icon)
    ```
*   **Web (React/Vue)**: Sử dụng Vite/Webpack dynamic import kết hợp với thuộc tính `fill="currentColor"` của SVG để đổi màu tự động theo biến CSS.
*   **Mobile (Flutter/React Native)**: Định nghĩa assets theo gói (package) và nhuộm màu động bằng `ColorFilter` (Flutter) hoặc thuộc tính `tint` (Compose/SwiftUI) trong RAM.

---

## 5. Cơ chế Inspect & Chụp màn hình để Kiểm thử trực quan (Visual UI Testing & Inspection)

Để hỗ trợ AI Agent và Lập trình viên kiểm thử trực quan giao diện thực tế (phát hiện tràn khung, lệch trục, sai tỷ lệ), dự án tích hợp sẵn các phím tắt tiện ích khi `DEBUG_UI = True` (mặc định tại `src/config.py`):

*   **`F12` (UI Inspector / Debug Mode)**: 
    * *Cách hoạt động*: Nhấn `F12` để bật/tắt chế độ Inspect. Khi bật, di chuột qua phần tử sẽ hiện viền đứt nét màu tím pastel, click chuột trái sẽ tự động copy toàn bộ cấu trúc phân cấp, kích thước và stylesheet của phần tử đó vào Clipboard dưới dạng văn bản.
*   **`F11` (Chụp ảnh toàn màn hình ứng dụng)**: 
    * *Cách hoạt động*: Nhấn `F11` để chụp lại toàn bộ cửa sổ ứng dụng hiện hành. Ảnh chụp được lưu **ghi đè** tại `artifacts/ui_screenshot.png` (để AI Agent đọc trực tiếp) và đồng thời lưu một bản sao đánh số lịch sử tại thư mục `artifacts/snapshots/`.
*   **`F10` (Chụp ảnh phần tử liên tiếp lưu lịch sử)**: 
    * *Cách hoạt động*: Nhấn `F10` để bật/tắt chế độ chụp ảnh phần tử liên tiếp (viền xanh lá rà chuột). Khi click vào bất kỳ phần tử nào, ứng dụng sẽ chụp riêng phần tử đó và lưu thành các tệp tin đánh số lịch sử trong thư mục `artifacts/snapshots/`.
*   **`F9` (Chụp ảnh phần tử liên tiếp ghi đè trực tiếp)**: 
    * *Cách hoạt động*: Nhấn `F9` để bật/tắt chế độ chụp ảnh phần tử liên tiếp và **ghi đè** trực tiếp vào tệp tin cố định: `artifacts/widget_screenshot.png`. File này phục vụ trực tiếp cho các AI Agent đọc và trao đổi trực quan về thiết kế UI nhỏ nhất với lập trình viên mà không cần quan tâm đến snapshots.

*   **Tắt chế độ Debug khi Deploy**: Trước khi đóng gói sản phẩm để phát hành (production deployment), hãy sửa `DEBUG_UI = False` trong `src/config.py` hoặc đặt biến môi trường `DEBUG_UI=false`. Khi đó toàn bộ các phím tắt gỡ lỗi trên sẽ bị vô hiệu hóa hoàn toàn để bảo mật và tối ưu hóa tài nguyên.

---

## 🗺️ Bản đồ Chỉ mục UI (UI Index Map)

Tùy vào phần phát triển giao diện, hãy tra cứu đúng hướng dẫn:
* [1. Quản lý State & Custom Hooks](state_management.md) – Cách định nghĩa Hook cho PyQt6, Kivy, Web và cách tích hợp vào View Page.
* [2. Đa luồng & Tác vụ chạy nền](background_execution.md) – Quy chuẩn thiết kế Daemon Pattern, Graceful Shutdown và Hybrid Model.
* [3. Quy chuẩn Thiết kế UI/UX](ui_ux_design/README.md) – Các nguyên lý chung và hướng dẫn cụ thể cho Web, Mobile, Desktop.


