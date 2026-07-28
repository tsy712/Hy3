# Hy3 Research Assistant — Installation Guide

## 1. Main Project Installation (Web Application)

### Quick Install (Recommended)

```bash
# 1. Enter the project directory
cd hy3-research-assistant-package

# 2. pip install (auto-handles all dependencies)
pip install -e .

# 3. Configure API key
# Copy .env.example to .env, then edit and fill in your API Key

# 4. Launch
hy3-research
# Open http://localhost:8000 in your browser
```

### Manual Install

```bash
# 1. Configure API key
copy .env.example .env
# Edit .env and fill in HY3_API_KEY

# 2. Install dependencies
cd backend
pip install -r requirements.txt

# 3. Launch
python main.py
```

### Windows One-Click Launch

Double-click `start.bat` (auto-detects API Key, installs dependencies, starts service).

---

## 2. MCP Server Installation

Integrate Hy3 capabilities into Claude Desktop / Cursor / CodeBuddy.

### Install

```bash
cd hy3-mcp-server
pip install -e .
```

### Windows One-Click Install

Double-click `hy3-mcp-server/setup.bat`

### Configure Claude Desktop

Add to `claude_desktop_config.json`:

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

### MCP Server Tools

| Tool Name | Function |
|-----------|----------|
| hy3_research | Deep research: search + analysis + report |
| hy3_code_review | Code review: bug detection + performance + security |
| hy3_doc_qa | Document Q&A: parsing + precise answers |
| hy3_data_analyze | Data analysis: CSV/JSON + insights |
| hy3_chat | General chat |

---

## Dependency Diagram

```
hy3-research-assistant (Main Project)
├── FastAPI + Uvicorn           ← Web framework
├── OpenAI SDK                  ← Hy3 API calls
├── httpx + BeautifulSoup       ← Web search
├── PyPDF2 + python-docx        ← Document parsing
└── python-multipart + aiofiles ← File upload

hy3-mcp-server (MCP Server)
├── fastmcp                     ← MCP protocol
├── OpenAI SDK                  ← Hy3 API calls
├── httpx                       ← HTTP requests
└── python-dotenv               ← Environment variables
```

Both packages can be installed and used independently.
