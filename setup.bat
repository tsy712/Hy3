@echo off
chcp 65001 >nul
echo ==============================================
echo   Hy3 MCP Server - 一键安装脚本
echo ==============================================
echo.

REM 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请先安装 Python 3.9+
    pause
    exit /b 1
)

echo [信息] Python 已检测到
echo.

REM 检查 API Key
if "%HY3_API_KEY%"=="" (
    if not exist ".env" (
        echo [警告] 未设置 HY3_API_KEY 环境变量，且未找到 .env 文件
        echo.
        echo 请先设置 API Key（二选一）：
        echo   方式1: set HY3_API_KEY=你的API密钥
        echo   方式2: copy .env.example .env 并填入密钥
        echo.
    ) else (
        echo [信息] 检测到 .env 配置文件
    )
) else (
    echo [信息] 检测到 HY3_API_KEY 环境变量
)
echo.

REM 安装依赖
echo [信息] 正在安装依赖...
pip install -r requirements.txt -q
echo.

REM 验证
echo [信息] 正在验证安装...
python -c "from fastmcp import FastMCP; print('  [OK] FastMCP')" 2>nul || echo "  [FAIL] FastMCP"
python -c "from openai import OpenAI; print('  [OK] OpenAI SDK')" 2>nul || echo "  [FAIL] OpenAI SDK"
python -c "import httpx; print('  [OK] httpx')" 2>nul || echo "  [FAIL] httpx"
echo.

echo ==============================================
echo   安装完成！
echo ==============================================
echo.
echo 在 CodeBuddy 中配置 MCP：
echo   将 configs/codebuddy-mcp.json 中的配置添加到
echo   CodeBuddy 的 MCP 设置中。
echo.
echo 在 Cursor 中配置 MCP：
echo   将 configs/cursor-mcp.json 中的内容复制到
echo   .cursor/mcp.json
echo.
echo 手动测试（需先设置 API Key）：
echo   cd src
echo   set HY3_API_KEY=你的API密钥
echo   python server.py
echo.
pause
