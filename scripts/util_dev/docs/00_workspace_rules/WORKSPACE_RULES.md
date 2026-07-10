# ⚙️ Workspace Development Rules (Quy tắc Phát triển)

Đây là các quy định bắt buộc phải tuân thủ khi phát triển và bảo trì mã nguồn trong dự án này:

## 1. Quy tắc Thiết kế Design Pattern ở tầng Thực thể (Entities)
Nếu tầng `Entities` (`src/layer_01_entities`) cần sử dụng các Design Pattern, bắt buộc phải đọc kỹ và tuân thủ tuyệt đối quy chuẩn tại tệp hướng dẫn [README.md](../03_entity_design_patterns/README.md).

## 2. Quy trình sinh Use Case mới
Nếu cần tạo bất kỳ Use Case mới nào ở Layer 2, bắt buộc phải sử dụng công cụ sinh cấu trúc tự động của hệ thống, không tự tạo bằng tay. 
* **GUI:** `python scripts/util_dev/project_manager_app/run_project_manager_app/desktop/run_desktop.py`
* **CLI:** `python scripts/util_dev/project_manager_app/run_project_manager_app/cli/run_cli.py`

## 3. Quy chuẩn viết code & UI
Trước khi viết code, chỉnh sửa UI, hoặc cấu trúc hệ thống, AI bắt buộc phải đọc tệp Bản đồ Chỉ mục Tài liệu [README.md](../README.md) để tìm và đọc đúng file hướng dẫn chi tiết của phân mục đó.

## 4. Quy tắc Commit thay đổi code
* Chỉ commit lại dưới local, không push lên repo trừ khi có yêu cầu trực tiếp của lập trình viên.
* **Trước khi commit:** Bắt buộc chạy định dạng code với lệnh `black src/` (hoặc `.venv/Scripts/black src/`), sau đó kiểm tra kiểu tĩnh bằng lệnh `.venv/Scripts/pyright src/` (Windows) hoặc `.venv/bin/pyright src/` (Linux/macOS) và đảm bảo không có lỗi (`0 errors`).
* **Trước khi push:** Bắt buộc gộp (Squash) toàn bộ các commit trung gian tại local thành một commit duy nhất rõ nghĩa bằng lệnh `git rebase -i HEAD~N` (với N là số lượng commit).
