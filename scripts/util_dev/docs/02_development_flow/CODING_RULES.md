# Python Clean Coding Style Rules

> [!IMPORTANT]
> **AI CODING RULES (MANDATORY)**
> This document defines coding practices, formatting, type safety, error handling, and logging protocols for the project. All generated code MUST adhere to these rules.

---

## 1. Strict Type Hints (Type Safety)

*   All function and method signatures MUST have full type annotations for parameters and return values.
*   Avoid using `Any`. Use descriptive types, `Union`, `Optional`, or generics.
*   *Example (Bad):*
    ```python
    def process_data(data):
        return data.strip()
    ```
*   *Example (Good):*
    ```python
    def process_data(data: str) -> str:
        return data.strip()
    ```
*   **Dependency Injection Type Casting & Registration:** 
    *   **Tại sao cần tránh `.resolve()` lồng nhau:** Khi đăng ký DI (ví dụ: trong `app_context_desktop.py`), việc gọi `.resolve(Interface)` để truyền vào constructor của class khác sẽ làm Pyright hiểu nhầm kiểu trả về là `Unknown` hoặc `None`, sinh lỗi `reportOptionalMemberAccess`.
    *   **Quy chuẩn Đăng ký (DI Registration - Good):** Khởi tạo tường minh thành các biến cục bộ và đăng ký lần lượt vào container. Cách này đảm bảo Pyright suy luận kiểu chính xác 100%:
        ```python
        # Tốt: Instantiation trực tiếp và truyền tham chiếu biến
        ds_task = SqliteTaskDataSource()
        self.container.register(ITaskDataSource, ds_task)
        
        repo_task = TaskRepository(ds_task)
        self.container.register(ITaskRepository, repo_task)
        
        interactor_task = TaskInteractor(repo_task)
        self.container.register(TaskInteractor, interactor_task)
        ```
    *   **Quy chuẩn Phân giải (DI Resolution - Good):** Khi resolve đối tượng trong UI hoặc Controller, hãy type annotate rõ ràng hoặc sử dụng đối tượng Class làm khóa định vị:
        ```python
        from typing import cast
        # Sử dụng cast hoặc type annotation
        self.use_case = cast(GetTasksUseCase, container.resolve(GetTasksUseCase))
        # HOẶC:
        self.use_case: GetTasksUseCase = container.resolve(GetTasksUseCase)
        ```

---

## 2. Clean Architecture Error Handling (Exceptions)

*   **No Raw Exception Leakage:** Layer 4 exceptions (such as `sqlite3.Error`, `requests.HTTPError`) MUST NOT leak into Layer 2 (Use Cases) or Layer 3. They MUST be caught in Layer 4 and translated into Domain/Application Exceptions defined in Layer 1 or 2.
*   Use custom Domain Exceptions derived from a base exception class for business failures.
*   *Example (Layer 4 Data Source):*
    ```python
    # inside SQLiteDataSource
    try:
        self.conn.execute("INSERT ...")
    except sqlite3.IntegrityError as e:
        raise DatabaseWriteError("Task already exists in storage") from e
    ```

---

## 3. Strict Logging Protocol

*   Do not use raw `print()` statements for application logging. Always use the central system logger (`app_logger.py` or standard logging module).
*   **Logging levels:**
    *   `INFO` for major system flow transitions (e.g., Use Case start/complete, server launch).
    *   `WARNING` for minor issues that can be recovered from.
    *   `ERROR` / `CRITICAL` for application crashes or failure to execute transactions.

---

## 4. Class Organization & Formatting

*   Follow PEP 8 styling strictly.
*   Keep files highly focused: One class per file by default, unless the classes are tightly coupled small helper objects (e.g., a DTO and its sub-structures).
*   Limit method lengths: No method should exceed 50 lines of executable code. If it does, refactor it into smaller, descriptive private helper methods.
*   Document every public class and method with a clear English docstring describing its responsibility.
