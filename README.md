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
│   ├── cli.py              # CLI entry point (use hy3-research command after pip install)
│   └── requirements.txt   # Python dependencies
├── hy3-mcp-server/         # MCP Server sub-project (installable independently)
│   ├── src/                # Source code
│   │   ├── server.py       # FastMCP server (5 Tools)
│   │   └── hy3_client.py  # Hy3 API client
│   ├── pyproject.toml      # pip install configuration
│   └── requirements.txt   # Python dependencies
├── frontend/
│   └── index.html          # Modern web frontend (dark theme, streaming rendering, Markdown display)
├── pyproject.toml          # Main project pip install configuration
├── .env.example            # Environment variable configuration template
├── .gitignore
├── start.bat               # Windows one-click startup script
└── README.md
```

---

> **【Newcomers Must Read】Environment Setup Pitfall Guide**
> 
> Since the official Hy3 repository depends on `deepspeed` + `flash-attn` with strict CUDA version requirements, **please first determine which scenario applies to you**:
> 
> **Option A (Recommended)**: If you're using a school server or personal laptop **without an NVIDIA GPU (≥24GB)** → skip the model fine-tuning module and just run `python server.py` to experience basic functionality. This project calls cloud APIs via HTTP and does not require a GPU / CUDA / local model.
> 
> **Option B (Hardcore)**: If you have an NVIDIA GPU and want to run the Hy3 model locally → ensure **PyTorch version matches your CUDA driver**. Docker deployment is strongly recommended (version compatibility table and Docker guide below).
> 
> See the detailed risk explanation in the ⚠️ section below →

---

## Environment Requirements

### Hardware Requirements

| Item | Minimum | Recommended |
|------|---------|-------------|
| CPU | Any dual-core processor | Quad-core or higher |
| Memory | 512 MB | 1 GB+ |
| Disk | 200 MB | 500 MB+ |
| GPU | **Not required** | **Not required** |
| Network | Broadband | Stable broadband |

> **Important: This project does NOT require a GPU or CUDA.**  
> All AI inference tasks are completed via HTTP calls to the Tencent Hunyuan Hy3 cloud API, with no local model loading, inference, or training involved.  
> If your goal is to **run/fine-tune the Hy3 model itself locally**, please refer to the [official Hy3 repository](https://github.com/Tencent-Hunyuan/Hy3) for hardware requirements (NVIDIA GPU + CUDA 11.8+ required).

### Software Requirements

| Dependency | Version Requirement | Notes |
|------------|---------------------|-------|
| Python | **3.9+** (main project) / **3.10+** (MCP Server) | 3.11 recommended |
| pip | 23.0+ | Installed with Python |
| OS | Windows 10+ / macOS 12+ / Linux (any distribution) | All supported |

### Dependency Overview

This project does **NOT** depend on PyTorch, Transformers, CUDA, or other deep learning frameworks. Only 11 lightweight packages are required:

```
fastapi>=0.115.0        # Web framework
uvicorn>=0.34.0         # ASGI server
openai>=1.50.0          # Hy3 API calls (OpenAI-compatible interface)
python-multipart        # File upload support
aiofiles                # Async file I/O
PyPDF2>=3.0.0           # PDF parsing
python-docx>=1.1.0      # Word document parsing
httpx>=0.28.0           # HTTP client (web search)
beautifulsoup4>=4.12.0  # HTML parsing
lxml>=5.3.0             # High-performance XML/HTML parser
```

> Total installation size is approximately **80 MB** — no multi-GB model weight files to download.

---

## ⚠️ Risk Warning: The Huge Difference Between Two Operating Modes

Many developers encountering Hy3 for the first time confuse the following two scenarios. **Please confirm which one applies to you:**

| Dimension | 🟢 Mode A: This Application (Recommended) | 🔴 Mode B: Running Hy3 Model Locally |
|-----------|------------------------------------------|--------------------------------------|
| What it does | Calls Tencent cloud API via HTTP | Loads and runs inference on model locally on GPU |
| GPU needed? | **No** | **Required** (NVIDIA GPU) |
| CUDA needed? | **No** | **Required** (CUDA 11.8 or 12.1) |
| Install size | ~80 MB | ~20 GB+ (including model weights) |
| Install time | < 2 minutes | 30 minutes ~ 2 hours |
| Works on first try? | ✅ Almost never fails | ❌ High chance of issues |

> **If you just want to use Hy3's intelligence for research, coding, and Q&A → Mode A, this document covers everything.**  
> **If you want to deploy the Hy3 model itself on your own GPU server → Mode B, please continue reading the risk details below.**

### 🔴 Mode B: Known Pitfalls of Running Hy3 Locally

The official Hy3 model repository depends on `deepspeed` + `flash-attn`, two notoriously difficult-to-install deep learning components. **Incorrect version combinations can lead to compilation failures or runtime crashes.**

#### 1. DeepSpeed + Flash-Attention Version Compatibility Table

| Torch Version | CUDA Version | DeepSpeed | Flash-Attn | Notes |
|---------------|-------------|-----------|------------|-------|
| 2.1.x | 11.8 | 0.12.x | 2.5.x | Stable combination, try this first |
| 2.2.x | 12.1 | 0.13.x | 2.5.x | Newer combination |
| 2.3.x | 12.1 | 0.14.x | 2.6.x | Latest, may have compatibility issues |
| 2.4.x+ | 12.4+ | 0.15.x+ | 2.7.x+ | Bleeding edge, stability not fully verified |

> **Key lesson**: Don't run `pip install deepspeed` directly. First verify your `torch.__version__` and `nvcc --version`, then select versions according to the table above.
> ```bash
> # Check versions first
> python -c "import torch; print(torch.__version__)"
> nvcc --version  # or nvidia-smi to check CUDA Driver version
> 
> # Then install precisely (example: CUDA 11.8 + Torch 2.1.x)
> pip install torch==2.1.2 torchvision==0.16.2 --index-url https://download.pytorch.org/whl/cu118
> pip install deepspeed==0.12.6
> pip install flash-attn==2.5.8 --no-build-isolation
> ```

#### 2. Common Causes of flash-attn Compilation Failures

- **Ninja not installed**: `pip install ninja`
- **GCC/G++ version too low**: Requires GCC 9+ (Linux) or Visual Studio Build Tools 2022+ (Windows)
- **CUDA Toolkit not installed or wrong path**: Ensure `nvcc` is executable and in PATH
- **Insufficient RAM**: `flash-attn` compilation peak memory can reach **32 GB+**; insufficient memory causes termination by OOM Killer
- **Windows compatibility**: `flash-attn` has limited Windows support; strongly recommended to compile under WSL2 or native Linux

#### 3. Minimum GPU Memory Requirements

| Model Size | FP16 | FP32 | INT8 Quantized |
|------------|------|------|----------------|
| 7B | ~14 GB | ~28 GB | ~8 GB |
| 13B | ~26 GB | ~52 GB | ~14 GB |
| 34B | ~68 GB | ~136 GB | ~35 GB |

> **⚠️ If you're reviewing this repository on a MacBook / thin-and-light laptop / desktop with integrated graphics**: Mode B is impossible to run.  
> **⚠️ If you only have a single 8GB/12GB consumer GPU (e.g., RTX 3060/4060)**: You can only run the 7B quantized version and will need CPU offload.  
> **Recommended hardware for review**: NVIDIA GPU ≥ 24 GB VRAM (e.g., RTX 3090/4090, A5000, A100).

#### 4. Recommended: One-Click Docker Deployment (Skip Compilation Hell)

If you must run the Hy3 model locally, **we strongly recommend using the official Docker image** to avoid manually compiling `deepspeed` + `flash-attn`:

```bash
# Pull the official Hy3 image (if available)
docker pull tencent-hunyuan/hy3:latest

