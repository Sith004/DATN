@echo off
chcp 65001 >nul
title Hệ thống Đánh giá Rủi ro Tín dụng - Nguyễn Trọng Thể
color 0A
cls

echo ================================================================
echo   ĐỒ ÁN TỐT NGHIỆP: ĐÁNH GIÁ & DỰ BÁO RỦI RO TÍN DỤNG
echo   Sinh viên: Nguyễn Trọng Thể - MSSV: 1150080117
echo ================================================================
echo.

:: 1. Địa chỉ IP mặc định của Ubuntu
set "UBUNTU_IP=192.168.100.34"

echo [1/3] Đang kiểm tra kết nối mạng tới Ubuntu (%UBUNTU_IP%)...
powershell -Command "if (Test-NetConnection %UBUNTU_IP% -Port 22 -InformationLevel Quiet) { exit 0 } else { exit 1 }"
if errorlevel 1 (
    echo.
    echo [CẢNH BÁO] Không tìm thấy Ubuntu tại IP: %UBUNTU_IP%!
    set /p "UBUNTU_IP=>> Vui lòng nhập địa chỉ IP hiện tại của Ubuntu (xem bằng lệnh 'hostname -I'): "
)

echo.
echo [2/3] Đang mở đường hầm SSH kết nối PostgreSQL...
:: Tắt các tiến trình SSH tunnel cũ nếu có
taskkill /F /IM ssh.exe >nul 2>&1

:: Khởi chạy đường hầm SSH ngầm
start /B ssh -N -L 15432:127.0.0.1:5433 the@%UBUNTU_IP%
timeout /t 2 /nobreak >nul

:: Kiểm tra cổng 15432
powershell -Command "if (Test-NetConnection 127.0.0.1 -Port 15432 -InformationLevel Quiet) { exit 0 } else { exit 1 }"
if errorlevel 1 (
    echo [LỖI] Chưa mở được cổng 15432. Vui lòng kiểm tra lại máy ảo Ubuntu!
    pause
    exit /b
)
echo       Đường hầm SSH đã sẵn sàng: 127.0.0.1:15432 -^> Ubuntu:5433

echo.
echo [3/3] Đang khởi chạy ứng dụng Streamlit...
cd /d F:\DATN\project
.\.venv\Scripts\python.exe -m streamlit run app.py

:: Tự động dọn dẹp khi tắt ứng dụng
echo.
echo Đang đóng đường hầm SSH...
taskkill /F /IM ssh.exe >nul 2>&1
echo Đã tắt hoàn tất.
