# 🏛️ python-clean-architecture-kit

A production-ready Clean Architecture template and automated scaffolding kit designed specifically for Python applications. 

This kit enables you to build scalable, testable, and loosely-coupled applications supporting multiple platforms (CLI, Web API via FastAPI, Desktop via PyQt6, Mobile via Kivy) out of the box.

---

## 🌟 Core Features

- **Strict Layer Separation:** Structured into 5 decoupled layers conforming to Uncle Bob's Clean Architecture.
- **Automated Feature Generation:** Built-in Project Manager tool (both GUI & CLI) to instantly generate new features, including DTOs, Interactors, Repository interfaces, concrete DataSources, and unit tests.
- **Smart DI Container & Bootstrap:** Automated dependency injection registration with dependency resolving capabilities.
- **Production-Ready Scaffolding:**
  - **Async/Await Native:** Fully asynchronous from routing to database data sources.
  - **Environment-Driven Configuration:** Centralized config (`src/config.py`) loading from environment variables.
  - **Standard Logging System:** Integrated stream logging (`src/app_logger.py`) across all layers.
- **Decoupled Runners:** Platform entry-points are organized in `scripts/run/` to keep the project root clean.

---

## 📂 Project Structure

```
learn/
├── src/                                  # Application Source Code
│   ├── app_logger.py                     # Standardized Logging Helper
│   ├── config.py                         # Environment Variables Config Loader
│   ├── layer_01_entities/                # Pure Business Entities & Validation
│   ├── layer_02_usecases/                # Business Logic & Ports (Interfaces)
│   ├── layer_03_interface_adapters/      # Adapters (Controllers, Presenters, Gateways)
│   ├── layer_04_infrastructure/          # Concrete Frameworks (SQLite, PyQt6, FastAPI)
│   └── layer_05_bootstrap/               # Dependency Injection & Wiring
│
├── scripts/                              # Helper Scripts
│   ├── run/                              # Unified Execution Directory
│   │   ├── cli/                          # CLI Runner Scripts
│   │   └── desktop/                      # PyQt6 GUI Runner Scripts
│   └── util_dev/                         # Developer Utilities & Project Manager App
│       ├── project_manager_app/          # The Scaffolder Application (Clean Architecture)
│       └── rename_module.py              # CLI tool to rename modules & auto-fix imports
│
├── tests/                                # Automated Unit Tests (100% Mocked)
└── docs/                                 # Architecture & Development Manuals
```

---

## 🚀 Getting Started

### 1. Launch the Project Manager App
The Project Manager handles all codebase operations under a unified, premium PyQt6 GUI or a flexible CLI shell.

- **PyQt6 GUI Window:**
  ```bash
  python scripts/util_dev/project_manager_app/run_project_manager_app/desktop/run_desktop.py
  ```
- **CLI Shell (Interactive Menu):**
  ```bash
  python scripts/util_dev/project_manager_app/run_project_manager_app/cli/run_cli.py
  ```
  *CLI này hoạt động dưới dạng **Interactive Menu** (giao diện dòng lệnh tương tác chọn số). Khi khởi chạy, bạn sẽ tương tác theo các bước:*
  
  1. **Khởi động (Welcome Flow):** Nếu chưa có project nào được tạo, CLI sẽ yêu cầu bạn nhập:
     * `N` để tạo project mới (Ví dụ: `trading_bot`).
     * `L` để load khôi phục lại một project cũ đã lưu.
  2. **Giao diện Menu chính:** Sau khi kích hoạt project, CLI sẽ hiện danh sách chức năng từ `0` đến `9`. Bạn chỉ cần **gõ số tương ứng** và nhấn `Enter` để kích hoạt:
     * `1` ➔ **Generate Feature:** Nhập tiếp tên feature (VD: `PlaceOrder`), nền tảng (VD: `web`), và cơ sở dữ liệu (VD: `sqlite`) khi được nhắc.
     * `2` ➔ **Check Imports:** Tự động quét và báo cáo vi phạm ranh giới kiến trúc Clean Architecture.
     * `3` & `4` & `5` ➔ **Backup & Khôi phục:** Lưu trạng thái, khôi phục hoặc xem danh sách dự án.
     * `6` ➔ **Reset Workspace:** Quét sạch code rác để đưa workspace về trạng thái nguyên bản.
     * `7` ➔ **Refactor Module:** Đổi tên hoặc di chuyển tệp/thư mục và tự động cập nhật import toàn hệ thống.
     * `8` ➔ **Migrate Clean Code:** Tự động chuẩn hóa Protocol sang ABC và print sang app_logger.
     * `9` ➔ **Setup Environment:** Tự động cài đặt môi trường ảo `.venv` và pip packages.
     * `0` ➔ **Thoát.**

