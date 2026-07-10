class RunnerFactory:
    """
    Concrete Factory cho runner scripts.
    """
    @staticmethod
    def get_run_cli_template(pascal_name: str, snake_name: str) -> str:
        return f'''import sys
import os

# scripts/run/cli/ la 3 cap sau project root -> can ../../../
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from src.layer_04_infrastructure.ui.cli.commands.{snake_name}_cli import run_cli

if __name__ == "__main__":
    run_cli()
'''

    @staticmethod
    def get_run_desktop_template(pascal_name: str, snake_name: str) -> str:
        return f'''import sys
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
'''

    @staticmethod
    def get_run_cli_project_template(project_snake: str) -> str:
        """Runner script cho toàn bộ dự án CLI - đặt tên theo project, không theo feature."""
        return f'''import sys
import os

# scripts/run/cli/ la 3 cap sau project root -> can ../../../
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from src.layer_04_infrastructure.ui.cli.commands.welcome_cli import run_cli

if __name__ == "__main__":
    run_cli()
'''

    @staticmethod
    def get_run_desktop_project_template(project_snake: str) -> str:
        """Runner script cho toàn bộ dự án Desktop - đặt tên theo project, không theo feature."""
        return f'''import sys
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
'''
