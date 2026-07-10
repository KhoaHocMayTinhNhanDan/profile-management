#!/bin/bash
# Script đóng gói ứng dụng Desktop (PyQt6) bằng PyInstaller
echo "=== Start Packaging Desktop Application ==="

# 1. Kiểm tra môi trường ảo
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

# 2. Đảm bảo pyinstaller được cài đặt
if ! command -v pyinstaller &> /dev/null; then
    echo "Installing PyInstaller..."
    pip install pyinstaller
fi

# 3. Tự động tìm runner script trong scripts/run/desktop/
RUNNER_SCRIPT=$(find scripts/run/desktop -name "run_*.py" | head -n 1)

if [ -z "$RUNNER_SCRIPT" ]; then
    echo "ERROR: Không tìm thấy file runner trong scripts/run/desktop/ (dạng run_*.py)"
    exit 1
fi

echo "Found runner script: $RUNNER_SCRIPT"

# 4. Đóng gói ứng dụng
# Cấu hình lưu trữ kết quả trong thư mục deployments/desktop/results
DIST_DIR="deployments/desktop/results"
BUILD_DIR="deployments/desktop/build_temp"

echo "Running PyInstaller..."
pyinstaller --noconfirm \
            --clean \
            --windowed \
            --distpath "$DIST_DIR" \
            --workpath "$BUILD_DIR" \
            --specpath "deployments/desktop" \
            "$RUNNER_SCRIPT"

echo "=== Build completed! Output is saved in: $DIST_DIR ==="
