# Hy3 MCP Server

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/Python-3.9+-green.svg" alt="Python: 3.9+">
  <img src="https://img.shields.io/badge/MCP-Protocol-purple.svg" alt="MCP Protocol">
  <img src="https://img.shields.io/badge/Hy3-Tencent%20Hunyuan-orange.svg" alt="Hy3: Tencent Hunyuan">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen.svg" alt="Status: Active">
  <img src="https://img.shields.io/badge/FastMCP-%3E%3D2.0.0-blue.svg" alt="FastMCP >= 2.0.0">
  <br>
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Docker-Supported-2496ED.svg?logo=docker&logoColor=white" alt="Docker">
</p>

<p align="center">
  <b>基于 MCP (Model Context Protocol) 协议，封装腾讯混元 Hy3 大模型能力的智能工具集</b>
  <br>
  可一键安装、即插即用到任何支持 MCP 的 AI 客户端（CodeBuddy / WorkBuddy / Cursor / Cline / Claude Desktop 等）
</p>

---

## 📺 效果演示

<p align="center">
  <em>在 CodeBuddy 中接入 Hy3 MCP Server 后的实际对话效果：</em>
  <br><br>
  <img src="./docs/demo-codebuddy-hy3-research.gif" alt="CodeBuddy + Hy3 MCP Server 效果演示" width="85%">
  <br>
  <sub>▲ 示例：在 CodeBuddy 中调用 <code>hy3_research</code> 工具进行深度研究</sub>
</p>

> 💡 **推荐**: 更多演示截图和客户端配置效果请参见 [`docs/screenshots/`](./docs/screenshots/) 目录。

---

## 📑 目录

