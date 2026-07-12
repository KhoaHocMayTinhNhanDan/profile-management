import sys
import os

# scripts/run/desktop/ la 3 cap sau project root -> can ../../../
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
)


def main():
    try:
        from PyQt6.QtWidgets import QApplication
    except ImportError:
        print("Loi: Thu vien PyQt6 chua duoc cai dat! Vui long chay: pip install PyQt6")
        sys.exit(1)

    from src.layer_05_bootstrap.app_context_desktop import AppContextDesktop
    from src.layer_04_infrastructure.ui.desktop_qt6.main_window import MainWindow

    # Clear stale locks at startup for single-user desktop experience
    try:
        from src.layer_04_infrastructure.databases.sqlite.sqlite_document_store import (
            SqliteDocumentStore,
        )

        store = SqliteDocumentStore()
        profiles = store.list_documents("profiles")
        for profile in profiles:
            updated = False
            for doc in profile.get("documents", []):
                if doc.get("is_locked"):
                    doc["is_locked"] = False
                    doc["locked_by"] = ""
                    updated = True
            if updated:
                store.set_document("profiles", profile["profile_id"], profile)
    except Exception as e:
        print(f"Lỗi dọn dẹp khóa thừa lúc khởi động: {e}")

    root_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..")
    )
    app = QApplication(sys.argv)
    context = AppContextDesktop()
    window = MainWindow(context)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
