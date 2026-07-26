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
hy3-research-assistant/
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
├── .gitignore
├── start.bat               # Windows 一键启动脚本
└── README.md
```

## 环境要求

### 硬件要求

| 项目 | 最低配置 | 推荐配置 |
|------|---------|---------|
| CPU | 任意双核处理器 | 四核及以上 |
| 内存 | 512 MB | 1 GB+ |
| 磁盘 | 200 MB | 500 MB+ |
| GPU | **不需要** | **不需要** |
| 网络 | 宽带连接 | 稳定宽带 |

> **重要说明：本项目不需要 GPU 或 CUDA。**  
> 所有 AI 推理任务均通过 HTTP 调用腾讯混元 Hy3 云端 API 完成，不涉及本地模型加载、推理或训练。  
> 如果你的目标是 **本地运行/微调 Hy3 模型本身**，请参考 [Hy3 官方仓库](https://github.com/Tencent-Hunyuan/Hy3) 的硬件要求（需要 NVIDIA GPU + CUDA 11.8+）。

### 软件要求

| 依赖 | 版本要求 | 说明 |
|------|---------|------|
| Python | **3.9+**（主项目）/ **3.10+**（MCP Server） | 推荐 3.11 |
| pip | 23.0+ | 随 Python 一起安装 |
| 操作系统 | Windows 10+ / macOS 12+ / Linux（任意发行版） | 均支持 |

### 依赖包总览

本项目**不依赖** PyTorch、Transformers、CUDA 等深度学习框架。全部依赖仅 11 个轻量级包：

```
fastapi>=0.115.0        # Web 框架
uvicorn>=0.34.0         # ASGI 服务器
openai>=1.50.0          # Hy3 API 调用（OpenAI 兼容接口）
python-multipart        # 文件上传支持
aiofiles                # 异步文件读写
PyPDF2>=3.0.0           # PDF 解析
python-docx>=1.1.0      # Word 文档解析
httpx>=0.28.0           # HTTP 客户端（网页搜索）
beautifulsoup4>=4.12.0  # HTML 解析
lxml>=5.3.0             # XML/HTML 高性能解析器
```

> 总安装大小约 **80 MB**，无需下载数 GB 的模型权重文件。

---

## 快速开始

### 零、获取 Hy3 API Key

使用前需要有效的 Hy3 API 密钥。获取方式请参考 [Hy3 官方文档](https://github.com/Tencent-Hunyuan/Hy3)。

### 一、克隆项目

```bash
git clone https://github.com/Tencent-Hunyuan/Hy3.git
cd hy3-research-assistant
```

### 二、配置 API 密钥

**方式 A：环境变量（推荐）**

| 操作系统 | 命令 |
|---------|------|
| Windows (CMD) | `set HY3_API_KEY=你的API密钥` |
| Windows (PowerShell) | `$env:HY3_API_KEY="你的API密钥"` |
| macOS / Linux | `export HY3_API_KEY=你的API密钥` |

**方式 B：.env 文件（持久化）**

```bash
# 复制模板
copy .env.example .env        # Windows CMD
cp .env.example .env          # macOS / Linux

# 用任意文本编辑器打开 .env，填入密钥：
# HY3_API_KEY=你的API密钥
```

### 三、安装与启动

<details open>
<summary><b>方式一：pip 安装（推荐，支持命令行启动）</b></summary>

```bash
# === Windows (PowerShell) ===
python -m venv venv
.\venv\Scripts\activate
pip install -e .
hy3-research

# === macOS / Linux ===
python3 -m venv venv
source venv/bin/activate
pip install -e .
hy3-research

# 服务运行在 http://localhost:8000
```

</details>

<details>
<summary><b>方式二：手动安装（不创建命令行入口）</b></summary>

```bash
# === Windows (PowerShell) ===
python -m venv venv
.\venv\Scripts\activate
cd backend
pip install -r requirements.txt
python main.py

# === macOS / Linux ===
python3 -m venv venv
source venv/bin/activate
cd backend
pip install -r requirements.txt
python main.py

# 服务运行在 http://localhost:8000
```

</details>

<details>
<summary><b>方式三：一键脚本（Windows）</b></summary>

```bash
# 双击 start.bat 或在终端中运行：
.\start.bat
```

</details>

安装完成后，打开浏览器访问 `http://localhost:8000` 即可使用。

### 四、验证安装

```bash
# 健康检查
curl http://localhost:8000/health
# 预期输出: {"status":"healthy","hy3_connected":true}

# 或直接浏览器打开 http://localhost:8000/health
```

