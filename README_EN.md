# Hy3 Research Assistant

An intelligent research assistant powered by Tencent Hunyuan Hy3 model, offering **Deep Research**, **Code Analysis**, and **Document Q&A**.

## Overview

This project is the complete implementation of Tencent Rhino-Bird Open Source Program [Issue #4](https://github.com/Tencent-Hunyuan/Hy3/issues/4). All intelligent tasks (research planning, report generation, code analysis, document Q&A) are performed via the **Hy3 API** (OpenAI-compatible interface), without model training, fine-tuning, or local inference.

### Hy3's Role in the Project

| Feature | Hy3's Role |
|---------|-----------|
| Deep Research | Research plan formulation → Search keyword generation → Long-form report writing → Executive summary extraction |
| Code Analysis | Code comprehension, Bug detection, Performance optimization suggestions, Security audit, Quality scoring |
| Document Q&A | Multi-document reading comprehension, Evidence-driven precise Q&A |

## Project Structure

```
hy3-research-assistant/
├── backend/
│   ├── main.py            # FastAPI server (6 API endpoints, all SSE streaming)
│   ├── hy3_client.py      # Hy3 API client wrapper (OpenAI-compatible)
│   ├── tools.py            # Utility functions (web search, PDF/DOCX/code file parsing)
│   └── requirements.txt   # Python dependencies
├── frontend/
│   └── index.html          # Modern web frontend (dark theme, streaming, Markdown rendering)
├── .env.example            # Environment variable template
├── .gitignore
├── start.bat               # Windows one-click launch script
└── README.md
```

## Quick Start

### Requirements

- Python 3.9+
- A valid Hy3 API Key

### Install & Launch

```bash
# 1. Clone the project
cd hy3-research-assistant

# 2. Configure API key
# Windows
set HY3_API_KEY=your-api-key
# Or copy .env.example to .env and fill in your key

# 3. Install dependencies
cd backend
pip install -r requirements.txt

# 4. Start the server
python main.py
# Service runs at http://localhost:8000
```

Open your browser and visit `http://localhost:8000`.

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

## CodeBuddy Collaboration Notes

This project was built with the assistance of CodeBuddy AI programming assistant:

- **Collaborative Design**: AI participated in overall architecture planning, feature module decomposition, and front-end/back-end interaction design
- **Code Generation**: AI wrote `backend/main.py` (server and all prompt engineering), `backend/hy3_client.py` (API client wrapper), `backend/tools.py` (search and file parsing), `frontend/index.html` (complete frontend interface)
- **Documentation**: AI generated the README, configuration templates, and startup scripts
- **Code Review & Polish**: AI assisted with syntax checking, Chinese-English translation, and structural optimization
