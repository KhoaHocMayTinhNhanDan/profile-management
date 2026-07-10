# 🌐 Quy chuẩn Thiết kế Web UX (FastAPI / Web Frontend)

Tài liệu này định nghĩa các nguyên tắc thiết kế giao diện và tối ưu hóa trải nghiệm người dùng trên nền tảng Web dựa trên các nghiên cứu của **Nielsen Norman Group** và tiêu chuẩn thực chiến của **Smashing Magazine**.

---

## 🖥️📱 1. Thiết kế Phản hồi (Responsive Web Design)
Giao diện web phải chạy mượt mà từ màn hình điện thoại 320px đến màn hình UltraWide 4K:

*   **Tư duy Mobile-First (Thiết kế cho di động trước):** Thiết kế bố cục cột đơn giản cho màn hình nhỏ nhất để lọc ra những nội dung cốt lõi nhất, sau đó dùng CSS Media Queries (`min-width`) để mở rộng layout thành nhiều cột trên Desktop.
*   **Hệ thống lưới linh hoạt (CSS Grid & Flexbox):** Tránh sử dụng chiều rộng pixel cứng (`width: 800px`), sử dụng tỉ lệ phần trăm hoặc đơn vị tương đối (`width: 100%`, `max-width: 1200px`, `rem`, `em`, `vh`, `vw`).
*   **Điểm ngắt tiêu chuẩn (Standard Breakpoints):**
    *   *Mobile:* `< 768px` (bố cục 1 cột dọc).
    *   *Tablet:* `768px` đến `1024px` (bố cục 2 cột).
    *   *Desktop:* `> 1024px` (bố cục lưới nhiều cột hoàn chỉnh).

---

## ♿ 2. Tính tiếp cận & SEO (Accessibility & SEO)
Mã nguồn HTML sinh ra phải dễ đọc cho cả người dùng và các công cụ tìm kiếm (Google Search Crawler):

*   **Phân cấp Heading chuẩn chỉ (Heading Hierarchy):**
    *   Mỗi trang web **bắt buộc chỉ có duy nhất một thẻ `<h1>`** (đại diện cho tiêu đề trang).
    *   Sử dụng các thẻ `<h2>`, `<h3>` theo đúng thứ tự phân cấp nội dung logic (không nhảy cóc từ `<h1>` xuống `<h4>`).
*   **Nhãn mô tả tài nguyên:**
    *   Mọi thẻ ảnh `<img>` bắt buộc phải có thuộc tính `alt` mô tả nội dung ảnh (hỗ trợ SEO hình ảnh và trình đọc màn hình cho người khiếm thị).
    *   Mọi nút bấm chỉ có icon (không có chữ) bắt buộc phải có thuộc tính `aria-label` mô tả chức năng.
*   **Trạng thái tương tác:** Mọi thẻ `<a>`, `<button>` phải có trạng thái `:focus-visible` rõ ràng khi người dùng điều hướng bằng phím `Tab`.

---

## ⚡ 3. Tối ưu Hiệu năng & Tốc độ tải trang (Web Performance)
Tốc độ tải trang ảnh hưởng trực tiếp đến tỷ lệ giữ chân người dùng (Bounce Rate):

*   **Tối ưu hóa hình ảnh:** Nén ảnh về định dạng hiện đại (`WebP`, `AVIF`) thay vì dùng ảnh `PNG`/`JPG` dung lượng lớn.
*   **Trì hoãn tải tài nguyên (Lazy Loading):** Thêm thuộc tính `loading="lazy"` vào các thẻ `<img>` và `<iframe>` nằm ngoài vùng nhìn thấy ban đầu (Below the fold) để giảm băng thông tải trang.
*   **Tối ưu tài nguyên CSS/JS:** Tránh import các thư viện nặng một cách bừa bãi. Sử dụng async/defer cho các file script bên ngoài.
