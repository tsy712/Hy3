@echo off
chcp 65001 >nul
echo ==============================================
echo   Hy3 Research Assistant - 一键启动
echo ==============================================
echo.

REM 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请先安装 Python 3.10+
    pause
    exit /b 1
)

echo [信息] Python 已检测到
echo.

REM 检查虚拟环境
if not exist "venv\Scripts\python.exe" (
    echo [信息] 未检测到虚拟环境，正在创建...
    python -m venv venv
    echo [信息] 虚拟环境已创建
)

REM 激活虚拟环境并检查依赖
call venv\Scripts\activate.bat

echo [信息] 正在检查依赖...
pip install -e . -q 2>nul
if %errorlevel% neq 0 (
    echo [警告] pip install 失败，尝试强制重新安装...
    pip install -e . --force-reinstall
)
echo.

REM 检查 API Key
if "%HY3_API_KEY%"=="" (
    if not exist ".env" (
        echo [警告] 未检测到 .env 文件或 HY3_API_KEY 环境变量
        echo.
        echo 请执行以下操作之一：
        echo   1. 复制 .env.example 为 .env 并填入 API Key
        echo   2. 设置环境变量: set HY3_API_KEY=你的API密钥
        echo.
    ) else (
        echo [信息] 检测到 .env 配置文件
    )
) else (
    echo [信息] 检测到 HY3_API_KEY 环境变量
)
echo.

echo [信息] 正在启动 Hy3 Research Assistant...
echo.
echo   访问地址: http://localhost:8000
echo   API 文档: http://localhost:8000/docs
echo   按 Ctrl+C 停止服务
echo.

python backend/main.py

pause
