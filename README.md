# Hy3 MCP Server

基于 MCP（Model Context Protocol）协议，封装腾讯混元 Hy3 大模型能力的智能工具集。

## 特性

- **一键安装，即插即用** — `setup.bat` / `setup.sh` 自动化安装
- **5 个 MCP 工具** — 深度研究、代码审查、文档问答、数据分析、通用对话
- **4 个 MCP 客户端支持** — CodeBuddy / Cursor / Claude Desktop / Cline
- **双配置方式** — 环境变量 + `.env` 文件，灵活适配
- **自动重试** — 指数退避，应对网络波动
- **多编码支持** — 自动检测 UTF-8 / GBK / GB2312
- **双层搜索降级** — DuckDuckGo HTML → Instant Answer API

## 工具能力

| 工具 | 功能 | 输入 | 典型场景 |
|------|------|------|----------|
| `hy3_research` | 深度研究 | 主题 + 搜索深度 | 行业分析、技术调研 |
| `hy3_code_review` | 代码审查 | 代码 + 语言 + 审查重点 | Bug 检测、安全审计 |
| `hy3_doc_qa` | 文档问答 | 文件路径 + 问题 | PDF/TXT/MD/代码解读 |
| `hy3_data_analyze` | 数据分析 | CSV/JSON + 分析目标 | 数据洞察、趋势发现 |
| `hy3_chat` | 通用对话 | 消息 + 系统提示词 | 写作、翻译、解释 |

## 一键安装

### 1. 克隆并进入目录

```bash
git clone https://github.com/your-org/hy3-mcp-server.git
cd hy3-mcp-server
```

### 2. 配置 API Key（二选一）

**方式一：环境变量**
```bash
# Windows (PowerShell)
$env:HY3_API_KEY="你的API密钥"

# macOS/Linux
export HY3_API_KEY="你的API密钥"
```

**方式二：.env 文件**
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 API Key
```

### 3. 运行安装脚本

```bash
# Windows
setup.bat

# macOS / Linux
bash setup.sh
```

## 客户端配置

安装完成后，根据你的 MCP 客户端选择对应配置：

### CodeBuddy

在 CodeBuddy 的 MCP 设置中添加：

```json
{
  "mcpServers": {
    "hy3-assistant": {
      "type": "stdio",
      "command": "python",
      "args": ["src/server.py"],
      "cwd": "/your/path/to/hy3-mcp-server",
      "env": {
        "HY3_API_KEY": "你的API密钥",
        "HY3_MODEL": "hunyuan-pro"
      }
    }
  }
}
```

### Cursor

在项目根目录创建 `.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "hy3-assistant": {
      "command": "python",
      "args": ["src/server.py"],
      "cwd": "/your/path/to/hy3-mcp-server",
      "env": {
        "HY3_API_KEY": "你的API密钥",
        "HY3_MODEL": "hunyuan-pro"
      }
    }
  }
}
```

详细配置也可参考 `configs/` 目录下的各客户端 JSON 模板。

## 项目结构

```
hy3-mcp-server/
├── src/
│   ├── __init__.py          # 包信息
│   ├── server.py             # MCP Server 主程序（5 个 Tool）
│   └── hy3_client.py         # Hy3 API 客户端封装
├── configs/                  # 各客户端 MCP 配置模板
│   ├── codebuddy-mcp.json
│   ├── cursor-mcp.json
│   ├── claude-mcp.json
│   └── cline-mcp.json
├── tests/
│   └── test_hy3_client.py    # 单元测试
├── .env.example              # 环境变量模板
├── .gitignore
├── requirements.txt          # Python 依赖
├── setup.bat                 # Windows 一键安装
├── setup.sh                  # Linux/macOS 一键安装
└── README.md
```

## 环境变量

| 变量 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `HY3_API_KEY` | ✅ 必填 | - | Hy3 大模型 API 密钥 |
| `HY3_BASE_URL` | 可选 | `https://api.hunyuan.cloud.tencent.com/v1` | API 基础端点 |
| `HY3_MODEL` | 可选 | `hunyuan-pro` | 使用的模型名称 |

> 💡 配置方式：支持环境变量和 `.env` 文件两种配置（环境变量优先级更高）

## 数据源

| 类型 | 说明 |
|------|------|
| **网络搜索** | DuckDuckGo 双层搜索（HTML 解析 → Instant Answer API 降级） |
| **本地文件** | 支持 .txt .md .py .js .ts .json .csv .html .css .yaml .yml .toml .ini .cfg .conf .sh .bat .sql .java .go .rs .c .cpp .h 等文本格式 |
| **核心推理** | 所有 AI 分析 / 生成 / 审查能力由腾讯混元 Hy3 大模型（OpenAI 兼容接口）提供 |

## 技术细节

- **MCP 框架**: FastMCP >= 2.0.0（stdio 传输）
- **AI 推理**: 腾讯混元 Hy3 大模型（OpenAI 兼容接口：`https://api.hunyuan.cloud.tencent.com/v1`）
- **搜索降级策略**:
  1. DuckDuckGo HTML 搜索（完整解析标题、链接、摘要）
  2. DuckDuckGo Instant Answer API（结构化数据）
- **重试机制**: 指数退避（1s → 2s → 4s），最多 3 次重试
- **配置方式**: 支持环境变量和 `.env` 文件两种配置（环境变量优先级更高）
- **编码兼容**: 自动检测 UTF-8 → GBK → GB2312 → Latin-1
- **安全**: API Key 通过环境变量或 .env 文件传入，`.gitignore` 已排除 `.env`

## 运行测试

```bash
cd tests
python -m pytest test_hy3_client.py -v
```

## 许可证

MIT License
