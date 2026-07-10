"""
Script: Migrate all Protocol interfaces -> ABC + abstractmethod
         Replace all print() -> logger.debug() / logger.info()

Chạy từ thư mục gốc dự án:
    python scripts/util_dev/migrate_protocol_and_logging.py
"""
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # project root
SRC  = ROOT / "src"

# ─────────────────────────────────────────────────────────────────
# 1. Migrate Protocol → ABC trong tất cả file interface (i_*.py)
# ─────────────────────────────────────────────────────────────────

INTERFACE_DIRS = [
    SRC / "layer_02_usecases" / "gateways_interface",
    SRC / "layer_03_gateways" / "gateways" / "outbound",
]

def migrate_interface_file(path: Path) -> bool:
    """Chuyển Protocol → ABC+abstractmethod trong một file."""
    content = path.read_text(encoding="utf-8")
    original = content

    # Thay import: from typing import Protocol, Any → from abc import ABC, abstractmethod + Any
    content = re.sub(
        r"from typing import Protocol, Any",
        "from abc import ABC, abstractmethod\nfrom typing import Any",
        content
    )
    content = re.sub(
        r"from typing import Protocol",
        "from abc import ABC, abstractmethod",
        content
    )

    # Thay kế thừa: class IXxx(Protocol): → class IXxx(ABC):
    content = re.sub(
        r"\(Protocol\):",
        "(ABC):",
        content
    )

    # Xóa docstring "Protocol for Layer 4..." nếu có (không còn chính xác)
    content = content.replace(
        '    """\n    Protocol for Layer 4 (Infrastructure) to implement.\n    """\n',
        '    """Abstract interface for Layer 4 (Infrastructure) to implement."""\n'
    )

    # Thêm @abstractmethod trước mỗi def (chỉ những def là method của class - indent = 4)
    # Tìm pattern: 4 spaces + def (không có @abstractmethod trước đó)
    lines = content.split("\n")
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Nếu là method def trong class (indent = 4 spaces) và chưa có @abstractmethod
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

    # Thay ... → pass (trông rõ ràng hơn trong ABC)
    content = re.sub(r"^        \.\.\.$", "        pass", content, flags=re.MULTILINE)

    if content != original:
        path.write_text(content, encoding="utf-8")
        return True
    return False


def migrate_all_interfaces():
    changed = []
    for d in INTERFACE_DIRS:
        for f in sorted(d.glob("i_*.py")):
            if migrate_interface_file(f):
                changed.append(f.relative_to(ROOT))
    return changed


# ─────────────────────────────────────────────────────────────────
# 2. Replace print() → logger.xxx() trong toàn bộ src/
# ─────────────────────────────────────────────────────────────────

# Heuristic: print("[Layer 2]...") → logger.debug(...)
# print(f"[Layer X ...]...) → logger.debug(...)

LOGGER_IMPORT = "from src.app_logger import get_logger"
LOGGER_DEF    = 'logger = get_logger(__name__)'

def _choose_level(msg: str) -> str:
    """Chọn log level phù hợp dựa theo nội dung message."""
    low = msg.lower()
    if "error" in low or "fail" in low:
        return "error"
    if "warning" in low or "warn" in low:
        return "warning"
    if "initializ" in low or "bootstrap" in low or "connect" in low or "starting" in low:
        return "info"
    return "debug"

def _replace_print_line(line: str) -> str:
    """Thay thế một dòng print() thành logger.xxx()."""
    stripped = line.lstrip()
    indent   = line[: len(line) - len(stripped)]

    # Chỉ xử lý dòng bắt đầu bằng print(
    if not stripped.startswith("print("):
        return line

    # Lấy toàn bộ argument của print()
    inner = stripped[6:]  # bỏ "print("
    inner = inner.rstrip()
    if inner.endswith(")"):
        inner = inner[:-1]  # bỏ ")" cuối

    level = _choose_level(inner)
    return f"{indent}logger.{level}({inner})"


def migrate_print_in_file(path: Path) -> bool:
    """Thay print() → logger.xxx() trong một file .py."""
    content = path.read_text(encoding="utf-8")
    original = content

    if "print(" not in content:
        return False

    lines = content.split("\n")
    new_lines = [_replace_print_line(l) for l in lines]
    content = "\n".join(new_lines)

    # Thêm import logger nếu cần và chưa có
    if content != original:  # có thay đổi
        if LOGGER_IMPORT not in content:
            # Chèn sau dòng import đầu tiên hoặc đầu file
            insert_at = 0
            for i, line in enumerate(content.split("\n")):
                if line.startswith("import ") or line.startswith("from "):
                    insert_at = i + 1
            lines2 = content.split("\n")
            lines2.insert(insert_at, LOGGER_IMPORT)
            lines2.insert(insert_at + 1, LOGGER_DEF)
            content = "\n".join(lines2)

    if content != original:
        path.write_text(content, encoding="utf-8")
        return True
    return False


def migrate_all_prints():
    changed = []
    for py_file in sorted(SRC.rglob("*.py")):
        # Bỏ qua __pycache__ và chính file này
        if "__pycache__" in str(py_file):
            continue
        if py_file.name == "app_logger.py":
            continue
        if migrate_print_in_file(py_file):
            changed.append(py_file.relative_to(ROOT))
    return changed


# ─────────────────────────────────────────────────────────────────
# 3. Main
# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("STEP 1: Migrating Protocol → ABC")
    print("=" * 60)
    changed_interfaces = migrate_all_interfaces()
    for f in changed_interfaces:
        print(f"  ✅  {f}")
    print(f"\n  Total: {len(changed_interfaces)} interface file(s) updated.")

    print()
    print("=" * 60)
    print("STEP 2: Migrating print() → logger.xxx()")
    print("=" * 60)
    changed_prints = migrate_all_prints()
    for f in changed_prints:
        print(f"  ✅  {f}")
    print(f"\n  Total: {len(changed_prints)} source file(s) updated.")

    print()
    print("Done! Run your tests to verify.")