# Launch (mount model directory)
docker run --gpus all \
  -v /path/to/models:/models \
  -p 7860:7860 \
  tencent-hunyuan/hy3:latest
```

> If an official Docker image has not been released yet, you can submit an Issue request in the official Hy3 repository, or build your own using the `Dockerfile` template.

---

## Quick Start

### 0. Get Hy3 API Key

A valid Hy3 API key is required. Refer to the [official Hy3 documentation](https://github.com/Tencent-Hunyuan/Hy3) for how to obtain one.

### 1. Clone the Project

```bash
git clone https://github.com/Tencent-Hunyuan/Hy3.git
cd hy3-research-assistant
```

### 2. Configure API Key

**Method A: Environment Variable (Recommended)**

| OS | Command |
|----|---------|
| Windows (CMD) | `set HY3_API_KEY=your_api_key` |
| Windows (PowerShell) | `$env:HY3_API_KEY="your_api_key"` |
| macOS / Linux | `export HY3_API_KEY=your_api_key` |

**Method B: .env File (Persistent)**

```bash
# Copy the template
copy .env.example .env        # Windows CMD
cp .env.example .env          # macOS / Linux

# Open .env with any text editor and fill in your key:
# HY3_API_KEY=your_api_key
```

### 3. Install and Start

**Method 1: pip Install (Recommended, supports CLI launch)**

```bash
# === Windows (PowerShell) ===
python -m venv venv
.\venv\Scripts\activate
pip install -e .
hy3-research

