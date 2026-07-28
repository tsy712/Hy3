# Environment Requirements & Project Structure

<p align="center">
  <a href="environment.md">🇨🇳 中文</a> · <strong>🇺🇸 English</strong> · <a href="../README_EN.md">⬅ Back to README</a>
</p>

---

## Hardware Requirements

| Item | Minimum | Recommended |
|------|---------|-------------|
| CPU | Any dual-core | Quad-core or better |
| RAM | 512 MB | 1 GB+ |
| Disk | 200 MB | 500 MB+ |
| GPU | **Not required** | **Not required** |
| Network | Broadband | Stable broadband |

> **Important: This project does not require a GPU or CUDA.**
> All AI inference tasks are completed via HTTP calls to Tencent Hunyuan Hy3 cloud API, with no local model loading, inference, or training.
> If your goal is to **run/fine-tune the Hy3 model locally**, please refer to the [Running Hy3 Locally Guide](local-hy3-model_EN.md).

## Software Requirements

| Dependency | Version | Notes |
|------------|---------|-------|
| Python | **3.9+** (main project) / **3.10+** (MCP Server) | 3.11 recommended |
| pip | 23.0+ | Installed with Python |
| OS | Windows 10+ / macOS 12+ / Linux (any distro) | All supported |

## Dependency Overview

This project **does not depend** on PyTorch, Transformers, CUDA, or other deep-learning frameworks. All dependencies are just 11 lightweight packages:

```
fastapi>=0.115.0        # Web framework
uvicorn>=0.34.0         # ASGI server
openai>=1.50.0          # Hy3 API calls (OpenAI-compatible interface)
python-multipart        # File upload support
aiofiles                # Async file read/write
PyPDF2>=3.0.0           # PDF parsing
python-docx>=1.1.0      # Word document parsing
httpx>=0.28.0           # HTTP client (web search)
beautifulsoup4>=4.12.0  # HTML parsing
lxml>=5.3.0             # High-performance XML/HTML parser
```

> Total install size is about **80 MB**, no need to download multi-GB model weights.

## Pre-configured Files

| File | Description | What You Need to Do |
|------|-------------|---------------------|
| `.env.example` | Environment variable template | Copy to `.env` and fill in `HY3_API_KEY` |
| `backend/requirements.txt` | 11 lightweight dependencies | No changes needed; pip installs automatically |
| `docker-compose.yml` | Docker orchestration file | No changes needed; works out of the box |
| `Dockerfile` | Container image build file | No changes needed |
| `start.bat` | Windows double-click startup script | No changes needed |

## Project Structure

```
hy3-research-assistant/
├── Dockerfile              # Container image build file
├── docker-compose.yml      # Docker one-click orchestration file
├── backend/
│   ├── main.py            # FastAPI server (6 API endpoints, all SSE streaming)
│   ├── hy3_client.py      # Hy3 API client wrapper (OpenAI-compatible interface)
│   ├── tools.py            # Utility functions (web search, PDF/DOCX/code file parsing)
│   ├── cli.py              # CLI startup entry (hy3-research command after pip install)
│   └── requirements.txt   # Python dependencies
├── hy3-mcp-server/         # MCP Server subproject (can be installed independently)
│   ├── src/                # Source code
│   │   ├── server.py       # FastMCP server (5 Tools)
│   │   └── hy3_client.py  # Hy3 API client
│   ├── pyproject.toml      # pip install config
│   └── requirements.txt   # Python dependencies
├── frontend/
│   └── index.html          # Modern web frontend (dark theme, streaming rendering, Markdown display)
├── pyproject.toml          # Main project pip install config
├── .env.example            # Environment variable template
├── .gitignore
├── start.bat               # Windows one-click startup script
└── README.md
```
