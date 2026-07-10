# AI Rules: Project Manager App

## Commands
- GUI: `python scripts/util_dev/project_manager_app/run_project_manager_app/desktop/run_desktop.py`
- CLI: `python scripts/util_dev/project_manager_app/run_project_manager_app/cli/run_cli.py`

## Scaffolding API
```python
from scripts.util_dev.project_manager_app.layer_04_infrastructure.databases.local.file_data_source import FileDataSource
from scripts.util_dev.project_manager_app.layer_03_interface_adapters.gateways.inbound.file_repository import FileRepository
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.generate_feature.generate_feature_dto import GenerateFeatureInput
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.generate_feature.generate_feature_interactor import GenerateFeatureInteractor

out = GenerateFeatureInteractor(FileRepository(FileDataSource())).execute(GenerateFeatureInput(
    feature_name="feature_name", platforms=["desktop"], db_techs=["sqlite"],
    project_root_dir="project_root", project_name="neon_trade_bot"
))
```

## Architecture Rules
1. **Dependency Direction:** Entities (L1) <- Usecases (L2) <- Adapters (L3) <- Infra (L4).
2. **L2 Isolation (No I/O in Usecase):** Usecases must not perform direct filesystem, database, or API calls. Access infra only via interfaces defined in `src/layer_02_usecases/gateways_interface/`.
3. **DI Resolution:** UI Pages (L4) must resolve controllers from the DI container context:
   - Correct: `self.controller = self.app_ctx.container.resolve(ControllerClass)`
   - Violation: `self.controller = ControllerClass(InteractorClass())`
4. **No Layer Bypassing (Anti-Shortcut):**
   - **View-Controller:** UI View must execute requests via Controller. Direct calls to Interactor from View are forbidden.
   - **Presenter Requirement:** Interactor output must be formatted via a Presenter (Layer 3) before returning to the UI View. Do not return raw Interactor DTOs directly to the View.
   - **Repository-DataSource:** Repositories must delegate data storage and remote API operations to DataSource interfaces.
5. **Decoupled Execution Threads (UI & Core Engine Separation):**
   - **Rule:** The UI Thread (main GUI thread) must never run heavy processing, continuous loops, polling, or core business execution cycles.
   - **Implementation:** All core background execution, polling, strategy loops, or heavy computing must run on independent OS background threads or daemons (placed under `src/layer_04_infrastructure/external_services/`).
   - **UI Role:** The UI should only act as a reactive viewer/monitor, pulling read-only data from the DB or responding to event-driven signals emitted by the background engines.
