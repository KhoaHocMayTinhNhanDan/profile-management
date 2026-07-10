class CommonFactory:
    """
    Concrete Factory cho các template chung của Clean Architecture (Entities, UseCases, DB, Bootstrap).
    """

    @staticmethod
    def get_usecase_interactor_template(pascal_name: str, snake_name: str) -> str:
        return f'''
from src.layer_02_usecases.gateways_interface.i_{snake_name}_repository import I{pascal_name}Repository
from .{snake_name}_dto import {pascal_name}Input, {pascal_name}Output

class {pascal_name}Interactor:
    def __init__(self, repository: I{pascal_name}Repository):
        self._repository = repository

    async def execute(self, input_data: {pascal_name}Input) -> {pascal_name}Output:
        await self._repository.save_db(input_data)
        return {pascal_name}Output(status="success", message="Executed")
'''

    @staticmethod
    def get_usecase_dto_template(pascal_name: str) -> str:
        return f'''
from dataclasses import dataclass

@dataclass
class {pascal_name}Input:
    pass

@dataclass
class {pascal_name}Output:
    status: str
    message: str
'''

    @staticmethod
    def get_usecase_repository_interface_template(pascal_name: str) -> str:
        return f'''
from abc import ABC, abstractmethod
from typing import Any

class I{pascal_name}Repository(ABC):
    @abstractmethod
    async def save_db(self, data: Any) -> None:
        pass
'''

    @staticmethod
    def get_controller_template(pascal_name: str, snake_name: str, platform: str) -> str:
        return f'''
from src.layer_02_usecases.usecases.{snake_name}.{snake_name}_dto import {pascal_name}Input
from src.layer_02_usecases.usecases.{snake_name}.{snake_name}_interactor import {pascal_name}Interactor
from src.layer_03_interface_adapters.presenters.{platform}.{snake_name} import {pascal_name}Presenter

class {pascal_name}Controller:
    def __init__(self, interactor: {pascal_name}Interactor):
        self._interactor = interactor
        self._presenter = {pascal_name}Presenter()

    async def handle_request(self, request_data: dict) -> dict:
        input_data = {pascal_name}Input()
        output_data = await self._interactor.execute(input_data)
        return self._presenter.present(output_data)
'''

    @staticmethod
    def get_presenter_template(pascal_name: str, snake_name: str) -> str:
        return f'''
from src.layer_02_usecases.usecases.{snake_name}.{snake_name}_dto import {pascal_name}Output

class {pascal_name}Presenter:
    def present(self, output: {pascal_name}Output) -> dict:
        return {{"status": output.status, "message": output.message}}
'''

    @staticmethod
    def get_outbound_data_source_interface_template(pascal_name: str) -> str:
        return f'''
from abc import ABC, abstractmethod
from typing import Any

class I{pascal_name}DataSource(ABC):
    @abstractmethod
    async def save(self, data: Any) -> Any:
        pass
'''

    @staticmethod
    def get_repository_template(pascal_name: str, snake_name: str) -> str:
        return f'''
from src.layer_02_usecases.gateways_interface.i_{snake_name}_repository import I{pascal_name}Repository
from src.layer_03_interface_adapters.gateways.outbound.i_{snake_name}_data_source import I{pascal_name}DataSource

class {pascal_name}Repository(I{pascal_name}Repository):
    def __init__(self, data_source: I{pascal_name}DataSource):
        self._data_source = data_source

    async def save_db(self, data):
        await self._data_source.save(data)
'''

    @staticmethod
    def get_data_source_impl_template(pascal_name: str, snake_name: str, tech: str) -> str:
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
            import_part = "from typing import Any\nfrom src.config import DB_POSTGRES_URL\n"
            init_part = f"""    def __init__(self, conn=None):
        self._conn = conn or DB_POSTGRES_URL
"""
            save_logic = f"""        logger.info("Saving data via PostgreSQL...")
        # TODO: Postgres SQL logic
        return {{'id': 99, **data}}"""
        elif tech.lower() == "mongodb":
            class_name = f"Mongodb{pascal_name}DataSource"
            import_part = "from typing import Any\nfrom src.config import DB_MONGODB_URL\n"
            init_part = f"""    def __init__(self, conn=None):
        self._conn = conn or DB_MONGODB_URL
"""
            save_logic = f"""        logger.info("Saving data via MongoDB...")
        # TODO: MongoDB logic
        return {{'id': 'mongo_id_1', **data}}"""
        elif tech.lower() == "redis":
            class_name = f"Redis{pascal_name}DataSource"
            import_part = "from typing import Any\nfrom src.config import DB_REDIS_URL\n"
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

        return f'''{import_part}from src.shared.logger.app_logger import get_logger
from src.layer_03_interface_adapters.gateways.outbound.i_{snake_name}_data_source import I{pascal_name}DataSource

logger = get_logger(__name__)

class {class_name}(I{pascal_name}DataSource):
{init_part}
    async def save(self, data):
{save_logic}
'''

    @staticmethod
    def get_test_template(pascal_name: str, snake_name: str) -> str:
        return f'''
import pytest
import asyncio
from unittest.mock import Mock
from src.layer_02_usecases.usecases.{snake_name}.{snake_name}_dto import {pascal_name}Input, {pascal_name}Output
from src.layer_02_usecases.usecases.{snake_name}.{snake_name}_interactor import {pascal_name}Interactor
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
'''

    @staticmethod
    def get_integration_test_template(pascal_name: str, snake_name: str) -> str:
        return f'''import unittest
import asyncio
from unittest.mock import Mock
from src.layer_02_usecases.usecases.{snake_name}.{snake_name}_interactor import {pascal_name}Interactor
from src.layer_03_interface_adapters.controllers.desktop.{snake_name} import {pascal_name}Controller
from src.layer_02_usecases.gateways_interface.i_{snake_name}_repository import I{pascal_name}Repository

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
'''

    @staticmethod
    def get_di_container_template() -> str:
        return '''class DIContainer:
    def __init__(self):
        self._services = {}
        
    def register(self, interface, implementation):
        self._services[interface] = implementation
        
    def resolve(self, interface):
        return self._services.get(interface)
'''

    @staticmethod
    def get_app_context_base_template() -> str:
        return '''import os
from .di_container import DIContainer

class AppContextBase:
    def __init__(self):
        self.container = DIContainer()
        self._register_infrastructure()

    def _register_infrastructure(self):
        # <-- BIND_REPOSITORY_HERE -->
        pass
'''

    @staticmethod
    def get_app_context_desktop_template() -> str:
        return '''from .app_context_base import AppContextBase
from src.layer_04_infrastructure.ui.desktop_qt6.ui_services.theme.theme_manager import ThemeManager
from src.layer_04_infrastructure.ui.desktop_qt6.ui_services.i18n.i18n_manager import I18nManager
from src.layer_04_infrastructure.ui.desktop_qt6.ui_services.light_dark_mode_manager import LightDarkModeManager

class AppContextDesktop(AppContextBase):
    def __init__(self):
        self.mode_manager = LightDarkModeManager("dark")
        self.theme_manager = ThemeManager(self.mode_manager, "classic")
        self.i18n_manager = I18nManager("en")
        super().__init__()

    def _register_infrastructure(self):
        super()._register_infrastructure()
        # <-- BIND_REPOSITORY_HERE -->
'''

    @staticmethod
    def get_app_context_web_template() -> str:
        return '''from .app_context_base import AppContextBase

class AppContextWeb(AppContextBase):
    def __init__(self):
        super().__init__()

    def _register_infrastructure(self):
        super()._register_infrastructure()
        # <-- BIND_REPOSITORY_HERE -->
'''

    @staticmethod
    def get_app_context_mobile_template() -> str:
        return '''from .app_context_base import AppContextBase

class AppContextMobile(AppContextBase):
    def __init__(self):
        super().__init__()

    def _register_infrastructure(self):
        super()._register_infrastructure()
        # <-- BIND_REPOSITORY_HERE -->
'''

    @staticmethod
    def get_app_context_cli_template() -> str:
        return '''from .app_context_base import AppContextBase

class AppContextCLI(AppContextBase):
    def __init__(self):
        super().__init__()

    def _register_infrastructure(self):
        super()._register_infrastructure()
        # <-- BIND_REPOSITORY_HERE -->
'''

    @staticmethod
    def get_app_logger_template() -> str:
        return '''import logging

def get_logger(name: str):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
'''

    @staticmethod
    def get_config_template() -> str:
        return '''import os

DB_SQLITE_PATH = os.getenv("DB_SQLITE_PATH", "app.db")
DB_POSTGRES_URL = os.getenv("DB_POSTGRES_URL", "postgresql://user:pass@localhost/db")
DB_MONGODB_URL = os.getenv("DB_MONGODB_URL", "mongodb://localhost:27017")
DB_REDIS_URL = os.getenv("DB_REDIS_URL", "redis://localhost:6379")
'''
