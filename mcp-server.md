# Hy3 MCP Server — Multi-Client Configuration Guide / 多客户端配置指南

> 📖 [Back to README / 返回 README](../README.md)

---

`hy3-mcp-server` wraps Hy3 capabilities as MCP (Model Context Protocol) tools, enabling AI editors/clients to **automatically invoke** Deep Research, Code Analysis, Document Q&A, and more during conversations.  
`hy3-mcp-server` 将 Hy3 大模型能力封装为 MCP (Model Context Protocol) 工具，让 AI 编辑器/客户端在对话中**自动调用**深度研究、代码分析、文档问答等功能。

---

## Installation / 安装

```bash
cd hy3-mcp-server
pip install -e .
```

---

## Client Configuration / 客户端配置

### CodeBuddy / WorkBuddy

CodeBuddy natively supports MCP Server — the simplest setup. / CodeBuddy 原生支持 MCP Server，配置最简单。

In CodeBuddy Settings → MCP, add: / 在 CodeBuddy 设置 → MCP 中添加：

```json
{
  "mcpServers": {
    "hy3": {
      "command": "hy3-mcp",
      "env": {
        "HY3_API_KEY": "your-api-key"
      }
    }
  }
}
```

> Or directly edit the `mcp.json` file and restart CodeBuddy. / 或直接编辑 `mcp.json` 文件，重启 CodeBuddy 后即可使用。

---

### Claude Desktop

Edit Claude Desktop's config file: / 编辑 Claude Desktop 的配置文件：

| OS / 系统 | Config File Path / 配置文件路径 |
|------|-------------|
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Linux | `~/.config/Claude/claude_desktop_config.json` |

Add the following: / 添加以下配置：

```json
{
  "mcpServers": {
    "hy3": {
      "command": "hy3-mcp",
      "args": [],
      "env": {
        "HY3_API_KEY": "your-api-key"
      }
    }
  }
}
```

**Steps / 步骤**：
1. Open Claude Desktop → Settings → Developer → Edit Config / 打开 Claude Desktop → Settings → Developer → Edit Config
2. Paste the JSON config above / 粘贴上述 JSON 配置
3. Restart Claude Desktop / 重启 Claude Desktop
4. A 🔌 icon appears at the bottom of the chat. Click to see 5 tools including `hy3_research` / 对话框底部会出现 🔌 图标，点击可看到 `hy3_research` 等 5 个工具

---

### Cursor

