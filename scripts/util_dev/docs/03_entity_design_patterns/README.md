# GoF Design Patterns Structural Specification (Token-Optimized)

> [!IMPORTANT]
> **AI STRICT RULES:**
> 1. **NO CODE SHORTCUTS:** Never combine multiple files into a single file. You MUST split code logically into separate files as specified in the layouts.
> 2. **STRICT DIRECTORY STRUCTURE:** You MUST create the exact directories, `__init__.py` files, and module structures defined below.
> 3. **CLEAN CODE:** Do not omit boilerplate, imports, or helper methods.
> 4. **NAMING CONVENTION (REAL-WORLD ADAPTATION):**
>    - **Role-Suffixed Patterns:** For patterns representing interchangeable behaviors, algorithms, commands, adapters, factories, decorators, handlers, visitors, observers, or similar extensible roles (e.g., Strategy, State, Command, Abstract Factory, Factory Method, Observer, Visitor, Adapter, Proxy, Decorator, Chain of Responsibility/Handler), implementation files MUST be named using the format `[domain]_[pattern_role].py`.
>      - *Example (Strategy):* `paypal_strategy.py`, `stripe_strategy.py`
>      - *Example (Abstract Factory):* `postgres_factory.py`, `sqlite_factory.py`
>      - *Example (Command):* `save_user_command.py`
>      - *Example (Chain of Responsibility):* `validation_handler.py`, `logging_handler.py`
>    - **Domain-Based Patterns:** For patterns whose primary purpose is to model domain structures or subsystem composition (e.g., Composite, Facade, Flyweight, Memento), component and subsystem files MUST use natural domain names (e.g., `folder.py`, `file.py`), while the public entry-point, abstraction, or manager class MUST retain the GoF pattern role as a suffix (e.g., `media_facade.py`, `history_caretaker.py`).
> 5. **STRICT FOLDER STRUCTURE GUARANTEE:** Even if a component package or layout directory contains only a single file (e.g., a single `facade_class.py` inside `facade/`), you **MUST** create the target subfolder and place the file inside it. **NEVER** pull files out of their designated subfolders to the parent directory.
> 6. **NO PATTERN DEGRADATION & PURITY:** Never substitute the requested GoF pattern with another pattern or a simplified implementation. **Every mandatory GoF participant MUST be represented as a separate class.** When the GoF pattern defines interchangeable concrete participants (e.g., Strategy, State, Command, Observer, Visitor, Decorator, Abstract Factory, Factory Method, Chain of Responsibility), **generate at least two concrete implementations** unless explicitly instructed otherwise. Do not generate unnecessary concrete implementations for patterns that do not require them.
> 7. **ROLE MAPPING DOCUMENTATION:** Every generated class MUST clearly correspond to an official GoF participant role. The class docstring MUST explicitly state the corresponding official GoF participant role (e.g., "GoF Role: ConcreteObserver").
> 8. **NO PATTERN MIXING:** Do not mix patterns (e.g., adding Singleton/Service Locator to a Factory, or State with Mediator) unless explicitly requested. Keep the design pattern implementation pure.
> 9. **SOLID COMPLIANCE:** All generated code MUST strictly comply with SOLID principles. High-level modules MUST depend only on abstractions.
> 10. **DEPENDENCY & IMPORT DIRECTION:** Dependencies MUST always point toward abstractions. Concrete implementations MUST NEVER import sibling concrete implementations, depend directly on contexts, or create circular/bidirectional dependencies. **State classes must NOT instantiate Context objects**; they should receive the context dynamically via parameter passing.
> 11. **NO STATIC DISPATCH & ANTI-PATTERNS:** For behavioral patterns, select behaviors exclusively via dynamic dispatch/polymorphism. **ALL forms of static behavior dispatching are STRICTLY FORBIDDEN**, including: `if/elif`, `switch/case`, `match/case`, `isinstance()`, `type()`, dictionary-based dispatch, string-matching reflection, or service locators.
> 12. **PYTHON INTERFACE UNIFICATION:** All abstract interface classes in Python MUST inherit from `abc.ABC` and define abstract methods using `@abc.abstractmethod`. Do not use plain classes, `NotImplementedError`-only methods, or `typing.Protocol` unless explicitly requested.
> 13. **INSTANTIATION CONTROL:** This rule applies only to Abstract Factory, Factory Method, and Builder. Client code MUST obtain product instances only through the creation mechanism defined by the pattern. Direct instantiation of concrete product classes outside the pattern boundary is prohibited.
> 14. **LAYOUT VALIDATION:**
>     All layouts define the minimum required structure. Additional files are allowed only when they improve separation of responsibilities.
>     Before completing generation, verify that:
>     - all mandatory GoF participants exist;
>     - the required folder layout is preserved;
>     - no circular dependencies/imports exist;
>     - all behavioral dispatch uses polymorphism only.
> 15. **PATTERN COMPOSITION:**
>     When a GoF Design Pattern is embedded inside another, the embedded pattern MUST remain a complete, self-contained package following this specification.
>     The composing pattern MUST interact only through the embedded package's exported Public Entry Point (see Pattern Entry Point Specification) and MUST NOT access its internal participants directly.
>     This rule applies only to nested pattern composition.
> 16. **PUBLIC PACKAGE API:**
>     Every pattern package (or wrapper package when Cấu trúc 2 is applied) MUST expose exactly one Public Entry Point to serve as its external gateway. All other internal components are considered private implementation details.
> 17. **PACKAGE EXPORTS:**
>     The package root `__init__.py` of the outermost package MUST re-export only the designated Public Entry Point through explicit imports and `__all__`. All internal subpackages MUST contain an `__init__.py` for package structure definition.


