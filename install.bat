@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
:: ============================================
:: Hy3 研究助手 — Windows 一键安装脚本
:: ============================================
:: 使用方式: 右键 "以管理员身份运行" 或 双击执行
:: ============================================

title Hy3 研究助手 — 一键安装

echo.
echo ========================================
echo    Hy3 研究助手 — 一键安装脚本
echo ========================================
echo.

:: --- [1/4] 检测 Python ---
echo [1/4] 检测 Python 环境...
set PYTHON=
for %%p in (python python3 py) do (
    where %%p >nul 2>&1
    if !errorlevel!==0 (
        for /f "tokens=2" %%v in ('%%p --version 2^>^&1') do (
            set VERSION=%%v
            set PYTHON=%%p
            echo   [OK] 找到 python !VERSION!
            goto :found_python
        )
    )
)

:found_python
if "%PYTHON%"=="" (
    echo   [错误] 未找到 Python，请先安装 Python 3.9+
    echo.
    echo   下载地址: https://www.python.org/downloads/
    echo   (安装时请勾选 "Add Python to PATH")
    echo.
    pause
    exit /b 1
)

:: --- [2/4] 创建虚拟环境 ---
echo.
echo [2/4] 创建虚拟环境...
if not exist "venv" (
    %PYTHON% -m venv venv
    echo   [OK] 虚拟环境已创建
) else (
    echo   [SKIP] 虚拟环境已存在
)

call .\venv\Scripts\activate.bat
echo   [OK] 虚拟环境已激活

:: --- [3/4] 安装依赖 ---
echo.
echo [3/4] 安装依赖包（请稍候）...
python -m pip install --upgrade pip -q 2>nul
pip install -e . -q
echo   [OK] 主项目依赖安装完成

if exist "hy3-mcp-server\" (
    pip install -e hy3-mcp-server -q 2>nul
    echo   [OK] MCP Server 依赖安装完成
)

:: --- [4/4] 配置 .env ---
echo.
echo [4/4] 配置环境变量...
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env >nul
        echo   [OK] 已从模板创建 .env 文件
        echo.
        echo   [注意] 请编辑 .env 文件，填入你的 HY3_API_KEY
        echo          可以用记事本打开: notepad .env
    ) else (
        echo   [错误] 未找到 .env.example 模板文件
    )
) else (
    echo   [SKIP] .env 文件已存在
)

:: --- 完成 ---
echo.
echo ========================================
echo    安装完成！
echo ========================================
echo.
echo   启动服务: .\venv\Scripts\activate ^&^& hy3-research
echo   或双击:  start.bat
echo   或 Docker:  docker-compose up -d
echo.
echo   前端页面: http://localhost:8000
echo   API 文档: http://localhost:8000/docs
echo   健康检查: http://localhost:8000/health
echo.
pause
