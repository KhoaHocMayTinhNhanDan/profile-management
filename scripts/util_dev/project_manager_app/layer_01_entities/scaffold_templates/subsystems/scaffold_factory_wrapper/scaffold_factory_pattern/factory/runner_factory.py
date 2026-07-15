class RunnerFactory:
    """
    Concrete Factory cho runner scripts.
    """

    @staticmethod
    def get_run_cli_template(pascal_name: str, snake_name: str) -> str:
        return f"""import sys
import os

# scripts/run/cli/ la 3 cap sau project root -> can ../../../
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from src.layer_04_infrastructure.ui.cli.commands.{snake_name}_cli import run_cli

if __name__ == "__main__":
    run_cli()
"""

    @staticmethod
    def get_run_desktop_template(pascal_name: str, snake_name: str) -> str:
        return f"""import sys
import os

# scripts/run/desktop/ la 3 cap sau project root -> can ../../../
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

def main():
    try:
        from PyQt6.QtWidgets import QApplication
    except ImportError:
        print("Loi: Thu vien PyQt6 chua duoc cai dat! Vui long chay: pip install PyQt6")
        sys.exit(1)

    from src.layer_05_bootstrap.app_context_desktop import AppContextDesktop
    from src.layer_04_infrastructure.ui.desktop_qt6.main_window import MainWindow

    app = QApplication(sys.argv)
    context = AppContextDesktop()
    window = MainWindow(context)
    window.switch_to_page("{snake_name}")
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
"""

    @staticmethod
    def get_run_cli_project_template(project_snake: str) -> str:
        """Runner script cho toàn bộ dự án CLI - đặt tên theo project, không theo feature."""
        return f"""import sys
import os

# scripts/run/cli/ la 3 cap sau project root -> can ../../../
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from src.layer_04_infrastructure.ui.cli.commands.welcome_cli import run_cli

if __name__ == "__main__":
    run_cli()
"""

    @staticmethod
    def get_run_desktop_project_template(project_snake: str) -> str:
        """Runner script cho toàn bộ dự án Desktop - đặt tên theo project, không theo feature."""
        return f"""import sys
import os

# scripts/run/desktop/ la 3 cap sau project root -> can ../../../
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

def main():
    try:
        from PyQt6.QtWidgets import QApplication
    except ImportError:
        print("Loi: Thu vien PyQt6 chua duoc cai dat! Vui long chay: pip install PyQt6")
        sys.exit(1)

    from src.layer_05_bootstrap.app_context_desktop import AppContextDesktop
    from src.layer_04_infrastructure.ui.desktop_qt6.main_window import MainWindow

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    app = QApplication(sys.argv)
    context = AppContextDesktop()
    window = MainWindow(context)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
"""

    @staticmethod
    def get_run_mobile_template(pascal_name: str, snake_name: str) -> str:
        return f"""import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

def main():
    try:
        import kivy
    except ImportError:
        print("Loi: Thu vien Kivy chua duoc cai dat! Vui long chay: pip install kivy")
        sys.exit(1)

    from src.layer_05_bootstrap.app_context_mobile import AppContextMobile
    from src.layer_04_infrastructure.ui.mobile_kivy.main_window import KivyApp

    context = AppContextMobile()
    app = KivyApp(context)
    app.run()

if __name__ == "__main__":
    main()
"""

    @staticmethod
    def get_run_web_template(pascal_name: str, snake_name: str) -> str:
        return f"""import sys
import os
import webbrowser
import time
import threading

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

def open_browser():
    time.sleep(1.5)
    page_route = "" if "{snake_name}" == "welcome" else "{snake_name}".replace("_", "-")
    webbrowser.open(f"http://127.0.0.1:8000/{{page_route}}")

def main():
    try:
        import uvicorn
    except ImportError:
        print("Loi: Thu vien uvicorn chua duoc cai dat! Vui long chay: pip install uvicorn fastapi")
        sys.exit(1)

    threading.Thread(target=open_browser, daemon=True).start()

    import uvicorn
    uvicorn.run("src.layer_04_infrastructure.ui.web_fastapi.fastapi.main:app", host="127.0.0.1", port=8000, reload=False)

if __name__ == "__main__":
    main()
"""

    @staticmethod
    def get_run_mobile_project_template(project_snake: str) -> str:
        return f"""import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

def main():
    try:
        import kivy
    except ImportError:
        print("Loi: Thu vien Kivy chua duoc cai dat! Vui long chay: pip install kivy")
        sys.exit(1)

    from src.layer_05_bootstrap.app_context_mobile import AppContextMobile
    from src.layer_04_infrastructure.ui.mobile_kivy.main_window import KivyApp

    context = AppContextMobile()
    app = KivyApp(context)
    app.run()

if __name__ == "__main__":
    main()
"""

    @staticmethod
    def get_run_web_project_template(project_snake: str) -> str:
        return f"""import sys
import os
import webbrowser
import time
import threading

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:8000/level_05_pages/welcome.html")

def main():
    try:
        import uvicorn
    except ImportError:
        print("Loi: Thu vien uvicorn chua duoc cai dat! Vui long chay: pip install uvicorn fastapi")
        sys.exit(1)

    threading.Thread(target=open_browser, daemon=True).start()

    import uvicorn
    uvicorn.run("src.layer_04_infrastructure.ui.web_fastapi.fastapi.main:app", host="127.0.0.1", port=8000, reload=False)

if __name__ == "__main__":
    main()
"""

    @staticmethod
    def get_run_tauri_project_template(project_snake: str) -> str:
        return f"""import sys
import os
import subprocess
import threading
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

def start_backend():
    try:
        import uvicorn
    except ImportError:
        print("Loi: Thu vien uvicorn chua duoc cai dat! Vui long chay: pip install uvicorn fastapi")
        sys.exit(1)
    uvicorn.run("src.layer_04_infrastructure.ui.web_fastapi.fastapi.main:app", host="127.0.0.1", port=8000, reload=False)

def main():
    # 1. Start backend in background thread
    threading.Thread(target=start_backend, daemon=True).start()
    time.sleep(2) # Wait for backend to start
    
    print("=" * 60)
    print("🚀 DocumentManagerApp Backend running on http://127.0.0.1:8000")
    print("🚀 Ready to launch Tauri Desktop Window...")
    print("=" * 60)
    
    # 2. Run tauri app. Try npx first to bypass local cargo compilation
    tauri_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "src", "layer_04_infrastructure", "ui", "desktop_tauri"))
    src_tauri_dir = os.path.join(tauri_dir, "src-tauri")
    
    success = False
    try:
        print("🔄 Khoi chay Tauri qua npx (phien ban dung san)...")
        res = subprocess.run(["npx", "@tauri-apps/cli@1", "dev"], cwd=src_tauri_dir, shell=True)
        if res.returncode == 0:
            success = True
    except Exception:
        pass
        
    if not success:
        print("🔄 npx that bai hoac khong co san, thu chay qua cargo tauri dev...")
        try:
            res = subprocess.run(["cargo", "tauri", "dev"], cwd=tauri_dir, shell=True)
            if res.returncode == 0:
                success = True
        except Exception:
            pass

    if not success:
        print("Loi: Khong the khoi chay Tauri tu dong.")
        print("Vui long lam theo mot trong cac cach sau:")
        print("  Cach 1 (Dung npx - khong can bien dich):")
        print(f"     cd {{src_tauri_dir}}")
        print("     npx @tauri-apps/cli@1 dev")
        print("  Cach 2 (Cai dat tauri-cli):")
        print("     cargo install tauri-cli --version '^1'")
        print(f"     cd {{tauri_dir}} && cargo tauri dev")
        
        # Keep process alive so backend keeps running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Shutting down backend...")

if __name__ == "__main__":
    main()
"""
