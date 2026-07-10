# Clean Architecture Directory Structure Rules

> [!IMPORTANT]
> **STRICT ARCHITECTURAL DIRECTORY RULES (MANDATORY)**
> This document enforces strict boundaries on where files and folders are allowed to exist. Both human developers and AI models MUST follow this specification to prevent architectural decay.

---

## 1. Zero Custom Root-Level Directories in Layer 4 (Infrastructure)

The **Layer 4 (Infrastructure)** is strictly limited to the following **five (5) standard subfolders**. Creating any other custom directory directly under `layer_04_infrastructure/` is **STRICTLY FORBIDDEN**.

```
layer_04_infrastructure/
├── databases/         # Local/remote physical databases (e.g., sqlite/, postgres/)
├── devices/           # Hardware integrations, sensors, local OS resources
├── external_services/ # API clients, SDKs, external integrations (e.g., binance/, high_performance_calc/)
├── ui/                # User Interfaces (e.g., desktop_qt6/, cli/)
└── web_drivers/       # Web automation drivers (e.g., selenium/, playwright/)
```

> [!IMPORTANT]
> **SELF-DOCUMENTING STRUCTURE (SCREAMING ARCHITECTURE)**
> To preserve the self-documenting nature of the project structure, all five (5) directories MUST be created under `layer_04_infrastructure/` upon project initialization, each containing a `.gitkeep` placeholder file even if currently unused.

### ❌ Forbidden Custom Directories
*   `layer_04_infrastructure/high_performance_calc/` ➔ **FORBIDDEN**. Must be moved under `external_services/high_performance_calc/`.
*   `layer_04_infrastructure/my_custom_api/` ➔ **FORBIDDEN**. Must be moved under `external_services/my_custom_api/`.
*   `layer_04_infrastructure/temp_cache/` ➔ **FORBIDDEN**.

---

## 2. Zero Custom Root-Level Directories in Layer 3 (Interface Adapters)

The **Layer 3 (Interface Adapters)** is strictly limited to the following subfolders:

```
layer_03_interface_adapters/
├── controllers/       # Handles incoming request mapping (e.g., cli/, desktop/)
├── presenters/        # Formats output data for UI rendering
└── gateways/          # Core adapters bridging Use Cases and Infrastructure
    ├── inbound/       # Repository implementations (ONLY)
    └── outbound/      # Data source abstract interfaces (ONLY)
```

### ❌ Forbidden Custom Directories
*   `layer_03_interface_adapters/gateways/repository/` ➔ **FORBIDDEN**.
*   `layer_03_interface_adapters/gateways/data_source/` ➔ **FORBIDDEN**.
*   `layer_03_interface_adapters/custom_adapters/` ➔ **FORBIDDEN**.

---

## 3. Strict Boundary Rules for Hybrid Languages (Rust / C++)

If you compile or include external performance engines (Rust/C++) in the project, they must act as **Infrastructure Drivers** and obey the following layout guidelines:

1.  **Placement:** The source code and binary assets (e.g., `.pyd`, `.so`, `.dll`) MUST be isolated inside the appropriate subfolder of Layer 4. (For example, a high-performance calculating engine compiled from Rust belongs under `layer_04_infrastructure/external_services/high_performance_calc/`).
2.  **Interface Compliance:** Never let Layer 2 (Use Cases) or Layer 3 (Adapters) import the compiled libraries directly. You MUST write a Python Adapter class inside Layer 4 implementing the outbound data source interface defined in Layer 3, converting low-level C-types or Rust objects into Python Entity structures.
