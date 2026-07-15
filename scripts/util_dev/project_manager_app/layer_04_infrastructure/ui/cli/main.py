import os
import sys
import argparse

if hasattr(sys.stdout, "reconfigure"):
    getattr(sys.stdout, "reconfigure")(encoding="utf-8", errors="replace")
from scripts.util_dev.project_manager_app.layer_05_bootstrap.app_context_cli import (
    AppContextCLI,
)
from scripts.util_dev.project_manager_app.config.project_config import (
    read_project_name,
    write_project_name,
    clear_project_config,
)


def print_menu(project_name: str):
    print("\n==================================================")
    print("🛠️  CLEAN ARCHITECTURE PROJECT MANAGER")
    print(f"📦  Project đang hoạt động: [{project_name}]")
    print("==================================================")
    print("1. 🚀 Generate Feature (Sinh cấu trúc Clean Architecture)")
    print("2. 🔍 Check Imports (Kiểm tra quy tắc kiến trúc)")
    print("3. 💾 Save Project (Lưu backup dự án hiện tại)")
    print("4. 📂 Load Project (Khôi phục dự án đã lưu)")
    print("5. 📋 List Projects (Xem danh sách dự án)")
    print("6. 🧹 Reset Workspace (Xóa sạch thư mục code)")
    print("7. 🔄 Rename Module (Đổi tên/Di chuyển module)")
    print("8. 🪄 Migrate Clean Code (Chuyển Protocol ➔ ABC & print ➔ logger)")
    print("9. 🛠️ Setup Environment (Cài đặt môi trường ảo và packages)")
    print("10. ❌ Delete Project (Xóa dự án đã lưu)")
    print("0. ❌ Thoát")
    print("==================================================")


def welcome_flow(app_ctx, root_dir) -> str:
    """Màn hình chào mừng: yêu cầu tạo hoặc load project trước khi vào menu chính."""
    print("\n==================================================")
    print("🛠️  CLEAN ARCHITECTURE PROJECT MANAGER")
    print("==================================================")
    print("⚠️  Chưa có project nào đang hoạt động trong workspace.")
    print("\nBạn muốn:")
    print("  N. Tạo project mới")
    print("  L. Load project đã lưu")
    print("  0. Thoát")
    print("==================================================")

    while True:
        choice = input("👉 Chọn (N/L/0): ").strip().upper()

        if choice == "0":
            sys.exit(0)

        elif choice == "N":
            name = input("📝 Nhập tên project mới (VD: trading_bot): ").strip()
            if not name:
                print("❌ Tên project không được để trống!")
                continue
            if write_project_name(root_dir, name):
                print(f"✅ Đã khởi tạo project: [{name}]")
                return name
            else:
                print("❌ Không thể lưu cấu hình project!")
                continue

        elif choice == "L":
            projs = app_ctx.list_controller.execute()
            if not projs:
                print("❌ Chưa có project nào được lưu!")
                continue
            print("Các project đã lưu:", ", ".join(projs))
            proj = input("Nhập tên project muốn load: ").strip()
            if proj in projs:
                src_dir = os.path.join(root_dir, "src")
                tests_dir = os.path.join(root_dir, "tests")
                ok = app_ctx.load_controller.execute(proj, src_dir, tests_dir)
                if ok:
                    write_project_name(root_dir, proj)
                    print(f"✅ Đã load và kích hoạt project: [{proj}]")
                    return proj
                else:
                    print("❌ Lỗi khi load project!")
            else:
                print("❌ Không tìm thấy project!")


