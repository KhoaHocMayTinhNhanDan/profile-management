import sys
import os

# Add project root to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..")))

def main():
    try:
        from PyQt6.QtWidgets import QApplication
    except ImportError:
        print("Loi: Thu vien PyQt6 chua duoc cai dat! Vui long chay: pip install PyQt6")
        sys.exit(1)

    from scripts.util_dev.project_manager_app.layer_04_infrastructure.ui.desktop_qt6.main_window import MainWindow

    app = QApplication(sys.argv)
    
    # Force QMessageBox to have readable text and light background
    app.setStyleSheet("""
        QMessageBox {
            background-color: #f0f0f0;
        }
        QMessageBox QLabel {
            color: #000000;
            font-size: 13px;
        }
        QMessageBox QPushButton {
            background-color: #e0e0e0;
            color: #000000;
            border: 1px solid #ababab;
            border-radius: 4px;
            padding: 5px 15px;
            min-width: 70px;
        }
        QMessageBox QPushButton:hover {
            background-color: #d0d0d0;
        }
    """)
    
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))
    window = MainWindow(project_root)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
