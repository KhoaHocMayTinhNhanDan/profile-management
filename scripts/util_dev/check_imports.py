import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')  # type: ignore

# Add project root to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from scripts.util_dev.project_manager_app.layer_05_bootstrap.app_context_cli import AppContextCLI

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    app_ctx = AppContextCLI(root_dir)
    output = app_ctx.check_imports_controller.execute(root_dir)
    if output.status == "error":
        for v in (output.violations or []):
            print(f"❌ {v[0]}: Layer {v[1]} imports Layer {v[2]}")
        print(output.message)
        sys.exit(1)
    else:
        print(f"✅ {output.message}")
        sys.exit(0)

if __name__ == "__main__":
    main()
