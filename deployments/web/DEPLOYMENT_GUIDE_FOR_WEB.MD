# Web Deployment Guide (Clean Architecture)

Hướng dẫn triển khai chi tiết cho ứng dụng Web tách biệt Frontend và Backend.

## 1. Phân Tách Vai Trò trong Kiến Trúc
* **Backend API (FastAPI):** Nằm tại `src/layer_04_infrastructure/ui/web/fastapi/`. Đóng vai trò là cổng phân phối dữ liệu HTTP (Presentation Layer) điều hướng Use Cases.
* **Frontend UI (Static UI):** Nằm tại `src/layer_04_infrastructure/ui/web/frontend/`. Là giao diện tĩnh chạy hoàn toàn trong trình duyệt của Client.

---

## 2. Phương Án 1: Triển Khai Monolithic (Chung một Server)
Nếu muốn chạy cả Frontend và Backend chung trên một máy chủ (ví dụ: Render hoặc VPS):
1. Cấu hình FastAPI mount thư mục tĩnh Frontend trong `app_context_web.py`:
   ```python
   from fastapi.staticfiles import StaticFiles
   # Mount thư mục frontend làm trang chủ
   app.mount("/", StaticFiles(directory="src/layer_04_infrastructure/ui/web/frontend", html=True), name="frontend")
   ```
2. Chạy ứng dụng thông qua Dockerfile đi kèm:
   ```bash
   docker build -t my-web-app -f deployments/web/Dockerfile .
   docker run -p 8000:8000 my-web-app
   ```

---

## 3. Phương Án 2: Triển Khai Tách Biệt (Tối Ưu Chi Phí / Miễn Phí)
Để tối ưu hóa tải và tận dụng các gói hosting miễn phí:

### A. Backend (FastAPI)
* Triển khai container Python lên **Render**, **Fly.io**, hoặc **Railway** sử dụng `deployments/web/Dockerfile`.
* **Lưu ý:** Phải cấu hình Middleware **CORS** trong `app_context_web.py` để cho phép tên miền Frontend gửi yêu cầu API đến Backend.

### B. Frontend (GitHub Pages / Vercel / Netlify - MIỄN PHÍ)
* Đẩy riêng thư mục `src/layer_04_infrastructure/ui/web/frontend/` lên **GitHub Pages** hoặc **Vercel**.
* Thay đổi địa chỉ API Base URL trong mã nguồn Javascript của Frontend (ví dụ: `buttons.js`, `inputs.js`...) trỏ trực tiếp đến tên miền Backend đã deploy ở bước A (ví dụ: `https://my-backend.onrender.com/api`).
