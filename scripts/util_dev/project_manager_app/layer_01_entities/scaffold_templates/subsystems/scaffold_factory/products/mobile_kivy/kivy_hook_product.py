from ..abstract.i_hook_product import AbstractHook


class KivyHook(AbstractHook):
    def get_async_template(self) -> str:
        return '''import threading
from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivy.clock import Clock

class UseAsync(EventDispatcher):
    """
    Custom Hook tổng quát hóa hỗ trợ chạy bất đồng bộ mọi tác vụ IO/CPU nặng trên Mobile Kivy.
    """
    loading = BooleanProperty(False)
    success = BooleanProperty(False)
    result = ObjectProperty(None)
    error_msg = StringProperty("")

    def execute(self, fn, *args, **kwargs) -> bool:
        if self.loading:
            return False
        self.loading = True
        self.success = False
        self.result = None
        self.error_msg = ""
        
        def job():
            try:
                res = fn(*args, **kwargs)
                Clock.schedule_once(lambda dt: self._on_finished(True, res, ""))
            except Exception as e:
                Clock.schedule_once(lambda dt: self._on_finished(False, None, str(e)))
                
        threading.Thread(target=job, daemon=True).start()
        return True

    def _on_finished(self, success, result, error_msg):
        self.loading = False
        self.success = success
        self.result = result
        self.error_msg = error_msg
'''

    def get_feature_template(self, pascal_name: str, snake_name: str) -> str:
        return f'''from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty, DictProperty, StringProperty
from src.layer_03_interface_adapters.controllers.mobile.{snake_name} import {pascal_name}Controller

class Use{pascal_name}(EventDispatcher):
    """
    Custom Hook quản lý trạng thái hiển thị và luồng công việc cho tính năng {pascal_name} trên Kivy.
    """
    loading = BooleanProperty(False)
    error_msg = StringProperty("")
    data = DictProperty({{}})
'''