- [项目简介](#项目简介)
- [项目结构](#项目结构)
- [🚀 快速开始](#快速开始)
- [在 AI 客户端中配置](#在-ai-客户端中配置)
- [🔧 工具说明](#工具说明)
- [技术细节](#技术细节)
- [⚙️ 环境变量](#环境变量)
- [🧪 手动测试](#手动测试)
- [❓ 常见问题 (FAQ)](#常见问题-faq)
- [CodeBuddy 协作说明](#codebuddy-协作说明)

---

## 项目简介

本项目是**腾讯犀牛鸟实战计划 [Issue #3](https://github.com/Tencent-Hunyuan/Hy3/issues/3)** 的完整实现。通过 MCP 协议将 Hy3 大模型的能力暴露为标准化工具（Tools），让支持 MCP 的 AI 客户端可以直接调用 Hy3 完成深度研究、代码评审、文档问答、数据分析等任务。

### Hy3 在本项目中的角色

所有工具的**核心推理、分析、生成能力**均由 Hy3 API 提供：

| 工具 | Hy3 的角色 |
|------|-----------|
| `hy3_research` | 搜索资料整合 → 报告规划 → 长文撰写 → 执行摘要提炼 |
| `hy3_code_review` | 代码理解 → Bug 检测 → 性能分析 → 安全审计 → 优化建议 |
| `hy3_doc_qa` | 文档阅读理解 → 证据驱动的精准问答 |
| `hy3_data_analyze` | 数据模式识别 → 趋势分析 → 洞察生成 → 行动建议 |
| `hy3_chat` | 自由对话、创意写作、翻译、解释等通用场景 |

---

## 项目结构

```
hy3-mcp-server/
├── src/
│   ├── server.py          # MCP Server 主程序（5 个 Tool）
│   ├── hy3_client.py      # Hy3 API 客户端（OpenAI 兼容封装）
│   └── __init__.py
├── configs/
│   ├── codebuddy-mcp.json # CodeBuddy / WorkBuddy 配置示例
│   ├── cursor-mcp.json    # Cursor 配置示例
│   ├── claude-mcp.json    # Claude Desktop 配置示例
│   └── cline-mcp.json     # Cline 配置示例
├── demo/
│   ├── cover.png          # 项目封面图
│   └── index.html         # 演示页面
├── v2-async/              # v2 异步架构版（性能优化）
│   ├── src/               # 异步 MCP Server + hy3_client
│   ├── tests/             # pytest 单元测试
│   ├── pyproject.toml     # pip 安装配置
│   └── README.md          # v2 版本文档
├── tests/                 # 测试文件
│   ├── test_hy3_client.py
│   └── test_server.py
├── requirements.txt        # Python 依赖
├── setup.bat               # Windows 一键安装脚本
├── setup.sh                # Linux/macOS 一键安装脚本
├── .env.example            # 环境变量模板
└── README.md               # 本文档
```

> 📌 **版本说明**: `v2-async/` 为异步架构版本（Python 3.10+），支持 httpx 异步并发；根目录为 v1 同步版（Python 3.9+），更稳定。详细对比见 [`v2-async/README.md`](./v2-async/README.md)。

---

## 快速开始

### 环境要求

- Python 3.9+
- 有效的 Hy3 API Key

### 一键安装

**Windows：**
```batch
cd hy3-mcp-server
set HY3_API_KEY=你的API密钥
setup.bat
```

**Linux / macOS：**
```bash
cd hy3-mcp-server
export HY3_API_KEY=你的API密钥
bash setup.sh
```

或手动安装：
```bash
pip install -r requirements.txt
```

---

## 在 AI 客户端中配置

### 1. CodeBuddy / WorkBuddy

将以下配置添加到 CodeBuddy 的 MCP 设置中：

```json
{
  "mcpServers": {
    "hy3-assistant": {
      "type": "stdio",
      "command": "python",
      "args": ["src/server.py"],
      "cwd": "你的hy3-mcp-server项目路径",
      "env": {
        "HY3_API_KEY": "你的API密钥",
        "HY3_MODEL": "hunyuan-pro"
      }
    }
  }
}
```

配置完成后，在 CodeBuddy 对话中即可直接调用 Hy3 工具，例如：
> "请用 hy3_research 帮我研究一下大模型在医疗领域的应用"

### 2. Cursor

将 `configs/cursor-mcp.json` 的内容复制到 `.cursor/mcp.json`（项目级）或 `~/.cursor/mcp.json`（全局级）。

### 3. Claude Desktop

将 `configs/claude-mcp.json` 的内容添加到 Claude Desktop 的配置文件中：
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### 4. Cline (VS Code 插件)

将 `configs/cline-mcp.json` 的内容添加到 Cline 的 MCP 设置中。

---

## 工具说明

### 🔬 hy3_research — 深度研究助手

自动搜索网络资料，由 Hy3 大模型分析并生成结构化研究报告。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `topic` | string | ✅ | 研究主题 |
| `depth` | string | ❌ | 研究深度：`"detailed"`(默认) 或 `"brief"` |

**示例调用：**
```
请用 hy3_research 研究"新能源汽车电池回收技术的现状与挑战"，depth=detailed
```

### 💻 hy3_code_review — 代码评审助手

对代码进行多维度审查：Bug 检测、性能分析、安全审计、优化建议。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `code` | string | ✅ | 需审查的完整代码 |
| `language` | string | ❌ | 编程语言，默认 `"auto"` |
| `review_focus` | string | ❌ | 审查重点：`"comprehensive"`(默认)、`"security"`、`"performance"`、`"bugs"` |

**示例调用：**
```
请用 hy3_code_review 审查以下代码，重点关注安全问题：
[贴入代码]
```

### 📚 hy3_doc_qa — 文档问答助手

读取本地文档，由 Hy3 基于文档内容精准回答。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file_path` | string | ✅ | 文档的本地路径 |
| `question` | string | ✅ | 你想问的问题 |

支持格式：`.txt` `.md` `.py` `.js` `.ts` `.json` `.csv` `.html` `.css` `.yaml`

**示例调用：**
```
请用 hy3_doc_qa 读取 /path/to/report.md，回答"报告中有哪些关键数据指标？"
```

### 📊 hy3_data_analyze — 数据分析助手

读取 CSV 或 JSON 数据，由 Hy3 进行深度分析和洞察输出。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file_path` | string | ✅ | 数据文件路径（.csv/.json） |
| `analysis_goal` | string | ❌ | 分析目标，默认 `"全面分析"` |

**示例调用：**
```
请用 hy3_data_analyze 分析 /path/to/sales.csv，"分析各季度的销售趋势并找出异常数据"
```

### 💬 hy3_chat — 通用对话助手

与 Hy3 自由对话，适用于其他工具未覆盖的灵活场景。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `message` | string | ✅ | 你想说的话或问题 |
| `system_prompt` | string | ❌ | 设定 AI 角色与行为 |

---

## 技术细节

- **MCP 协议**: 使用 Python FastMCP 框架，遵循标准 stdio 传输模式
- **Hy3 调用**: 通过 OpenAI 兼容接口，支持 `HY3_API_KEY`、`HY3_BASE_URL`、`HY3_MODEL` 环境变量
- **配置方式**: 支持环境变量和 `.env` 文件两种配置（环境变量优先级更高）
- **数据源**: DuckDuckGo 网页搜索（无需额外 API Key）、本地文件读取
- **安全**: API Key 仅通过环境变量或 `.env` 文件传入，代码中无硬编码

---

## ⚙️ 环境变量

支持两种配置方式（优先级：环境变量 > `.env` 文件）：

### 方式一：环境变量

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `HY3_API_KEY` | ✅ | - | Hy3 API 密钥 |
| `HY3_BASE_URL` | ❌ | `https://api.hunyuan.cloud.tencent.com/v1` | API 端点 |
| `HY3_MODEL` | ❌ | `hunyuan-pro` | 模型名称 |

### 方式二：`.env` 文件

在项目根目录创建 `.env` 文件：

```env
HY3_API_KEY=你的API密钥
HY3_MODEL=hunyuan-pro
# HY3_BASE_URL=https://api.hunyuan.cloud.tencent.com/v1  # 可选
```

> ⚠️ 请勿将 `.env` 文件提交到 Git 仓库（已在 `.gitignore` 中排除）。

---

## 手动测试

启动 MCP Server 进行本地验证：
```bash
cd src
export HY3_API_KEY=你的API密钥
python server.py
```

或使用 MCP Inspector 调试：
```bash
npx @modelcontextprotocol/inspector python src/server.py
```

---

## ❓ 常见问题 (FAQ)

<details>
<summary><b>Q: 启动时提示 "HY3_API_KEY not found" 怎么办？</b></summary>

A: 请确认已正确设置环境变量或 `.env` 文件。在终端中运行以下命令验证：
```bash
# Windows (CMD)
echo %HY3_API_KEY%
# Windows (PowerShell)
$env:HY3_API_KEY
# Linux/macOS
echo $HY3_API_KEY
```
如为空，请重新设置：
```bash
export HY3_API_KEY=你的API密钥
```
或创建 `.env` 文件在项目根目录中。
</details>

<details>
<summary><b>Q: 在 CodeBuddy 中看不到 hy3 工具怎么办？</b></summary>

A: 请检查以下事项：
1. 确保 JSON 配置中的 `cwd` 路径正确（建议使用绝对路径）
2. 确保 `python` 命令可用（终端中运行 `python --version` 验证）
3. 检查 `src/server.py` 文件是否存在且无语法错误
4. 重启 CodeBuddy 以重新加载 MCP 配置
5. 查看 CodeBuddy 的 MCP 日志
</details>

<details>
<summary><b>Q: 工具调用返回错误怎么办？</b></summary>

A: 常见原因及解决方案：
- **API Key 无效**: 确认 Key 有效且未过期
- **网络问题**: 检查是否能访问 `https://api.hunyuan.cloud.tencent.com`
- **模型不可用**: 尝试将 `HY3_MODEL` 改为其他可用模型
- **请求超时**: 复杂任务（如深度研究）可能需要较长时间
</details>

<details>
<summary><b>Q: 支持哪些文档格式和代码语言？</b></summary>

A:
- **文档问答** (`hy3_doc_qa`): 支持 `.txt` `.md` `.py` `.js` `.ts` `.json` `.csv` `.html` `.css` `.yaml`
- **数据分析** (`hy3_data_analyze`): 支持 `.csv` 和 `.json`
- **代码评审** (`hy3_code_review`): 支持所有编程语言，`language="auto"` 自动检测
</details>

<details>
<summary><b>Q: 如何更新到最新版本？</b></summary>

A:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
python src/server.py
```
</details>

---

## CodeBuddy 协作说明

本项目借助 CodeBuddy AI 编程助手完成：

- **架构设计**: AI 参与 MCP Server 整体架构、工具拆解和接口设计
- **代码生成**: AI 编写了 `server.py`（5 个 MCP Tool + Hy3 调用逻辑）、`hy3_client.py`（API 客户端封装）
- **多客户端适配**: AI 生成了 CodeBuddy、Cursor、Claude Desktop、Cline 四种客户端的配置示例
- **文档撰写**: AI 编写了 README、安装脚本、配置说明
- **代码审查**: AI 辅助进行了语法验证和结构优化
