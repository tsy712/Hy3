# Hy3 Research Assistant / Hy3 研究助手

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License MIT">
  <img src="https://img.shields.io/badge/Python-3.9+-green.svg" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/FastAPI-latest-teal.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/Hy3-Tencent%20Hunyuan-orange.svg" alt="Hy3 Tencent Hunyuan">
  <img src="https://img.shields.io/badge/Docker-Supported-2496ED.svg?logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen.svg" alt="Status Active">
  <br>
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/GPU-Not%20Required-success.svg" alt="GPU Not Required">
  <img src="https://img.shields.io/badge/SSE-Streaming-blue.svg" alt="SSE Streaming">
</p>

<p align="center">
  <b>An intelligent research assistant powered by Tencent Hunyuan Hy3 / 基于腾讯混元 Hy3 大模型的智能研究助手</b>
  <br>
  <b>Deep Research</b>, <b>Code Analysis</b>, <b>Document Q&A</b> — three core capabilities / 提供 <b>深度研究</b>、<b>代码分析</b>、<b>文档问答</b> 三大核心功能
</p>

<p align="center">
  <a href="https://github.com/Tencent-Hunyuan/Hy3"><img src="https://img.shields.io/badge/⭐-Star%20This%20Repo%20%E2%80%94%20If%20You%20Find%20It%20Useful!-yellow?style=for-the-badge" alt="Star"></a>
  <br>
  <sub>If this project helps you, please click <b>⭐ Star</b> in the top right corner! / 如果本项目对你有帮助，欢迎点击右上角 <b>⭐ Star</b> 支持！</sub>
</p>

---

## 🚀 Get Started / 一键使用

```bash
# 1. Configure API Key / 配置 API Key（复制 .env.example 后填入密钥）
cp .env.example .env

# 2. Start services / 启动服务
docker-compose up -d
```

Open **http://localhost:8000** in your browser. / 浏览器打开 **http://localhost:8000** 即可使用。

