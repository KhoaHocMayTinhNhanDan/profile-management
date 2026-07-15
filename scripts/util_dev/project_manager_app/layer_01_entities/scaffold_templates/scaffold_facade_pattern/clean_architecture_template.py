"""
CleanArchitectureTemplate — Facade Pattern

Lớp này là Facade, giữ nguyên toàn bộ API công khai để tương thích ngược.
Nó đóng vai trò là Client hoặc wrapper gọi xuống bộ Abstract Factory được thiết kế chuẩn GoF:
    templates/
    ├── wrapper/                         ← ScaffoldFactoryWrapper (Entry Point)
    ├── factory/                         ← Interface & Concrete Factories
    └── products/                        ← Phân cấp sản phẩm template chuỗi UI
"""

from ..subsystems import ScaffoldFactoryWrapper


class CleanArchitectureTemplate:
    """
    Facade — Thực thể cốt lõi chứa quy tắc về hình dáng của mã nguồn Clean Architecture.
    Delegate toàn bộ logic xuống bộ các concrete factory & products học thuật.

    GoF Role: Facade
    """

    # =========================================================================
    # Common — UseCase, Gateway, Repository, DataSource, Bootstrap
    # =========================================================================

    @staticmethod
    def get_usecase_interactor_template(pascal_name: str, snake_name: str) -> str:
        return ScaffoldFactoryWrapper.get_usecase_interactor_template(
            pascal_name, snake_name
        )

    @staticmethod
    def get_usecase_dto_template(pascal_name: str) -> str:
        return ScaffoldFactoryWrapper.get_usecase_dto_template(pascal_name)

    @staticmethod
    def get_usecase_repository_interface_template(pascal_name: str) -> str:
        return ScaffoldFactoryWrapper.get_usecase_repository_interface_template(
            pascal_name
        )

    @staticmethod
    def get_controller_template(
        pascal_name: str, snake_name: str, platform: str, group: str = ""
    ) -> str:
        return ScaffoldFactoryWrapper.get_controller_template(
            pascal_name, snake_name, platform, group
        )

    @staticmethod
    def get_presenter_template(
        pascal_name: str, snake_name: str, group: str = ""
    ) -> str:
        return ScaffoldFactoryWrapper.get_presenter_template(
            pascal_name, snake_name, group
        )

    @staticmethod
    def get_outbound_data_source_interface_template(pascal_name: str) -> str:
        return ScaffoldFactoryWrapper.get_outbound_data_source_interface_template(
            pascal_name
        )

    @staticmethod
    def get_repository_template(pascal_name: str, snake_name: str) -> str:
        return ScaffoldFactoryWrapper.get_repository_template(pascal_name, snake_name)

    @staticmethod
    def get_data_source_impl_template(
        pascal_name: str, snake_name: str, tech: str
    ) -> str:
        return ScaffoldFactoryWrapper.get_data_source_impl_template(
            pascal_name, snake_name, tech
        )

    @staticmethod
    def get_test_template(pascal_name: str, snake_name: str, group: str = "") -> str:
        return ScaffoldFactoryWrapper.get_test_template(pascal_name, snake_name, group)

    @staticmethod
    def get_integration_test_template(
        pascal_name: str, snake_name: str, group: str = ""
    ) -> str:
        return ScaffoldFactoryWrapper.get_integration_test_template(
            pascal_name, snake_name, group
        )

    @staticmethod
    def get_di_container_template() -> str:
        return ScaffoldFactoryWrapper.get_di_container_template()

    @staticmethod
    def get_app_context_base_template() -> str:
        return ScaffoldFactoryWrapper.get_app_context_base_template()

    @staticmethod
    def get_app_context_desktop_template() -> str:
        return ScaffoldFactoryWrapper.get_app_context_desktop_template()

    @staticmethod
    def get_app_context_web_template() -> str:
        return ScaffoldFactoryWrapper.get_app_context_web_template()

    @staticmethod
    def get_app_context_mobile_template() -> str:
        return ScaffoldFactoryWrapper.get_app_context_mobile_template()

    @staticmethod
    def get_app_context_cli_template() -> str:
        return ScaffoldFactoryWrapper.get_app_context_cli_template()

    @staticmethod
    def get_app_logger_template() -> str:
        return ScaffoldFactoryWrapper.get_app_logger_template()

    @staticmethod
    def get_config_template() -> str:
        return ScaffoldFactoryWrapper.get_config_template()

    # =========================================================================
    # Desktop — PyQt6 (Sử dụng qua Client của Abstract Factory)
    # =========================================================================

    @staticmethod
    def get_ui_pyqt6_atom_buttons_template() -> str:
        wrapper = ScaffoldFactoryWrapper("desktop_qt6")
        return wrapper.get_buttons()

    @staticmethod
    def get_ui_pyqt6_atom_inputs_template() -> str:
        wrapper = ScaffoldFactoryWrapper("desktop_qt6")
        return wrapper.get_inputs()

    @staticmethod
    def get_ui_pyqt6_atom_labels_template() -> str:
        wrapper = ScaffoldFactoryWrapper("desktop_qt6")
        return wrapper.get_labels()

    @staticmethod
    def get_ui_pyqt6_page_template(pascal_name: str, snake_name: str) -> str:
        wrapper = ScaffoldFactoryWrapper("desktop_qt6")
        return wrapper.get_page(pascal_name, snake_name)

    @staticmethod
    def get_ui_pyqt6_main_window_template(project_name: str = "Application") -> str:
        return ScaffoldFactoryWrapper("desktop_qt6").get_main_window(project_name)

    @staticmethod
    def get_ui_pyqt6_ui_inspector_template() -> str:
        return ScaffoldFactoryWrapper("desktop_qt6").get_ui_inspector()

    # =========================================================================
    # Desktop — PyQt5
    # =========================================================================

    @staticmethod
    def get_ui_pyqt5_template(pascal_name: str, snake_name: str) -> str:
        return ScaffoldFactoryWrapper.get_ui_pyqt5_template(pascal_name, snake_name)

    # =========================================================================
    # Desktop — Tkinter
    # =========================================================================

    @staticmethod
    def get_ui_tkinter_template(pascal_name: str, snake_name: str) -> str:
        return ScaffoldFactoryWrapper.get_ui_tkinter_template(pascal_name, snake_name)

    # =========================================================================
    # Mobile — Kivy (Sử dụng qua Client của Abstract Factory)
    # =========================================================================

    @staticmethod
    def get_ui_kivy_atom_buttons_template() -> str:
        wrapper = ScaffoldFactoryWrapper("mobile_kivy")
        return wrapper.get_buttons()

    @staticmethod
    def get_ui_kivy_atom_inputs_template() -> str:
        wrapper = ScaffoldFactoryWrapper("mobile_kivy")
        return wrapper.get_inputs()

    @staticmethod
    def get_ui_kivy_atom_labels_template() -> str:
        wrapper = ScaffoldFactoryWrapper("mobile_kivy")
        return wrapper.get_labels()

    @staticmethod
    def get_ui_kivy_template(pascal_name: str, snake_name: str) -> str:
        wrapper = ScaffoldFactoryWrapper("mobile_kivy")
        return wrapper.get_page(pascal_name, snake_name)

    @staticmethod
    def get_ui_kivy_ui_inspector_template() -> str:
        wrapper = ScaffoldFactoryWrapper("mobile_kivy")
        return wrapper.get_ui_inspector()

    @staticmethod
    def get_ui_kivy_main_window_template(project_name: str) -> str:
        wrapper = ScaffoldFactoryWrapper("mobile_kivy")
        return wrapper.get_main_window(project_name)

    # =========================================================================
    # Web — FastAPI Backend
    # =========================================================================

    @staticmethod
    def get_fastapi_router_template(
        pascal_name: str, snake_name: str, group: str = ""
    ) -> str:
        return ScaffoldFactoryWrapper.get_fastapi_router_template(
            pascal_name, snake_name, group
        )

    @staticmethod
    def get_fastapi_main_template(project_name: str) -> str:
        return ScaffoldFactoryWrapper.get_fastapi_main_template(project_name)

    @staticmethod
    def get_fastapi_debug_router_template() -> str:
        return ScaffoldFactoryWrapper.get_fastapi_debug_router_template()

    # =========================================================================
    # Web — Frontend (Sử dụng qua Client của Abstract Factory)
    # =========================================================================

    @staticmethod
    def get_ui_web_atom_buttons_template() -> str:
        wrapper = ScaffoldFactoryWrapper("web")
        return wrapper.get_buttons()

    @staticmethod
    def get_ui_web_atom_inputs_template() -> str:
        wrapper = ScaffoldFactoryWrapper("web")
        return wrapper.get_inputs()

    @staticmethod
    def get_ui_web_atom_labels_template() -> str:
        wrapper = ScaffoldFactoryWrapper("web")
        return wrapper.get_labels()

    @staticmethod
    def get_ui_web_html_template(pascal_name: str, snake_name: str) -> str:
        wrapper = ScaffoldFactoryWrapper("web")
        return wrapper.get_page(pascal_name, snake_name)

    @staticmethod
    def get_ui_web_ui_inspector_template() -> str:
        wrapper = ScaffoldFactoryWrapper("web")
        return wrapper.get_ui_inspector()

    # =========================================================================
    # CLI
    # =========================================================================

    @staticmethod
    def get_ui_cli_template(pascal_name: str, snake_name: str) -> str:
        return ScaffoldFactoryWrapper.get_ui_cli_template(pascal_name, snake_name)

    # =========================================================================
    # Runner scripts
    # =========================================================================

    @staticmethod
    def get_run_cli_template(pascal_name: str, snake_name: str) -> str:
        return ScaffoldFactoryWrapper.get_run_cli_template(pascal_name, snake_name)

    @staticmethod
    def get_run_desktop_template(pascal_name: str, snake_name: str) -> str:
        return ScaffoldFactoryWrapper.get_run_desktop_template(pascal_name, snake_name)

    @staticmethod
    def get_run_cli_project_template(project_snake: str) -> str:
        return ScaffoldFactoryWrapper.get_run_cli_project_template(project_snake)

    @staticmethod
    def get_run_desktop_project_template(project_snake: str) -> str:
        return ScaffoldFactoryWrapper.get_run_desktop_project_template(project_snake)

    @staticmethod
    def get_run_mobile_template(pascal_name: str, snake_name: str) -> str:
        return ScaffoldFactoryWrapper.get_run_mobile_template(pascal_name, snake_name)

    @staticmethod
    def get_run_web_template(pascal_name: str, snake_name: str) -> str:
        return ScaffoldFactoryWrapper.get_run_web_template(pascal_name, snake_name)

    @staticmethod
    def get_run_mobile_project_template(project_snake: str) -> str:
        return ScaffoldFactoryWrapper.get_run_mobile_project_template(project_snake)

    @staticmethod
    def get_run_web_project_template(project_snake: str) -> str:
        return ScaffoldFactoryWrapper.get_run_web_project_template(project_snake)

    @staticmethod
    def get_run_tauri_project_template(project_snake: str) -> str:
        return ScaffoldFactoryWrapper.get_run_tauri_project_template(project_snake)

    # =========================================================================
    # PyQt6 Presentation Services & Templates
    # =========================================================================

    @staticmethod
    def get_ui_pyqt6_i18n_manager_template() -> str:
        from .presentation_templates import I18N_MANAGER_TEMPLATE

        return I18N_MANAGER_TEMPLATE

    @staticmethod
    def get_ui_pyqt6_light_dark_mode_manager_template() -> str:
        from .presentation_templates import LIGHT_DARK_MODE_MANAGER_TEMPLATE

        return LIGHT_DARK_MODE_MANAGER_TEMPLATE

    @staticmethod
    def get_ui_pyqt6_theme_manager_template() -> str:
        from .presentation_templates import THEME_MANAGER_TEMPLATE

        return THEME_MANAGER_TEMPLATE

    @staticmethod
    def get_ui_pyqt6_base_qss_template() -> str:
        from .presentation_templates import BASE_QSS_TEMPLATE

        return BASE_QSS_TEMPLATE

    @staticmethod
    def get_ui_pyqt6_atom_buttons_qss_template() -> str:
        wrapper = ScaffoldFactoryWrapper("desktop_qt6")
        return wrapper.get_buttons_qss()

    @staticmethod
    def get_ui_pyqt6_atom_inputs_qss_template() -> str:
        wrapper = ScaffoldFactoryWrapper("desktop_qt6")
        return wrapper.get_inputs_qss()

    @staticmethod
    def get_ui_pyqt6_atom_labels_qss_template() -> str:
        wrapper = ScaffoldFactoryWrapper("desktop_qt6")
        return wrapper.get_labels_qss()

    @staticmethod
    def get_ui_pyqt6_settings_store_template() -> str:
        from .presentation_templates import SETTINGS_STORE_TEMPLATE

        return SETTINGS_STORE_TEMPLATE

    @staticmethod
    def get_ui_pyqt6_assets_loader_template() -> str:
        from .presentation_templates import ASSETS_LOADER_TEMPLATE

        return ASSETS_LOADER_TEMPLATE

    @staticmethod
    def get_ui_pyqt6_themes_readme_template() -> str:
        from .presentation_templates import THEMES_README_TEMPLATE

        return THEMES_README_TEMPLATE

    @staticmethod
    def get_ui_pyqt6_classic_theme_json_template(
        accent_color_dark="#89b4fa",
        accent_hover_dark="#b4befe",
        accent_color_light="#4f46e5",
        accent_hover_light="#4338ca",
        font_family="Inter, Roboto, sans-serif",
    ) -> str:
        from .presentation_templates import CLASSIC_THEME_JSON_TEMPLATE

        return CLASSIC_THEME_JSON_TEMPLATE.format(
            ACCENT_COLOR_DARK=accent_color_dark,
            ACCENT_HOVER_DARK=accent_hover_dark,
            ACCENT_COLOR_LIGHT=accent_color_light,
            ACCENT_HOVER_LIGHT=accent_hover_light,
            FONT_FAMILY=font_family,
        )

    @staticmethod
    def get_ui_pyqt6_classic_theme_qss_template() -> str:
        from .presentation_templates import CLASSIC_THEME_QSS_TEMPLATE

        return CLASSIC_THEME_QSS_TEMPLATE

    @staticmethod
    def get_ui_pyqt6_down_arrow_svg_template() -> str:
        return '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#cdd6f4" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>'

    @staticmethod
    def get_ui_pyqt6_base_page_template() -> str:
        from .presentation_templates import BASE_PAGE_TEMPLATE

        return BASE_PAGE_TEMPLATE

    @staticmethod
    def get_ui_pyqt6_locale_json_template(lang: str) -> str:
        from .presentation_templates import (
            EN_JSON_TEMPLATE,
            VI_JSON_TEMPLATE,
            ZH_JSON_TEMPLATE,
        )

        if lang == "vi":
            return VI_JSON_TEMPLATE
        elif lang == "zh":
            return ZH_JSON_TEMPLATE
        return EN_JSON_TEMPLATE

    @staticmethod
    def get_ui_pyqt6_use_async_template() -> str:
        wrapper = ScaffoldFactoryWrapper("desktop_qt6")
        return wrapper.get_async_hook()

    @staticmethod
    def get_ui_kivy_use_async_template() -> str:
        wrapper = ScaffoldFactoryWrapper("mobile_kivy")
        return wrapper.get_async_hook()

    @staticmethod
    def get_ui_web_use_async_template() -> str:
        wrapper = ScaffoldFactoryWrapper("web")
        return wrapper.get_async_hook()

    @staticmethod
    def get_ui_pyqt6_feature_hook_template(pascal: str, snake: str) -> str:
        wrapper = ScaffoldFactoryWrapper("desktop_qt6")
        return wrapper.get_feature_hook(pascal, snake)

    @staticmethod
    def get_ui_kivy_feature_hook_template(pascal: str, snake: str) -> str:
        wrapper = ScaffoldFactoryWrapper("mobile_kivy")
        return wrapper.get_feature_hook(pascal, snake)

    @staticmethod
    def get_ui_web_feature_hook_template(pascal: str, snake: str) -> str:
        wrapper = ScaffoldFactoryWrapper("web")
        return wrapper.get_feature_hook(pascal, snake)

    @staticmethod
    def get_dockerfile_template() -> str:
        return """# Stage 1: Builder (Compile dependencies)
FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runner (Lightweight production runtime)
FROM python:3.12-slim AS runner

WORKDIR /app

# Run as non-root user for security
RUN groupadd -g 999 appuser && \\
    useradd -r -u 999 -g appuser appuser

# Copy installed packages from builder
COPY --from=builder /root/.local /home/appuser/.local
COPY . .

# Set environment variables
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Default execution starts the Web API (FastAPI)
CMD ["uvicorn", "src.layer_05_bootstrap.web_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

    @staticmethod
    def get_github_actions_ci_template() -> str:
        return """name: CI Quality Gate

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  quality-check:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
        cache: 'pip'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        pip install black pyright pytest

    - name: Code Formatting (Black Check)
      run: |
        black --check src/

    - name: Static Type Checking (Pyright)
      run: |
        mkdir -p src
        pyright src/

    - name: Run Unit Tests (Pytest)
      run: |
        pytest tests/
"""

    @staticmethod
    def get_dockerignore_template() -> str:
        return """# Git and CI configuration
.git
.github
 
# Python virtual environment & cache files
.venv
venv
ENV
__pycache__/
*.pyc
*.pyo
*.pyd
.pytest_cache/
.pyright_cache/
.ropeproject/
 
# IDE configurations
.vscode/
.idea/
 
# Testing & technical docs (not needed on production)
docs/
tests/
 
# DEV TOOLS & DESKTOP RUNNERS (Excluded entirely from production web api container)
scripts/util_dev/
scripts/run/desktop/
"""

    @staticmethod
    def get_design_token_linter_template() -> str:
        return ScaffoldFactoryWrapper.get_design_token_linter_template()

    @staticmethod
    def get_test_theme_tokens_linter_template() -> str:
        return ScaffoldFactoryWrapper.get_test_theme_tokens_linter_template()