- **CLI Shell (Non-Interactive Mode - Dành cho AI & CI/CD):**
  ```bash
  python scripts/util_dev/project_manager_app/run_project_manager_app/cli/run_cli.py [options]
  ```
  *Chế độ này cho phép thực thi thẳng một hành động duy nhất thông qua các tham số dòng lệnh (Arguments/Flags), kết thúc ngay lập tức mà không hỏi thêm câu nào. Cực kỳ tối ưu cho các tác vụ tự động hóa và AI Agent:*

  * **Kích hoạt dự án mới & sinh Feature:**
    ```bash
    python scripts/util_dev/project_manager_app/run_project_manager_app/cli/run_cli.py --project-name trading_bot --generate-feature PlaceOrder --platforms web,desktop --db sqlite
    ```
  * **Kiểm tra vi phạm import ranh giới kiến trúc:**
    ```bash
    python scripts/util_dev/project_manager_app/run_project_manager_app/cli/run_cli.py --check-imports
    ```
  * **Cấu hình môi trường ảo tự động:**
    ```bash
    python scripts/util_dev/project_manager_app/run_project_manager_app/cli/run_cli.py --setup-env
    ```
  * **Đổi tên/Di chuyển module tự động cập nhật import:**
    ```bash
    python scripts/util_dev/project_manager_app/run_project_manager_app/cli/run_cli.py --rename-module src/layer_01_entities/old_name.py --new-name new_name
    ```
  * **Lưu backup dự án hiện tại:**
    ```bash
    python scripts/util_dev/project_manager_app/run_project_manager_app/cli/run_cli.py --save-project trading_bot
    ```
  * **Khôi phục dự án cũ:**
    ```bash
    python scripts/util_dev/project_manager_app/run_project_manager_app/cli/run_cli.py --load-project trading_bot
    ```
  * **Xem danh sách dự án:**
    ```bash
    python scripts/util_dev/project_manager_app/run_project_manager_app/cli/run_cli.py --list-projects
    ```
  * **Xóa sạch workspace (Reset):**
    ```bash
    python scripts/util_dev/project_manager_app/run_project_manager_app/cli/run_cli.py --reset-workspace
    ```

---

## 🛠️ Main Features & Modules

### 1. Dashboard
Provides a centralized overview of the active project.
- Scans and counts code files across layers (Entities, Usecases, Adapters, Infrastructure, Bootstrap).
- Lists generated runner scripts and database configurations.

### 2. Add Feature (Scaffolding)
Instantly generate clean architecture components:
- Automatically creates Entities, Interactors, DTOs, Repository interfaces, concrete DataSources, and pytest templates.
- Generates bootstrapping DI wiring and platform-specific runner scripts (CLI, Desktop, Web API) under `scripts/run/`.

### 3. Refactor Module (Rename & Move)
A smart refactoring manager powered by the `rope` engine to safely restructure files and folders without breaking imports.
- **Rename Module:** Rename any file or folder at its current location. All imports in other files pointing to it will be automatically updated.
- **Move Module (Cut & Paste):** Move any python file or package to a new destination directory. All absolute and relative imports across the project will be resolved and modified to match the new location.

### 4. Developer Utilities
A unified suite of helper tools for daily code maintenance:
- **Scan Imports (Check Architecture):** Enforces static analysis rules. Checks if higher-level layers (e.g., Entities, Usecases) incorrectly import lower-level ones (e.g., Infrastructure, Bootstrap).
- **Clean Code Migration:** Migrates Python `Protocol` interfaces to `ABC` (Abstract Base Class) and replaces raw `print()` statements with structured loggers (`src/app_logger.py`).
- **Setup Environment:** Initializes Python virtual environment (`.venv`), upgrades `pip`, and installs all core dependencies (FastAPI, PyQt6, pytest, black, pyright, rope) with live real-time output log redirection to the System Logs Panel.

### 5. Danger Zone (Reset Workspace)
Safely placed at the bottom of the navigation to prevent accidental clicks:
- Clears the active project state.
- Purges temporary scaffolding files to return the workspace to a pristine template state.

---

## 📖 Documentation
Check the detailed documentation in the `docs/` folder:
- [Clean Architecture Guide](../01_architecture_rules/ARCHITECTURE.md) – Detailed guide on layers, interfaces, and inbound/outbound structures.
- [Development Process Manual](../02_development_flow/DESIGN_PROCESS.md) – Step-by-step checklist on writing business logic.

---
*Keep your architecture clean!*
