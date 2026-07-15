class CommonFactory:
    """
    Concrete Factory cho các template chung của Clean Architecture (Entities, UseCases, DB, Bootstrap).
    """

    @staticmethod
    def get_usecase_interactor_template(pascal_name: str, snake_name: str) -> str:
        return f"""
from src.layer_02_usecases.gateways_interface.i_{snake_name}_repository import I{pascal_name}Repository
from .{snake_name}_dto import {pascal_name}Input, {pascal_name}Output

class {pascal_name}Interactor:
    def __init__(self, repository: I{pascal_name}Repository):
        self._repository = repository

    async def execute(self, input_data: {pascal_name}Input) -> {pascal_name}Output:
        await self._repository.save_db(input_data)
        return {pascal_name}Output(status="success", message="Executed")
"""

    @staticmethod
    def get_usecase_dto_template(pascal_name: str) -> str:
        return f"""
from dataclasses import dataclass

@dataclass
class {pascal_name}Input:
    pass

@dataclass
class {pascal_name}Output:
    status: str
    message: str
"""

    @staticmethod
    def get_usecase_repository_interface_template(pascal_name: str) -> str:
        return f"""
from abc import ABC, abstractmethod
from typing import Any

class I{pascal_name}Repository(ABC):
    @abstractmethod
    async def save_db(self, data: Any) -> None:
        pass
"""

    @staticmethod
    def get_controller_template(
        pascal_name: str, snake_name: str, platform: str, group: str = ""
    ) -> str:
        usecase_subpath = f"{group}.{snake_name}" if group else snake_name
        return f"""
from src.layer_02_usecases.usecases.{usecase_subpath}.{snake_name}_dto import {pascal_name}Input
from src.layer_02_usecases.usecases.{usecase_subpath}.{snake_name}_interactor import {pascal_name}Interactor
from src.layer_03_interface_adapters.presenters.{platform}.{snake_name} import {pascal_name}Presenter

class {pascal_name}Controller:
    def __init__(self, interactor: {pascal_name}Interactor):
        self._interactor = interactor
        self._presenter = {pascal_name}Presenter()

    async def handle_request(self, request_data: dict) -> dict:
        # Tự động unpack data nếu có tham số, tránh lỗi khi DTO thêm trường bắt buộc
        input_data = {pascal_name}Input(**request_data) if request_data else {pascal_name}Input()
        output_data = await self._interactor.execute(input_data)
        return self._presenter.present(output_data)
"""

    @staticmethod
    def get_presenter_template(
        pascal_name: str, snake_name: str, group: str = ""
    ) -> str:
        usecase_subpath = f"{group}.{snake_name}" if group else snake_name
        return f"""
from src.layer_02_usecases.usecases.{usecase_subpath}.{snake_name}_dto import {pascal_name}Output

class {pascal_name}Presenter:
    def present(self, output: {pascal_name}Output) -> dict:
        return {{"status": output.status, "message": output.message}}
"""

    @staticmethod
    def get_outbound_data_source_interface_template(pascal_name: str) -> str:
        return f"""
from abc import ABC, abstractmethod
from typing import Any

class I{pascal_name}DataSource(ABC):
    @abstractmethod
    async def save(self, data: Any) -> Any:
        pass
"""

    @staticmethod
    def get_repository_template(pascal_name: str, snake_name: str) -> str:
        return f"""
from src.layer_02_usecases.gateways_interface.i_{snake_name}_repository import I{pascal_name}Repository
from src.layer_03_interface_adapters.gateways.outbound.i_{snake_name}_data_source import I{pascal_name}DataSource

class {pascal_name}Repository(I{pascal_name}Repository):
    def __init__(self, data_source: I{pascal_name}DataSource):
        self._data_source = data_source

    async def save_db(self, data):
        await self._data_source.save(data)
"""

    @staticmethod
    def get_data_source_impl_template(
        pascal_name: str, snake_name: str, tech: str
    ) -> str:
        if tech.lower() == "sqlite":
            class_name = f"Sqlite{pascal_name}DataSource"
            import_part = "import sqlite3\nfrom src.config import DB_SQLITE_PATH\n"
            init_part = f"""    def __init__(self, conn=None):
        if conn is None:
            self._conn = sqlite3.connect(DB_SQLITE_PATH, check_same_thread=False)
        else:
            self._conn = conn
"""
            save_logic = f"""        logger.info("Saving data via SQLite...")
        cursor = self._conn.cursor()
        # TODO: SQL logic
        self._conn.commit()
        return {{'id': 1, **data}}"""
        elif tech.lower() == "postgres":
            class_name = f"Postgres{pascal_name}DataSource"
            import_part = (
                "from typing import Any\nfrom src.config import DB_POSTGRES_URL\n"
            )
            init_part = f"""    def __init__(self, conn=None):
        self._conn = conn or DB_POSTGRES_URL
"""
            save_logic = f"""        logger.info("Saving data via PostgreSQL...")
        # TODO: Postgres SQL logic
        return {{'id': 99, **data}}"""
        elif tech.lower() == "mongodb":
            class_name = f"Mongodb{pascal_name}DataSource"
            import_part = (
                "from typing import Any\nfrom src.config import DB_MONGODB_URL\n"
            )
            init_part = f"""    def __init__(self, conn=None):
        self._conn = conn or DB_MONGODB_URL
"""
            save_logic = f"""        logger.info("Saving data via MongoDB...")
        # TODO: MongoDB logic
        return {{'id': 'mongo_id_1', **data}}"""
        elif tech.lower() == "redis":
            class_name = f"Redis{pascal_name}DataSource"
            import_part = (
                "from typing import Any\nfrom src.config import DB_REDIS_URL\n"
            )
            init_part = f"""    def __init__(self, conn=None):
        self._conn = conn or DB_REDIS_URL
"""
            save_logic = f"""        logger.info("Saving data via Redis...")
        # TODO: Redis logic
        return {{'id': 1, **data}}"""
        elif tech.lower() == "mock":
            class_name = f"Mock{pascal_name}DataSource"
            import_part = ""
            init_part = ""
            save_logic = f"""        logger.info("Saving data to memory store...")
        return {{'id': 1, **data}}"""
        else:
            class_name = f"{tech.capitalize()}{pascal_name}DataSource"
            import_part = ""
            init_part = ""
            save_logic = f"""        logger.info(f"Saving data for {pascal_name}")
        return True"""

        return f"""{import_part}from src.shared.logger.app_logger import get_logger
from src.layer_03_interface_adapters.gateways.outbound.i_{snake_name}_data_source import I{pascal_name}DataSource

logger = get_logger(__name__)

class {class_name}(I{pascal_name}DataSource):
{init_part}
    async def save(self, data):
{save_logic}
"""

    @staticmethod
    def get_test_template(pascal_name: str, snake_name: str, group: str = "") -> str:
        usecase_subpath = f"{group}.{snake_name}" if group else snake_name
        return f"""
import pytest
import asyncio
from unittest.mock import Mock
from src.layer_02_usecases.usecases.{usecase_subpath}.{snake_name}_dto import {pascal_name}Input, {pascal_name}Output
from src.layer_02_usecases.usecases.{usecase_subpath}.{snake_name}_interactor import {pascal_name}Interactor
from src.layer_02_usecases.gateways_interface.i_{snake_name}_repository import I{pascal_name}Repository

def test_{snake_name}_success():
    mock_repo = Mock(spec=I{pascal_name}Repository)
    async def mock_save(*args, **kwargs):
        pass
    mock_repo.save_db = mock_save
    
    usecase = {pascal_name}Interactor(mock_repo)
    input_dto = {pascal_name}Input()
    
    output_dto = asyncio.run(usecase.execute(input_dto))
    
    assert isinstance(output_dto, {pascal_name}Output)
    assert output_dto.status == "success"
"""

    @staticmethod
    def get_integration_test_template(
        pascal_name: str, snake_name: str, group: str = ""
    ) -> str:
        usecase_subpath = f"{group}.{snake_name}" if group else snake_name
        return f"""import unittest
import asyncio
from unittest.mock import Mock
from src.layer_02_usecases.usecases.{usecase_subpath}.{snake_name}_interactor import {pascal_name}Interactor
from src.layer_02_usecases.gateways_interface.i_{snake_name}_repository import I{pascal_name}Repository

try:
    from src.layer_03_interface_adapters.controllers.desktop_qt6.{snake_name} import {pascal_name}Controller  # type: ignore
except ImportError:
    try:
        from src.layer_03_interface_adapters.controllers.web_fastapi.{snake_name} import {pascal_name}Controller  # type: ignore
    except ImportError:
        try:
            from src.layer_03_interface_adapters.controllers.cli.{snake_name} import {pascal_name}Controller  # type: ignore
        except ImportError:
            class {pascal_name}Controller:  # type: ignore
                def __init__(self, interactor):
                    self.interactor = interactor
                async def handle_request(self, data):
                    return {{"status": "success", "message": "Fallback controller"}}

class Test{pascal_name}IntegrationFlow(unittest.TestCase):
    def setUp(self):
        # 1. Setup mock gateway
        self.mock_repo = Mock(spec=I{pascal_name}Repository)
        async def mock_save(*args, **kwargs):
            pass
        self.mock_repo.save_db = mock_save
        
        # 2. Setup interactor and controller
        self.interactor = {pascal_name}Interactor(self.mock_repo)
        self.controller = {pascal_name}Controller(self.interactor)

    def test_integration_flow_success(self):
        # Simulate execution from Controller (entry point) through Interactor to presenter
        output_dict = asyncio.run(self.controller.handle_request({{}}))
        
        self.assertIsInstance(output_dict, dict)
        self.assertEqual(output_dict.get("status"), "success")
"""

    @staticmethod
    def get_di_container_template() -> str:
        return """class DIContainer:
    def __init__(self):
        self._services = {}
        
    def register(self, interface, implementation):
        self._services[interface] = implementation
        
    def resolve(self, interface):
        return self._services.get(interface)
"""

    @staticmethod
    def get_app_context_base_template() -> str:
        return """import os
from .di_container import DIContainer

class AppContextBase:
    def __init__(self):
        self.container = DIContainer()
        self._register_infrastructure()

    def _register_infrastructure(self):
        # <-- BIND_REPOSITORY_HERE -->
        pass
"""

    @staticmethod
    def get_app_context_desktop_template() -> str:
        return """from .app_context_base import AppContextBase
from src.layer_04_infrastructure.ui.desktop_qt6.services.theme.theme_manager import ThemeManager
from src.layer_04_infrastructure.ui.desktop_qt6.services.i18n.i18n_manager import I18nManager
from src.layer_04_infrastructure.ui.desktop_qt6.services.light_dark_mode_manager import LightDarkModeManager
from src.layer_04_infrastructure.ui.desktop_qt6.services.settings_store import SettingsStore

class AppContextDesktop(AppContextBase):
    def __init__(self):
        self.settings_store = SettingsStore()
        
        mode = self.settings_store.get("mode", "dark")
        theme = self.settings_store.get("theme", "classic")
        lang = self.settings_store.get("language", "en")
        
        self.mode_manager = LightDarkModeManager(mode)
        self.theme_manager = ThemeManager(self.mode_manager, theme)
        self.i18n_manager = I18nManager(lang)
        
        # Đăng ký tự động lưu cấu hình khi người dùng thay đổi trên giao diện
        self.mode_manager.subscribe(lambda m: self.settings_store.set("mode", m))
        self.theme_manager.subscribe(lambda t, _: self.settings_store.set("theme", t))
        self.i18n_manager.subscribe(lambda l: self.settings_store.set("language", l))
        
        super().__init__()

    def _register_infrastructure(self):
        super()._register_infrastructure()
        # <-- BIND_REPOSITORY_HERE -->
"""

    @staticmethod
    def get_app_context_web_template() -> str:
        return """from .app_context_base import AppContextBase

class AppContextWeb(AppContextBase):
    def __init__(self):
        super().__init__()

    def _register_infrastructure(self):
        super()._register_infrastructure()
        # <-- BIND_REPOSITORY_HERE -->
"""

    @staticmethod
    def get_app_context_mobile_template() -> str:
        return """from .app_context_base import AppContextBase

class AppContextMobile(AppContextBase):
    def __init__(self):
        super().__init__()

    def _register_infrastructure(self):
        super()._register_infrastructure()
        # <-- BIND_REPOSITORY_HERE -->
"""

    @staticmethod
    def get_app_context_cli_template() -> str:
        return """from .app_context_base import AppContextBase

class AppContextCLI(AppContextBase):
    def __init__(self):
        super().__init__()

    def _register_infrastructure(self):
        super()._register_infrastructure()
        # <-- BIND_REPOSITORY_HERE -->
"""

    @staticmethod
    def get_app_logger_template() -> str:
        return """import logging

def get_logger(name: str):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
"""

    @staticmethod
    def get_config_template() -> str:
        return """import os
 
# UI Debug Mode (kích hoạt F12 phân tích phần tử và F11 chụp ảnh màn hình)
DEBUG_UI = os.getenv("DEBUG_UI", "true").lower() in ("true", "1", "yes")
"""

    @staticmethod
    def get_design_token_linter_template() -> str:
        return r"""import re

class DesignTokenLinter:
    '''
    Magic Value Guard: Ensures that no hardcoded style parameters (sizing, colors, fonts)
    are present in the UI templates, forcing the use of design tokens.
    '''
    SIZE_REGEX = re.compile(r'\b(?!(?:0|100%|auto|transparent|inherit)\b)\d+(?:\.\d+)?(?:px|em|rem|vh|vw|pt)\b')
    COLOR_REGEX = re.compile(r'#(?:[0-9a-fA-F]{3,8})\b|\brgba?\(\s*\d+|\bhsl\(\s*\d+')
    FONT_REGEX = re.compile(r'font-family:\s*[\x27\x22]?(?!(?:\{FONT_FAMILY\}|\{\{\s*FONT_FAMILY\s*\}\})\b)[a-zA-Z0-9\s,-]+[\x27\x22]?;')

    @classmethod
    def lint_content(cls, content: str, file_name: str = "template") -> list[str]:
        errors = []
        cleaned_content = re.sub(r'#.*$', '', content, flags=re.MULTILINE)
        cleaned_content = re.sub(r'/\*.*?\*/', '', cleaned_content, flags=re.DOTALL)
        
        lines = cleaned_content.splitlines()
        for line_num, line in enumerate(lines, 1):
            if any(term in line for term in ["data:image", "base64", "<svg", "<path", "polyline", "Rectangle", "pos=", "size="]):
                continue
                
            for match in cls.SIZE_REGEX.finditer(line):
                start, end = match.span()
                chunk_before = line[max(0, start-10):start]
                if "{" in chunk_before or "}" in line[end:end+10]:
                    continue
                errors.append(f"[{file_name}:{line_num}] Hardcoded size '{match.group(0)}' found: '{line.strip()}'")
                
            for match in cls.COLOR_REGEX.finditer(line):
                start, end = match.span()
                chunk_before = line[max(0, start-10):start]
                if "{" in chunk_before or "}" in line[end:end+10]:
                    continue
                errors.append(f"[{file_name}:{line_num}] Hardcoded color '{match.group(0)}' found: '{line.strip()}'")
                
            for match in cls.FONT_REGEX.finditer(line):
                errors.append(f"[{file_name}:{line_num}] Hardcoded font family '{match.group(0)}' found: '{line.strip()}'")
                
        return errors
"""

    @staticmethod
    def get_test_theme_tokens_linter_template() -> str:
        return """import os
import unittest
from .design_token_linter import DesignTokenLinter

class TestThemeTokensLinter(unittest.TestCase):
    def test_lint_all_ui_templates(self):
        ui_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "src", "layer_04_infrastructure", "ui"))
        self.assertTrue(os.path.exists(ui_dir), f"UI directory not found: {ui_dir}")
        
        errors = []
        for root_path, _, files in os.walk(ui_dir):
            for file in files:
                if file.endswith((".py", ".qss", ".kv", ".html", ".css")):
                    file_path = os.path.join(root_path, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # Skip folders that define the actual raw theme presets, inspectors, managers, and base QSS resets
                    norm_path = file_path.replace("\\\\", "/")
                    if any(term in norm_path for term in [
                        "services/theme/themes",
                        "ui_inspector",
                        "theme_manager",
                        "base.qss",
                        "theme_strategy"
                    ]):
                        continue
                        
                    file_errors = DesignTokenLinter.lint_content(content, os.path.relpath(file_path, ui_dir))
                    errors.extend(file_errors)
                    
        self.assertEqual(errors, [], "UI templates contain hardcoded magic style values:\\n" + "\\n".join(errors))
"""
