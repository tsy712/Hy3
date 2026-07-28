# Hy3 MCP Server

<p align="center">
  <a href="README.md">🇨🇳 中文</a> · <strong>🇺🇸 English</strong>
</p>

A collection of intelligent tools based on the MCP (Model Context Protocol) that wrap the capabilities of Tencent Hunyuan Hy3 large model.

## Features

- **One-click install, plug & play** — automated installation via `setup.bat` / `setup.sh`
- **5 MCP tools** — deep research, code review, document Q&A, data analysis, general chat
- **4 MCP client supports** — CodeBuddy / Cursor / Claude Desktop / Cline
- **Dual configuration** — environment variables + `.env` file, flexible adaptation
- **Auto retry** — exponential backoff to handle network fluctuations
- **Multi-encoding support** — auto-detect UTF-8 / GBK / GB2312
- **Dual-layer search fallback** — DuckDuckGo HTML → Instant Answer API

## Tool Capabilities

| Tool | Function | Input | Typical Scenario |
|------|----------|-------|------------------|
| `hy3_research` | Deep research | Topic + search depth | Industry analysis, technology research |
| `hy3_code_review` | Code review | Code + language + focus | Bug detection, security audit |
| `hy3_doc_qa` | Document Q&A | File path + question | PDF/TXT/MD/code interpretation |
| `hy3_data_analyze` | Data analysis | CSV/JSON + analysis goal | Data insight, trend discovery |
| `hy3_chat` | General chat | Message + system prompt | Writing, translation, explanation |

## One-Click Install

### 1. Clone and Enter Directory

```bash
git clone https://github.com/your-org/hy3-mcp-server.git
cd hy3-mcp-server
```

### 2. Configure API Key (choose one)

**Option 1: Environment Variable**
```bash
# Windows (PowerShell)
$env:HY3_API_KEY="your_api_key"

# macOS/Linux
export HY3_API_KEY="your_api_key"
```

**Option 2: .env File**
```bash
cp .env.example .env
# Edit .env and fill in your API Key
```

### 3. Run Install Script

```bash
# Windows
setup.bat

# macOS / Linux
bash setup.sh
```

## Client Configuration

After installation, choose the corresponding configuration for your MCP client:

### CodeBuddy

Add the following in CodeBuddy's MCP settings:

```json
{
  "mcpServers": {
    "hy3-assistant": {
      "type": "stdio",
      "command": "python",
      "args": ["src/server.py"],
      "cwd": "/your/path/to/hy3-mcp-server",
      "env": {
        "HY3_API_KEY": "your_api_key",
        "HY3_MODEL": "hunyuan-pro"
      }
    }
  }
}
```

### Cursor

Create `.cursor/mcp.json` in the project root:

```json
{
  "mcpServers": {
    "hy3-assistant": {
      "command": "python",
      "args": ["src/server.py"],
      "cwd": "/your/path/to/hy3-mcp-server",
      "env": {
        "HY3_API_KEY": "your_api_key",
        "HY3_MODEL": "hunyuan-pro"
      }
    }
  }
}
```

Detailed configuration can also refer to the JSON templates in the `configs/` directory for each client.

## Project Structure

```
hy3-mcp-server/
├── src/
│   ├── __init__.py          # Package info
│   ├── server.py             # MCP Server main program (5 Tools)
│   └── hy3_client.py         # Hy3 API client wrapper
├── configs/                  # MCP configuration templates for each client
│   ├── codebuddy-mcp.json
│   ├── cursor-mcp.json
│   ├── claude-mcp.json
│   └── cline-mcp.json
├── tests/
│   └── test_hy3_client.py    # Unit tests
├── .env.example              # Environment variable template
├── .gitignore
├── requirements.txt          # Python dependencies
├── setup.bat                 # Windows one-click install
├── setup.sh                  # Linux/macOS one-click install
└── README.md
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `HY3_API_KEY` | ✅ Required | - | Hy3 large model API key |
| `HY3_BASE_URL` | Optional | `https://api.hunyuan.cloud.tencent.com/v1` | API base endpoint |
| `HY3_MODEL` | Optional | `hunyuan-pro` | Model name to use |

> 💡 Configuration supports both environment variables and `.env` files (environment variables take priority).

## Data Sources

| Type | Description |
|------|-------------|
| **Web Search** | DuckDuckGo dual-layer search (HTML parsing → Instant Answer API fallback) |
| **Local Files** | Supports .txt .md .py .js .ts .json .csv .html .css .yaml .yml .toml .ini .cfg .conf .sh .bat .sql .java .go .rs .c .cpp .h and other text formats |
| **Core Inference** | All AI analysis / generation / review capabilities are provided by Tencent Hunyuan Hy3 large model (OpenAI-compatible interface) |

## Technical Details

- **MCP Framework**: FastMCP >= 2.0.0 (stdio transport)
- **AI Inference**: Tencent Hunyuan Hy3 large model (OpenAI-compatible interface: `https://api.hunyuan.cloud.tencent.com/v1`)
- **Search Fallback Strategy**:
  1. DuckDuckGo HTML search (full parsing of title, link, snippet)
  2. DuckDuckGo Instant Answer API (structured data)
- **Retry Mechanism**: Exponential backoff (1s → 2s → 4s), up to 3 retries
- **Configuration**: Supports both environment variables and `.env` files (environment variables take priority)
- **Encoding Compatibility**: Auto-detect UTF-8 → GBK → GB2312 → Latin-1
- **Security**: API Key passed via environment variable or .env file; `.gitignore` excludes `.env`

## Running Tests

```bash
cd tests
python -m pytest test_hy3_client.py -v
```

## License

MIT License
