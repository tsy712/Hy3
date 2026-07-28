# Hy3 研究助手

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
  <b>基于腾讯混元 Hy3 大模型的智能研究助手</b>
  <br>
  提供 <b>深度研究</b>、<b>代码分析</b>、<b>文档问答</b> 三大核心功能
</p>

---

## 📺 效果演示

<p align="center">
  <em>Hy3 研究助手 Web 界面与深度研究报告生成效果：</em>
  <br><br>
  <img src="../效果演示/demo-hy3-research-assistant.gif" alt="Hy3 研究助手效果演示" width="85%">
  <br>
  <sub>▲ 示例：输入研究主题 → Hy3 自动搜索分析 → 生成结构化研究报告</sub>
</p>

<p align="center">
  <em>接入 MCP Server 后在 CodeBuddy 中的调用效果：</em>
  <br><br>
  <img src="../效果演示/demo-mcp-integration.gif" alt="MCP Server 接入效果演示" width="85%">
  <br>
  <sub>▲ 示例：在 CodeBuddy 中透明调用 Hy3 工具完成代码评审</sub>
</p>

> 💡 **把你的演示 GIF 放到 `效果演示/` 文件夹中即会自动替换。**

> ⚡ **本项目不需要 GPU、不需要 CUDA、不需要安装 PyTorch / DeepSpeed / Flash-Attention。**
> 所有 AI 能力通过云端 API 调用，本地只需 Python 3.9+ 即可运行。

---

## 📑 目录

