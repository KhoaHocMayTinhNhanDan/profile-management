# 🏛️ Kiến trúc Clean Architecture – Hướng dẫn cho người mới

> Tài liệu này giải thích **tại sao** cấu trúc thư mục trông như vậy,  
> và những **lỗi phổ biến** cần tránh khi làm việc với dự án này.

---

## 1. Tổng quan 5 tầng

```
src/
├── layer_01_entities/           # Quy tắc nghiệp vụ thuần túy (Entity)
├── layer_02_usecases/           # Luồng xử lý nghiệp vụ (Use Case / Interactor)
├── layer_03_interface_adapters/ # Chuyển đổi dữ liệu vào/ra (Controller, Presenter, Gateway)
├── layer_04_infrastructure/     # Kỹ thuật cụ thể (Database, UI, API)
└── layer_05_bootstrap/          # Khởi tạo & Dependency Injection
```

Quy tắc quan trọng nhất: **Tầng trong không bao giờ import tầng ngoài.**  
Mũi tên phụ thuộc luôn hướng vào trong (từ tầng 4 → tầng 1).

---

## 2. ⚠️ Lưu ý quan trọng: `gateways/inbound/` và `gateways/outbound/`

Đây là điểm **dễ gây nhầm lẫn nhất** cho người mới.

### Cấu trúc thực tế của `layer_03_interface_adapters/gateways/`

```
layer_03_interface_adapters/
└── gateways/
    ├── inbound/        ← Repository IMPLEMENTATION (code thật)
    │   └── task_manager_repository.py
    └── outbound/       ← Data Source INTERFACE (hợp đồng abstract)
        └── i_task_manager_data_source.py
```

### ❌ Sai lầm phổ biến – ĐỪNG làm điều này

```
layer_03_interface_adapters/
└── gateways/
    ├── repository/     ← KHÔNG tạo thư mục này! (phá vỡ kiến trúc)
    ├── inbound/
    └── outbound/
```

> Nếu bạn thấy thiếu "repository" và tự tạo thư mục `repository/`,  
> bạn đang phá vỡ nguyên tắc Dependency Inversion của Clean Architecture.

---

## 3. Tại sao lại gọi là `inbound` và `outbound`?

Hãy tưởng tượng **Use Case (tầng 2)** là trung tâm. Mọi luồng dữ liệu được nhìn từ góc độ của nó:

```
[Giao diện/UI]  →  Controller  →  [USE CASE]  →  Repository (inbound)  →  DataSource (outbound)  →  [Database]
                                                  ↑ dữ liệu đi vào UC    ↑ dữ liệu đi ra ngoài hệ thống
```

| Thư mục | Ý nghĩa | Chứa gì |
|---|---|---|
| `gateways/inbound/` | Dữ liệu **đi vào** Use Case | **Repository implementation** – lớp trung gian giữa UC và DB |
| `gateways/outbound/` | Dữ liệu **đi ra** khỏi hệ thống | **Data Source interface** – hợp đồng abstract cho DB/API |

---

## 4. Luồng dữ liệu đầy đủ – ví dụ Task Manager

```
scripts/run/desktop/run_task_manager.py   ← Điểm khởi chạy
        │
        ▼
layer_05_bootstrap/app_context_desktop.py ← DI Container khởi tạo mọi thứ
        │
        ▼
layer_04_infrastructure/ui/desktop_qt6/task_manager_window.py  ← UI (PyQt6)
        │  gọi
        ▼
layer_03_interface_adapters/controllers/desktop/task_manager.py ← Controller
        │  tạo Input DTO, gọi
        ▼
layer_02_usecases/usecases/task_manager/task_manager_interactor.py ← Use Case
        │  gọi repository interface (I...Repository từ tầng 2)
        ▼
layer_03_interface_adapters/gateways/inbound/task_manager_repository.py
        │  (INBOUND: implement ITaskManagerRepository)
        │  gọi data source interface (I...DataSource từ tầng 3)
        ▼
layer_04_infrastructure/database/sqlite/task_manager_data_source.py
        │  (OUTBOUND: implement ITaskManagerDataSource)
        ▼
[SQLite Database: tasks.db]
```

---

## 5. Vai trò của từng file – giải thích ngắn gọn

### `layer_02_usecases/gateways_interface/i_task_manager_repository.py`
```python
# HỢP ĐỒNG cho tầng 2 – Use Case chỉ biết đến interface này
class ITaskManagerRepository(ABC):
    def get_all_tasks(self) -> list: ...
    def add_task(self, title: str) -> dict: ...
```
→ Use Case phụ thuộc vào **abstract này**, không phụ thuộc vào implementation cụ thể.

---

