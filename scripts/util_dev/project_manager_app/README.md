# 🏛️ python-clean-architecture-kit

A production-ready Clean Architecture template and automated scaffolding kit designed specifically for Python applications. 

This kit enables you to build scalable, testable, and loosely-coupled applications supporting multiple platforms (CLI, Web API via FastAPI, Desktop via PyQt6, Mobile via Kivy) out of the box.

---

## 🌟 Core Features

- **Strict Layer Separation:** Structured into 5 decoupled layers conforming to Uncle Bob's Clean Architecture.
- **Automated Feature Generation:** Built-in Project Manager tool (both GUI & CLI) to instantly generate new features, including DTOs, Interactors, Repository interfaces, concrete DataSources, and unit tests.
- **Smart DI Container & Bootstrap:** Automated dependency injection registration with dependency resolving capabilities.
- **Production-Ready Scaffolding:**
  - **Async/Await Native:** Fully asynchronous from routing to database data sources.
  - **Environment-Driven Configuration:** Centralized config (`src/config.py`) loading from environment variables.
  - **Standard Logging System:** Integrated stream logging (`src/app_logger.py`) across all layers.
- **Decoupled Runners:** Platform entry-points are organized in `scripts/run/` to keep the project root clean.

---

## 📂 Project Structure

```
learn/
├── src/                                  # Application Source Code
│   ├── app_logger.py                     # Standardized Logging Helper
│   ├── config.py                         # Environment Variables Config Loader
│   ├── layer_01_entities/                # Pure Business Entities & Validation
│   ├── layer_02_usecases/                # Business Logic & Ports (Interfaces)
│   ├── layer_03_interface_adapters/      # Adapters (Controllers, Presenters, Gateways)
│   ├── layer_04_infrastructure/          # Concrete Frameworks (SQLite, PyQt6, FastAPI)
│   └── layer_05_bootstrap/               # Dependency Injection & Wiring
│
├── scripts/                              # Helper Scripts
│   ├── project_manager_app/              # The Scaffolder Application (Clean Architecture)
│   ├── run/                              # Unified Execution Directory
│   │   ├── cli/                          # CLI Runner Scripts
│   │   └── desktop/                      # PyQt6 GUI Runner Scripts
│   └── util_dev/                         # Developer Utilities
│
├── tests/                                # Automated Unit Tests (100% Mocked)
└── docs/                                 # Architecture & Development Manuals
```

---

## 🚀 Getting Started

### 1. Requirements
Install the dependencies using Poetry or pip:
```bash
pip install fastapi uvicorn PyQt6 pymongo redis pytest
```

### 2. Launch the Project Manager App
The Project Manager handles codebase operations (generating features, linting imports, saving/loading project backups, resetting workspace).

- **PyQt6 GUI Window:**
  ```bash
  python scripts/util_dev/project_manager_app/run_project_manager_app/desktop/run_desktop.py
  ```
- **CLI Shell:**
  ```bash
  python scripts/util_dev/project_manager_app/run_project_manager_app/cli/run_cli.py
  ```

### 3. Generate a New Feature
1. Open the Project Manager App.
2. Select **Generate Feature**.
3. Input your feature name in `PascalCase` (e.g., `PlaceOrder`) and select desired platforms/databases.
4. The tool will automatically generate all necessary code boilerplate, write DI bindings in `layer_05_bootstrap`, and output ready-to-run startup scripts under `scripts/run/`.

### 4. Run Unit Tests
Validate layer rules and verify interactors without touching databases:
```bash
pytest tests/
```

---

## 📖 Documentation
Check the detailed documentation in the `docs/` folder:
- [Clean Architecture Guide](file:///docs/ARCHITECTURE.md) – Detailed guide on layers, interfaces, and inbound/outbound structures.
- [Development Process Manual](file:///docs/DESIGN_PROCESS.md) – Step-by-step checklist on writing business logic.

---
*Keep your architecture clean!*
