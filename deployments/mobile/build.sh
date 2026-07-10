#!/bin/bash
# Script đóng gói ứng dụng Mobile (Kivy) sang Android (.apk) bằng Buildozer
# Lưu ý: Nên chạy script này trên Linux (Ubuntu) vì Buildozer chưa hỗ trợ Windows trực tiếp.
echo "=== Start Packaging Mobile Application ==="

# 1. Đảm bảo buildozer được cài đặt
if ! command -v buildozer &> /dev/null; then
    echo "Installing Buildozer & dependencies..."
    pip install buildozer cython
fi

# 2. Khởi tạo buildozer spec nếu chưa tồn tại
if [ ! -f "buildozer.spec" ]; then
    echo "Initializing buildozer.spec..."
    buildozer init
    
    # Cập nhật một số cấu hình mặc định cho Kivy Clean Architecture
    # Tự động thay đổi thư mục nguồn chính vào src
    if [ -f "buildozer.spec" ]; then
        sed -i 's/package.name = myapp/package.name = cleanapp/g' buildozer.spec
        # Chỉ định file entrypoint chạy chính của mobile app
        # (Chỉ hướng dẫn, lập trình viên sẽ tự cấu hình chi tiết theo ý muốn)
    fi
fi

# 3. Đóng gói ứng dụng sang định dạng Android Debug APK
echo "Building Android APK in debug mode..."
buildozer -v android debug

echo "=== Build completed! Output is saved in the bin/ directory ==="
