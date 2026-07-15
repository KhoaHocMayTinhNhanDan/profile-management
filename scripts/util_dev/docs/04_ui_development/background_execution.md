# Quy chuẩn Tách biệt Logic Chạy nền (Daemon Pattern) khỏi Giao diện UI

Để đảm bảo tính ổn định và tránh lỗi đơ cứng giao diện (UI Freeze), mọi tiến trình xử lý liên tục hoặc tốn tài nguyên (ví dụ: vòng lặp đồng bộ dữ liệu, lắng nghe sự kiện từ mạng, tính toán xử lý dữ liệu lớn, giám sát hệ thống hoặc chạy tiến trình daemon 24/7) **bắt buộc phải được tách biệt hoàn toàn khỏi luồng hiển thị (UI Thread)** bằng một cơ chế chạy nền (Daemon).

### Nguyên tắc Vận hành
* **Độc lập luồng (Thread Decoupling):** UI Thread chỉ chịu trách nhiệm hiển thị giao diện và nhận tương tác từ người dùng. Logic xử lý lâu dài, vòng lặp vô hạn (Infinite Loops) hoặc các tác vụ I/O blocking của ứng dụng phải chạy độc lập trên luồng nền (Worker Thread) hoặc tiến trình riêng biệt (Subprocess/Service).
* **Mô hình Quan sát (Observer Pattern):** UI không kéo (pull) dữ liệu định kỳ từ lõi một cách chủ động trên luồng chính. Lõi xử lý nền (Daemon) sẽ chủ động đẩy (push) thông tin trạng thái và kết quả thông qua các cơ chế bất đồng bộ như Event Callbacks, Signals hoặc Message Queues.
* **Tắt máy an toàn (Graceful Shutdown):** Khi người dùng tắt ứng dụng UI, giao diện phải gửi yêu cầu dừng (stop/shutdown) đến Daemon và chờ Daemon dọn dẹp tài nguyên (lưu trạng thái hiện tại, đóng kết nối mạng, hoàn thành tác vụ đang dở dang) một cách an toàn trước khi đóng hẳn luồng UI và thoát chương trình. Tránh việc tắt giao diện đột ngột dẫn đến tắt nóng (hard kill) tiến trình nền.

### Ví dụ Mô hình Daemon Chạy nền Tổng quát
```python
# layer_04_infrastructure/external_services/app_execution_daemon.py
import threading
import time

class AppExecutionDaemon:
    """Daemon chạy nền tổng quát quản lý các tác vụ thực thi dài hạn của ứng dụng"""
    def __init__(self):
        self._running = False
        self._thread = None
        self.on_update_callback = None  # Callback đẩy dữ liệu cập nhật về UI

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self, timeout: float = 2.0):
        self._running = False
        if self._thread and self._thread.is_alive():
            # ⚠️ Tránh treo UI: Giới hạn thời gian chờ luồng kết thúc, không block vô hạn
            self._thread.join(timeout=timeout)

    def _loop(self):
        while self._running:
            # Thực thi tác vụ xử lý cốt lõi của ứng dụng tại đây
            time.sleep(1.0)
            
            # Thông báo trạng thái cập nhật mới cho phía giao diện (UI)
            if self.on_update_callback:
                self.on_update_callback({
                    "status": "ACTIVE",
                    "timestamp": time.time(),
                    "payload": {}
                })
```

### 📐 Cây Quyết định Chọn Vị trí Triển khai (Decision Tree)

Khi thiết kế tác vụ chạy nền, vị trí mã nguồn được quyết định theo sơ đồ sau:

```
Tác vụ ngắn hạn & gắn chặt với vòng đời UI?
     │
  ┌──┴──┐
  │     │
 Yes    No ➔ Tác vụ cốt lõi 24/7 & độc lập với UI hoặc dùng chung cho nhiều loại giao diện (CLI/Web/Desktop)?
  │               │
  │            ┌──┴──┐
  │            │     │
  │           Yes    No ➔ Dùng Mô hình phối hợp Lai (Hybrid Model)
  │            │
  ▼            ▼
[Vị trí 1]   [Vị trí 2]
```

#### 1. Vị trí 1: Custom Hooks (`layer_04_infrastructure/ui/<platform>/hooks/`)
* **Điều kiện áp dụng:** Vòng đời ngắn, đi kèm với màn hình (tải dữ liệu bất đồng bộ khi mở trang, bộ timer đếm ngược...).
* **Cách thực hiện:** Dùng công cụ luồng đồ họa của nền tảng (`QThread`/`QTimer` trong PyQt6, `Clock` trong Kivy).

#### 2. Vị trí 2: Dịch vụ ngoài (`layer_04_infrastructure/external_services/`)
* **Điều kiện áp dụng:** Tác vụ lõi chạy liên tục 24/7 độc lập với việc đóng/mở UI, hoặc tái sử dụng cho CLI, PyQt6, FastAPI, Kivy.
* **Cách thực hiện:** Viết bằng Python thuần (`threading`/`multiprocessing`), liên kết với UI qua Event Callbacks/Interfaces.

#### 3. Vị trí 3: Mô hình Phối hợp Lai (Hybrid Model)
* **Điều kiện áp dụng:** Tác vụ cốt lõi, xử lý nặng liên tục nhưng cần cập nhật lên giao diện (UI) theo thời gian thực.
* **Quy trình hoạt động:**
  * **External Service:** Duy trì vòng lặp dữ liệu/logic chính bằng luồng Python thuần.
  * **UI Custom Hook:** Bọc một tiến trình đồ họa (như `QThread`) đóng vai trò cầu nối (Bridge) lắng nghe (subscribe) sự kiện từ External Service, sau đó phát ra UI Signals (`pyqtSignal` / Kivy properties) để cập nhật màn hình an toàn.
