#!/bin/bash
set -e

echo "============================================"
echo "  Hy3 Research Assistant — 腾讯混元智能研究助手"
echo "============================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 未安装！请先安装 Python 3.9+"
    exit 1
fi

# Check .env
if [ ! -f ".env" ]; then
    echo "[INFO] 未找到 .env 文件，从 .env.example 复制…"
    cp .env.example .env
    echo "[WARN] 请编辑 .env 文件，填入你的 HY3_API_KEY"
fi

# Check/Create venv
if [ ! -d "venv" ]; then
    echo "[INFO] 创建虚拟环境…"
    python3 -m venv venv
fi

# Activate and install
source venv/bin/activate
echo "[INFO] 安装依赖…"
pip install -q -r requirements.txt
pip install -q -e .

echo ""
echo "[INFO] 启动服务…"
echo "  前端: http://localhost:8000"
echo "  API 文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止"
echo "============================================"

python -m backend.cli --host 0.0.0.0 --port 8000
