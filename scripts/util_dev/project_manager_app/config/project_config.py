import json
import os
from typing import Optional

CONFIG_FILENAME = "project_config.json"


def _config_path(root_dir: str) -> str:
    return os.path.join(
        root_dir,
        "scripts",
        "util_dev",
        "project_manager_app",
        "appdata",
        CONFIG_FILENAME,
    )


def _legacy_config_path(root_dir: str) -> str:
    return os.path.join(root_dir, "src", CONFIG_FILENAME)


def _read_json(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def read_project_name(root_dir: str) -> str:
    config = _read_json(_config_path(root_dir))
    project_name = config.get("project_name")
    if isinstance(project_name, str) and project_name.strip():
        return project_name.strip()

    legacy_config = _read_json(_legacy_config_path(root_dir))
    legacy_project_name = legacy_config.get("project_name")
    if isinstance(legacy_project_name, str) and legacy_project_name.strip():
        return legacy_project_name.strip()

    return ""


def write_project_name(root_dir: str, project_name: str) -> bool:
    try:
        path = _config_path(root_dir)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            json.dump({"project_name": project_name}, file, indent=4)
        return True
    except OSError:
        return False


def clear_project_config(root_dir: str) -> bool:
    ok = True
    for path in (_config_path(root_dir), _legacy_config_path(root_dir)):
        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                ok = False
    return ok
