# DESIGN_PROCESS.md

# Sổ tay Thiết kế & Phát triển (Design & Dev Manual)

## 1. Triết lý thiết kế: Inside-Out
*Trước khi viết code, hãy luôn tư duy theo luồng này để đảm bảo tính "Clean":*

1.  **Nghiệp vụ (Layer 01 & 02):** - Viết User Story: "Là [người dùng], tôi muốn [hành động] để [lợi ích]."
    - Tạo Entity: Định nghĩa cấu trúc dữ liệu thuần túy.
    - Viết UseCase: Xây dựng logic hành động (dựa trên interface).
2.  **Hợp đồng (Layer 03 - Gateways):** - Định nghĩa `Protocol` cho các kết nối (Database, External API). 
    - Đảm bảo các tầng nghiệp vụ không bị "ô nhiễm" bởi công nghệ.
3.  **Lắp ráp (Layer 05 - Bootstrap):** - Dùng `app_context.py` để kết nối các mảnh ghép.
    - Sử dụng Mock để test luồng nghiệp vụ trước khi có database/UI thật.
4.  **Triển khai chi tiết (Layer 04 - Infrastructure):** - Viết code thực thi cho Database, UI, Web Drivers...
    - "Điền vào chỗ trống" dựa trên các interface đã định nghĩa ở bước 2.

---

## 2. Quy trình Phát triển thực tế siêu tốc (Checklist)
*Template này được trang bị công cụ sinh mã tự động (Generator). Hãy làm đúng luồng sau để tiết kiệm 80% thời gian code:*

- [ ] **Bước A (Lõi dữ liệu):** Phân tích và tạo Entity trong `src/layer_01_entities/` (Định nghĩa các Class thuần túy, không import Framework).
- [ ] **Bước B (Auto-Generate):** 
    - Chạy Project Manager App (CLI hoặc GUI):
      - GUI: `python scripts/util_dev/project_manager_app/run_project_manager_app/desktop/run_desktop.py`
      - CLI: `python scripts/util_dev/project_manager_app/run_project_manager_app/cli/run_cli.py`
    - Chọn chức năng `Generate Feature` và nhập tên Tính năng (Ví dụ: `PlaceOrder`). Tool sẽ tự động đẻ ra toàn bộ: DTO, Interactor (Layer 02), Controllers/Presenters (Layer 03), Database Repositories (Layer 04), tự động nối dây DI ở Layer 05, và sinh sẵn script chạy ở `scripts/run/`.
- [ ] **Bước C (Điền Logic):**
    - Mở file Interactor vừa được tạo ở `layer_02`, viết logic nghiệp vụ dựa trên Entity.
    - Mở file Repository/Adapter vừa được tạo ở `layer_04`, viết code gọi API, Query DB thực tế.
    - Mở file Giao diện ở `layer_04_infrastructure/ui/` để vẽ nút bấm.
- [ ] **Bước D (Kiểm chứng):** Chạy Unit Test (`pytest`) hoặc test bằng Mock DB trước khi ráp Data thật.

---

## 3. Nguyên tắc vàng
- **Không bao giờ** import `Infrastructure` (Layer 04) hay `Gateways` (Layer 03) vào `UseCases` (Layer 02).
- **Luôn** dùng `Interface` (`abc.ABC`) để định nghĩa giao tiếp giữa các tầng (Dependency Inversion).
- **Tách biệt:** Mọi chi tiết (PyQt5, Tkinter, FastAPI, Database) bắt buộc nằm ở `layer_04_infrastructure/`.

---

## 4. Bí quyết vận hành
- **Automation:** Đừng bao giờ tạo file bằng tay cho các luồng Use Case mới. Luôn dùng Tool Generator.
- **Cross-Cutting Concerns:** Các thành phần dùng chung như Logger, Config, Exception... hãy để vào `src/shared/`.
- **Mock DB:** Tận dụng tối đa biến môi trường `USE_MOCK_DB=true` trong `app_context_base.py` để test nhanh logic màn hình mà không cần cài đặt Database thật.
- **Khởi tạo lại:** Khi cần xây app mới hoàn toàn, dùng lệnh `python scripts/util_dev/start_new_project.py` để quét sạch code rác.

---
*Cấu trúc dự án này tuân thủ Clean Architecture. Hãy giữ cho nó luôn "sạch"!*