Create `.cursor/mcp.json` in the project root (or edit Cursor's MCP config directly): / 在项目根目录创建 `.cursor/mcp.json`（或直接编辑 Cursor 的 MCP 配置）：

```json
{
  "mcpServers": {
    "hy3": {
      "command": "hy3-mcp",
      "env": {
        "HY3_API_KEY": "your-api-key"
      }
    }
  }
}
```

**Steps / 步骤**：
1. Cursor → Settings → Features → MCP
2. Click "Add new MCP Server"
3. Enter name `hy3` and command `hy3-mcp`
4. Add `HY3_API_KEY` under Environment Variables
5. Save and restart Cursor / 保存后重启 Cursor

---

### Cline (VS Code Plugin / 插件)

Cline is an MCP client implemented as a VS Code plugin. / Cline 是通过 VS Code 插件实现的 MCP 客户端。

1. Open VS Code → Install the Cline plugin / 打开 VS Code → 安装 Cline 插件
2. Cline Settings → MCP Servers
3. Add: / 添加以下配置：

```json
{
  "mcpServers": {
    "hy3": {
      "command": "hy3-mcp",
      "env": {
        "HY3_API_KEY": "your-api-key"
      }
    }
  }
}
```

4. Cline will auto-load after saving. Hy3 tools are now callable in conversations. / 保存后 Cline 会自动加载，在对话中即可调用 Hy3 工具

---

### Any MCP Client / 任意 MCP 客户端

Any standard MCP-protocol-compatible client can connect. The pattern is the same: set `command` to `hy3-mcp` and pass `HY3_API_KEY` as an environment variable.  
只要支持 MCP 协议的标准客户端都可以接入，配置模式相同：指定 `command` 为 `hy3-mcp`，并传入 `HY3_API_KEY` 环境变量。

---

## Instant Effect After Connection: Demo / 连接即生效：效果演示

### Example 1: Deep Research / 深度研究 — "Research the latest WebAssembly developments"

**User input / 用户输入：**
> Research the latest developments in WebAssembly in 2024, including new features, ecosystem tools, and browser support. / 帮我调研一下 WebAssembly 在 2024 年的最新进展，包括新特性、生态工具和浏览器支持情况。

**AI auto-invokes the `hy3_research` tool** → Hy3 immediately starts searching, analyzing, and generating a report. The AI directly replies with a 1000+ word structured research report. The user never leaves their AI client — the entire process is automated.  
**AI 自动调用 `hy3_research` 工具** → Hy3 随即开始搜索、分析、生成报告，最终直接回复一份千字以上的结构化研究报告。用户无需离开当前 AI 客户端，全程自动化。

```
[AI] Researching WebAssembly 2024 progress... / 正在为您调研 WebAssembly 2024 进展...

🔬 Invoking tool / 调用工具: hy3_research(query="WebAssembly 2024 latest developments new features ecosystem tools browser support")

## WebAssembly 2024 Annual Research Briefing

### 1. Key New Features
- Standardization milestone: GC proposal (Garbage Collection) officially adopted...
...
```

---

### Example 2: Code Review / 代码评审 — "Review this Python code"

**User input / 用户输入：**
> @main.py Review this code for performance issues and security vulnerabilities. / @main.py 帮我审查这份代码，看看有没有性能问题和安全隐患。

**AI auto-invokes the `hy3_code_review` tool** → reads file content → analyzes code structure → returns a graded review report.  
**AI 自动调用 `hy3_code_review` 工具** → 读取文件内容 → 分析代码结构 → 返回分级评审报告。

```
[AI] Analyzing main.py... / 正在分析 main.py...

💻 Invoking tool / 调用工具: hy3_code_review(files=["main.py"])

## Code Review Report — main.py / 代码评审报告 — main.py

**Overall Score / 总体评分**: 7/10

### 🔴 Security Issues / 安全隐患
- L42: User input not sanitized for XSS
- L78: Hardcoded API key risk

### 🟡 Performance Issues / 性能问题
- L115: Repeated HTTP client creation in loop; recommend reuse
- L203: Large file reads without size limits
...
```

---

### Example 3: Document Q&A / 文档问答 — "What risk clauses should I watch for in this contract?"

**User input / 用户输入：**
> @contract.pdf What legal risks are in this contract? List the clauses I should pay attention to. / @contract.pdf 这份合同有什么法律风险？帮我列出需要注意的条款。

**AI auto-invokes the `hy3_doc_qa` tool** → parses the PDF → understands contract content → analyzes clause-by-clause with original citations.  
**AI 自动调用 `hy3_doc_qa` 工具** → 解析 PDF → 理解合同内容 → 逐条分析风险并引用原文。

```
[AI] Analyzing contract.pdf... / 正在分析 contract.pdf...

📚 Invoking tool / 调用工具: hy3_doc_qa(files=["contract.pdf"], query="legal risks and attention points")

## Contract Risk Analysis / 合同风险分析

### ⚠️ Clauses to Watch (4 total)

1. **Confidentiality Clause (Section 5.2)**
   > [Citation] "Party B shall not... for 5 years after partnership"
   Note: The confidentiality period is relatively long; consider confirming industry norms.
...
```

---

## Available Tools / 提供的工具

| Tool / 工具名 | Function / 功能 | Use Case / 适用场景 |
|--------|------|---------|
| `hy3_research` | Deep Research: search + analysis + report / 深度研究：搜索 + 分析 + 生成报告 | Industry research, competitive analysis, academic surveys / 行业调研、竞品分析、学术综述 |
| `hy3_code_review` | Code Review: bug detection + performance + security audit / 代码评审：Bug 检测 + 性能分析 + 安全审计 | PR Review, code quality control / PR Review、代码质量把控 |
| `hy3_doc_qa` | Document Q&A: file parsing + precise answers / 文档问答：文件解析 + 精准回答 | Contract review, paper comprehension, document lookup / 合同审查、论文理解、文档查阅 |
| `hy3_data_analyze` | Data Analysis: CSV/JSON + insights / 数据分析：CSV/JSON + 洞察输出 | Report interpretation, trend analysis / 数据报表解读、趋势判断 |
| `hy3_chat` | General Chat: free-form Q&A / 通用对话：自由问答 | Programming consultations, tech Q&A, creative generation / 编程咨询、技术答疑、创意生成 |

---

## Troubleshooting / 故障排查

| Problem / 问题 | Solution / 解决方案 |
|------|---------|
| Tools don't appear / 工具列表未出现 | Restart the AI client, verify the `hy3-mcp` command is executable / 重启 AI 客户端，确认 `hy3-mcp` 命令可执行 |
| Tool invocation errors / 调用工具报错 | Check if `HY3_API_KEY` is correct and set in the client's environment variables / 检查 `HY3_API_KEY` 是否正确，是否在客户端配置中设置了环境变量 |
| Timeout / 返回超时 | Deep Research tasks take ~30-90 seconds. If timeout occurs, check network and API connectivity / 深度研究任务耗时约 30-90 秒，如超时请检查网络和 API 连通性 |
