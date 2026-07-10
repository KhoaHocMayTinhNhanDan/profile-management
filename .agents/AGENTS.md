# Workspace Rules

## 1. Quy tắc Thiết kế Design Pattern ở tầng Thực thể (Entities)
Nếu tầng `Entities` (`src/layer_01_entities`) cần sử dụng các Design Pattern, bắt buộc phải đọc kỹ và tuân thủ tuyệt đối quy chuẩn tại tệp hướng dẫn [DESIGN_PATTERNS_STRUCT_HELPER.md](file:///d:/DEV/python/learning/clean-architecture/learn/docs/01_design_patterns/DESIGN_PATTERNS_STRUCT_HELPER.md).

## 2. Quy trình sinh Use Case mới
Nếu trong quá trình phát triển cần tạo bất kỳ Use Case mới nào ở Layer 2, bắt buộc phải sử dụng công cụ sinh cấu trúc tự động **`scripts\project_manager_app`** của hệ thống, không tự tạo bằng tay để tránh vi phạm cấu trúc Clean Architecture.

## 3. khi thực hiện xong thay đổi code
Chỉ commit lại, không push lên repo trừ khi tôi yêu cầu