# === macOS / Linux ===
python3 -m venv venv
source venv/bin/activate
pip install -e .
hy3-research

# Service runs at http://localhost:8000
```

**Method 2: Manual Install (no CLI entry point)**

```bash
# === Windows (PowerShell) ===
python -m venv venv
.\venv\Scripts\activate
cd backend
pip install -r requirements.txt
python main.py

# === macOS / Linux ===
python3 -m venv venv
source venv/bin/activate
cd backend
pip install -r requirements.txt
python main.py

# Service runs at http://localhost:8000
```

**Method 3: One-Click Script (Windows)**

```bash
# Double-click start.bat or run in terminal:
.\start.bat
```

After installation, open your browser and visit `http://localhost:8000`.

### 4. Verify Installation

```bash
# Health check
curl http://localhost:8000/health
# Expected output: {"status":"healthy","hy3_connected":true}

# Or open http://localhost:8000/health directly in browser
```

### Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HY3_API_KEY` | Hy3 API key (**required**) | - |
| `HY3_BASE_URL` | API endpoint URL | `https://api.hunyuan.cloud.tencent.com/v1` |
| `HY3_MODEL` | Model name | `hunyuan-pro` |
| `PORT` | Service port | `8000` |

---

## Frequently Asked Questions (FAQ)

### Q: Is a GPU required? Do I need CUDA installed?

**No.** All AI capabilities in this project are implemented through cloud API calls; only a lightweight web server runs locally. An ordinary laptop is sufficient.

### Q: How is this different from the official Hy3 repository's requirements.txt?

The official Hy3 repository includes model training/fine-tuning dependencies (`torch`, `transformers`, `deepspeed`, `flash-attn`, etc.), requiring an NVIDIA GPU + CUDA. This project is an upper-layer application of Hy3, depending only on a web framework and HTTP client. **The two do not conflict with each other.**

### Q: I want to run the Hy3 model locally — what are the pitfalls?

Please read the **⚠️ Risk Warning** section above in full. Key points:
- Installing `deepspeed` + `flash-attn` is extremely prone to failure; versions must be precisely matched in the order: Torch → CUDA → Deepspeed → Flash-Attn
- Requires NVIDIA GPU ≥ 24 GB VRAM + 32 GB system memory (for compiling flash-attn)
- Docker deployment is strongly recommended over manual compilation
- If you're using a regular laptop (integrated graphics or < 8GB VRAM), give up on local execution and just use this application's cloud API mode

### Q: What if pip install fails?

```bash
# 1. Upgrade pip
python -m pip install --upgrade pip

# 2. If you encounter lxml compilation errors on Windows, install the precompiled version:
pip install lxml --only-binary=lxml

# 3. Check Python version
python --version  # Must be >= 3.9
```

### Q: The page won't open after starting the service?

1. Confirm the terminal shows `Uvicorn running on http://0.0.0.0:8000`
2. Check if your firewall is blocking port 8000
3. Try `http://127.0.0.1:8000` (instead of localhost)

### Q: Sees "HY3_API_KEY not set"?

```bash
# Temporary setting (only valid for current terminal session)
# Windows CMD:     set HY3_API_KEY=your_key
# Windows PowerShell: $env:HY3_API_KEY="your_key"
# macOS/Linux:     export HY3_API_KEY=your_key

# Or create a .env file for permanent effect
echo HY3_API_KEY=your_key > .env    # Windows
echo "HY3_API_KEY=your_key" > .env  # macOS/Linux
```

### Q: How do I provide Hy3 capabilities to other LLM clients?

Use the project's built-in MCP Server:

```bash
cd hy3-mcp-server
pip install -e .
# Then configure the hy3-mcp command in Claude Desktop / Cursor
```

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

---

## Hy3 MCP Server

`hy3-mcp-server` is a standalone Python package that wraps Hy3's large model capabilities as MCP (Model Context Protocol) tools, enabling clients like Claude Desktop and Cursor to directly call them.

### Installation

```bash
cd hy3-mcp-server
pip install -e .
```

### Configure Claude Desktop

Add the following to Claude Desktop's `claude_desktop_config.json`:

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

### Available Tools

| Tool Name | Function |
|-----------|----------|
| `hy3_research` | Deep research: search + analysis + report generation |
| `hy3_code_review` | Code review: bug detection + performance analysis + security audit |
| `hy3_doc_qa` | Document Q&A: file parsing + precise answering |
| `hy3_data_analyze` | Data analysis: CSV/JSON + insight output |
| `hy3_chat` | General chat: free-form Q&A |
