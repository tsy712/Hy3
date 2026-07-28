# Hy3 MCP Server — Multi-Client Configuration Guide

<p align="center">
  <a href="mcp-server.md">🇨🇳 中文</a> · <strong>🇺🇸 English</strong> · <a href="../README_EN.md">⬅ Back to README</a>
</p>

---

`hy3-mcp-server` wraps Hy3 large-model capabilities into MCP (Model Context Protocol) tools, allowing AI editors/clients to **automatically invoke** deep research, code analysis, document Q&A, and other features during conversations.

---

## Installation

```bash
cd hy3-mcp-server
pip install -e .
```

---

## Client Configuration

### CodeBuddy / WorkBuddy

CodeBuddy has native MCP Server support, making configuration the easiest.

Add the following in CodeBuddy Settings → MCP:

```json
{
  "mcpServers": {
    "hy3": {
      "command": "hy3-mcp",
      "env": {
        "HY3_API_KEY": "your_api_key"
      }
    }
  }
}
```

> Or directly edit the `mcp.json` file and restart CodeBuddy.

---

### Claude Desktop

Edit the Claude Desktop configuration file:

| OS | Configuration File Path |
|----|-------------------------|
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Linux | `~/.config/Claude/claude_desktop_config.json` |

Add the following configuration:

```json
{
  "mcpServers": {
    "hy3": {
      "command": "hy3-mcp",
      "args": [],
      "env": {
        "HY3_API_KEY": "your_api_key"
      }
    }
  }
}
```

**Steps**:
1. Open Claude Desktop → Settings → Developer → Edit Config
2. Paste the JSON configuration above
3. Restart Claude Desktop
4. A 🔌 icon will appear at the bottom of the chat; click it to see the 5 tools such as `hy3_research`

---

### Cursor

Create `.cursor/mcp.json` in the project root (or directly edit Cursor's MCP configuration):

```json
{
  "mcpServers": {
    "hy3": {
      "command": "hy3-mcp",
      "env": {
        "HY3_API_KEY": "your_api_key"
      }
    }
  }
}
```

**Steps**:
1. Cursor → Settings → Features → MCP
2. Click "Add new MCP Server"
3. Enter name `hy3` and command `hy3-mcp`
4. Add `HY3_API_KEY` in Environment Variables
5. Save and restart Cursor

---

### Cline (VS Code Extension)

Cline is an MCP client implemented as a VS Code extension.

1. Open VS Code → Install the Cline extension
2. Cline settings → MCP Servers
3. Add the following configuration:

```json
{
  "mcpServers": {
    "hy3": {
      "command": "hy3-mcp",
      "env": {
        "HY3_API_KEY": "your_api_key"
      }
    }
  }
}
```

4. Cline will auto-load after saving; you can invoke Hy3 tools in conversations

---

### Any MCP Client

Any standard MCP client can be connected using the same pattern: specify `command` as `hy3-mcp` and pass the `HY3_API_KEY` environment variable.

---

## Connect and Use: Demo

### Example 1: Deep Research — "Research the latest WebAssembly progress"

**User input:**
> Help me research the latest WebAssembly progress in 2024, including new features, ecosystem tools, and browser support.

**AI automatically calls the `hy3_research` tool** → Hy3 then searches, analyzes, and generates a report, finally replying with a structured research report of over a thousand words. The user stays in the current AI client throughout the fully automated process.

```
[AI] Researching WebAssembly 2024 progress for you...

🔬 Calling tool: hy3_research(query="WebAssembly 2024 latest progress new features ecosystem tools browser support")

## WebAssembly 2024 Annual Research Brief

### 1. Key New Features
- Standard finalized: GC proposal (Garbage Collection) officially incorporated...
...
```

---

### Example 2: Code Review — "Review this Python code"

**User input:**
> @main.py Please review this code for performance issues and security risks.

**AI automatically calls the `hy3_code_review` tool** → reads file content → analyzes code structure → returns a graded review report.

```
[AI] Analyzing main.py...

💻 Calling tool: hy3_code_review(files=["main.py"])

## Code Review Report — main.py

**Overall Score**: 7/10

### 🔴 Security Risks
- L42: User input not XSS-filtered
- L78: API Key hardcoded

### 🟡 Performance Issues
- L115: HTTP client recreated inside loop, recommend reuse
- L203: Large file read without upper limit
...
```

---

### Example 3: Document Q&A — "What risks should I pay attention to in this contract?"

**User input:**
> @contract.pdf What are the legal risks in this contract? Please list the clauses I should pay attention to.

**AI automatically calls the `hy3_doc_qa` tool** → parses PDF → understands contract content → analyzes risks clause by clause with source citations.

```
[AI] Analyzing contract.pdf...

📚 Calling tool: hy3_doc_qa(files=["contract.pdf"], query="legal risks and precautions")

## Contract Risk Analysis

### ⚠️ Clauses to Watch (4 in total)

1. **Confidentiality Clause (Section 5.2)**
   > [Citation] "Party B shall not... within 5 years after the partnership period"
   Note: The confidentiality period is long; confirm whether it is industry standard
...
```

---

## Available Tools

| Tool Name | Function | Use Case |
|-----------|----------|----------|
| `hy3_research` | Deep research: search + analysis + report generation | Industry research, competitive analysis, academic review |
| `hy3_code_review` | Code review: bug detection + performance analysis + security audit | PR review, code quality control |
| `hy3_doc_qa` | Document Q&A: file parsing + precise answers | Contract review, paper comprehension, document lookup |
| `hy3_data_analyze` | Data analysis: CSV/JSON + insight output | Data report interpretation, trend judgment |
| `hy3_chat` | General chat: free Q&A | Programming consultation, technical Q&A, creative generation |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Tool list does not appear | Restart the AI client and confirm `hy3-mcp` command is executable |
| Tool call error | Check whether `HY3_API_KEY` is correct and set as an environment variable in the client configuration |
| Response timeout | Deep research tasks take about 30–90 seconds; if timed out, check network and API connectivity |
