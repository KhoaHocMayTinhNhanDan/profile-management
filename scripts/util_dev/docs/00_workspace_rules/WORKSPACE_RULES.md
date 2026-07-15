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

## 3. Quy trình làm việc & Quy tắc Đẩy mã nguồn của AI (AI Agent Decision Tree)

Mọi hoạt động phát triển, kiểm thử, commit, và push mã nguồn của AI Agent bắt buộc phải tuân theo sơ đồ quyết định tuần tự sau:

```
Nhận Yêu cầu ➔ Yêu cầu có tính phức tạp hoặc thay đổi cấu trúc không?
                   │
                ┌──┴──┐
                │     │
               Yes    No ➔ Trực tiếp Nghiên cứu & Viết code (Bước 2)
                │
                ▼
      [Bước 1: Lập Kế hoạch (Planning)]
        - Tạo/Cập nhật implementation_plan.md
        - Gắn RequestFeedback = True và UserFacing = True
        - BẮT BUỘC DỪNG LẠI và đợi Phản hồi phê duyệt từ Lập trình viên
                   │
                   ▼
      [Bước 2: Nghiên cứu & Thực thi]
        - Đọc README.md tài liệu để tìm đúng quy chuẩn layer
        - BẮT BUỘC tuân thủ Atomic UI (nếu chạm vào UI)
        - Cập nhật/dọn dẹp docstrings & comments lỗi thời
                   │
                   ▼
      [Bước 3: Định dạng & Kiểm tra Kiểu (Pyright)]
        - Định dạng code bằng black
        - Chạy pyright kiểm tra kiểu tĩnh
        - Pyright sạch lỗi (0 errors, 0 warnings)?
                   │
                ┌──┴──┐
                │     │
               No    Yes
                │     │
      Sửa lỗi & ┘     ▼
      Chạy lại   [Bước 4: Commit cục bộ (Local Commit)]
                      - Commit sau khi Pyright sạch lỗi
                      - Lập trình viên yêu cầu push bằng văn bản trực tiếp?
                                 │
                              ┌──┴──┐
                              │     │
                             No    Yes
                              │     │
                    Dừng lại, ┘     ▼
                    KHÔNG push    [Bước 5: Squash & Đẩy code (Push)]
                                    - Gộp commit (Squash) bằng git rebase
                                    - Chạy git push lên Remote
```

---

### Mô tả Chi tiết Các Bước trong Cây Quyết định:

#### 1. Bước 1: Lập Kế hoạch (Planning)
* **Hành động:** Tạo/cập nhật `implementation_plan.md` làm tài liệu thiết kế. Gắn `RequestFeedback = True` trong Artifact Metadata để hiển thị nút "Proceed".
* **Ràng buộc:** BẮT BUỘC dừng lại chờ phê duyệt của Lập trình viên trước khi tạo hoặc chỉnh sửa bất kỳ tệp mã nguồn nào.

#### 2. Bước 2: Nghiên cứu & Thực thi
* **Ràng buộc:** Mở [README.md](../README.md) để tìm đúng tài liệu layer. Khi sửa đổi UI, bắt buộc tuân thủ phân cấp ranh giới tại [atomic_design.md](../04_ui_development/ui_ux_design/common_theory/atomic_design.md).
* **Bảo trì chú thích:** Giữ comment còn giá trị, chủ động cập nhật hoặc xóa các comment/docstring đã lỗi thời.

#### 3. Bước 3: Định dạng & Kiểm tra Kiểu (Pyright)
* **Công cụ:** Chạy `black src/` để format. Chạy `.venv/Scripts/pyright` (hoặc `.venv/bin/pyright`) không kèm tham số.
* **Vòng lặp sửa lỗi (Debugging Loop):** Lặp liên tục việc sửa code và chạy lại pyright cho đến khi đạt trạng thái sạch lỗi (`0 errors, 0 warnings`) trên các tệp thay đổi mới được phép commit.

#### 4. Bước 4: Commit cục bộ (Local Commit)
* **Quy tắc:** Chỉ commit cục bộ sau khi đã chạy pyright sạch lỗi hoàn toàn.

#### 5. Bước 5: Squash & Đẩy code (Push)
* **Gộp commit:** Trước khi push, chạy `git rebase -i HEAD~N` để gộp các commit trung gian thành một commit duy nhất rõ nghĩa.
* **Ràng buộc Push:** Chỉ chạy `git push` khi có yêu cầu bằng văn bản trực tiếp của Lập trình viên (Ví dụ: *"push code nhé"*, *"hãy push lên repo"*).