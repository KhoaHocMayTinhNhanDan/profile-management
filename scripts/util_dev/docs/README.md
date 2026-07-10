# 🏛️ Python Clean Architecture Kit - Documentation Hub

Chào mừng bạn đến với trung tâm tài liệu hướng dẫn phát triển của dự án. Tài liệu này được thiết kế để cả **Lập trình viên** và **AI Assistant** nhanh chóng tra cứu đúng quy chuẩn khi làm việc.

---

## 🚀 Hướng dẫn nhanh khởi chạy dự án (Quick Start)

### 1. Khởi tạo môi trường phát triển (Setup Environment)
Chạy script tự động để tạo môi trường ảo `.venv` và cài đặt toàn bộ các thư viện cần thiết:
```bash
python scripts/util_dev/setup_env.py
```
*(Script này sẽ tự động khởi tạo `.venv`, cài đặt FastAPI, PyQt6, Pytest, PyInstaller, Mongo, Redis và cấu hình hệ thống).*


### 2. Khởi chạy Công cụ Quản lý Dự án (Project Manager App)
Công cụ này hỗ trợ bạn tự động sinh code tính năng mới, kiểm tra import, dọn dẹp workspace:
* **Giao diện đồ họa (PyQt6 GUI):**
  ```bash
  python scripts/util_dev/project_manager_app/run_project_manager_app/desktop/run_desktop.py
  ```
* **Giao diện CLI:**
  ```bash
  python scripts/util_dev/project_manager_app/run_project_manager_app/cli/run_cli.py
  ```

### 3. Chạy Unit Test kiểm tra ranh giới kiến trúc
```bash
pytest tests/
```

---

## 🗺️ Bản đồ Chỉ mục Tài liệu (Documentation Index Map)

Hãy chọn đúng tệp hướng dẫn phù hợp với tác vụ bạn đang thực hiện để tuân thủ thiết kế hệ thống:

| Phân mục cần làm | Tệp hướng dẫn chi tiết | Nội dung chính |
| :--- | :--- | :--- |
| **Quy tắc làm việc** | [WORKSPACE_RULES.md](00_workspace_rules/WORKSPACE_RULES.md) | [BẮT BUỘC] Quy tắc thiết kế Entity, cách commit, quy trình sinh Use Case mới |
| **Kiến trúc tổng quan** | [ARCHITECTURE.md](01_architecture_rules/ARCHITECTURE.md) | Giải thích lý thuyết 5 Layer, Inbound/Outbound, Luồng dữ liệu đi trong dự án |
| **Ràng buộc Biên giới & DI** | [ARCHITECTURE_RULES.md](01_architecture_rules/ARCHITECTURE_RULES.md) | [QUY TẮC CỨNG] Cấm import tầng ngoài vào trong, luật Dependency Injection |
| **Ràng buộc cấu trúc file** | [PROJECT_STRUCTURE_RULES.md](01_architecture_rules/PROJECT_STRUCTURE_RULES.md) | [QUY TẮC CỨNG] Quy định 5 thư mục Layer 4 và cấu trúc Inbound/Outbound Layer 3 |
| **Quy trình code tính năng** | [DESIGN_PROCESS.md](02_development_flow/DESIGN_PROCESS.md) | Hướng dẫn từng bước phát triển Inside-Out từ Entity lên Infra |
| **Quy chuẩn Code & Exception** | [CODING_RULES.md](02_development_flow/CODING_RULES.md) | Quy tắc Type Hint, Logging (cấm print), xử lý DB Exception sang Domain Exception |
| **Thiết kế Entity & Patterns** | [README.md](03_entity_design_patterns/README.md) | Quy chuẩn đặt tên file pattern và tóm tắt GoF Layouts (Strategy, State...) |
| **Phát triển giao diện (UI)** | [README.md](04_ui_development/README.md) | Cấu trúc UI Atoms/Molecules, Hook Pattern, Threading & Daemon Pattern |
| **Quy chuẩn Thiết kế UI/UX** | [README.md](04_ui_development/ui_ux_design/README.md) | Nguyên lý chung và hướng dẫn thiết kế chuyên biệt cho Web, Mobile, Desktop |
| **Sử dụng Tool sinh code** | [project_manager_app.md](05_tools/project_manager_app.md) | Hướng dẫn chạy và sử dụng GUI/CLI của Project Manager App để sinh code tự động |

---
*Keep your architecture clean!*
