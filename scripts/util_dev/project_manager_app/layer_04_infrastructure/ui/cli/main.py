import os
import sys
import argparse
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from scripts.util_dev.project_manager_app.layer_05_bootstrap.app_context_cli import AppContextCLI
from scripts.util_dev.project_manager_app.config.project_config import read_project_name, write_project_name, clear_project_config

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
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../"))
    app_ctx = AppContextCLI(root_dir)
    src_dir = os.path.join(root_dir, "src")
    tests_dir = os.path.join(root_dir, "tests")
    
    # Project-Centric: Đọc state dự án hiện tại
    project_name = read_project_name(root_dir)
    if not project_name:
        project_name = welcome_flow(app_ctx, root_dir)
    
    while True:
        print_menu(project_name)
        choice = input("👉 Chọn một chức năng (0-6): ").strip()
        
        if choice == '1':
            name = input("Nhập tên feature (VD: CreateOrder): ").strip()
            if not name: continue
            plat_in = input("Nhập platforms (VD: web,desktop,mobile,cli) [bỏ qua để tạo web]: ").strip()
            platforms = plat_in if plat_in else "web"
            db_in = input("Nhập DB techs (VD: sqlite,postgres,mongodb,redis,mock) [bỏ qua để tạo sqlite]: ").strip()
            db_techs = db_in if db_in else "sqlite"
            
            args = argparse.Namespace(name=name, platforms=platforms, db=db_techs)
            # Truyền project_name để sinh runner đúng tên dự án
            app_ctx.generate_feature_controller.execute(args, root_dir, project_name)
            
        elif choice == '2':
            output = app_ctx.check_imports_controller.execute(root_dir)
            if output.status == "error":
                for v in output.violations:
                    print(f"❌ {v[0]}: Layer {v[1]} imports Layer {v[2]}")
                print(output.message)
            else:
                print(f"✅ {output.message}")
                
        elif choice == '3':
            # Auto-save dùng project_name hiện tại - không hỏi lại
            print(f"💾 Đang lưu project [{project_name}]...")
            ok = app_ctx.save_controller.execute(project_name, src_dir, tests_dir)
            print("✅ Đã lưu!" if ok else "❌ Lỗi!")
                
        elif choice == '4':
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
                
        elif choice == '5':
            projs = app_ctx.list_controller.execute()
            print("Các project đã lưu:", ", ".join(projs))
            
        elif choice == '6':
            print("⚠️  CẢNH BÁO: Thao tác này sẽ XÓA SẠCH thư mục src/ và tests/.")
            confirm = input("Bạn có chắc chắn? (y/N): ").strip().lower()
            if confirm == 'y':
                ok = app_ctx.reset_controller.execute()
                if ok:
                    # Xóa cấu hình project hiện tại - đưa workspace về trạng thái trống
                    clear_project_config(root_dir)
                    print("✅ Đã xóa sạch workspace! Project config đã được reset.")
                    # Quay lại welcome flow để tạo project mới
                    project_name = welcome_flow(app_ctx, root_dir)
                else:
                    print("❌ Lỗi!")
                
        elif choice == '0':
            print("Tạm biệt!")
            break

if __name__ == "__main__":
    main()