---

## Scope

This specification defines **only the internal implementation structure of GoF Design Patterns**. Application entry points, demonstration clients, test code, integration code, and project-specific bootstrapping are intentionally excluded unless explicitly requested.

> [!NOTE]
> Every GoF Design Pattern MUST be implemented as a self-contained package named using the format `[domain]_<pattern_name>_pattern/` (or `[domain]_<pattern_name>_wrapper/` when wrapped). This package represents the implementation boundary of the pattern. All mandatory GoF participants, abstractions, concrete implementations, helper modules, and internal subpackages belonging to the pattern MUST reside inside this package.

---

## 📐 Pattern Entry Point Specification (Quy chuẩn Cổng vào của Package Pattern)

Để đảm bảo tính đóng gói và ranh giới kiến trúc của từng package chứa mẫu thiết kế (Design Pattern Package), chúng ta áp dụng 2 cấu trúc chuẩn sau tùy thuộc vào việc participant gốc có đáp ứng đầy đủ vai trò Public API hay không:

### Cấu trúc 1: Tiếp cận trực tiếp qua Participant gốc (Không dùng Wrapper)
Áp dụng khi participant gốc của GoF Pattern (như `Context` trong Strategy/State, `Facade` trong Facade, `Proxy` trong Proxy) đáp ứng đầy đủ tất cả tiêu chí tại kiểm thử quyết định `Rule EP-01`.
*   **Cấu trúc thư mục:**
    ```
    [domain]_[pattern]_pattern/ (Thư mục gốc của package)
    ├── __init__.py (Chỉ export duy nhất participant gốc qua __all__)
    └── [Các thư mục con/tệp tin tùy biến theo đặc tả của từng GoF Pattern]
        └── ... (Ví dụ: context/ & strategy/ đối với Strategy Pattern; facade/ đối với Facade Pattern)
    ```

### Cấu trúc 2: Wrapper bao bọc toàn bộ Package
Áp dụng khi các participant gốc không đáp ứng đủ các tiêu chí tại `Rule EP-01` (ví dụ: cần lớp Wrapper để đơn giản hóa giao diện hoặc tự động điều phối). Phương án này giúp cô lập hoàn toàn các thành phần GoF thuần khiết bên trong một package con, tránh trộn lẫn logic nghiệp vụ/lazy-load với pattern gốc.
*   **Cấu trúc thư mục:**
    ```
    [domain]_[pattern]_wrapper/ (Thư mục package Wrapper ngoài cùng)
    │
    ├── __init__.py (Chỉ export lớp Wrapper duy nhất qua __all__)
    ├── [domain]_[pattern]_wrapper.py (Lớp Wrapper đóng vai trò Public Entry Point)
    │
    └── [domain]_[pattern]_pattern/ (Thư mục package con chứa các GoF participants thuần khiết)
        ├── __init__.py
        └── [Các thư mục con/tệp tin tùy biến theo đặc tả của từng GoF Pattern]
            └── ... (Ví dụ: factory/ & products/ đối với Abstract Factory; builder/ & director/ đối với Builder)
    ```

