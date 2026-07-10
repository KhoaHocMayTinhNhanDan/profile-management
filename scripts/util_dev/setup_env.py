import os
import sys
import subprocess
import json

def run_command(command, shell=False):
    print(f"Executing: {' '.join(command) if isinstance(command, list) else command}")
    try:
        subprocess.run(command, check=True, shell=shell)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return False
    return True

def main():
    # Set console code page to UTF-8 on Windows to prevent UnicodeEncodeError
    if os.name == "nt":
        os.system("chcp 65001 > nul 2>&1")
        
    print("=== Python Clean Architecture Kit Setup ===")
    
    # 1. Initialize virtual environment (.venv)
    if not os.path.exists(".venv"):
        print("Creating virtual environment (.venv)...")
        if not run_command([sys.executable, "-m", "venv", ".venv"]):
            print("Failed to create virtual environment.")
            return
    else:
        print("Virtual environment (.venv) already exists.")

    # 2. Determine python/pip paths in venv
    if os.name == "nt":  # Windows
        python_bin = os.path.join(".venv", "Scripts", "python.exe")
        pip_bin = os.path.join(".venv", "Scripts", "pip.exe")
    else:  # Linux/macOS
        python_bin = os.path.join(".venv", "bin", "python")
        pip_bin = os.path.join(".venv", "bin", "pip")

    # 3. Upgrade pip and install core dependencies
    print("Upgrading pip in virtual environment...")
    run_command([python_bin, "-m", "pip", "install", "--upgrade", "pip"])

    print("Installing required libraries (FastAPI, PyQt6, pytest, black, pyinstaller)...")
    requirements = [
        "fastapi",
        "uvicorn",
        "PyQt6",
        "pytest",
        "pymongo",
        "redis",
        "black",
        "pyinstaller"
    ]
    
    # If a package is locked on Windows, we notify the user.
    if not run_command([pip_bin, "install"] + requirements):
        print("\n[WARNING] Some files are locked by VS Code or another python process.")
        print("Please close VS Code and run: .venv\\Scripts\\pip.exe install " + " ".join(requirements))

    # 4. Configure VS Code Settings
    vscode_dir = ".vscode"
    os.makedirs(vscode_dir, exist_ok=True)
    settings_file = os.path.join(vscode_dir, "settings.json")
    
    settings = {}
    if os.path.exists(settings_file):
        try:
            with open(settings_file, "r") as f:
                settings = json.load(f)
        except json.JSONDecodeError:
            pass

    # Automatically set Python interpreter for VS Code
    settings["python.defaultInterpreterPath"] = "${workspaceFolder}/" + python_bin.replace("\\", "/")
    settings["python.analysis.extraPaths"] = ["${workspaceFolder}"]
    settings["python.autoComplete.extraPaths"] = ["${workspaceFolder}"]
    settings["python.languageServer"] = "Jedi"
    settings["editor.semanticHighlighting.enabled"] = True

    with open(settings_file, "w") as f:
        json.dump(settings, f, indent=4)
    print("Configured VS Code settings successfully.")

    print("\n=== Setup Completed! ===")
    print("NOTE: Please reload VS Code window (Developer: Reload Window) for changes to take effect.")

if __name__ == "__main__":
    main()
