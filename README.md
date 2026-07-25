# Hy3 研究助手

基于腾讯混元 Hy3 大模型的智能研究助手，提供**深度研究**、**代码分析**、**文档问答**三大核心功能。

## 项目简介

本项目是腾讯犀牛鸟实战计划 [Issue #4](https://github.com/Tencent-Hunyuan/Hy3/issues/4) 的完整实现。所有智能任务（研究规划、报告生成、代码分析、文档问答）均通过调用 **Hy3 API**（OpenAI 兼容接口）完成，不涉及模型训练、微调或本地推理。

### Hy3 在项目中的角色

| 功能模块 | Hy3 的角色 |
|---------|-----------|
| 深度研究 | 研究计划制定 → 搜索关键词生成 → 长文报告撰写 → 执行摘要提炼 |
| 代码分析 | 代码理解、Bug 检测、性能优化建议、安全审计、质量评分 |
| 文档问答 | 多文档阅读理解、证据驱动的精准问答 |

## 项目结构

```
hy3-research-assistant-package/
├── backend/
│   ├── main.py            # FastAPI 服务器（6 个 API 端点，全部支持 SSE 流式输出）
│   ├── hy3_client.py      # Hy3 API 客户端封装（OpenAI 兼容接口）
│   ├── tools.py            # 工具函数（网页搜索、PDF/DOCX/代码文件解析）
│   ├── cli.py              # 命令行启动入口（pip 安装后可用 hy3-research 命令）
│   └── requirements.txt   # Python 依赖
├── hy3-mcp-server/         # MCP Server 子项目（可独立安装）
│   ├── src/                # 源代码
│   │   ├── server.py       # FastMCP 服务端（5 个 Tool）
│   │   └── hy3_client.py  # Hy3 API 客户端
│   ├── pyproject.toml      # pip 安装配置
│   └── requirements.txt   # Python 依赖
├── frontend/
│   └── index.html          # 现代化 Web 前端（暗色主题、流式渲染、Markdown 展示）
├── pyproject.toml          # 主项目 pip 安装配置
├── .env.example            # 环境变量配置模板
├── start.bat               # Windows 一键启动脚本
├── 安装说明.md              # 详细安装说明
└── README.md
```

## 快速开始

### 环境要求

- Python 3.9+
- 有效的 Hy3 API Key

### 方式一：pip 安装（推荐）

```bash
cd hy3-research-assistant-package

# pip 安装（自动处理依赖）
pip install -e .

# 配置 API 密钥
# Windows:  set HY3_API_KEY=你的API密钥
# macOS/Linux: export HY3_API_KEY=你的API密钥
# 或复制 .env.example 为 .env 并填入密钥

# 一键启动
hy3-research
# 服务运行在 http://localhost:8000
```

### 方式二：手动安装

```bash
cd backend
pip install -r requirements.txt
cd ..
python backend/main.py
```

### 方式三：Windows 一键启动

双击 `start.bat`（自动检测 API Key、安装依赖、启动服务）

### 可选环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `HY3_API_KEY` | Hy3 API 密钥（必填） | - |
| `HY3_BASE_URL` | API 端点地址 | `https://api.hunyuan.cloud.tencent.com/v1` |
| `HY3_MODEL` | 模型名称 | `hunyuan-pro` |
| `PORT` | 服务端口 | `8000` |

## 三大功能

### 深度研究 (Deep Research)

输入研究主题，Hy3 将自动完成：

1. **研究规划** — 将主题拆解为子问题，生成搜索关键词
2. **资料搜索** — 自动搜索相关网页资料
3. **报告撰写** — 基于搜索结果生成 1500-3000 字专业研究报告
4. **执行摘要** — 提炼核心发现的简明摘要

### 代码分析 (Code Analysis)

粘贴代码或上传代码文件，Hy3 将提供：

- 代码概览与核心功能解读
- 执行逻辑与关键流程分析
- 潜在 Bug、性能隐患、安全问题诊断
- 具体优化建议与最佳实践
- 1-10 分代码质量评分

### 文档问答 (Document Q&A)

上传多个文档（支持 PDF、DOCX、TXT、代码文件等），向 Hy3 提问：

- 基于文档内容精准回答
- 引用原始段落作为证据
- 明确标注信息缺失情况

## API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 前端页面 |
| `/health` | GET | 服务健康检查 |
| `/api/research` | POST | 深度研究（流式） |
| `/api/analyze-code` | POST | 粘贴代码分析（流式） |
| `/api/analyze-code-file` | POST | 上传代码文件分析（流式） |
| `/api/qa-documents` | POST | 多文档问答（流式） |

所有智能端点均使用 Server-Sent Events (SSE) 实现流式输出，支持前端实时渲染。

## 技术栈

- **后端**: FastAPI + OpenAI SDK + Uvicorn
- **前端**: 原生 HTML/CSS/JS + marked.js（Markdown 渲染）
- **模型**: 腾讯混元 Hy3（通过 OpenAI 兼容接口调用）
- **工具**: DuckDuckGo 网页搜索、PyPDF2、python-docx

## Hy3 MCP Server

`hy3-mcp-server` 为独立的子项目，将 Hy3 能力封装为 MCP 协议工具。

### 快速安装

```bash
cd hy3-mcp-server
pip install -e .
# 或双击 setup.bat（Windows）
```

### 配置 Claude Desktop

在 `claude_desktop_config.json` 中添加：

```json
{
  "mcpServers": {
    "hy3": {
      "command": "hy3-mcp",
      "env": { "HY3_API_KEY": "你的API密钥" }
    }
  }
}
```

### MCP 工具列表

| 工具名 | 功能 |
|--------|------|
| `hy3_research` | 深度研究：搜索 + 分析 + 报告 |
| `hy3_code_review` | 代码评审：Bug检测 + 性能 + 安全 |
| `hy3_doc_qa` | 文档问答：解析 + 精准回答 |
| `hy3_data_analyze` | 数据分析：CSV/JSON + 洞察 |
| `hy3_chat` | 通用对话 |

---

## CodeBuddy 协作说明

本项目借助 CodeBuddy AI 编程助手完成：

- **协同设计**：AI 参与整体架构规划、功能模块拆解、前后端交互设计
- **代码生成**：AI 编写了后端服务器、API 客户端、工具函数、前端界面
- **文档撰写**：AI 生成了 README、配置模板、启动脚本、安装说明
- **安装包制作**：AI 创建了 pyproject.toml，支持 pip install -e . 安装
