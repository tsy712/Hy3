@echo off
chcp 65001 >nul
title Hy3 Research Assistant

echo ============================================
echo   Hy3 Research Assistant — 腾讯混元智能研究助手
echo ============================================
echo.

:: Check Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python 未安装！请先安装 Python 3.9+
    pause
    exit /b 1
)

:: Check .env
if not exist ".env" (
    echo [INFO] 未找到 .env 文件，从 .env.example 复制…
    copy .env.example .env >nul
    echo [WARN] 请编辑 .env 文件，填入你的 HY3_API_KEY
    echo.
)

:: Check/Create venv
if not exist "venv\" (
    echo [INFO] 创建虚拟环境…
    python -m venv venv
)

:: Activate and install
call venv\Scripts\activate.bat
echo [INFO] 安装依赖…
pip install -q -r requirements.txt
pip install -q -e .

echo.
echo [INFO] 启动服务…
echo   前端: http://localhost:8000
echo   API 文档: http://localhost:8000/docs
echo.
echo 按 Ctrl+C 停止
echo ============================================

python -m backend.cli --host 0.0.0.0 --port 8000

pause