- [🚀 一分钟上手](#-一分钟上手)
- [项目简介](#项目简介)
- [📚 文档导航](#-文档导航)
- [三大功能](#三大功能)
- [API 端点概览](#api-端点概览)
- [👨‍💻 支持的 AI 客户端](#-支持的-ai-客户端)
- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [⚙️ 环境变量](#️-环境变量)
- [❓ 常见问题 (FAQ)](#-常见问题-faq)

---

## 🚀 一分钟上手

```bash
git clone https://github.com/Tencent-Hunyuan/Hy3.git && cd hy3-research-assistant
cp .env.example .env                     # 编辑 .env 填入 HY3_API_KEY
docker-compose up -d                     # 浏览器打开 http://localhost:8000
```

> [安装 Docker Desktop](https://docs.docker.com/get-docker/) 即可，不需要 NVIDIA Container Toolkit。

**其他启动方式**：`pip install -e . && hy3-research`（命令行）、双击 `start.bat`（Windows）。

> 详细步骤 → [快速开始指南](docs/quick-start.md)

---

## 项目简介

本项目是腾讯犀牛鸟实战计划 [Issue #4](https://github.com/Tencent-Hunyuan/Hy3/issues/4) 的完整实现。通过调用 **Hy3 API**（OpenAI 兼容接口）完成所有智能任务，不涉及模型训练/微调/本地推理。

---

## 📚 文档导航

| 文档 | 内容 |
|------|------|
| [快速开始指南](docs/quick-start.md) | 安装、配置 API Key、3 种启动方式的详细步骤 |
| [环境要求与项目结构](docs/environment.md) | 硬件/软件要求、依赖包、目录结构 |
| [本地运行 Hy3 模型](docs/local-hy3-model.md) | DeepSpeed / Flash-Attention 版本兼容、编译避坑、显存要求 |
| [功能介绍](docs/features.md) | 深度研究、代码分析、文档问答的详细说明 |
| [API 参考](docs/api-reference.md) | 6 个 API 端点、环境变量、技术栈 |
| [MCP Server](docs/mcp-server.md) | 为 Claude Desktop / Cursor 提供 Hy3 能力 |
| [常见问题](docs/faq.md) | GPU、CUDA、pip 报错、端口、MCP 等 |

---

## 三大功能

| 功能 | 说明 |
|------|------|
| 🔬 深度研究 | 自动搜索 → 分析 → 1500-3000 字专业报告 → 执行摘要 |
| 💻 代码分析 | Bug 检测、性能优化、安全审计、1-10 质量评分 |
| 📚 文档问答 | 多文档上传（PDF/DOCX/TXT），精准回答 + 原文引用 |

> 详细说明 → [功能介绍](docs/features.md)

---

## API 端点概览

| 端点 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 前端页面 |
| `/health` | GET | 健康检查 |
| `/api/research` | POST | 深度研究（SSE 流式） |
| `/api/analyze-code` | POST | 粘贴代码分析（SSE 流式） |
| `/api/analyze-code-file` | POST | 上传文件分析（SSE 流式） |
| `/api/qa-documents` | POST | 多文档问答（SSE 流式） |

---

## 技术栈

**后端** FastAPI + OpenAI SDK + Uvicorn · **前端** HTML/CSS/JS + marked.js · **模型** Hy3 (OpenAI 兼容接口)

---

## 项目结构

```
hy3-research-assistant/
├── Dockerfile, docker-compose.yml   # Docker 部署
├── backend/                         # FastAPI 服务端（main.py / hy3_client.py / tools.py / cli.py）
├── frontend/index.html              # Web 前端
├── hy3-mcp-server/                  # 独立 MCP Server 子项目
├── pyproject.toml, .env.example     # pip 安装 + 环境配置
└── start.bat                        # Windows 一键启动
```

---

## 👨‍💻 支持的 AI 客户端

Hy3 研究助手配套的 MCP Server 可接入以下 AI 客户端：

| 客户端 | 配置难度 | 说明 |
|--------|:--:|------|
| **CodeBuddy** | ⭐ | 原生支持，一键配置 JSON |
| **WorkBuddy** | ⭐ | 与 CodeBuddy 相同配置 |
| **Cursor** | ⭐⭐ | 通过 `mcp.json` 配置 |
| **Claude Desktop** | ⭐⭐ | 通过 `claude_desktop_config.json` |
| **Cline (VS Code)** | ⭐⭐ | 通过插件 MCP 设置 |

> 📘 各客户端配置详情 → [MCP Server 文档](docs/mcp-server.md)

---

## ⚙️ 环境变量

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `HY3_API_KEY` | ✅ | — | Hy3 API 密钥 |
| `HY3_BASE_URL` | ❌ | `https://api.hunyuan.cloud.tencent.com/v1` | API 端点 |
| `HY3_MODEL` | ❌ | `hunyuan-pro` | 模型名称 |
| `HOST` | ❌ | `0.0.0.0` | 服务监听地址 |
| `PORT` | ❌ | `8000` | 服务端口 |

使用 `.env` 文件配置示例：

```env
HY3_API_KEY=你的API密钥
HY3_MODEL=hunyuan-pro
# HOST=0.0.0.0
# PORT=8000
```

> ⚠️ 请勿将 `.env` 文件提交到 Git 仓库。

---

## ❓ 常见问题 (FAQ)

<details>
<summary><b>Q: 启动后无法访问 http://localhost:8000？</b></summary>

A: 检查以下几点：
- Docker 是否正在运行（`docker ps` 验证）
- 端口 8000 是否被占用（`netstat -an | findstr 8000`）
- `.env` 文件中 `HY3_API_KEY` 是否正确填入
- 容器日志：`docker-compose logs -f`
</details>

<details>
<summary><b>Q: Docker 启动太慢怎么办？</b></summary>

A: 首次启动需要下载镜像，之后会快很多。如果不需要 Docker，也可以使用以下方式直接运行：
```bash
pip install -e .
hy3-research
```
或 Windows 用户直接双击 `start.bat`。
</details>

<details>
<summary><b>Q: 需要 GPU 吗？</b></summary>

A: **不需要！** 本项目所有 AI 能力通过云端 Hy3 API 调用，本地只需要 Python 3.9+ 环境和网络连接即可运行。不需要 GPU、CUDA、PyTorch 等重型依赖。
</details>

<details>
<summary><b>Q: 深度研究报告要等多久？</b></summary>

A: 深度研究需要联网搜索 + AI 分析 + 报告生成，通常需要 30-90 秒。等待时间取决于：
- 研究主题的复杂度
- 网络搜索速度
- Hy3 API 的响应速度
报告以 SSE 流式方式输出，你可以实时看到生成进度。
</details>

<details>
<summary><b>Q: 支持哪些文件格式？</b></summary>

A:
- **文档问答**: PDF、DOCX、TXT、Markdown
- **代码分析**: 任何文本代码文件（支持粘贴或上传文件）
- **数据分析**: CSV、JSON
</details>

<details>
<summary><b>Q: API Key 从哪里获取？</b></summary>

A: 请访问腾讯混元开放平台申请 API Key。具体地址请参考官方文档。
</details>

---

## 📄 License

MIT License © 2024 Tencent Hunyuan Team
