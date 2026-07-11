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

### Lựa chọn Vị trí Triển khai Kiến trúc (UI Hooks vs External Services)
Dựa trên mục đích và phạm vi sử dụng, việc đặt mã nguồn chạy nền sẽ được phân chia vào hai vị trí cụ thể trong Tầng 4 (Infrastructure):

1. **Triển khai trực tiếp tại Custom Hooks (`layer_04_infrastructure/ui/<platform>/hooks/`):**
   * **Trường hợp áp dụng:** Các tác vụ chạy nền có vòng đời ngắn, gắn liền với vòng đời của giao diện hiển thị (ví dụ: tải dữ liệu bất đồng bộ khi mở trang, đồng bộ nhẹ dữ liệu UI, chạy một bộ timer đếm ngược trên màn hình).
   * **Cách thực hiện:** Sử dụng các công cụ luồng của chính nền tảng đồ họa đó (ví dụ: `QThread` / `QTimer` trong PyQt6, `Clock` / `threading` trong Kivy).

2. **Triển khai tại Dịch vụ ngoài (`layer_04_infrastructure/external_services/`):**
   * **Trường hợp áp dụng:** Tác vụ chạy nền mang tính chất cốt lõi của ứng dụng, cần hoạt động liên tục 24/7 độc lập với việc giao diện UI đóng/mở, hoặc cần tái sử dụng chung cho nhiều loại giao diện đầu ra khác nhau (CLI, PyQt6, FastAPI, Kivy).
   * **Cách thực hiện:** Triển khai bằng Python thuần (sử dụng module `threading` hoặc `multiprocessing` chuẩn) không phụ thuộc vào bất kỳ thư viện giao diện nào, sau đó liên kết với UI thông qua Callback Interface.

3. **Mô hình Phối hợp Lai (Hybrid / Collaborative Model):**
   * **Trường hợp áp dụng:** Đây là mô hình phổ biến và tối ưu nhất cho các ứng dụng phức tạp. Lõi xử lý nặng chạy liên tục dưới dạng **Dịch vụ ngoài (External Service)**, nhưng giao diện UI cần một **Custom Hook** đóng vai trò làm "cầu nối" (Bridge).
   * **Cách hoạt động:**
     * **External Service:** Duy trì vòng lặp dữ liệu/logic chính bằng luồng Python thuần.
     * **UI Custom Hook:** Khởi chạy một tiến trình/luồng đồ họa của riêng UI (như `QThread` trong PyQt6) chỉ để đăng ký lắng nghe (subscribe) sự kiện từ External Service, chuyển đổi dữ liệu thô nhận được thành các UI Signals (`pyqtSignal` hoặc Kivy properties) để cập nhật giao diện một cách an toàn mà không gây xung đột xung nhịp giữa hai bên.
