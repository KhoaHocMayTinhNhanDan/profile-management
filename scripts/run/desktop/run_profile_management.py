import sys
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