def main():
    root_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../../../../")
    )
    app_ctx = AppContextCLI(root_dir)
    src_dir = os.path.join(root_dir, "src")
    tests_dir = os.path.join(root_dir, "tests")

    # -------------------------------------------------------------------------
    # Non-Interactive Mode (Dành cho AI và CI/CD)
    # -------------------------------------------------------------------------
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(
            description="Clean Architecture Project Manager - Non-Interactive CLI"
        )
        parser.add_argument(
            "--project-name", type=str, help="Tên project cần kích hoạt (nếu chưa có)"
        )

        # Các hành động độc lập
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "--generate-feature",
            type=str,
            metavar="FEATURE_NAME",
            help="Sinh cấu trúc Clean Architecture cho feature",
        )
        group.add_argument(
            "--check-imports",
            action="store_true",
            help="Kiểm tra quy tắc import giữa các layer",
        )
        group.add_argument(
            "--reset-workspace",
            action="store_true",
            help="Xóa sạch workspace (src/ và tests/)",
        )
        group.add_argument(
            "--setup-env",
            action="store_true",
            help="Thiết lập môi trường ảo và cài đặt thư viện",
        )
        group.add_argument(
            "--rename-module",
            type=str,
            metavar="PATH",
            help="Đường dẫn đến module cần đổi tên/di chuyển",
        )
        group.add_argument(
            "--migrate-clean-code",
            action="store_true",
            help="Chuyển Protocol -> ABC và dọn dẹp print",
        )
        group.add_argument(
            "--save-project",
            type=str,
            metavar="NAME",
            help="Sao lưu backup project hiện tại",
        )
        group.add_argument(
            "--load-project",
            type=str,
            metavar="NAME",
            help="Khôi phục project đã sao lưu",
        )
        group.add_argument(
            "--delete-project",
            type=str,
            metavar="NAME",
            help="Xóa dự án đã sao lưu",
        )
        group.add_argument(
            "--list-projects",
            action="store_true",
            help="Xem danh sách các project đã lưu",
        )

        # Các tham số bổ trợ
        parser.add_argument(
            "--platforms",
            type=str,
            default="web",
            help="Các nền tảng (VD: web_fastapi,desktop_qt6,desktop_tauri,mobile_kivy,mobile_flutter,mobile_react_native,mobile_jetpack_compose,cli) - dùng cho --generate-feature",
        )
        parser.add_argument(
            "--db",
            type=str,
            default="sqlite",
            help="Công nghệ Database (VD: sqlite,postgres,mongodb) - dùng cho --generate-feature",
        )
        parser.add_argument(
            "--group",
            type=str,
            default="",
            help="Nhóm Usecase (VD: auth, order) - dùng cho --generate-feature",
        )
        parser.add_argument(
            "--new-name", type=str, help="Tên mới của module - dùng cho --rename-module"
        )
        parser.add_argument(
            "--theme-preset",
            "--color-palette",
            dest="color_palette",
            type=str,
            default="Catppuccin_Mocha",
            choices=[
                "Catppuccin_Mocha",
                "Dracula",
                "Nord",
                "Gruvbox",
                "Material",
                "Tokyo_Night",
                "One_Dark",
                "Rose_Pine",
                "Office_Navy",
            ],
            help="Theme preset mặc định (bao gồm cả hệ màu và cấu trúc hình học Atoms) - dùng cho --generate-feature",
        )

        parser.add_argument(
            "--theme",
            type=str,
            default="default_theme",
            help="Theme preset hình học (modern_round, flat_retro, default_theme) - dùng cho --generate-feature",
        )

        cli_args = parser.parse_args()

        # 1. Xác định hoặc kích hoạt dự án
        active_project = read_project_name(root_dir)
        if cli_args.project_name:
            write_project_name(root_dir, cli_args.project_name)
            active_project = cli_args.project_name
        elif not active_project and not (
            cli_args.setup_env
            or cli_args.reset_workspace
            or cli_args.list_projects
            or cli_args.load_project
        ):
            print(
                "❌ Lỗi: Chưa có project nào đang hoạt động. Vui lòng truyền --project-name <name> để kích hoạt trước."
            )
            sys.exit(1)

        # 2. Xử lý các lệnh
        if cli_args.generate_feature:
            gen_args = argparse.Namespace(
                name=cli_args.generate_feature,
                platforms=cli_args.platforms,
                db=cli_args.db,
                group=cli_args.group,
                color_palette=cli_args.color_palette,
                theme=cli_args.theme,
            )
            app_ctx.generate_feature_controller.execute(
                gen_args, root_dir, active_project or "project"
            )
            sys.exit(0)

        elif cli_args.check_imports:
            output = app_ctx.check_imports_controller.execute(root_dir)
            if output.status == "error":
                for v in output.violations or []:
                    print(f"❌ {v[0]}: Layer {v[1]} imports Layer {v[2]}")
                print(output.message)
                sys.exit(1)
            else:
                print(f"✅ {output.message}")
                sys.exit(0)

        elif cli_args.reset_workspace:
            ok = app_ctx.reset_controller.execute()
            if ok:
                clear_project_config(root_dir)
                print("✅ Đã xóa sạch workspace và reset project config thành công!")
                sys.exit(0)
            else:
                print("❌ Lỗi khi reset workspace!")
                sys.exit(1)

        elif cli_args.setup_env:
            res = app_ctx.setup_environment_controller.execute()
            print(f"[{'SUCCESS' if res.success else 'ERROR'}] {res.message}")
            sys.exit(0 if res.success else 1)

        elif cli_args.rename_module:
            if not cli_args.new_name:
                print("❌ Lỗi: Cần truyền --new-name <tên_mới> để đổi tên module.")
                sys.exit(1)
            res = app_ctx.rename_module_controller.execute(
                cli_args.rename_module, cli_args.new_name
            )
            print(f"[{'SUCCESS' if res.success else 'ERROR'}] {res.message}")
            sys.exit(0 if res.success else 1)

        elif cli_args.migrate_clean_code:
            res = app_ctx.migrate_clean_code_controller.execute(root_dir)
            print(f"[{'SUCCESS' if res.success else 'INFO'}] {res.message}")
            sys.exit(0 if res.success else 1)

        elif cli_args.save_project:
            print(f"💾 Đang lưu project [{cli_args.save_project}]...")
            ok = app_ctx.save_controller.execute(
                cli_args.save_project, src_dir, tests_dir
            )
            print("✅ Đã lưu!" if ok else "❌ Lỗi!")
            sys.exit(0 if ok else 1)

        elif cli_args.load_project:
            ok = app_ctx.load_controller.execute(
                cli_args.load_project, src_dir, tests_dir
            )
            if ok:
                write_project_name(root_dir, cli_args.load_project)
                print(
                    f"✅ Đã khôi phục và kích hoạt project: [{cli_args.load_project}]"
                )
                sys.exit(0)
            else:
                print("❌ Lỗi khi khôi phục project!")
                sys.exit(1)

        elif cli_args.delete_project:
            ok = app_ctx.delete_controller.execute(cli_args.delete_project)
            if ok:
                print(f"✅ Đã xóa dự án: [{cli_args.delete_project}]")
                sys.exit(0)
            else:
                print("❌ Lỗi khi xóa dự án!")
                sys.exit(1)

        elif cli_args.list_projects:
            projs = app_ctx.list_controller.execute()
            print("Các project đã lưu:", ", ".join(projs))
            sys.exit(0)

    # -------------------------------------------------------------------------
    # Interactive Mode (Dành cho Lập trình viên)
    # -------------------------------------------------------------------------
    project_name = read_project_name(root_dir)
    if not project_name:
        project_name = welcome_flow(app_ctx, root_dir)

    while True:
        print_menu(project_name)
        choice = input("👉 Chọn một chức năng (0-9): ").strip()

        if choice == "1":
            name = input("Nhập tên feature (VD: CreateOrder): ").strip()
            if not name:
                continue
            group = input(
                "Nhập Usecase Group (tùy chọn, VD: auth, order) [bỏ qua để để phẳng]: "
            ).strip()
            plat_in = input(
                "Nhập platforms (VD: web,desktop,mobile,cli) [bỏ qua để tạo web]: "
            ).strip()
            platforms = plat_in if plat_in else "web"
            db_in = input(
                "Nhập DB techs (VD: sqlite,postgres,mongodb,redis,mock) [bỏ qua để tạo sqlite]: "
            ).strip()
            db_techs = db_in if db_in else "sqlite"

            args = argparse.Namespace(
                name=name, platforms=platforms, db=db_techs, group=group
            )
            # Truyền project_name để sinh runner đúng tên dự án
            app_ctx.generate_feature_controller.execute(args, root_dir, project_name)

        elif choice == "2":
            output = app_ctx.check_imports_controller.execute(root_dir)
            if output.status == "error":
                for v in output.violations or []:
                    print(f"❌ {v[0]}: Layer {v[1]} imports Layer {v[2]}")
                print(output.message)
            else:
                print(f"✅ {output.message}")

        elif choice == "3":
            # Auto-save dùng project_name hiện tại - không hỏi lại
            print(f"💾 Đang lưu project [{project_name}]...")
            ok = app_ctx.save_controller.execute(project_name, src_dir, tests_dir)
            print("✅ Đã lưu!" if ok else "❌ Lỗi!")

        elif choice == "4":
            projs = app_ctx.list_controller.execute()
            print("Các project đã lưu:", ", ".join(projs))
            proj = input("Nhập tên project muốn load: ").strip()
            if proj in projs:
                ok = app_ctx.load_controller.execute(proj, src_dir, tests_dir)
                if ok:
                    write_project_name(root_dir, proj)
                    project_name = proj
                    print(f"✅ Đã load và kích hoạt project: [{project_name}]")
                else:
                    print("❌ Lỗi!")
            else:
                print("❌ Không tìm thấy!")

        elif choice == "5":
            projs = app_ctx.list_controller.execute()
            print("Các project đã lưu:", ", ".join(projs))

        elif choice == "6":
            print("⚠️  CẢNH BÁO: Thao tác này sẽ XÓA SẠCH thư mục src/ và tests/.")
            confirm = input("Bạn có chắc chắn? (y/N): ").strip().lower()
            if confirm == "y":
                ok = app_ctx.reset_controller.execute()
                if ok:
                    # Xóa cấu hình project hiện tại - đưa workspace về trạng thái trống
                    clear_project_config(root_dir)
                    print("✅ Đã xóa sạch workspace! Project config đã được reset.")
                    # Quay lại welcome flow để tạo project mới
                    project_name = welcome_flow(app_ctx, root_dir)
                else:
                    print("❌ Lỗi!")

        elif choice == "7":
            target_path = input(
                "Nhập đường dẫn module cần đổi tên (VD: src/layer_01_entities/old_name.py): "
            ).strip()
            new_name = input("Nhập tên mới (VD: new_name): ").strip()
            if target_path and new_name:
                res = app_ctx.rename_module_controller.execute(target_path, new_name)
                print(f"[{'SUCCESS' if res.success else 'ERROR'}] {res.message}")

        elif choice == "8":
            confirm = (
                input(
                    "⚠️  Xác nhận chạy di chuyển Protocol -> ABC và print -> logger? (y/N): "
                )
                .strip()
                .lower()
            )
            if confirm == "y":
                res = app_ctx.migrate_clean_code_controller.execute(root_dir)
                print(f"[{'SUCCESS' if res.success else 'INFO'}] {res.message}")
                if res.changed_interfaces:
                    print("Các interface được cập nhật:")
                    for f in res.changed_interfaces:
                        print(f"  ✅  {f}")
                if res.changed_prints:
                    print("Các source file được loại bỏ print:")
                    for f in res.changed_prints:
                        print(f"  ✅  {f}")

        elif choice == "9":
            confirm = (
                input("⚠️  Xác nhận cấu hình môi trường và cài đặt thư viện? (y/N): ")
                .strip()
                .lower()
            )
            if confirm == "y":
                res = app_ctx.setup_environment_controller.execute()
                print(f"[{'SUCCESS' if res.success else 'ERROR'}] {res.message}")

        elif choice == "10":
            projs = app_ctx.list_controller.execute()
            if not projs:
                print("❌ Chưa có dự án nào được lưu!")
                continue
            print("Các dự án đã lưu:", ", ".join(projs))
            proj = input("Nhập tên dự án muốn xóa: ").strip()
            if proj in projs:
                confirm = (
                    input(
                        f"⚠️ Bạn có chắc muốn xóa dự án '{proj}'? Thao tác này không thể khôi phục! (y/N): "
                    )
                    .strip()
                    .lower()
                )
                if confirm == "y":
                    ok = app_ctx.delete_controller.execute(proj)
                    if ok:
                        print(f"✅ Đã xóa dự án: [{proj}]")
                    else:
                        print("❌ Lỗi khi xóa dự án!")
            else:
                print("❌ Không tìm thấy dự án!")

        elif choice == "0":
            print("Tạm biệt!")
            break


if __name__ == "__main__":
    main()
