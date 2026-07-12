from PyQt6.QtCore import QObject, pyqtSignal
from src.layer_03_interface_adapters.controllers.desktop.generate_document_from_template import (
    GenerateDocumentFromTemplateController,
)


class UseGenerateDocumentFromTemplate(QObject):
    """
    Custom Hook quản lý trạng thái hiển thị và luồng công việc cho tính năng GenerateDocumentFromTemplate.
    """

    data_changed = pyqtSignal(dict)
    loading = pyqtSignal(bool)
    error = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
