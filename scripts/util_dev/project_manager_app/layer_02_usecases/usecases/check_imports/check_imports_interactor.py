import ast
from pathlib import Path
from typing import List, Tuple
from scripts.util_dev.project_manager_app.layer_02_usecases.gateways_interface.i_file_repository import IFileRepository
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.check_imports.check_imports_dto import CheckImportsInput, CheckImportsOutput

LAYERS = {
    'layer_01_entities': 1,
    'layer_02_usecases': 2,
    'layer_03_interface_adapters': 3,
    'layer_04_infrastructure': 4,
    'layer_05_bootstrap': 5,
}

ALLOWED_IMPORTS = {
    1: [1],
    2: [1, 2],
    3: [1, 2, 3],
    4: [1, 2, 3, 4, 5],
    5: [1, 2, 3, 4, 5],
}

class CheckImportsInteractor:
    def __init__(self, file_repo: IFileRepository):
        self._file_repo = file_repo

    def execute(self, input_data: CheckImportsInput) -> CheckImportsOutput:
        project_root = Path(input_data.project_root_dir)
        src_dir = project_root / 'src'
        
        if not src_dir.exists():
            return CheckImportsOutput("error", "src directory not found!", [])

        all_violations = []
        for py_file in src_dir.rglob('*.py'):
            violations = self._check_file(py_file)
            if violations:
                all_violations.extend(violations)

        if all_violations:
            return CheckImportsOutput("error", "Import violations found.", all_violations)
        else:
            return CheckImportsOutput("ok", "No import violations found. Architecture is clean!", [])

    def _get_layer_from_path(self, file_path: Path) -> int:
        for layer_name, layer_num in LAYERS.items():
            if layer_name in str(file_path):
                return layer_num
        return 0

    def _get_imported_modules(self, file_path: Path) -> List[str]:
        if not self._file_repo.file_exists(str(file_path)):
            return []
            
        content = self._file_repo.read_file(str(file_path))
        
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return []

        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module if node.module else ''
                if module and not module.startswith('.'):
                    imports.append(module)
        return imports

    def _get_imported_layer(self, import_module: str) -> int:
        if import_module.startswith('src.'):
            parts = import_module.split('.')
            if len(parts) >= 2:
                layer_name = parts[1]
                for ln, lnum in LAYERS.items():
                    if ln == layer_name:
                        return lnum
        for layer_name, layer_num in LAYERS.items():
            if import_module.startswith(layer_name):
                return layer_num
        return 0

    def _check_file(self, file_path: Path) -> List[Tuple[str, int, int]]:
        violations = []
        current_layer = self._get_layer_from_path(file_path)
        if current_layer == 0:
            return violations

        imported_modules = self._get_imported_modules(file_path)
        for mod in imported_modules:
            target_layer = self._get_imported_layer(mod)
            if target_layer == 0:
                continue
            if target_layer not in ALLOWED_IMPORTS.get(current_layer, []):
                violations.append((file_path.name, current_layer, target_layer))
        return violations
