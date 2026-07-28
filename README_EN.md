# Hy3 Research Assistant

An intelligent research assistant powered by Tencent Hunyuan Hy3 model, offering **Deep Research**, **Code Analysis**, and **Document Q&A**.

## Overview

This project is the complete implementation of Tencent Rhino-Bird Open Source Program [Issue #4](https://github.com/Tencent-Hunyuan/Hy3/issues/4). All intelligent tasks (research planning, report generation, code analysis, document Q&A) are performed via the **Hy3 API** (OpenAI-compatible interface), without model training, fine-tuning, or local inference.

### Hy3's Role in the Project

| Feature | Hy3's Role |
|---------|------------|
| Deep Research | Research plan formulation → Search keyword generation → Long-form report writing → Executive summary extraction |
| Code Analysis | Code comprehension, Bug detection, Performance optimization suggestions, Security audit, Quality scoring |
| Document Q&A | Multi-document reading comprehension, Evidence-driven precise Q&A |

## Project Structure

```
hy3-research-assistant-package/
├── backend/
│   ├── main.py            # FastAPI server (6 API endpoints, all SSE streaming)
│   ├── hy3_client.py      # Hy3 API client wrapper (OpenAI-compatible)
│   ├── tools.py            # Utility functions (web search, PDF/DOCX/code parsing)
│   ├── cli.py              # CLI entry point (hy3-research command after pip install)
│   └── requirements.txt   # Python dependencies
├── hy3-mcp-server/         # MCP Server sub-project (installable independently)
│   ├── src/                # Source code
│   │   ├── server.py       # FastMCP server (5 Tools)
│   │   └── hy3_client.py  # Hy3 API client
│   ├── pyproject.toml      # pip install configuration
│   └── requirements.txt   # Python dependencies
├── frontend/
│   └── index.html          # Modern web frontend (dark theme, streaming, Markdown rendering)
├── pyproject.toml          # Main project pip install configuration
├── .env.example            # Environment variable template
├── start.bat               # Windows one-click launch script
├── 安装说明.md              # Detailed installation guide
└── README.md
```

## Quick Start

### Requirements

- Python 3.9+
- A valid Hy3 API Key

### Option 1: pip Install (Recommended)

```bash
cd hy3-research-assistant-package

# pip install (auto-handles dependencies)
pip install -e .

# Configure API key
# Windows:  set HY3_API_KEY=your-api-key
# macOS/Linux: export HY3_API_KEY=your-api-key
# Or copy .env.example to .env and fill in your key

# One-click launch
hy3-research
# Service runs at http://localhost:8000
```

### Option 2: Manual Install

```bash
cd backend
pip install -r requirements.txt
cd ..
python backend/main.py
```

### Option 3: Windows One-Click Launch

Double-click `start.bat` (auto-detects API Key, installs dependencies, starts service)

### Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HY3_API_KEY` | Hy3 API key (required) | - |
| `HY3_BASE_URL` | API endpoint URL | `https://api.hunyuan.cloud.tencent.com/v1` |
| `HY3_MODEL` | Model name | `hunyuan-pro` |
| `PORT` | Service port | `8000` |

## Three Core Features

### Deep Research

Enter a research topic, and Hy3 will automatically:

1. **Research Planning** — Break down the topic into sub-questions, generate search keywords
2. **Literature Search** — Automatically search relevant web sources
3. **Report Writing** — Generate a 1500-3000 word professional research report based on search results
4. **Executive Summary** — Extract a concise summary of key findings

### Code Analysis

Paste code or upload a code file, and Hy3 will provide:

- Code overview and core functionality explanation
- Execution logic and key flow analysis
- Potential bugs, performance issues, and security vulnerability diagnosis
- Specific optimization suggestions and best practices
- Code quality score (1-10)

### Document Q&A

Upload multiple documents (PDF, DOCX, TXT, code files, etc.) and ask Hy3 questions:

- Precise answers based on document content
- Quote original passages as evidence
- Clearly indicate when information is missing

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Frontend page |
| `/health` | GET | Health check |
| `/api/research` | POST | Deep research (streaming) |
| `/api/analyze-code` | POST | Paste code analysis (streaming) |
| `/api/analyze-code-file` | POST | Upload code file analysis (streaming) |
| `/api/qa-documents` | POST | Multi-document Q&A (streaming) |

All intelligent endpoints use Server-Sent Events (SSE) for streaming output, supporting real-time frontend rendering.

## Tech Stack

- **Backend**: FastAPI + OpenAI SDK + Uvicorn
- **Frontend**: Native HTML/CSS/JS + marked.js (Markdown rendering)
- **Model**: Tencent Hunyuan Hy3 (via OpenAI-compatible interface)
- **Tools**: DuckDuckGo web search, PyPDF2, python-docx

## Hy3 MCP Server

`hy3-mcp-server` is a standalone sub-project that wraps Hy3 capabilities as MCP protocol tools.

### Quick Install

```bash
cd hy3-mcp-server
pip install -e .
# Or double-click setup.bat (Windows)
```

### Configure Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "hy3": {
      "command": "hy3-mcp",
      "env": { "HY3_API_KEY": "your-api-key" }
    }
  }
}
```

### MCP Tool List

| Tool Name | Function |
|-----------|----------|
| `hy3_research` | Deep research: search + analysis + report |
| `hy3_code_review` | Code review: bug detection + performance + security |
| `hy3_doc_qa` | Document Q&A: parsing + precise answers |
| `hy3_data_analyze` | Data analysis: CSV/JSON + insights |
| `hy3_chat` | General chat |

---

## CodeBuddy Collaboration Notes

This project was built with the assistance of CodeBuddy AI programming assistant:

- **Collaborative Design**: AI participated in overall architecture planning, feature module decomposition, and front-end/back-end interaction design
- **Code Generation**: AI wrote the backend server, API client, utility functions, and frontend interface
- **Documentation**: AI generated the README, configuration templates, startup scripts, and installation guides
- **Package Creation**: AI created pyproject.toml, enabling `pip install -e .` installation
