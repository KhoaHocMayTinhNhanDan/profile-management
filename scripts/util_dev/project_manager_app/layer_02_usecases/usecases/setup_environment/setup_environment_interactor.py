import os
import sys
import subprocess
from typing import Callable, Optional
from .setup_environment_dto import SetupEnvironmentInput, SetupEnvironmentOutput


class SetupEnvironmentInteractor:
    def __init__(self):
        self._log_callback: Optional[Callable[[str], None]] = None

    def _log(self, message: str):
        if self._log_callback:
            self._log_callback(message)
        else:
            print(message)

    def _run_command(self, command, shell=False) -> bool:
        cmd_str = " ".join(command) if isinstance(command, list) else command
        self._log(f"Executing: {cmd_str}")
        try:
            process = subprocess.Popen(
                command,
                shell=shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                encoding="utf-8",
                errors="replace",
            )

            # Đọc output theo thời gian thực
            if process.stdout:
                for line in process.stdout:
                    cleaned_line = line.rstrip()
                    if cleaned_line:
                        self._log(cleaned_line)

            process.wait()
            if process.returncode != 0:
                self._log(f"Command exited with code {process.returncode}")
                return False
        except Exception as e:
            self._log(f"Error executing command: {e}")
            return False
        return True

    def execute(self, input_data: SetupEnvironmentInput) -> SetupEnvironmentOutput:
        self._log_callback = input_data.log_callback

        if os.name == "nt":
            os.system("chcp 65001 > nul 2>&1")

        self._log("=== Python Clean Architecture Kit Setup ===")

        # 1. Initialize virtual environment (.venv)
        if not os.path.exists(".venv"):
            self._log("Creating virtual environment (.venv)...")
            if not self._run_command([sys.executable, "-m", "venv", ".venv"]):
                return SetupEnvironmentOutput(
                    success=False, message="Failed to create virtual environment."
                )
        else:
            self._log("Virtual environment (.venv) already exists.")

        # 2. Determine python/pip paths in venv
        if os.name == "nt":  # Windows
            python_bin = os.path.join(".venv", "Scripts", "python.exe")
            pip_bin = os.path.join(".venv", "Scripts", "pip.exe")
        else:  # Linux/macOS
            python_bin = os.path.join(".venv", "bin", "python")
            pip_bin = os.path.join(".venv", "bin", "pip")

        # 3. Upgrade pip and install core dependencies
        self._log("Upgrading pip in virtual environment...")
        self._run_command([python_bin, "-m", "pip", "install", "--upgrade", "pip"])

        self._log(
            "Installing required libraries (FastAPI, PyQt6, pytest, black, pyinstaller, pyright, rope)..."
        )
        requirements = [
            "fastapi",
            "uvicorn",
            "PyQt6",
            "pytest",
            "pymongo",
            "redis",
            "black",
            "pyinstaller",
            "pyright",
            "rope",
        ]

        if not self._run_command([pip_bin, "install"] + requirements):
            msg = (
                "[WARNING] Some files are locked by VS Code or another python process. "
                "Please close VS Code and run: .venv\\Scripts\\pip.exe install "
                + " ".join(requirements)
            )
            return SetupEnvironmentOutput(success=False, message=msg)

        return SetupEnvironmentOutput(
            success=True, message="Environment setup completed successfully!"
        )
