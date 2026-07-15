class DesktopTkinterFactory:
    """
    Concrete Factory tạo UI templates cho Desktop Tkinter.
    """

    @staticmethod
    def get_ui_tkinter_template(pascal_name: str, snake_name: str) -> str:
        return f"""
import tkinter as tk

class {pascal_name}Page(tk.Frame):
    def __init__(self, parent, context):
        super().__init__(parent)
        self.context = context
        
        lbl = tk.Label(self, text="Màn hình {pascal_name} - Tkinter", font=("Arial", 16))
        lbl.pack(pady=20)
        
        btn = tk.Button(self, text="Thực thi {pascal_name}")
        btn.pack()
"""
