# Khái niệm Custom Hooks trong Phát triển UI

**Custom Hooks** đóng vai trò là thực thể trung gian chịu trách nhiệm đóng gói trạng thái (State) của UI và quản lý luồng tác vụ. Hệ thống sinh code tự động phân loại Hooks thành hai nhóm chính:

### A. Helper Hook Tổng Quát (`use_async.py` / `use_async.js`)
* **Mục đích**: Sinh ra một lần duy nhất tại gốc thư mục `hooks/`.
* **Vai trò**: Cung cấp cơ chế bọc luồng phụ (Thread) và bộ hẹn giờ tổng quát để thực thi *bất kỳ* hàm Python/JS IO hoặc CPU-heavy nào dưới nền mà không làm khóa (freeze) luồng đồ họa chính.
* **Cách dùng**: Page chỉ cần gọi `self.async_hook.execute(slow_function, arg1, ...)` và lắng nghe tín hiệu `finished`.

### B. Usecase Hook Riêng Biệt (`use_[usecase_name].py` / `use_[usecase_name].js`)
* **Mục đích**: Được sinh ra tự động mỗi khi bạn thêm một Feature/Usecase mới.
* **Vai trò**: Đại diện cho trạng thái và logic luồng của duy nhất tính năng đó. Nó được import và tham chiếu trực tiếp đến **Controller tương ứng ở Tầng 3** để kích hoạt các nghiệp vụ kinh doanh.
* **Cách dùng**: Page `ExchangePage` sẽ tương tác trực tiếp với `UseExchange` hook để truy xuất dữ liệu sàn và cập nhật trạng thái lên UI.

---

## Mẫu Thiết kế Hooks cho Từng Nền Tảng

### A. Desktop (PyQt6 / Qt5)
Sử dụng `QObject`, `QThread`, `QTimer` và hệ thống tín hiệu `pyqtSignal`:

```python
# hooks/use_connection.py
from PyQt6.QtCore import QObject, pyqtSignal, QThread

class ConnectionWorker(QThread):
    finished = pyqtSignal(bool, str)

    def __init__(self, exchange_id):
        super().__init__()
        self.exchange_id = exchange_id

    def run(self):
        # Giả lập hoặc thực hiện tác vụ ngầm kiểm tra kết nối API
        success = True  
        self.finished.emit(success, "Kết nối thành công")

class UseConnection(QObject):
    finished = pyqtSignal(bool, str)
    loading = pyqtSignal(bool)

    def test_api(self, exchange_id):
        self.loading.emit(True)
        self.worker = ConnectionWorker(exchange_id)
        self.worker.finished.connect(self._on_finished)
        self.worker.start()

    def _on_finished(self, success, msg):
        self.loading.emit(False)
        self.finished.emit(success, msg)
```

### B. Mobile (Kivy)
Sử dụng Kivy Properties (`NumericProperty`, `StringProperty`), `Clock` để gõ nhịp và `threading.Thread` cho luồng phụ:

```python
# hooks/use_connection.py
import threading
from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty, StringProperty
from kivy.clock import Clock

class UseConnection(EventDispatcher):
    loading = BooleanProperty(False)
    status_msg = StringProperty("")

    def test_api(self, exchange_id):
        self.loading = True
        
        def job():
            # Chạy tác vụ ngầm trên luồng phụ
            success = True
            msg = "Kết nối thành công"
            # Đưa cập nhật trạng thái về Main Thread an toàn thông qua Clock
            Clock.schedule_once(lambda dt: self._on_finished(success, msg))
            
        threading.Thread(target=job, daemon=True).start()

    def _on_finished(self, success, msg):
        self.loading = False
        self.status_msg = msg
```

### C. Web Frontend (Vanilla JS / Web Components)
Sử dụng Class EventTarget hoặc các mô hình Hook của Framework (như React/Vue):

```javascript
// hooks/useConnection.js (Vanilla JS EventTarget)
export class UseConnection extends EventTarget {
    constructor() {
        super();
        this.loading = false;
    }

    async testApi(exchangeId) {
        this.loading = true;
        this.dispatchEvent(new CustomEvent("loading", { detail: true }));

        try {
            const response = await fetch(`/api/test?exchange=${exchangeId}`);
            const data = await response.json();
            this.dispatchEvent(new CustomEvent("finished", { detail: { success: true, msg: data.message } }));
        } catch (err) {
            this.dispatchEvent(new CustomEvent("finished", { detail: { success: false, msg: err.message } }));
        } finally {
            this.loading = false;
            this.dispatchEvent(new CustomEvent("loading", { detail: false }));
        }
    }
}
```

---

## Hướng dẫn Tích hợp vào View Component

Khi kết hợp Page (View) và Hook, lập trình viên cần tuân thủ cấu trúc gắn kết sau:

1. **Khởi tạo Hook**: Hook được khởi tạo trong hàm dựng (`__init__` / `constructor`) của Page và lưu thành một thuộc tính cục bộ.
2. **Lắng nghe Tín hiệu (Subscribe/Bind)**: Đăng ký các hàm callback của Page để lắng nghe các tín hiệu thay đổi trạng thái từ Hook.
3. **Kích hoạt Hành động (Trigger)**: Khi người dùng tương tác (click nút, thay đổi giá trị nhập), Page gọi hàm tương ứng trên Hook để bắt đầu quy trình xử lý bất đồng bộ.
