# Clean Architecture Dependency & Design Rules

> [!IMPORTANT]
> **AI ARCHITECTURAL CONSTRAINTS (MANDATORY)**
> This document defines the dependencies, import boundaries, and architectural responsibilities of each layer. All generated code MUST strictly adhere to these rules.

---

## 1. The Dependency Rule (Strict Import Boundary)

Source code dependencies MUST only point inwards. **Inner layers MUST NEVER know anything about outer layers.**

```
[Layer 01: Entities] 🡠 [Layer 02: Use Cases] 🡠 [Layer 03: Adapters] 🡠 [Layer 04: Infra]
       (Purest Core)                                                      (Tech Details)
```

### ❌ Strictly Forbidden Imports (Instantly Rejected)
*   **No Outer Layer Imports:** Inner layers MUST NOT import from outer layers.
    *   *Example (in Layer 2):* `from src.layer_04_infrastructure.databases.sqlite... import ...` ➔ **VIOLATION**.
    *   *Example (in Layer 1):* `from src.layer_02_usecases... import ...` ➔ **VIOLATION**.
*   **No UI Framework Imports in Inner Layers:** Layer 1, Layer 2, and Layer 3 MUST NOT import UI/Presentation frameworks.
    *   *Example (in Layer 2 or 3):* `from PyQt6.QtWidgets import QPushButton` ➔ **VIOLATION**.
    *   *Example (in Layer 2):* `import kivy` ➔ **VIOLATION**.
*   **No Database/External Packages in Core:** Layer 1 and Layer 2 MUST NOT import libraries related to persistence, networking, or I/O.
    *   *Example (in Layer 1 or 2):* `import sqlite3`, `import requests`, `import httpx` ➔ **VIOLATION**.

---

## 2. Layer Responsibilities & Boundaries

### Layer 01: Entities (Pure Business Domain)
*   Must contain only pure Python objects, business logic, rules, and validators.
*   **Zero external dependencies** (except pure Python standard libraries like `dataclasses`, `enum`, `uuid`).
*   Must not know about databases, networks, use cases, or controllers.

### Layer 02: Use Cases (Application Logic / Interactors)
*   Orchestrates the flow of data to and from entities.
*   Must communicate with external systems (databases, APIs) **ONLY through abstract interfaces** defined in `gateways_interface/` inside this layer.
*   Must accept incoming request data via **Input DTOs** and return data via **Output DTOs**. Never pass raw entities to outer layers directly if they contain sensitive logic.

### Layer 03: Interface Adapters (Controllers, Presenters, Gateways)
*   Converts data from the format most convenient for Use Cases to the format most convenient for external agencies (UI, Databases).
*   Contains **Controllers** (handling UI/CLI input) and **Presenters** (formatting Use Case output for UI/CLI).
*   Contains **Repository implementations** (`gateways/inbound/`) which bridge Use Cases to Data Sources.

### Layer 04: Infrastructure (Technical Details)
*   Contains all framework-specific concrete code: physical UI views (PyQt6, CLI), database setups (SQLite, PostgreSQL), API clients, and network drivers.
*   This is the **ONLY** layer allowed to import databases, network libraries, or UI frameworks.

---

## 3. The Interface Rule (No Direct Dependency)

*   High-level modules (Layer 2) must not depend on low-level modules (Layer 4). Both must depend on abstractions.
*   Whenever a Use Case needs to fetch data from a database or call an external API, it MUST define an **Abstract Interface Class (ABC)** inside `layer_02_usecases/gateways_interface/`.
*   Layer 4 databases/external services MUST implement the outbound interfaces defined in Layer 3, which in turn are driven by the repository defined in Layer 2.

---

## 4. Dependency Injection Constraint (No Local Instantiation)

*   Use Cases and Interface Adapters **MUST NOT instantiate their dependencies locally**.
*   *Example (Bad):* 
    ```python
    # Inside TaskManagerInteractor
    def __init__(self):
        self.repository = TaskManagerRepository() # ❌ LOCAL INSTANTIATION VIOLATES DIP
    ```
*   *Example (Good):*
    ```python
    # Inside TaskManagerInteractor
    def __init__(self, repository: ITaskManagerRepository):
        self.repository = repository # ✅ INJECTED FROM BOOTSTRAP (Layer 5)
    ```
*   All component wiring and dependency creation MUST occur exclusively inside **Layer 05: Bootstrap** (`di_container.py` or `app_context_*.py`).
