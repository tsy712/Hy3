# Environment Requirements & Project Structure / 环境要求与项目结构

> 📖 [Back to README / 返回 README](../README.md)

---

## Hardware Requirements / 硬件要求

| Item / 项目 | Minimum / 最低配置 | Recommended / 推荐配置 |
|------|---------|---------|
| CPU | Any dual-core / 任意双核处理器 | Quad-core+ / 四核及以上 |
| RAM / 内存 | 512 MB | 1 GB+ |
| Disk / 磁盘 | 200 MB | 500 MB+ |
| GPU | **Not required** / **不需要** | **Not required** / **不需要** |
| Network / 网络 | Broadband / 宽带连接 | Stable broadband / 稳定宽带 |

> **Important: This project does NOT need GPU or CUDA.**
> All AI inference tasks are completed via HTTP calls to the Tencent Hunyuan Hy3 cloud API — no local model loading, inference, or training involved.
> If your goal is to **run / fine-tune the Hy3 model locally**, refer to the [Local Hy3 Model Guide](local-hy3-model.md).  
> **重要说明：本项目不需要 GPU 或 CUDA。**
> 所有 AI 推理任务均通过 HTTP 调用腾讯混元 Hy3 云端 API 完成，不涉及本地模型加载、推理或训练。
> 如果你的目标是**本地运行/微调 Hy3 模型本身**，请参考 [本地运行 Hy3 模型指南](local-hy3-model.md)。

## Software Requirements / 软件要求

| Dependency / 依赖 | Version / 版本要求 | Notes / 说明 |
|------|---------|------|
| Python | **3.9+** (main project / 主项目) / **3.10+** (MCP Server) | 3.11 recommended / 推荐 3.11 |
| pip | 23.0+ | Installed with Python / 随 Python 一起安装 |
| OS / 操作系统 | Windows 10+ / macOS 12+ / Linux (any distro / 任意发行版) | All supported / 均支持 |

## Dependency Overview / 依赖包总览

This project has **zero dependencies** on PyTorch, Transformers, CUDA, or any deep learning framework. Only 11 lightweight packages:  
本项目**不依赖** PyTorch、Transformers、CUDA 等深度学习框架。全部依赖仅 11 个轻量级包：

```
fastapi>=0.115.0        # Web framework / Web 框架
uvicorn>=0.34.0         # ASGI server / ASGI 服务器
openai>=1.50.0          # Hy3 API calls (OpenAI-compatible) / Hy3 API 调用（OpenAI 兼容接口）
python-multipart        # File upload support / 文件上传支持
aiofiles                # Async file I/O / 异步文件读写
PyPDF2>=3.0.0           # PDF parsing / PDF 解析
python-docx>=1.1.0      # Word document parsing / Word 文档解析
httpx>=0.28.0           # HTTP client (web search) / HTTP 客户端（网页搜索）
beautifulsoup4>=4.12.0  # HTML parsing / HTML 解析
lxml>=5.3.0             # High-performance XML/HTML parser / XML/HTML 高性能解析器
```

> Total install size ~**80 MB**. No multi-GB model weight downloads needed.  
> 总安装大小约 **80 MB**，无需下载数 GB 的模型权重文件。

## Preconfigured Files Overview / 预配置文件一览

| File / 文件 | Description / 说明 | What You Need to Do / 你需要做什么 |
|------|------|-------------|
| `.env.example` | Environment variable template / 环境变量模板 | Copy as `.env`, fill in `HY3_API_KEY` / 复制为 `.env`，填入 `HY3_API_KEY` |
| `backend/requirements.txt` | 11 lightweight dependencies / 11 个轻量依赖 | No changes needed; pip auto-installs / 无需修改，pip 自动安装 |
| `docker-compose.yml` | Docker orchestration file / Docker 编排文件 | No changes needed; works out of the box / 无需修改，开箱即用 |
| `Dockerfile` | Container image build file / 容器镜像构建文件 | No changes needed / 无需修改 |
| `start.bat` | Windows double-click launch script / Windows 双击启动脚本 | No changes needed / 无需修改 |

## Project Structure / 项目结构

```
hy3-research-assistant/
├── Dockerfile              # Container image build file / 容器镜像构建文件
├── docker-compose.yml      # Docker one-click orchestration / Docker 一键编排文件
├── backend/
│   ├── main.py            # FastAPI server (6 API endpoints, all SSE streaming) / FastAPI 服务器（6 个 API 端点，全部支持 SSE 流式输出）
│   ├── hy3_client.py      # Hy3 API client wrapper (OpenAI-compatible) / Hy3 API 客户端封装（OpenAI 兼容接口）
│   ├── tools.py            # Utility functions (web search, PDF/DOCX/code parsing) / 工具函数（网页搜索、PDF/DOCX/代码文件解析）
│   ├── cli.py              # CLI entry point (hy3-research command after pip install) / 命令行启动入口（pip 安装后可用 hy3-research 命令）
│   └── requirements.txt   # Python dependencies / Python 依赖
├── hy3-mcp-server/         # MCP Server sub-project (standalone install) / MCP Server 子项目（可独立安装）
│   ├── src/                # Source code / 源代码
│   │   ├── server.py       # FastMCP server (5 Tools) / FastMCP 服务端（5 个 Tool）
│   │   └── hy3_client.py  # Hy3 API client / Hy3 API 客户端
│   ├── pyproject.toml      # pip install config / pip 安装配置
│   └── requirements.txt   # Python dependencies / Python 依赖
├── frontend/
│   └── index.html          # Modern web frontend (dark theme, streaming, Markdown) / 现代化 Web 前端（暗色主题、流式渲染、Markdown 展示）
├── pyproject.toml          # Main project pip install config / 主项目 pip 安装配置
├── .env.example            # Environment variable config template / 环境变量配置模板
├── .gitignore
├── start.bat               # Windows one-click launch script / Windows 一键启动脚本
└── README.md
```
