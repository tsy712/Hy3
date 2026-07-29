#!/bin/bash
echo "=============================================="
echo "  Hy3 MCP Server - 一键安装脚本"
echo "=============================================="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到 Python，请先安装 Python 3.9+"
    exit 1
fi

echo "[信息] Python 已检测到"
echo ""

# 检查 API Key 或 .env 文件
if [ -z "$HY3_API_KEY" ]; then
    if [ ! -f ".env" ]; then
        echo "[警告] 未设置 HY3_API_KEY 环境变量，且未找到 .env 文件"
        echo ""
        echo "请先设置 API Key（二选一）："
        echo "  方式1: export HY3_API_KEY=你的API密钥"
        echo "  方式2: cp .env.example .env 并填入密钥"
        echo ""
    else
        echo "[信息] 检测到 .env 配置文件"
    fi
else
    echo "[信息] 检测到 HY3_API_KEY 环境变量"
fi
echo ""

# 安装依赖
echo "[信息] 正在安装依赖..."
cd "$(dirname "$0")"
pip3 install -r requirements.txt -q
echo ""

# 验证
echo "[信息] 正在验证安装..."
python3 -c "from fastmcp import FastMCP; print('  [OK] FastMCP')"
python3 -c "from openai import OpenAI; print('  [OK] OpenAI SDK')"
python3 -c "import httpx; print('  [OK] httpx')"
echo ""

echo "=============================================="
echo "  安装完成！"
echo "=============================================="
echo ""
echo "在 CodeBuddy 中配置 MCP："
echo "  将 configs/codebuddy-mcp.json 中的配置添加到"
echo "  CodeBuddy 的 MCP 设置中。"
echo ""
echo "在 Cursor 中配置 MCP："
echo "  将 configs/cursor-mcp.json 中的内容复制到"
echo "  .cursor/mcp.json"
echo ""
echo "手动测试（需先设置 API Key）："
echo "  cd src"
echo "  export HY3_API_KEY=你的API密钥"
echo "  python3 server.py"
echo ""
