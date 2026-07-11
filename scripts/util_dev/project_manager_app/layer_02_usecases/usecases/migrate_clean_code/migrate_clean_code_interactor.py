import os
import re
from pathlib import Path
from scripts.util_dev.project_manager_app.layer_02_usecases.gateways_interface.i_file_repository import (
    IFileRepository,
)
from .migrate_clean_code_dto import MigrateCleanCodeInput, MigrateCleanCodeOutput

LOGGER_IMPORT = "from src.app_logger import get_logger"
LOGGER_DEF = "logger = get_logger(__name__)"


class MigrateCleanCodeInteractor:
    def __init__(self, file_repo: IFileRepository):
        self._file_repo = file_repo

    def execute(self, input_data: MigrateCleanCodeInput) -> MigrateCleanCodeOutput:
        project_root = Path(input_data.project_root)
        src_dir = project_root / "src"

        changed_interfaces = []
        changed_prints = []

        # 1. Migrate Protocol -> ABC
        interface_dirs = [
            src_dir / "layer_02_usecases" / "gateways_interface",
            src_dir
            / "layer_03_gateways"
            / "gateways"
            / "outbound",  # Thư mục cũ hoặc mới
            src_dir
            / "layer_03_interface_adapters"
            / "gateways"
            / "outbound",  # Đường dẫn thực tế
        ]

        for d in interface_dirs:
            if not d.exists():
                continue
            for f in sorted(d.glob("i_*.py")):
                if self._migrate_interface_file(f):
                    changed_interfaces.append(str(f.relative_to(project_root)))

        # 2. Migrate print -> logger
        if src_dir.exists():
            for py_file in sorted(src_dir.rglob("*.py")):
                if "__pycache__" in str(py_file):
                    continue
                if py_file.name == "app_logger.py":
                    continue
                if self._migrate_print_in_file(py_file):
                    changed_prints.append(str(py_file.relative_to(project_root)))

        success = len(changed_interfaces) > 0 or len(changed_prints) > 0
        message = f"Migration completed. Updated {len(changed_interfaces)} interface(s) and {len(changed_prints)} source file(s)."
        return MigrateCleanCodeOutput(
            success=success,
            message=message,
            changed_interfaces=changed_interfaces,
            changed_prints=changed_prints,
        )

    def _migrate_interface_file(self, path: Path) -> bool:
        if not self._file_repo.file_exists(str(path)):
            return False
        content = self._file_repo.read_file(str(path))
        original = content

        content = re.sub(
            r"from typing import Protocol, Any",
            "from abc import ABC, abstractmethod\nfrom typing import Any",
            content,
        )
        content = re.sub(
            r"from typing import Protocol",
            "from abc import ABC, abstractmethod",
            content,
        )
        content = re.sub(r"\(Protocol\):", "(ABC):", content)
        content = content.replace(
            '    """\n    Protocol for Layer 4 (Infrastructure) to implement.\n    """\n',
            '    """Abstract interface for Layer 4 (Infrastructure) to implement."""\n',
        )

        lines = content.split("\n")
        new_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            if re.match(r"^    def ", line):
                prev_non_empty = ""
                for prev in reversed(new_lines):
                    if prev.strip():
                        prev_non_empty = prev.strip()
                        break
                if prev_non_empty != "@abstractmethod":
                    new_lines.append("    @abstractmethod")
            new_lines.append(line)
            i += 1
        content = "\n".join(new_lines)
        content = re.sub(
            r"^        \.\.\.$", "        pass", content, flags=re.MULTILINE
        )

        if content != original:
            self._file_repo.write_file(str(path), content)
            return True
        return False

    def _choose_level(self, msg: str) -> str:
        low = msg.lower()
        if "error" in low or "fail" in low:
            return "error"
        if "warning" in low or "warn" in low:
            return "warning"
        if (
            "initializ" in low
            or "bootstrap" in low
            or "connect" in low
            or "starting" in low
        ):
            return "info"
        return "debug"

    def _replace_print_line(self, line: str) -> str:
        stripped = line.lstrip()
        indent = line[: len(line) - len(stripped)]

        if not stripped.startswith("print("):
            return line

        inner = stripped[6:]
        inner = inner.rstrip()
        if inner.endswith(")"):
            inner = inner[:-1]

        level = self._choose_level(inner)
        return f"{indent}logger.{level}({inner})"

    def _migrate_print_in_file(self, path: Path) -> bool:
        if not self._file_repo.file_exists(str(path)):
            return False
        content = self._file_repo.read_file(str(path))
        original = content

        if "print(" not in content:
            return False

        lines = content.split("\n")
        new_lines = [self._replace_print_line(l) for l in lines]
        content = "\n".join(new_lines)

        if content != original:
            if LOGGER_IMPORT not in content:
                insert_at = 0
                for i, line in enumerate(content.split("\n")):
                    if line.startswith("import ") or line.startswith("from "):
                        insert_at = i + 1
                lines2 = content.split("\n")
                lines2.insert(insert_at, LOGGER_IMPORT)
                lines2.insert(insert_at + 1, LOGGER_DEF)
                content = "\n".join(lines2)

        if content != original:
            self._file_repo.write_file(str(path), content)
            return True
        return False
