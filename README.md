# Hy3 MCP Server

**基于 MCP 协议，封装腾讯混元 Hy3 大模型能力的智能工具集**
可一键安装、即插即用到任何支持 MCP 的 AI 客户端（CodeBuddy、Cursor、Claude Desktop、Cline 等）。

---

## 功能特性

封装 5 大智能工具，全部由 Hy3 大模型驱动：

| 工具 | 功能 | 适用场景 |
|------|------|----------|
| `hy3_research` | 深度研究助手 | 自动搜索 + 分析 + 生成结构化研究报告 |
| `hy3_code_review` | 代码评审 | 多维度代码审查、Bug 发现、安全分析 |
| `hy3_doc_qa` | 文档问答 | 读取本地文档，基于内容精准回答 |
| `hy3_data_analyze` | 数据分析 | CSV/JSON 数据深度分析与洞察输出 |
| `hy3_chat` | 通用对话 | 自由问答、写作、翻译等灵活场景 |

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API Key

方式一：设置环境变量
```bash
# Windows (CMD)
set HY3_API_KEY=你的API密钥

# Windows (PowerShell)
$env:HY3_API_KEY="你的API密钥"

# macOS / Linux
export HY3_API_KEY=你的API密钥
```

方式二：创建 `.env` 文件
```bash
cp .env.example .env
# 编辑 .env 文件，填入 HY3_API_KEY
```

### 3. 启动服务

```bash
cd src
python server.py
```

### 4. 配置 MCP 客户端

将 `configs/` 目录下对应客户端的配置添加到 MCP 设置中。例如 CodeBuddy：

```json
{
  "mcpServers": {
    "hy3-assistant": {
      "type": "stdio",
      "command": "python",
      "args": ["src/server.py"],
      "cwd": "/path/to/hy3-mcp-server",
      "env": {
        "HY3_API_KEY": "你的API密钥",
        "HY3_MODEL": "hunyuan-pro"
      }
    }
  }
}
```

---

## 环境变量

| 变量 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `HY3_API_KEY` | 是 | - | 腾讯混元 API 密钥 |
| `HY3_BASE_URL` | 否 | `https://api.hunyuan.cloud.tencent.com/v1` | API 端点 |
| `HY3_MODEL` | 否 | `hunyuan-pro` | 模型名称 |

---

## 项目结构

```
hy3-mcp-server/
├── src/
│   ├── __init__.py      # 包初始化
│   ├── hy3_client.py    # Hy3 API 客户端（OpenAI 兼容）
│   └── server.py        # MCP Server 主程序（5个工具）
├── configs/             # MCP 客户端配置模板
│   ├── codebuddy-mcp.json
│   ├── cursor-mcp.json
│   ├── claude-mcp.json
│   └── cline-mcp.json
├── tests/
│   └── test_hy3_client.py  # 单元测试
├── requirements.txt
├── .env.example
├── setup.bat            # Windows 一键安装
├── setup.sh             # Linux/macOS 一键安装
└── README.md
```

---

## 运行测试

```bash
python -m pytest tests/ -v
```

---

## 工具详解

### hy3_research — 深度研究
- 自动多关键词 DuckDuckGo 搜索
- Hy3 大模型生成结构化报告（含执行摘要）
- 支持 `brief`（简要）和 `detailed`（详细）两种深度

### hy3_code_review — 代码评审
- 7 维度审查：概览/Bug/性能/安全/质量/建议/评分
- 支持多种编程语言自动识别
- 4 种审查重点：全面/安全/性能/Bug

### hy3_doc_qa — 文档问答
- 支持 30+ 文本格式
- 多编码自动检测（UTF-8/GBK/GB2312）
- 回答附带原文引用证据

### hy3_data_analyze — 数据分析
- CSV/JSON 数据解析与预处理
- 自动统计字段数量、数据规模
- Hy3 深度分析 + 行动建议

### hy3_chat — 通用对话
- 自由对话，支持自定义系统提示词
- 适用于写作、翻译、解释等各种场景

---

## 技术架构

- **协议层**: MCP (Model Context Protocol) stdio 传输
- **框架层**: FastMCP — Python MCP 快速开发框架
- **模型层**: 腾讯混元 Hy3 大模型 (OpenAI 兼容 API)
- **搜索层**: DuckDuckGo（HTML 搜索 + Instant Answer API 两级降级）
- **客户端**: httpx + OpenAI Python SDK

---

## 许可证

MIT License
