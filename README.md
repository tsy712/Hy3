# Hy3 Research Assistant

基于**腾讯混元 Hy3 大模型**的智能研究助手工具集。

- 深度研究、代码分析、文档问答的 Web 服务（FastAPI + 前端）
- 7 个 MCP 工具 → 一键安装、即插即用到任何支持 MCP 的 AI 客户端

---

## 项目结构

```
Claw/
├── backend/                  # FastAPI 后端 (REST API + SSE)
│   ├── __init__.py           # 包初始化
│   ├── main.py               # FastAPI 应用 - 11 个 API 端点
│   ├── hy3_client.py         # Hy3 API 异步客户端
│   ├── tools.py              # 工具函数 (搜索/文件解析/代码执行)
│   └── cli.py                # CLI 启动入口 (hy3-research 命令)
│
├── frontend/
│   └── index.html            # Web 前端 (5 个功能面板、流式对话)
│
├── hy3-mcp-server/           # MCP Server 子项目
│   ├── src/
│   │   ├── __init__.py
│   │   └── server.py         # FastMCP 服务器 - 7 个 MCP 工具
│   ├── configs/              # AI 客户端 MCP 配置
│   │   ├── codebuddy-mcp.json
│   │   ├── cursor-mcp.json
│   │   └── claude-desktop-mcp.json
│   ├── pyproject.toml
│   ├── install.bat / .sh
│   └── requirements.txt
│
├── pyproject.toml            # 主项目 pip 安装配置
├── requirements.txt
├── .env.example
├── start.bat / .sh           # Windows / Linux 一键启动
└── README.md
```

---

## 快速开始

### 前置要求
- Python 3.9+
- Hy3 API Key（[腾讯混元控制台](https://hunyuan.cloud.tencent.com)）

### 1. 配置 API Key

```bash
copy .env.example .env
```

编辑 `.env`，填入你的 `HY3_API_KEY`。

### 2. 一键启动 (推荐)

**Windows:**
```bat
start.bat
```

**Linux/macOS:**
```bash
chmod +x start.sh && ./start.sh
```

### 3. 手动启动

```bash
# 安装依赖
pip install -r requirements.txt
pip install -e .

# 启动服务
python -m backend.cli --host 0.0.0.0 --port 8000
```

### 4. 访问

| 地址 | 说明 |
|------|------|
| **http://localhost:8000** | Web 前端 |
| **http://localhost:8000/docs** | Swagger API 文档 |

---

## Web 前端功能

| 面板 | 功能 | 说明 |
|------|------|------|
| 💬 智能对话 | SSE 流式对话 | 基于 Hy3 的多轮对话，Enter 发送 |
| 🔍 深度研究 | 搜索 + 分析 | 自动搜索互联网，Hy3 综合分析生成报告 |
| 🤖 Agent 模式 | 智能体 | 可执行代码、搜索、文件解析的自主 Agent |
| 📝 代码审查 | 5 维审查 | 正确性/安全性/性能/可维护性/最佳实践 |
| 📄 文件问答 | RAG 问答 | 上传 PDF/DOCX/TXT/MD，基于内容问答 |

---

## API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/chat/stream` | 流式对话 (SSE) |
| POST | `/api/chat` | 非流式对话 |
| POST | `/api/research` | 深度研究 (搜索 + RAG) |
| POST | `/api/agent` | Agent 模式 |
| POST | `/api/code-review` | 代码审查 |
| POST | `/api/embed` | 文本向量化 |
| POST | `/api/search` | 互联网搜索 |
| POST | `/api/fetch` | 网页抓取 |
| POST | `/api/parse-file` | 文件解析 |
| POST | `/api/execute` | Python 代码执行 |
| GET | `/api/health` | 健康检查 |

---

## MCP Server

Hy3 MCP Server 提供了 7 个 MCP 工具，可即插即用到任何支持 MCP 的 AI 客户端。

### 安装 MCP Server

```bash
cd hy3-mcp-server
pip install -e .
```

### MCP 工具列表

| 工具 | 说明 |
|------|------|
| `hy3_chat` | Hy3 对话 |
| `hy3_search` | 互联网搜索 |
| `hy3_fetch_web` | 网页抓取 |
| `hy3_code_review` | 代码审查 |
| `hy3_parse_file` | 文件解析 (PDF/DOCX/TXT) |
| `hy3_execute_code` | 安全 Python 执行 |
| `hy3_embed` | 文本向量化 |

### 支持的 AI 客户端

- **CodeBuddy** — 复制 `configs/codebuddy-mcp.json` 配置
- **Claude Desktop** — 复制 `configs/claude-desktop-mcp.json` 配置
- **Cursor** — 复制 `configs/cursor-mcp.json` 配置
- **Cline / Continue / 其他** — 参考以上配置修改 `command` 和 `args`

---

## CLI 命令

```bash
# 启动 Web 服务
hy3-research --host 0.0.0.0 --port 8000

# MCP Server
hy3-mcp
```

---

## 技术栈

- **后端**: FastAPI + Uvicorn + AsyncOpenAI + SSE
- **前端**: 纯 HTML/CSS/JS，深色主题，响应式布局
- **MCP**: FastMCP (基于 MCP 协议)
- **AI**: 腾讯混元 Hy3 (OpenAI 兼容 API)
- **搜索**: DuckDuckGo API
- **文件**: PyPDF2 + python-docx + BeautifulSoup4

---

## License

MIT