> All you need is [Docker Desktop](https://docs.docker.com/get-docker/). No GPU / CUDA / NVIDIA Container Toolkit required.  
> 仅需 [安装 Docker Desktop](https://docs.docker.com/get-docker/)，不需要 GPU / CUDA / NVIDIA Container Toolkit。  
> No Docker? One-click install: **`./install.sh`** (macOS / Linux) or **double-click `install.bat`** (Windows). See → [Quick Start Guide](docs/quick-start.md)  
> 无 Docker？一键安装：**`./install.sh`**（macOS / Linux）或 **双击 `install.bat`**（Windows）。详见 → [快速开始指南](docs/quick-start.md)

---

## 📺 Demo / 效果演示

<p align="center">
  <em>Hy3 Research Assistant Web UI & Deep Research Report Generation / Hy3 研究助手 Web 界面与深度研究报告生成效果：</em>
  <br><br>
  <img src="./docs/demo-hy3-research-assistant.gif" alt="Hy3 Research Assistant Demo" width="85%">
  <br>
  <sub>▲ Enter a research topic → Hy3 searches & analyzes → generates a structured research report / 输入研究主题 → Hy3 自动搜索分析 → 生成结构化研究报告</sub>
</p>

<p align="center">
  <em>MCP Server integration in CodeBuddy / 接入 MCP Server 后在 CodeBuddy 中的调用效果：</em>
  <br><br>
  <img src="./docs/demo-mcp-integration.gif" alt="MCP Server Integration Demo" width="85%">
  <br>
  <sub>▲ Transparently invoke Hy3 tools within CodeBuddy for code review / 在 CodeBuddy 中透明调用 Hy3 工具完成代码评审</sub>
</p>

> 💡 **Tip**: More screenshots in [`docs/screenshots/`](./docs/screenshots/). / 更多演示截图请参见 [`docs/screenshots/`](./docs/screenshots/) 目录。

> ⚡ **This project does NOT require GPU, CUDA, PyTorch, DeepSpeed, or Flash-Attention.**
> All AI capabilities are accessed via cloud API. You only need Python 3.9+ locally.  
> **本项目不需要 GPU、不需要 CUDA、不需要安装 PyTorch / DeepSpeed / Flash-Attention。**
> 所有 AI 能力通过云端 API 调用，本地只需 Python 3.9+ 即可运行。

---

## 📑 Table of Contents / 目录

- [Get Started in One Minute / 🚀 一分钟上手](#-get-started-in-one-minute--一分钟上手)
- [Project Overview / 项目简介](#project-overview--项目简介)
- [Documentation / 📚 文档导航](#-documentation--文档导航)
- [Three Core Features / 三大功能](#three-core-features--三大功能)
- [API Endpoints / API 端点概览](#api-endpoints--api-端点概览)
- [Supported AI Clients / 👨‍💻 支持的 AI 客户端](#-supported-ai-clients--支持的-ai-客户端)
- [Tech Stack / 技术栈](#tech-stack--技术栈)
- [Project Structure / 项目结构](#project-structure--项目结构)
- [Environment Variables / ⚙️ 环境变量](#️-environment-variables--环境变量)
- [FAQ / ❓ 常见问题](#-faq--常见问题)

---

## 🚀 Get Started in One Minute / 一分钟上手

```bash
git clone https://github.com/Tencent-Hunyuan/Hy3.git && cd hy3-research-assistant
cp .env.example .env                     # Edit .env and fill in HY3_API_KEY / 编辑 .env 填入 HY3_API_KEY
docker-compose up -d                     # Open http://localhost:8000 in browser / 浏览器打开 http://localhost:8000
```

> Just [install Docker Desktop](https://docs.docker.com/get-docker/). No NVIDIA Container Toolkit needed. / [安装 Docker Desktop](https://docs.docker.com/get-docker/) 即可，不需要 NVIDIA Container Toolkit。

**Other launch methods**: `pip install -e . && hy3-research` (CLI), double-click `start.bat` (Windows).  
**其他启动方式**：`pip install -e . && hy3-research`（命令行）、双击 `start.bat`（Windows）。

> Detailed steps → [Quick Start Guide](docs/quick-start.md) / 详细步骤 → [快速开始指南](docs/quick-start.md)

---

## Project Overview / 项目简介

This project is a complete implementation of Tencent Rhino-Bird Open Source Practice Plan [Issue #4](https://github.com/Tencent-Hunyuan/Hy3/issues/4). All intelligent tasks are performed via the **Hy3 API** (OpenAI-compatible interface) — no model training, fine-tuning, or local inference involved.  
本项目是腾讯犀牛鸟实战计划 [Issue #4](https://github.com/Tencent-Hunyuan/Hy3/issues/4) 的完整实现。通过调用 **Hy3 API**（OpenAI 兼容接口）完成所有智能任务，不涉及模型训练/微调/本地推理。

---

## 📚 Documentation / 文档导航

| Document / 文档 | Content / 内容 |
|------|------|
| [Quick Start Guide / 快速开始指南](docs/quick-start.md) | Installation, API Key setup, 3 launch methods / 安装、配置 API Key、3 种启动方式的详细步骤 |
| [Environment & Structure / 环境要求与项目结构](docs/environment.md) | Hardware/software requirements, dependencies, directory structure / 硬件/软件要求、依赖包、目录结构 |
| [Local Hy3 Model / 本地运行 Hy3 模型](docs/local-hy3-model.md) | ⚠️ DeepSpeed / Flash-Attention version compatibility, compilation pitfalls, VRAM requirements / DeepSpeed / Flash-Attention 版本兼容、编译避坑、显存要求 |
| [Features / 功能介绍](docs/features.md) | Detailed explanation of Deep Research, Code Analysis, Document Q&A / 深度研究、代码分析、文档问答的详细说明 |
| [API Reference / API 参考](docs/api-reference.md) | 6 API endpoints, environment variables, tech stack / 6 个 API 端点、环境变量、技术栈 |
| [MCP Server](docs/mcp-server.md) | Provide Hy3 capabilities to Claude Desktop / Cursor / 为 Claude Desktop / Cursor 提供 Hy3 能力 |
| [FAQ / 常见问题](docs/faq.md) | GPU, CUDA, pip errors, ports, MCP, etc. / GPU、CUDA、pip 报错、端口、MCP 等 |

---

## Three Core Features / 三大功能

| Feature / 功能 | Description / 说明 |
|------|------|
| 🔬 Deep Research / 深度研究 | Auto search → analysis → 1500-3000 word professional report → executive summary / 自动搜索 → 分析 → 1500-3000 字专业报告 → 执行摘要 |
| 💻 Code Analysis / 代码分析 | Bug detection, performance optimization, security audit, 1-10 quality score / Bug 检测、性能优化、安全审计、1-10 质量评分 |
| 📚 Document Q&A / 文档问答 | Multi-document upload (PDF/DOCX/TXT), precise answers + source citations / 多文档上传（PDF/DOCX/TXT），精准回答 + 原文引用 |

> Details → [Features](docs/features.md) / 详细说明 → [功能介绍](docs/features.md)

---

## API Endpoints / API 端点概览

| Endpoint / 端点 | Method / 方法 | Description / 说明 |
|------|------|------|
| `/` | GET | Frontend page / 前端页面 |
| `/health` | GET | Health check / 健康检查 |
| `/api/research` | POST | Deep Research (SSE streaming) / 深度研究（SSE 流式） |
| `/api/analyze-code` | POST | Paste code analysis (SSE streaming) / 粘贴代码分析（SSE 流式） |
| `/api/analyze-code-file` | POST | Upload code file analysis (SSE streaming) / 上传文件分析（SSE 流式） |
| `/api/qa-documents` | POST | Multi-document Q&A (SSE streaming) / 多文档问答（SSE 流式） |

---

## Tech Stack / 技术栈

**Backend** FastAPI + OpenAI SDK + Uvicorn · **Frontend** HTML/CSS/JS + marked.js · **Model** Hy3 (OpenAI-compatible API)  
**后端** FastAPI + OpenAI SDK + Uvicorn · **前端** HTML/CSS/JS + marked.js · **模型** Hy3 (OpenAI 兼容接口)

---

## Project Structure / 项目结构

```
hy3-research-assistant/
├── Dockerfile, docker-compose.yml   # Docker deployment / Docker 部署
├── install.sh, install.bat          # One-click install scripts (Linux/macOS + Windows) / 一键安装脚本
├── start.bat                        # Windows one-click launch / Windows 一键启动
├── backend/                         # FastAPI server (main.py / hy3_client.py / tools.py / cli.py) / FastAPI 服务端
├── frontend/index.html              # Web frontend / Web 前端
├── hy3-mcp-server/                  # Standalone MCP Server sub-project / 独立 MCP Server 子项目
├── pyproject.toml, .env.example     # pip install + env config / pip 安装 + 环境配置
└── docs/                            # 📚 Detailed documentation / 详细文档
```

---

## 👨‍💻 Supported AI Clients / 支持的 AI 客户端

The companion MCP Server integrates Hy3 into the following AI clients: / Hy3 研究助手配套的 MCP Server 可接入以下 AI 客户端：

| Client / 客户端 | Difficulty / 配置难度 | Notes / 说明 |
|--------|:--:|------|
| **CodeBuddy** | ⭐ | Native support, one-click JSON config / 原生支持，一键配置 JSON |
| **WorkBuddy** | ⭐ | Same config as CodeBuddy / 与 CodeBuddy 相同配置 |
| **Cursor** | ⭐⭐ | Via `mcp.json` / 通过 `mcp.json` 配置 |
| **Claude Desktop** | ⭐⭐ | Via `claude_desktop_config.json` / 通过 `claude_desktop_config.json` |
| **Cline (VS Code)** | ⭐⭐ | Via plugin MCP settings / 通过插件 MCP 设置 |

> 📘 Configuration details → [MCP Server Docs](docs/mcp-server.md) / 各客户端配置详情 → [MCP Server 文档](docs/mcp-server.md)

---

## 🔌 MCP — Instantly Effective After Connection / MCP 连接即生效

Once the MCP Server is configured, Hy3 tools automatically appear in your AI client. Just chat to trigger: / 配置好 MCP Server 后，Hy3 工具会自动出现在你的 AI 客户端中。直接对话即可触发：

```
User: "Research the latest WebAssembly developments in 2024"

AI auto-invokes hy3_research → searches & analyzes → generates a 1000+ word report ✅

User: "@main.py Review code quality"

AI auto-invokes hy3_code_review → security + performance + scoring ✅

User: "@contract.pdf Analyze contract risk clauses"

AI auto-invokes hy3_doc_qa → clause-by-clause analysis + source citations ✅
```

```
用户: "帮我调研 WebAssembly 2024 最新进展"

AI 自动调用 hy3_research → 搜索分析 → 生成千字报告 ✅

用户: "@main.py 审查代码质量"

AI 自动调用 hy3_code_review → 安全漏洞 + 性能建议 + 评分 ✅

用户: "@contract.pdf 分析合同风险条款"

AI 自动调用 hy3_doc_qa → 逐条分析 + 原文引用 ✅
```

> 💡 **No coding, no manual API calls** — just ask your AI, and Hy3 tools execute in the background.  
> **无需编写代码、无需手动调用 API** — 请直接向 AI 提问，Hy3 工具在后台自动执行。

---

## ⚙️ Environment Variables / 环境变量

| Variable / 变量名 | Required / 必填 | Default / 默认值 | Description / 说明 |
|--------|------|--------|------|
| `HY3_API_KEY` | ✅ | — | Hy3 API key / 密钥 |
| `HY3_BASE_URL` | ❌ | `https://api.hunyuan.cloud.tencent.com/v1` | API endpoint / API 端点 |
| `HY3_MODEL` | ❌ | `hunyuan-pro` | Model name / 模型名称 |
| `HOST` | ❌ | `0.0.0.0` | Server bind address / 服务监听地址 |
| `PORT` | ❌ | `8000` | Server port / 服务端口 |

Example `.env` file / 使用 `.env` 文件配置示例：

```env
HY3_API_KEY=your-api-key
HY3_MODEL=hunyuan-pro
# HOST=0.0.0.0
# PORT=8000
```

> ⚠️ Do NOT commit `.env` to your Git repository. / 请勿将 `.env` 文件提交到 Git 仓库。

---

## ❓ FAQ / 常见问题

<details>
<summary><b>Q: Can't access http://localhost:8000 after starting? / 启动后无法访问 http://localhost:8000？</b></summary>

A: Check the following / 检查以下几点：
- Is Docker running? (`docker ps` to verify) / Docker 是否正在运行（`docker ps` 验证）
- Is port 8000 in use? (`netstat -an | findstr 8000`) / 端口 8000 是否被占用（`netstat -an | findstr 8000`）
- Is `HY3_API_KEY` correctly set in `.env`? / `.env` 文件中 `HY3_API_KEY` 是否正确填入
- Check container logs: `docker-compose logs -f` / 查看容器日志：`docker-compose logs -f`
</details>

<details>
<summary><b>Q: Docker startup is too slow? / Docker 启动太慢怎么办？</b></summary>

A: The first launch needs to pull images; subsequent launches are much faster. If you don't need Docker, run directly: / 首次启动需要下载镜像，之后会快很多。如果不需要 Docker，也可以直接运行：
```bash
pip install -e .
hy3-research
```
Or Windows users can double-click `start.bat`. / Windows 用户直接双击 `start.bat`。
</details>

<details>
<summary><b>Q: Do I need a GPU? / 需要 GPU 吗？</b></summary>

A: **No!** All AI capabilities run via the cloud Hy3 API. You only need Python 3.9+ and an internet connection. No GPU, CUDA, PyTorch, or other heavy dependencies.  
**不需要！** 本项目所有 AI 能力通过云端 Hy3 API 调用，本地只需要 Python 3.9+ 环境和网络连接即可运行。不需要 GPU、CUDA、PyTorch 等重型依赖。
</details>

<details>
<summary><b>Q: How long does a deep research report take? / 深度研究报告要等多久？</b></summary>

A: Deep research requires web search + AI analysis + report generation, typically 30-90 seconds. Wait time depends on: / 深度研究需要联网搜索 + AI 分析 + 报告生成，通常需要 30-90 秒。等待时间取决于：
- Complexity of the research topic / 研究主题的复杂度
- Web search speed / 网络搜索速度
- Hy3 API response time / Hy3 API 的响应速度
The report is streamed via SSE, so you can watch the generation progress in real time. / 报告以 SSE 流式方式输出，你可以实时看到生成进度。
</details>

<details>
<summary><b>Q: What file formats are supported? / 支持哪些文件格式？</b></summary>

A:
- **Document Q&A**: PDF, DOCX, TXT, Markdown / 文档问答: PDF、DOCX、TXT、Markdown
- **Code Analysis**: Any text code file (paste or upload) / 代码分析: 任何文本代码文件（支持粘贴或上传文件）
- **Data Analysis**: CSV, JSON / 数据分析: CSV、JSON
</details>

<details>
<summary><b>Q: Where do I get an API Key? / API Key 从哪里获取？</b></summary>

A: Please visit the Tencent Hunyuan Open Platform to apply for an API key. Refer to the official documentation for the exact address. / 请访问腾讯混元开放平台申请 API Key。具体地址请参考官方文档。
</details>

---

## 📄 License

MIT License © 2024 Tencent Hunyuan Team
