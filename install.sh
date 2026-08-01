#!/bin/bash
set -e

echo "============================================"
echo "  Hy3 MCP Server — MCP 协议工具集安装"
echo "============================================"
echo ""

cd "$(dirname "$0")"

if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 未安装！"
    exit 1
fi

if [ ! -f ".env" ]; then
    if [ -f "../.env" ]; then
        cp "../.env" ".env"
    else
        cp "../.env.example" ".env"
        echo "[WARN] 请编辑 .env 文件，填入 HY3_API_KEY"
    fi
fi

echo "[INFO] 安装 hy3-mcp-server…"
pip install -q -e .

echo ""
echo "[SUCCESS] Hy3 MCP Server 安装完成！"
echo ""
echo "接下来，将对应的 MCP 配置文件复制到你的 AI 客户端："
echo "  - CodeBuddy:   configs/codebuddy-mcp.json"
echo "  - Cursor:      configs/cursor-mcp.json"
echo "  - Claude:      configs/claude-desktop-mcp.json"
echo ""
