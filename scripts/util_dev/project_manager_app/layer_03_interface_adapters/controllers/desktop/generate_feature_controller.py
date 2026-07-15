import argparse
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.generate_feature.generate_feature_interactor import (
    GenerateFeatureInteractor,
)
from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.generate_feature.generate_feature_dto import (
    GenerateFeatureInput,
)


class DesktopGenerateFeatureController:
    def __init__(self, interactor: GenerateFeatureInteractor):
        self._interactor = interactor

    def execute(
        self, args: argparse.Namespace, project_root_dir: str, project_name: str = ""
    ):
        feature_name = args.name
        platforms = args.platforms.split(",") if args.platforms else []
        db_techs = args.db.split(",") if args.db else []
        color_palette = getattr(args, "color_palette", "Catppuccin_Mocha")
        theme = getattr(args, "theme", "default_theme")
        group_name = getattr(args, "group", "")

        input_data = GenerateFeatureInput(
            feature_name=feature_name,
            platforms=[p.strip() for p in platforms if p.strip()],
            db_techs=[db.strip() for db in db_techs if db.strip()],
            project_root_dir=project_root_dir,
            project_name=project_name,
            group_name=group_name,
            color_palette=color_palette,
            theme=theme,
        )

        output = self._interactor.execute(input_data)
        if output.status == "ok":
            print(f"✅ Success: {output.message}")
        else:
            print(f"❌ Error: {output.message}")