### 可选环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `HY3_API_KEY` | Hy3 API 密钥（**必填**） | - |
| `HY3_BASE_URL` | API 端点地址 | `https://api.hunyuan.cloud.tencent.com/v1` |
| `HY3_MODEL` | 模型名称 | `hunyuan-pro` |
| `PORT` | 服务端口 | `8000` |

---

## 常见问题 (FAQ)

### Q: 需要 GPU 吗？需要安装 CUDA 吗？

**不需要。** 本项目所有 AI 能力通过云端 API 调用实现，本地仅运行轻量级 Web 服务器。一台普通笔记本即可运行。

### Q: 和 Hy3 官方仓库的 requirements.txt 有何区别？

Hy3 官方仓库包含模型训练/微调依赖（`torch`、`transformers`、`deepspeed`、`flash-attn` 等），需要 NVIDIA GPU + CUDA。本项目是 Hy3 的上层应用，只依赖 Web 框架和 HTTP 客户端，**两者互不冲突**。

### Q: pip install 报错怎么办？

```bash
# 1. 升级 pip
python -m pip install --upgrade pip

# 2. 如果在 Windows 上遇到 lxml 编译错误，安装预编译版：
pip install lxml --only-binary=lxml

# 3. 检查 Python 版本
python --version  # 需要 >= 3.9
```

### Q: 服务启动后页面打不开？

1. 确认终端显示 `Uvicorn running on http://0.0.0.0:8000`
2. 检查防火墙是否拦截端口 8000
3. 尝试 `http://127.0.0.1:8000`（而非 localhost）

### Q: 提示 "未设置 HY3_API_KEY"？

```bash
# 临时设置（仅当前终端有效）
# Windows CMD:     set HY3_API_KEY=你的密钥
# Windows PowerShell: $env:HY3_API_KEY="你的密钥"
# macOS/Linux:     export HY3_API_KEY=你的密钥

# 或创建 .env 文件永久生效
echo HY3_API_KEY=你的密钥 > .env    # Windows
echo "HY3_API_KEY=你的密钥" > .env  # macOS/Linux
```

### Q: 如何为其他 LLM 客户端提供 Hy3 能力？

使用项目自带的 MCP Server：

```bash
cd hy3-mcp-server
pip install -e .
# 然后在 Claude Desktop / Cursor 中配置 hy3-mcp 命令
```

## 三大功能

### 🔬 深度研究 (Deep Research)

输入研究主题，Hy3 将自动完成：

1. **研究规划** — 将主题拆解为子问题，生成搜索关键词
2. **资料搜索** — 自动搜索相关网页资料
3. **报告撰写** — 基于搜索结果生成 1500-3000 字专业研究报告
4. **执行摘要** — 提炼核心发现的简明摘要

### 💻 代码分析 (Code Analysis)

粘贴代码或上传代码文件，Hy3 将提供：

- 代码概览与核心功能解读
- 执行逻辑与关键流程分析
- 潜在 Bug、性能隐患、安全问题诊断
- 具体优化建议与最佳实践
- 1-10 分代码质量评分

### 📚 文档问答 (Document Q&A)

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

## CodeBuddy 协作说明

本项目借助 CodeBuddy AI 编程助手完成：

- **协同设计**：AI 参与整体架构规划、功能模块拆解、前后端交互设计
- **代码生成**：AI 编写了 `backend/main.py`（服务器和所有提示词工程）、`backend/hy3_client.py`（API 客户端封装）、`backend/tools.py`（搜索和文件解析）、`frontend/index.html`（完整前端界面）
- **文档撰写**：AI 生成了 README、配置模板、启动脚本
- **代码审查与打磨**：AI 辅助进行了语法检查、中英文翻译、结构优化

---

## Hy3 MCP Server

`hy3-mcp-server` 是一个独立的 Python 包，将 Hy3 大模型能力封装为 MCP (Model Context Protocol) 工具，让 Claude Desktop、Cursor 等客户端直接调用。

### 安装

```bash
cd hy3-mcp-server
pip install -e .
```

### 配置 Claude Desktop

在 Claude Desktop 的 `claude_desktop_config.json` 中添加：

```json
{
  "mcpServers": {
    "hy3": {
      "command": "hy3-mcp",
      "env": {
        "HY3_API_KEY": "你的API密钥"
      }
    }
  }
}
```

### 提供的工具

| 工具名 | 功能 |
|--------|------|
| `hy3_research` | 深度研究：搜索 + 分析 + 生成报告 |
| `hy3_code_review` | 代码评审：Bug 检测 + 性能分析 + 安全审计 |
| `hy3_doc_qa` | 文档问答：文件解析 + 精准回答 |
| `hy3_data_analyze` | 数据分析：CSV/JSON + 洞察输出 |
| `hy3_chat` | 通用对话：自由问答 |
