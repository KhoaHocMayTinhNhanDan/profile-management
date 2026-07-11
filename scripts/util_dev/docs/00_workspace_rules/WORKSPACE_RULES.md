# ⚙️ Workspace Development Rules (Quy tắc Phát triển)

Đây là các quy định bắt buộc phải tuân thủ khi phát triển và bảo trì mã nguồn trong dự án này:

## 1. Quy tắc Thiết kế Design Pattern ở tầng Thực thể (Entities)
Nếu tầng `Entities` (`src/layer_01_entities`) cần sử dụng các Design Pattern, bắt buộc phải đọc kỹ và tuân thủ tuyệt đối quy chuẩn tại tệp hướng dẫn [README.md](../03_entity_design_patterns/README.md).

## 2. Quy trình sinh Use Case mới
Nếu cần tạo bất kỳ Use Case hay Feature mới nào ở Layer 2, bắt buộc phải sử dụng công cụ sinh cấu trúc tự động của hệ thống, không tự tạo bằng tay. Công cụ này sẽ tự động khởi tạo:
* Toàn bộ cấu trúc thư mục và tệp tin khung (boilerplate) cho cả 5 layer của Clean Architecture (bao gồm Entities, DTOs, Interactor, Interfaces, Controllers, Presenters, Database Data Sources, UI Pages, và Async Hooks).
* Tự động đăng ký và liên kết Dependency Injection (DI) type-safe vào các tệp tin `app_context_*.py` tương ứng.
* Tự động tạo sẵn các tệp khung kiểm thử (`tests/unit` và `tests/integration`) cũng như tệp tin runner khởi chạy cho tính năng đó.

> [!NOTE]
> Nhờ đó, lập trình viên (hoặc AI) chỉ cần tập trung viết code logic nghiệp vụ (business logic) và tùy biến giao diện trực tiếp vào khung xương đã sinh ra, mà không cần bận tâm thiết lập kết nối giữa các tầng.

Cách khởi chạy công cụ (Xem chi tiết tại [project_manager_app.md](../05_tools/project_manager_app.md)):
* **GUI:** `python scripts/util_dev/project_manager_app/run_project_manager_app/desktop/run_desktop.py`
* **CLI:** `python scripts/util_dev/project_manager_app/run_project_manager_app/cli/run_cli.py`

## 3. Quy trình làm việc bắt buộc của AI (Workflow)
AI phải tuân thủ nghiêm ngặt quy trình làm việc tuyến tính theo các bước sau cho mọi yêu cầu phát triển hoặc chỉnh sửa có tính phức tạp:

1. **Lập Kế Hoạch (Planning):** 
   - AI bắt buộc phải nghiên cứu codebase và tạo/cập nhật bản thiết kế chi tiết tại tệp `implementation_plan.md`.
   - Bật cờ `RequestFeedback = True` trên bản kế hoạch để gửi yêu cầu phê duyệt đến lập trình viên.
   - **BẮT BUỘC DỪNG LẠI** và đợi phản hồi. Tuyệt đối không được phép chỉnh sửa hoặc tạo bất kỳ tệp mã nguồn nào trước khi bản kế hoạch được phê duyệt chính thức.
2. **Nghiên cứu tài liệu & Viết code:** 
   - Trước khi viết code hoặc sửa đổi UI, AI phải đọc tệp [README.md](../README.md) của dự án để tìm và đọc đúng file hướng dẫn chi tiết của phân mục/layer có liên quan.
   - **Chất lượng chú thích (Comments & Docstrings):** Giữ lại các comment và docstring cũ còn giá trị; đồng thời **chủ động cập nhật hoặc xóa bỏ** các chú thích đã lỗi thời, sai lệch để đảm bảo tài liệu trong code luôn phản ánh chính xác logic thực tế mới.
3. **Kiểm tra chất lượng trước khi bàn giao:**
   - Bắt buộc chạy định dạng code: `black src/` (hoặc `.venv/Scripts/black src/`).
   - Bắt buộc chạy kiểm tra kiểu tĩnh: `.venv/Scripts/pyright` (chạy không kèm tham số trên Windows để Node parser tự động đọc tệp pyrightconfig.json và quét lỗi toàn diện dự án) hoặc `.venv/bin/pyright` (Linux/macOS).
   - **Quy trình sửa lỗi lặp (Debugging Loop):** Nếu phát hiện bất kỳ lỗi kiểu tĩnh nào, AI bắt buộc phải tự động sửa đổi mã nguồn và chạy lại lệnh kiểm tra. Quy trình này phải được lặp đi lặp lại liên tục cho đến khi đạt kết quả sạch lỗi hoàn toàn (`0 errors, 0 warnings`) trên tất cả các tệp tạo mới cũng như các tệp cũ bị chỉnh sửa hoặc chịu tác động trực tiếp/gián tiếp mới được phép chuyển sang bước tiếp theo.

## 4. Quy tắc Commit & Push thay đổi code
* **Commit:** Chỉ commit lại dưới môi trường local sau khi đã kiểm tra Pyright sạch lỗi.
* **Tuyệt đối không tự ý Push:** AI chỉ được phép chạy lệnh push lên Remote Repository (`git push`) **khi và chỉ khi nhận được yêu cầu trực tiếp bằng văn bản từ lập trình viên** (ví dụ: *"hãy push lên repo"*, *"push code lên nhé"*).
* **Squash Commit:** Trước khi push, bắt buộc gộp (Squash) toàn bộ các commit trung gian tại local thành một commit duy nhất rõ nghĩa bằng lệnh `git rebase -i HEAD~N` (với N là số lượng commit).