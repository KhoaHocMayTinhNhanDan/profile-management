# Agent Instructions

Before writing any code, modifying any files, or performing architectural tasks, you MUST:
1. Read and strictly follow the workspace operations, formatting, and commit rules at [WORKSPACE_RULES.md](../scripts/util_dev/docs/00_workspace_rules/WORKSPACE_RULES.md).
2. Read the main index map at [README.md](../scripts/util_dev/docs/README.md) to locate and adhere to specific layer guidelines.
3. If you are modifying or creating UI components (under `layer_04_infrastructure/ui/` or `project_manager_app/layer_04_infrastructure/ui/`), you MUST:
   - Read and follow the **Atomic UI & Component Colocation** guidelines at [atomic_design.md](../scripts/util_dev/docs/04_ui_development/ui_ux_design/common_theory/atomic_design.md).
   - Read the UI/UX Guidelines Hub for layout, color, shortcuts, safe areas, and responsive principles at [ui_ux_design/README.md](../scripts/util_dev/docs/04_ui_development/ui_ux_design/README.md).
   - Read the state management rules at [state_management.md](../scripts/util_dev/docs/04_ui_development/state_management.md) and background thread rules at [background_execution.md](../scripts/util_dev/docs/04_ui_development/background_execution.md).
   - Follow the Colocated Assets rules: Always place component assets (images, icons) in a local `assets/` subfolder, and load them dynamically using `AssetsLoader.load_theme_icon(...)` or platform equivalent (for Web/Mobile). Never hardcode paths relative to the current working directory.
   - Follow the Design Prototype Loop rules: When asked to implement or modify complex UI components, you MUST first generate a visual mockup design using your image generation tool and present it to the user. Do NOT write UI code until the user approves the mockup design. After writing code, use the Visual UI Verification rule to ensure the implemented UI matches the approved mockup.
   - Follow the Visual UI Verification rules: After generating/modifying UI, run the app and press `F11` to capture a screenshot under `artifacts/ui_screenshot.png`, and visually inspect the screenshot for layout issues.
4. If you are modifying or creating domain entities (under `layer_01_entities/`), you MUST read and follow the **Entity Design Pattern** rules at [03_entity_design_patterns/README.md](../scripts/util_dev/docs/03_entity_design_patterns/README.md).
5. If you are refactoring project structures or introducing new packages, you MUST read the architecture constraints at [ARCHITECTURE_RULES.md](../scripts/util_dev/docs/01_architecture_rules/ARCHITECTURE_RULES.md) and structure rules at [PROJECT_STRUCTURE_RULES.md](../scripts/util_dev/docs/01_architecture_rules/PROJECT_STRUCTURE_RULES.md).
6. Always write code following the clean code standards and strict typing constraints documented at [CODING_RULES.md](../scripts/util_dev/docs/02_development_flow/CODING_RULES.md).
7. Whenever modifying or writing code, you MUST check if tests exist for the affected components. If tests do not exist, you MUST write them; if they exist, you MUST run them to verify correctness before finishing the task.
8. Before renaming or moving any files or directories (packages/modules), you MUST check if the built-in Project Manager Refactoring tool (`run_cli.py --rename-module` or `run_desktop.py`) supports the action. If supported, you MUST use the tool to perform the refactoring (which automatically updates all import paths system-wide) rather than manual renaming or git mv, to ensure system-wide import consistency.

