# Hy3 Research Assistant

An intelligent research assistant powered by Tencent Hunyuan Hy3 large language model, offering three core capabilities: **Deep Research**, **Code Analysis**, and **Document Q&A**.

## Project Overview

This project is a complete implementation of the Tencent RhinoBird Open Source Practical Program [Issue #4](https://github.com/Tencent-Hunyuan/Hy3/issues/4). All intelligent tasks (research planning, report generation, code analysis, document Q&A) are accomplished by calling the **Hy3 API** (OpenAI-compatible interface), with no model training, fine-tuning, or local inference involved.

### Hy3's Role in the Project

| Feature Module | Hy3's Role |
|----------------|------------|
| Deep Research | Research plan formulation → Search keyword generation → Long-form report writing → Executive summary extraction |
| Code Analysis | Code understanding, bug detection, performance optimization suggestions, security audits, quality scoring |
| Document Q&A | Multi-document reading comprehension, evidence-driven precise answering |

## Project Structure

```
hy3-research-assistant/
├── backend/
│   ├── main.py            # FastAPI server (6 API endpoints, all supporting SSE streaming)
│   ├── hy3_client.py      # Hy3 API client wrapper (OpenAI-compatible interface)
│   ├── tools.py            # Utility functions (web search, PDF/DOCX/code file parsing)
│   └── requirements.txt   # Python dependencies
├── frontend/
│   └── index.html          # Modern web frontend (dark theme, streaming rendering, Markdown display)
├── .env.example            # Environment variable configuration template
├── .gitignore
├── start.bat               # Windows one-click startup script
└── README.md
```

## Quick Start

### Environment Requirements

- Python 3.9+
- Valid Hy3 API Key

### Install and Start

```bash
# 1. Clone the project
cd hy3-research-assistant

# 2. Configure API key
# Windows
set HY3_API_KEY=your_api_key
# Or copy .env.example to .env and fill in your key

# 3. Install dependencies
cd backend
pip install -r requirements.txt

# 4. Start the service
python main.py
# Service runs at http://localhost:8000
```

Open your browser and visit `http://localhost:8000`.

### Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HY3_API_KEY` | Hy3 API key (**required**) | - |
| `HY3_BASE_URL` | API endpoint URL | `https://api.hunyuan.cloud.tencent.com/v1` |
| `HY3_MODEL` | Model name | `hunyuan-pro` |
| `PORT` | Service port | `8000` |

## Three Core Features

### 🔬 Deep Research

Enter a research topic and Hy3 will automatically:

1. **Research Planning** — Decompose the topic into sub-questions and generate search keywords
2. **Information Search** — Automatically search for relevant web content
3. **Report Writing** — Generate a 1500–3000 word professional research report based on search results
4. **Executive Summary** — Extract a concise summary of core findings

### 💻 Code Analysis

Paste code or upload code files and Hy3 will provide:

- Code overview and core functionality interpretation
- Execution logic and key flow analysis
- Potential bugs, performance issues, and security vulnerability diagnosis
- Specific optimization suggestions and best practices
- 1–10 code quality score

### 📚 Document Q&A

Upload multiple documents (PDF, DOCX, TXT, code files, etc.) and ask Hy3 questions:

- Precise answers based on document content
- Citations of original passages as evidence
- Clear indication when information is missing

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Frontend page |
| `/health` | GET | Service health check |
| `/api/research` | POST | Deep research (streaming) |
| `/api/analyze-code` | POST | Paste code analysis (streaming) |
| `/api/analyze-code-file` | POST | Upload code file analysis (streaming) |
| `/api/qa-documents` | POST | Multi-document Q&A (streaming) |

All intelligent endpoints use Server-Sent Events (SSE) for streaming output, supporting real-time rendering on the frontend.

## Tech Stack

- **Backend**: FastAPI + OpenAI SDK + Uvicorn
- **Frontend**: Vanilla HTML/CSS/JS + marked.js (Markdown rendering)
- **Model**: Tencent Hunyuan Hy3 (via OpenAI-compatible interface)
- **Tools**: DuckDuckGo web search, PyPDF2, python-docx

## CodeBuddy Collaboration Notes

This project was completed with the assistance of CodeBuddy AI programming assistant:

- **Co-design**: AI participated in overall architecture planning, feature module decomposition, and frontend-backend interaction design
- **Code generation**: AI wrote `backend/main.py` (server and all prompt engineering), `backend/hy3_client.py` (API client wrapper), `backend/tools.py` (search and file parsing), `frontend/index.html` (complete frontend interface)
- **Documentation**: AI generated the README, configuration templates, and startup scripts
- **Code review & polish**: AI assisted with syntax checking, Chinese-English translation, and structural optimization