*   **Rule EP-01 (Public Entry Point Selection Decision Test):** Mọi package triển khai Design Pattern bắt buộc phải cung cấp đúng một Public Entry Point duy nhất được export thông qua tệp `__init__.py` của gói ngoài cùng. Entry Point được quyết định thông qua quy trình kiểm thử quyết định sau:

    1.  **Sử dụng trực tiếp participant gốc của GoF Pattern (Cấu trúc 1)** CHỈ KHI nó thỏa mãn ĐỒNG THỜI tất cả các điều kiện sau:
        *   Nó đóng vai trò là điểm truy cập chính (primary entry point) cho tương tác của client.
        *   Bản thân nó cung cấp một Public API đầy đủ và có tính liên kết chặt chẽ (complete and cohesive).
        *   Nó không yêu cầu client phải tự điều phối thủ công (manually coordinate) các thành phần tham gia GoF Pattern khác nhau.
    2.  **Trong mọi trường hợp còn lại, BẮT BUỘC sử dụng Cấu trúc 2** bằng cách tạo ra đúng một Wrapper package ngoài cùng chứa lớp Wrapper tương ứng. Lớp Wrapper này sẽ là điểm truy cập công khai duy nhất (sole Public Entry Point). Tất cả các GoF participants còn lại đều là chi tiết triển khai nội bộ (internal implementation details). Mã nguồn bên ngoài package không được sử dụng trực tiếp bất kỳ thành phần nội bộ nào của package; mọi tương tác với package phải thông qua Public Entry Point đã được chỉ định.

    > [!IMPORTANT]
    > Việc lựa chọn giữa Cấu trúc 1 và Cấu trúc 2 phụ thuộc hoàn toàn vào yêu cầu thiết kế của Public API, không phụ thuộc vào loại mẫu thiết kế GoF (Ví dụ: Không phải Strategy lúc nào cũng dùng Cấu trúc 1, và không phải Abstract Factory lúc nào cũng dùng Cấu trúc 2).

*   **Rule EP-02 (Quy định đặt tên cho Cấu trúc 1):**
    *   **Tên thư mục package:** Có hậu tố `_pattern` (Ví dụ: `theme_strategy_pattern/`).
    *   **Tên tệp tin và lớp Entry Point:** Sử dụng tên vai trò gốc của GoF (Ví dụ: tệp `theme_context.py` chứa lớp `ThemeContext`).
*   **Rule EP-03 (Quy định đặt tên cho Cấu trúc 2):**
    *   **Tên thư mục package ngoài cùng:** Có hậu tố `_wrapper` (Ví dụ: `scaffold_factory_wrapper/`).
    *   **Tên Class Wrapper:** Phải phản ánh đúng vai trò nghiệp vụ (Ví dụ: `ScaffoldFactoryWrapper`, `TemplateRenderer`, `CommandDispatcher`).
    *   **Tên tệp tin Wrapper:** Trùng tên với thư mục package ngoài cùng: `[domain]_[pattern]_wrapper.py` (Ví dụ: `scaffold_factory_wrapper.py`).
    *   **Tên thư mục package con chứa Pattern:** Có hậu tố `_pattern` (Ví dụ: `scaffold_factory_pattern/`), nằm trực tiếp bên trong package Wrapper.

---

## 🗺️ GoF Design Patterns Index

Tùy vào nhóm thiết kế bạn cần tìm, hãy chọn đúng tài liệu hướng dẫn cụ thể:
* [1. Creational Patterns](patterns/creational.md) (Abstract Factory, Builder, Factory Method, Prototype, Singleton)
* [2. Structural Patterns](patterns/structural.md) (Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy)
* [3. Behavioral Patterns](patterns/behavioral.md) (Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor)
