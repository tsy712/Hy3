@echo off
echo ============================================
echo     Hy3 研究助手 - 一键启动脚本
echo ============================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 并添加到 PATH 环境变量。
    pause
    exit /b 1
)

REM 检查 API 密钥
if "%HY3_API_KEY%"=="" (
    echo [警告] 未设置 HY3_API_KEY 环境变量。
    echo 请在运行前设置 API 密钥：
    echo   set HY3_API_KEY=你的 API 密钥
    echo.
)

REM 安装依赖
echo [1/2] 正在安装 Python 依赖...
cd /d "%~dp0backend"
pip install -r requirements.txt -q

REM 启动服务器
echo [2/2] 正在启动服务器...
echo.
echo 服务器将在以下地址启动: http://localhost:8000
echo 按 Ctrl+C 停止服务器。
echo.
python main.py

pause