### `layer_03_interface_adapters/gateways/inbound/task_manager_repository.py`
```python
# IMPLEMENTATION của ITaskManagerRepository
class TaskManagerRepository(ITaskManagerRepository):
    def __init__(self, data_source: ITaskManagerDataSource):
        self._data_source = data_source   # nhận data source qua DI

    def get_all_tasks(self):
        return self._data_source.fetch_all()  # ủy quyền cho data source
```
→ Đây là **cầu nối** giữa Use Case và Database. Nằm ở **inbound** vì nó phục vụ Use Case.

---

### `layer_03_interface_adapters/gateways/outbound/i_task_manager_data_source.py`
```python
# HỢP ĐỒNG cho data source – có thể là SQLite, PostgreSQL, API...
class ITaskManagerDataSource(ABC):
    def fetch_all(self) -> list: ...
    def insert(self, title: str) -> dict: ...
```
→ Nằm ở **outbound** vì nó là cổng đi ra bên ngoài hệ thống (DB/API).

---

### `layer_04_infrastructure/database/sqlite/task_manager_data_source.py`
```python
# IMPLEMENTATION cụ thể: dùng SQLite
class SqliteTaskManagerDataSource(ITaskManagerDataSource):
    def fetch_all(self):
        # SQL thật ở đây
        return self._conn.execute("SELECT * FROM tasks").fetchall()
```
→ Đây là nơi duy nhất chứa **SQL thật / kỹ thuật cụ thể**.

---

## 6. Dependency Injection – tầng 5 Bootstrap

Tầng 5 là nơi **lắp ráp** tất cả các lớp lại với nhau:

```python
# layer_05_bootstrap/app_context_desktop.py
class AppContextDesktop(AppContextBase):
    def _register_infrastructure(self):
        # 1. Tạo data source cụ thể (SQLite)
        data_source = SqliteTaskManagerDataSource(conn)
        
        # 2. Tạo repository, inject data source vào
        repository = TaskManagerRepository(data_source)
        
        # 3. Tạo interactor (use case), inject repository vào
        interactor = TaskManagerInteractor(repository)
        
        # 4. Đăng ký vào container
        self.container.register(ITaskManagerRepository, repository)
        self.container.register(TaskManagerInteractor, interactor)
```

> Đây là lý do tại sao Use Case không bao giờ `import sqlite3` –  
> nó chỉ biết đến **interface**, còn implementation được inject từ bên ngoài.

---

## 7. Checklist khi thêm feature mới

Khi generate một feature mới (qua Project Manager hoặc thủ công), kiểm tra:

- [ ] `layer_01_entities/` – Entity có validate nghiệp vụ chưa?
- [ ] `layer_02_usecases/usecases/<feature>/` – Có đủ `_dto.py` và `_interactor.py`?
- [ ] `layer_02_usecases/gateways_interface/` – Có `i_<feature>_repository.py` (abstract)?
- [ ] `layer_03_interface_adapters/gateways/outbound/` – Có `i_<feature>_data_source.py` (abstract)?
- [ ] `layer_03_interface_adapters/gateways/inbound/` – Có `<feature>_repository.py` (implement)?
- [ ] `layer_04_infrastructure/database/<tech>/` – Có data source cụ thể?
- [ ] `layer_05_bootstrap/` – Đã wire DI Container chưa?
- [ ] `scripts/run/<platform>/run_<feature>.py` – Có runner script?

---

## 8. Cấu trúc thư mục đầy đủ

```
src/
├── layer_01_entities/
│   └── task.py                                    # Entity + validate
│
├── layer_02_usecases/
│   ├── gateways_interface/
│   │   └── i_task_manager_repository.py           # Interface (abstract)
│   └── usecases/
│       └── task_manager/
│           ├── task_manager_dto.py                # Input/Output DTO
│           └── task_manager_interactor.py         # Use Case logic
│
├── layer_03_interface_adapters/
│   ├── controllers/
│   │   ├── cli/task_manager.py
│   │   └── desktop/task_manager.py
│   ├── presenters/
│   │   ├── cli/task_manager.py
│   │   └── web/task_manager.py
│   └── gateways/
│       ├── inbound/                               # ← Repository IMPLEMENTATION
│       │   └── task_manager_repository.py
│       └── outbound/                              # ← DataSource INTERFACE
│           └── i_task_manager_data_source.py
│
├── layer_04_infrastructure/
│   ├── database/
│   │   └── sqlite/
│   │       └── task_manager_data_source.py        # SQLite implementation
│   └── ui/
│       ├── cli/commands/task_manager_cli.py
│       └── desktop_qt6/task_manager_window.py
│
└── layer_05_bootstrap/
    ├── di_container.py                            # DI Container
    ├── app_context_base.py
    ├── app_context_cli.py
    ├── app_context_desktop.py
    └── app_context_web.py

scripts/run/
├── cli/run_task_manager.py                        # Điểm chạy CLI
└── desktop/run_task_manager.py                    # Điểm chạy Desktop
```

---

*Tài liệu này được tạo tự động – cập nhật khi kiến trúc thay đổi.*
