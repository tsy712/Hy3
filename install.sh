#!/bin/bash
# ============================================
# Hy3 研究助手 — Linux / macOS 一键安装脚本
# ============================================
# 使用方式: chmod +x install.sh && ./install.sh
# ============================================

set -e

# --- 颜色定义 ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

BOLD='\033[1m'

# --- Banner ---
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   Hy3 研究助手 — 一键安装脚本${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# --- 检测 Python ---
echo -e "${BOLD}[1/4] 检测 Python 环境...${NC}"
PYTHON=""
for cmd in python3 python; do
    if command -v $cmd &> /dev/null; then
        VERSION=$($cmd --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
        MAJOR=$(echo $VERSION | cut -d. -f1)
        MINOR=$(echo $VERSION | cut -d. -f2)
        if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 9 ]; then
            PYTHON=$cmd
            echo -e "  ${GREEN}✓${NC} 找到 $PYTHON ($VERSION)"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo -e "${RED}✗ 未找到 Python 3.9+，请先安装 Python。${NC}"
    echo -e "   macOS:  brew install python@3.11"
    echo -e "   Ubuntu: sudo apt install python3.11 python3.11-venv"
    exit 1
fi

# --- 创建虚拟环境 ---
echo ""
echo -e "${BOLD}[2/4] 创建虚拟环境...${NC}"
if [ ! -d "venv" ]; then
    $PYTHON -m venv venv
    echo -e "  ${GREEN}✓${NC} 虚拟环境已创建"
else
    echo -e "  ${YELLOW}○${NC} 虚拟环境已存在，跳过"
fi

# 激活虚拟环境
source venv/bin/activate
echo -e "  ${GREEN}✓${NC} 虚拟环境已激活"

# --- 安装依赖 ---
echo ""
echo -e "${BOLD}[3/4] 安装依赖包...${NC}"
pip install --upgrade pip -q
pip install -e . -q
echo -e "  ${GREEN}✓${NC} 主项目依赖安装完成"

# 安装 MCP Server (如果有)
if [ -d "hy3-mcp-server" ]; then
    pip install -e hy3-mcp-server -q
    echo -e "  ${GREEN}✓${NC} MCP Server 依赖安装完成"
fi

# --- 配置 .env ---
echo ""
echo -e "${BOLD}[4/4] 配置环境变量...${NC}"
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "  ${GREEN}✓${NC} 已从模板创建 .env 文件"
        echo ""
        echo -e "  ${YELLOW}⚠${NC}  请编辑 .env 文件，填入你的 HY3_API_KEY："
        echo -e "     ${BOLD}nano .env${NC}       或       ${BOLD}vim .env${NC}"
        echo -e "     ${BOLD}code .env${NC}     或       ${BOLD}open -e .env${NC}"
    else
        echo -e "  ${RED}✗ 未找到 .env.example 模板文件${NC}"
    fi
else
    echo -e "  ${YELLOW}○${NC} .env 文件已存在，跳过"
fi

# --- 完成 ---
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   安装完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "  启动服务: ${BOLD}source venv/bin/activate && hy3-research${NC}"
echo -e "  或 Docker: ${BOLD}docker-compose up -d${NC}"
echo ""
echo -e "  前端页面: ${BLUE}http://localhost:8000${NC}"
echo -e "  API 文档: ${BLUE}http://localhost:8000/docs${NC}"
echo -e "  健康检查: ${BLUE}http://localhost:8000/health${NC}"
echo ""
