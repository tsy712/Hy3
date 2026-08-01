@echo off
chcp 65001 >nul
title Hy3 MCP Server

echo ============================================
echo   Hy3 MCP Server — MCP 协议工具集安装
echo ============================================
echo.

cd /d "%~dp0hy3-mcp-server"

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python 未安装！
    pause
    exit /b 1
)

if not exist ".env" (
    echo [INFO] 从父目录链接 .env 配置…
    if exist "..\.env" (
        copy "..\.env" ".env" >nul
    ) else (
        copy "..\.env.example" ".env" >nul
        echo [WARN] 请编辑 .env 文件，填入 HY3_API_KEY
    )
)

:: Install
echo [INFO] 安装 hy3-mcp-server…
pip install -q -e .

echo.
echo [SUCCESS] Hy3 MCP Server 安装完成！
echo.
echo 接下来，将对应的 MCP 配置文件复制到你的 AI 客户端：
echo   - CodeBuddy:   configs/codebuddy-mcp.json
echo   - Cursor:      configs/cursor-mcp.json
echo   - Claude:      configs/claude-desktop-mcp.json
echo.
echo 或在终端直接运行测试：
echo   python -m src.server
echo.
pause
