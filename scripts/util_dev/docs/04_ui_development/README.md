# Hướng dẫn Phát triển UI & Kiến trúc Hooks Đa Nền Tảng

Tài liệu này hướng dẫn chi tiết cách phát triển giao diện người dùng (UI) và tổ chức mã nguồn tầng hiển thị (Presentation/Infrastructure UI) theo mô hình **Atomic Design** kết hợp mẫu kiến trúc **Custom Hooks** tổng quát hóa cho mọi nền tảng (Desktop PyQt6, Mobile Kivy, Web Frontend).

---

## 1. Cấu trúc Thư mục UI tổng quát (`layer_04_infrastructure/ui/`)

Mã nguồn UI của bất kỳ nền tảng nào đều được tổ chức phân cấp đồng bộ:

```text
desktop_qt6/ (hoặc web_frontend, mobile_kivy)
│
├── level_01_atoms/        # Phần tử cơ bản nhỏ nhất (Buttons, Labels, Inputs, Frames)
├── level_02_molecules/    # Tổ hợp các atoms đơn giản (Form fields, Dialogs, Message boxes)
├── level_03_organisms/    # Giao diện phức tạp tự hoàn thiện (Sidebar, Charts, Tables)
├── level_04_templates/    # Bộ khung layout bố cục chung của trang (Page templates)
├── level_05_pages/        # Các trang màn hình cụ thể ghép từ các component trên
│
├── hooks/                 # Custom Hooks: Nơi quản lý State, Timers, và các luồng tác vụ bất đồng bộ
├── services/              # UI Services: Hệ quản trị Theme, Đa ngôn ngữ (i18n), Định tuyến (Navigation)
└── assets/                # Static Resources: Hình ảnh (images), biểu tượng (icons), phông chữ (fonts)
```

---

## 2. Nguyên tắc Ranh giới Clean Architecture

* **Tầng 3 (Interface Adapters / Presenters)**: Tuyệt đối không chứa bất kỳ import hoặc tham chiếu nào liên quan đến thư viện đồ họa của nền tảng (như PyQt6, Kivy, Web DOM/HTML). Các lớp Presenter được sinh tự động và chỉ đóng vai trò định dạng dữ liệu thuần Python.
* **Tầng 4 (Infrastructure / UI Hooks & Views)**: Là nơi duy nhất được import thư viện đồ họa GUI.
* **Tách biệt logic hiển thị và logic dữ liệu**: Các trang giao diện (`level_05_pages/`) chỉ làm nhiệm vụ vẽ giao diện, tuyệt đối không được tự khởi tạo luồng chạy nền, bộ hẹn giờ hoặc thực hiện truy vấn cơ sở dữ liệu / API trực tiếp.

---

## 🗺️ Bản đồ Chỉ mục UI (UI Index Map)

Tùy vào phần phát triển giao diện, hãy tra cứu đúng hướng dẫn:
* [1. Quản lý State & Custom Hooks](state_management.md) – Cách định nghĩa Hook cho PyQt6, Kivy, Web và cách tích hợp vào View Page.
* [2. Đa luồng & Tác vụ chạy nền](background_execution.md) – Quy chuẩn thiết kế Daemon Pattern, Graceful Shutdown và Hybrid Model.
* [3. Quy chuẩn Thiết kế UI/UX](ui_ux_design/README.md) – Các nguyên lý chung và hướng dẫn cụ thể cho Web, Mobile, Desktop.

