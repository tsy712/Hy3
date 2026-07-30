# Hy3 Research Assistant / Hy3 研究助手

An intelligent research assistant powered by Tencent Hunyuan Hy3, featuring **Deep Research**, **Code Analysis**, and **Document Q&A** as three core capabilities.  
基于腾讯混元 Hy3 大模型的智能研究助手，提供**深度研究**、**代码分析**、**文档问答**三大核心功能。

> ⚡ **This project does NOT require GPU, CUDA, PyTorch, DeepSpeed, or Flash-Attention.**  
> All AI capabilities are accessed via cloud API. You only need Python 3.9+ locally.  
> **本项目不需要 GPU、不需要 CUDA、不需要安装 PyTorch / DeepSpeed / Flash-Attention。**  
> 所有 AI 能力通过云端 API 调用，本地只需 Python 3.9+ 即可运行。

---

## 🚀 Quick Start Guide / 一键运行指南

**Don't skip this! Spend 30 seconds to get the project running — you can read the rest later. Nothing is worse than getting stuck on environment setup.**  
**别跑！先花 30 秒把项目跑起来再说——后续内容随时能看，卡在环境上就亏了。**

### Method 1: Docker (Zero Config, Three Commands) / 方式一：Docker（零配置，三行命令）

```bash
git clone https://github.com/Tencent-Hunyuan/Hy3.git && cd hy3-research-assistant
cp .env.example .env                          # Then open .env in a text editor and fill in HY3_API_KEY / 用记事本打开 .env，填入 HY3_API_KEY
docker-compose up -d                          # Open http://localhost:8000 / 打开 http://localhost:8000
```

> **Just [install Docker Desktop](https://docs.docker.com/get-docker/). No NVIDIA Container Toolkit needed.**  
> **[安装 Docker Desktop](https://docs.docker.com/get-docker/) 即可，不需要 NVIDIA Container Toolkit。**

### Method 2: pip (One-Line Install) / 方式二：pip（一行安装）

```bash
pip install -e . && hy3-research               # Visit http://localhost:8000 / 访问 http://localhost:8000
```

### Method 3: Windows Double-Click / 方式三：Windows 双击

```bash
.\start.bat                                    # Double-click or run in terminal / 双击或终端运行即可
```

---

### FAQ — 30-Second Quick Reference / 常见问题 30 秒速查

<details>
<summary><b>I don't have a GPU — can I run this? / 我没 GPU 能跑吗？</b></summary>

**Yes!** This project doesn't run local models — it only sends HTTP requests to the cloud API. An integrated-graphics laptop works perfectly.  
**能！** 本项目不跑本地模型，只发 HTTP 请求调用云端 API。核显笔记本完全够用。
</details>

<details>
<summary><b>Do I need CUDA / PyTorch? / 需要装 CUDA / PyTorch 吗？</b></summary>

**No.** Only 11 lightweight dependencies (FastAPI + OpenAI SDK + file parsers), ~80 MB total. Nothing to do with deepspeed / flash-attn.  
**不需要。** 11 个轻量依赖（FastAPI + OpenAI SDK + 文件解析），总计 ~80 MB。跟 deepspeed / flash-attn 没关系。
</details>

<details>
<summary><b>docker-compose error? / docker-compose 报错？</b></summary>

Try `docker compose up -d` (no hyphen). Newer Docker versions have it built in.  
试 `docker compose up -d`（无横杠），新版 Docker 内置。
</details>

---

## Project Overview / 项目简介

This project is a complete implementation of Tencent Rhino-Bird Open Source Practice Plan [Issue #4](https://github.com/Tencent-Hunyuan/Hy3/issues/4). All intelligent tasks (research planning, report generation, code analysis, document Q&A) are performed via the **Hy3 API** (OpenAI-compatible interface) — no model training, fine-tuning, or local inference involved.  
本项目是腾讯犀牛鸟实战计划 [Issue #4](https://github.com/Tencent-Hunyuan/Hy3/issues/4) 的完整实现。所有智能任务（研究规划、报告生成、代码分析、文档问答）均通过调用 **Hy3 API**（OpenAI 兼容接口）完成，不涉及模型训练、微调或本地推理。

### Hy3's Role in the Project / Hy3 在项目中的角色

| Feature Module / 功能模块 | Hy3's Role / Hy3 的角色 |
|---------|-----------|
| Deep Research / 深度研究 | Research planning → Search keyword generation → Long-form report writing → Executive summary / 研究计划制定 → 搜索关键词生成 → 长文报告撰写 → 执行摘要提炼 |
| Code Analysis / 代码分析 | Code comprehension, Bug detection, Performance optimization, Security audit, Quality scoring / 代码理解、Bug 检测、性能优化建议、安全审计、质量评分 |
| Document Q&A / 文档问答 | Multi-document comprehension, Evidence-driven precise Q&A / 多文档阅读理解、证据驱动的精准问答 |

---

## Preconfigured Files Overview / 预配置文件一览

| File / 文件 | Description / 说明 | What You Need to Do / 你需要做什么 |
|------|------|-------------|
| `.env.example` | [Environment variable template](.env.example) / 环境变量模板 | Copy as `.env`, fill in `HY3_API_KEY` / 复制为 `.env`，填入 `HY3_API_KEY` |
| `backend/requirements.txt` | [11 lightweight dependencies](backend/requirements.txt) / 11 个轻量依赖 | No changes needed; pip auto-installs / 无需修改，pip 自动安装 |
| `docker-compose.yml` | Docker orchestration file / Docker 编排文件 | No changes needed; works out of the box / 无需修改，开箱即用 |
| `Dockerfile` | Container image build file / 容器镜像构建文件 | No changes needed / 无需修改 |
| `start.bat` | Windows double-click launch script / Windows 双击启动脚本 | No changes needed / 无需修改 |

---

## Project Structure / 项目结构

```
hy3-research-assistant/
├── Dockerfile              # Container image build file / 容器镜像构建文件
├── docker-compose.yml      # Docker one-click orchestration / Docker 一键编排文件
├── backend/
│   ├── main.py            # FastAPI server (6 API endpoints, all SSE streaming) / FastAPI 服务器（6 个 API 端点，全部支持 SSE 流式输出）
│   ├── hy3_client.py      # Hy3 API client wrapper (OpenAI-compatible) / Hy3 API 客户端封装（OpenAI 兼容接口）
│   ├── tools.py            # Utility functions (web search, PDF/DOCX/code parsing) / 工具函数（网页搜索、PDF/DOCX/代码文件解析）
│   ├── cli.py              # CLI entry point (hy3-research command after pip install) / 命令行启动入口（pip 安装后可用 hy3-research 命令）
│   └── requirements.txt   # Python dependencies / Python 依赖
├── hy3-mcp-server/         # MCP Server sub-project (standalone install) / MCP Server 子项目（可独立安装）
│   ├── src/                # Source code / 源代码
│   │   ├── server.py       # FastMCP server (5 Tools) / FastMCP 服务端（5 个 Tool）
│   │   └── hy3_client.py  # Hy3 API client / Hy3 API 客户端
│   ├── pyproject.toml      # pip install config / pip 安装配置
│   └── requirements.txt   # Python dependencies / Python 依赖
├── frontend/
│   └── index.html          # Modern web frontend (dark theme, streaming, Markdown) / 现代化 Web 前端（暗色主题、流式渲染、Markdown 展示）
├── pyproject.toml          # Main project pip install config / 主项目 pip 安装配置
├── .env.example            # Environment variable config template / 环境变量配置模板
├── .gitignore
├── start.bat               # Windows one-click launch script / Windows 一键启动脚本
└── README.md
```

---

> 🚨 **【Newcomer Must-Read】Environment Setup Pitfall Guide**  
> **【新人必读】环境配置避坑指南**
> 
> Since Hy3's official repo depends on `deepspeed` + `flash-attn` with strict CUDA version requirements, **please first determine which scenario you fall into**:  
> 由于 Hy3 官方仓库依赖 `deepspeed` + `flash-attn`，对 CUDA 版本有严格要求，**请先确认你属于哪种情况**：
> 
> **Option A (Recommended)**: If you're using a school server, personal laptop, and **don't have an NVIDIA GPU (≥24GB)** → **skip the model fine-tuning module** and just run `python server.py` for basic features. This project uses HTTP to call the cloud API — no GPU / CUDA / local model needed.  
> **方案 A（推荐）**：如果你用的是学校服务器、个人笔记本，且 **没有 NVIDIA GPU (≥24GB)** → 请**跳过模型微调模块**，仅运行 `python server.py` 体验基础功能。本项目通过 HTTP 调用云端 API，不需要 GPU / CUDA / 本地模型。
> 
> **Option B (Hardcore)**: If you have an NVIDIA GPU and want to run Hy3 locally → you **must** ensure **PyTorch version matches your CUDA driver**. Docker is strongly recommended (see version compatibility table and Docker guide below).  
> **方案 B（硬核）**：如果你有 NVIDIA GPU 且想本地运行 Hy3 模型 → 请务必确保 **PyTorch 版本与 CUDA 驱动匹配**。强烈建议在 Docker 环境下运行（下方有版本对照表和 Docker 指南）。
> 
> See the detailed risk section ⚠️ below → / 详细风险说明见下方 ⚠️ 章节 →

---

## Environment Requirements / 环境要求

### Hardware / 硬件要求

| Item / 项目 | Minimum / 最低配置 | Recommended / 推荐配置 |
|------|---------|---------|
| CPU | Any dual-core / 任意双核处理器 | Quad-core+ / 四核及以上 |
| RAM / 内存 | 512 MB | 1 GB+ |
| Disk / 磁盘 | 200 MB | 500 MB+ |
| GPU | **Not required** / **不需要** | **Not required** / **不需要** |
| Network / 网络 | Broadband / 宽带连接 | Stable broadband / 稳定宽带 |

> **Important: This project does NOT need GPU or CUDA.**  
> All AI inference tasks are completed via HTTP calls to the Tencent Hunyuan Hy3 cloud API — no local model loading, inference, or training involved.  
> If your goal is to **run / fine-tune the Hy3 model locally**, refer to the [Hy3 Official Repo](https://github.com/Tencent-Hunyuan/Hy3) hardware requirements (NVIDIA GPU + CUDA 11.8+ required).  
> **重要说明：本项目不需要 GPU 或 CUDA。**  
> 所有 AI 推理任务均通过 HTTP 调用腾讯混元 Hy3 云端 API 完成，不涉及本地模型加载、推理或训练。  
> 如果你的目标是 **本地运行/微调 Hy3 模型本身**，请参考 [Hy3 官方仓库](https://github.com/Tencent-Hunyuan/Hy3) 的硬件要求（需要 NVIDIA GPU + CUDA 11.8+）。

### Software / 软件要求

| Dependency / 依赖 | Version / 版本要求 | Notes / 说明 |
|------|---------|------|
| Python | **3.9+** (main project) / **3.10+** (MCP Server) | 3.11 recommended / 推荐 3.11 |
| pip | 23.0+ | Installed with Python / 随 Python 一起安装 |
| OS / 操作系统 | Windows 10+ / macOS 12+ / Linux (any distro) / Linux（任意发行版） | All supported / 均支持 |

### Dependency Overview / 依赖包总览

This project has **zero dependencies** on PyTorch, Transformers, CUDA, or any deep learning framework. Only 11 lightweight packages:  
本项目**不依赖** PyTorch、Transformers、CUDA 等深度学习框架。全部依赖仅 11 个轻量级包：

```
fastapi>=0.115.0        # Web framework / Web 框架
uvicorn>=0.34.0         # ASGI server / ASGI 服务器
openai>=1.50.0          # Hy3 API calls (OpenAI-compatible) / Hy3 API 调用（OpenAI 兼容接口）
python-multipart        # File upload support / 文件上传支持
aiofiles                # Async file I/O / 异步文件读写
PyPDF2>=3.0.0           # PDF parsing / PDF 解析
python-docx>=1.1.0      # Word document parsing / Word 文档解析
httpx>=0.28.0           # HTTP client (web search) / HTTP 客户端（网页搜索）
beautifulsoup4>=4.12.0  # HTML parsing / HTML 解析
lxml>=5.3.0             # High-performance XML/HTML parser / XML/HTML 高性能解析器
```

> Total install size ~**80 MB**. No multi-GB model weight downloads needed.  
> 总安装大小约 **80 MB**，无需下载数 GB 的模型权重文件。

---

## ⚠️ Risk Warning: The Huge Difference Between Two Running Modes / 风险提示：两种运行模式的巨大差异

Many developers new to Hy3 confuse these two scenarios. **Please make sure you know which one you're in:**  
很多第一次接触 Hy3 的开发者会混淆以下两种场景。**请务必确认你属于哪一种：**

| Dimension / 维度 | 🟢 Mode A: This App (Recommended) / 本应用（推荐） | 🔴 Mode B: Run Hy3 Model Locally / 本地运行 Hy3 模型 |
|------|--------------------------|------------------------------|
| What it does / 做什么 | Call Tencent Cloud API via HTTP / 通过 HTTP 调用腾讯云端 API | Load and infer the model on local GPU / 在本地 GPU 上加载并推理模型 |
| Need GPU? / 需要 GPU？ | **No** / **不需要** | **Required** (NVIDIA GPU) / **必须**（NVIDIA GPU） |
| Need CUDA? / 需要 CUDA？ | **No** / **不需要** | **Required** (CUDA 11.8 or 12.1) / **必须**（CUDA 11.8 或 12.1） |
| Install size / 安装大小 | ~80 MB | ~20 GB+ (incl. model weights) / （含模型权重） |
| Install time / 安装时间 | < 2 min / 分钟 | 30 min ~ 2 hours / 小时 |
| Works first try? / 一次能跑通？ | ✅ Almost never fails / 几乎不会出问题 | ❌ High chance of issues / 高概率踩坑 |

> **If you just want to use Hy3's intelligence for research, coding, Q&A → Mode A, this doc covers everything.**  
> **If you want to deploy the Hy3 model itself on your own GPU server → Mode B, read the risks below.**  
> **如果你只是想使用 Hy3 的智能能力做研究、写代码、问答 → 模式 A，本文档完全覆盖。**  
> **如果你想在自己的 GPU 服务器上部署 Hy3 模型本身 → 模式 B，请继续阅读下方风险说明。**

### 🔴 Mode B: Known Pitfalls of Running Hy3 Locally / 本地运行 Hy3 模型的已知陷阱

Hy3's official model repo depends on `deepspeed` + `flash-attn` — two deep learning components notorious for difficult installation. **Wrong version combinations cause compilation failures or runtime crashes.**  
Hy3 官方模型仓库依赖 `deepspeed` + `flash-attn` 两个以"安装困难"著称的深度学习组件，**不正确的版本组合会导致编译失败或运行时崩溃**。

#### 1. DeepSpeed + Flash-Attention Version Compatibility Table / 版本兼容对照表

| Torch Version | CUDA Version | DeepSpeed | Flash-Attn | Notes / 说明 |
|-----------|----------|-----------|------------|------|
| 2.1.x | 11.8 | 0.12.x | 2.5.x | Stable combo, try first / 稳定组合，推荐先尝试 |
| 2.2.x | 12.1 | 0.13.x | 2.5.x | Newer combo / 较新组合 |
| 2.3.x | 12.1 | 0.14.x | 2.6.x | Latest combo, possible issues / 最新组合，可能有兼容问题 |
| 2.4.x+ | 12.4+ | 0.15.x+ | 2.7.x+ | Cutting-edge, stability unverified / 前沿组合，稳定性未充分验证 |

> **Key lesson**: Don't just `pip install deepspeed`. First check your `torch.__version__` and `nvcc --version`, then choose versions per the table above.  
> **关键教训**: 不要用 `pip install deepspeed` 直接安装，必须先确认你的 `torch.__version__` 和 `nvcc --version`，再按上表选择版本。
> ```bash
> # Check versions first / 先查版本
> python -c "import torch; print(torch.__version__)"
> nvcc --version  # Or nvidia-smi to check CUDA Driver version / 或 nvidia-smi 查看 CUDA Driver 版本
> 
> # Then install precisely (example: CUDA 11.8 + Torch 2.1.x) / 再精确安装（示例：CUDA 11.8 + Torch 2.1.x）
> pip install torch==2.1.2 torchvision==0.16.2 --index-url https://download.pytorch.org/whl/cu118
> pip install deepspeed==0.12.6
> pip install flash-attn==2.5.8 --no-build-isolation
> ```

#### 2. Common Reasons for flash-attn Compilation Failures / flash-attn 编译失败的常见原因

- **Ninja not installed**: `pip install ninja` / **Ninja 未安装**: `pip install ninja`
- **GCC/G++ version too low**: Need GCC 9+ (Linux) or Visual Studio Build Tools 2022+ (Windows) / **GCC/G++ 版本过低**: 需要 GCC 9+（Linux）或 Visual Studio Build Tools 2022+（Windows）
- **CUDA Toolkit not installed or wrong path**: Ensure `nvcc` is executable and in PATH / **CUDA Toolkit 未安装或路径不对**: 确保 `nvcc` 可执行且在 PATH 中
- **Insufficient RAM**: flash-attn compilation peak memory can reach **32 GB+**; OOM Killer may terminate the process / **RAM 不足**: `flash-attn` 编译峰值内存可达 **32 GB+**，内存不足会导致编译被 OOM Killer 终止
- **Windows compatibility**: flash-attn has limited Windows support; strongly recommend WSL2 or native Linux / **Windows 兼容性**: `flash-attn` 对 Windows 支持有限，强烈建议在 WSL2 或 Linux 原生环境下编译

#### 3. Minimum VRAM Requirements / 显存最低要求

| Model Size / 模型规模 | FP16 / 半精度 | FP32 / 全精度 | INT8 Quantized / INT8 量化 |
|---------|-------------|-------------|----------|
| 7B | ~14 GB | ~28 GB | ~8 GB |
| 13B | ~26 GB | ~52 GB | ~14 GB |
| 34B | ~68 GB | ~136 GB | ~35 GB |

> **⚠️ If you're using a MacBook / thin-and-light / integrated-graphics desktop**: Mode B is impossible to run.  
> **⚠️ If you only have a single 8GB/12GB consumer GPU (e.g. RTX 3060/4060)**: Only 7B quantized version, and CPU offload is needed.  
> **Recommended setup**: NVIDIA GPU ≥ 24 GB VRAM (e.g. RTX 3090/4090, A5000, A100).  
> 
> **⚠️ 如果你用 MacBook / 轻薄本 / 核显台式机**：模式 B 不可能跑通。  
> **⚠️ 如果你只有单张 8GB/12GB 消费级显卡（如 RTX 3060/4060）**：只能跑 7B 量化版，且需要 CPU offload。  
> **推荐评审环境**: NVIDIA GPU ≥ 24 GB 显存（如 RTX 3090/4090, A5000, A100）。

#### 4. Recommended: Use Docker for One-Click Deployment (Skip Compilation Hell) / 推荐：使用 Docker 一键部署（跳过编译地狱）

If you must run Hy3 locally, **strongly recommend using the official Docker image** to avoid manually compiling `deepspeed` + `flash-attn`:  
如果必须本地运行 Hy3 模型，**强烈建议使用官方 Docker 镜像**，避免手动编译 `deepspeed` + `flash-attn`：

```bash
# Pull Hy3 official image (if available) / 拉取 Hy3 官方镜像（如可用）
docker pull tencent-hunyuan/hy3:latest

# Start (mount model directory) / 启动（挂载模型目录）
docker run --gpus all \
  -v /path/to/models:/models \
  -p 7860:7860 \
  tencent-hunyuan/hy3:latest
```

> If an official Docker image is not yet available, file an Issue on the Hy3 official repo or build from the `Dockerfile` template yourself.  
> 如官方尚未发布 Docker 镜像，可在 Hy3 官方仓库提交 Issue 请求，或参考 `Dockerfile` 模板自行构建。

---

## Quick Start / 快速开始

### 0. Get a Hy3 API Key / 获取 Hy3 API Key

You need a valid Hy3 API key. See [Hy3 Official Docs](https://github.com/Tencent-Hunyuan/Hy3) for instructions.  
使用前需要有效的 Hy3 API 密钥。获取方式请参考 [Hy3 官方文档](https://github.com/Tencent-Hunyuan/Hy3)。

### 1. Clone the Repo / 克隆项目

```bash
git clone https://github.com/Tencent-Hunyuan/Hy3.git
cd hy3-research-assistant
```

### 2. Configure API Key / 配置 API 密钥

**Method A: Environment Variables (Recommended) / 方式 A：环境变量（推荐）**

| OS / 操作系统 | Command / 命令 |
|---------|------|
| Windows (CMD) | `set HY3_API_KEY=your-api-key` / `set HY3_API_KEY=你的API密钥` |
| Windows (PowerShell) | `$env:HY3_API_KEY="your-api-key"` / `$env:HY3_API_KEY="你的API密钥"` |
| macOS / Linux | `export HY3_API_KEY=your-api-key` / `export HY3_API_KEY=你的API密钥` |

**Method B: .env File (Persistent) / 方式 B：.env 文件（持久化）**

```bash
# Copy template / 复制模板
copy .env.example .env        # Windows CMD
cp .env.example .env          # macOS / Linux

# Open .env in any text editor, fill in your key: / 用任意文本编辑器打开 .env，填入密钥：
# HY3_API_KEY=your-api-key / HY3_API_KEY=你的API密钥
```

### 3. Install & Launch / 安装与启动

<details open>
<summary><b>Method 1: pip Install (Recommended, with CLI entry) / 方式一：pip 安装（推荐，支持命令行启动）</b></summary>

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

# Server runs at http://localhost:8000 / 服务运行在 http://localhost:8000
```

</details>

<details>
<summary><b>Method 2: Manual Install (no CLI entry) / 方式二：手动安装（不创建命令行入口）</b></summary>

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

# Server runs at http://localhost:8000 / 服务运行在 http://localhost:8000
```

</details>

<details>
<summary><b>Method 3: One-Click Script (Windows) / 方式三：一键脚本（Windows）</b></summary>

```bash
# Double-click start.bat or run in terminal: / 双击 start.bat 或在终端中运行：
.\start.bat
```

</details>

After installation, open your browser to `http://localhost:8000` to use the app.  
安装完成后，打开浏览器访问 `http://localhost:8000` 即可使用。

### 4. Verify Installation / 验证安装

```bash
# Health check / 健康检查
curl http://localhost:8000/health
# Expected output: {"status":"healthy","hy3_connected":true} / 预期输出: {"status":"healthy","hy3_connected":true}

# Or open http://localhost:8000/health in browser / 或直接浏览器打开 http://localhost:8000/health
```

### Optional Environment Variables / 可选环境变量

| Variable / 变量名 | Description / 说明 | Default / 默认值 |
|--------|------|--------|
| `HY3_API_KEY` | Hy3 API key (**required**) / Hy3 API 密钥（**必填**） | - |
| `HY3_BASE_URL` | API endpoint / API 端点地址 | `https://api.hunyuan.cloud.tencent.com/v1` |
| `HY3_MODEL` | Model name / 模型名称 | `hunyuan-pro` |
| `PORT` | Server port / 服务端口 | `8000` |

---

## FAQ / 常见问题

### Q: Do I need a GPU? CUDA? / 需要 GPU 吗？需要安装 CUDA 吗？

**No.** All AI capabilities run via cloud API. The local server is just a lightweight web server. Any ordinary laptop works.  
**不需要。** 本项目所有 AI 能力通过云端 API 调用实现，本地仅运行轻量级 Web 服务器。一台普通笔记本即可运行。

### Q: How is this different from Hy3's official requirements.txt? / 和 Hy3 官方仓库的 requirements.txt 有何区别？

Hy3's official repo includes model training/fine-tuning dependencies (`torch`, `transformers`, `deepspeed`, `flash-attn`, etc.), requiring NVIDIA GPU + CUDA. This project is an upper-layer app built on Hy3, depending only on a web framework and HTTP client. **The two do not conflict.**  
Hy3 官方仓库包含模型训练/微调依赖（`torch`、`transformers`、`deepspeed`、`flash-attn` 等），需要 NVIDIA GPU + CUDA。本项目是 Hy3 的上层应用，只依赖 Web 框架和 HTTP 客户端，**两者互不冲突**。

### Q: I want to run Hy3 locally — what are the pitfalls? / 我想本地运行 Hy3 模型，有什么坑？

Please read the full **⚠️ Risk Warning** section above. Key points: / 请完整阅读上方的 **⚠️ 风险提示** 章节。核心要点：
- `deepspeed` + `flash-attn` installation is very fragile; must precisely match versions in order: Torch → CUDA → Deepspeed → Flash-Attn / `deepspeed` + `flash-attn` 安装极其容易失败，必须按 Torch→CUDA→Deepspeed→Flash-Attn 的顺序精确匹配版本
- Requires NVIDIA GPU ≥ 24 GB VRAM + 32 GB system RAM (for flash-attn compilation) / 需要 NVIDIA GPU ≥ 24 GB 显存 + 32 GB 系统内存（编译 flash-attn）
- Docker deployment is strongly recommended over manual compilation / 强烈建议用 Docker 部署而非手动编译
- If you have a regular laptop (integrated graphics or < 8GB VRAM), skip local mode and use this app's cloud API mode / 如果你用的是普通笔记本（集成显卡或 < 8GB 显存），请放弃本地运行，使用本应用的云端 API 模式即可

### Q: pip install fails — what do I do? / pip install 报错怎么办？

```bash
# 1. Upgrade pip / 升级 pip
python -m pip install --upgrade pip

# 2. If you hit lxml build errors on Windows, install prebuilt: / 如果在 Windows 上遇到 lxml 编译错误，安装预编译版：
pip install lxml --only-binary=lxml

# 3. Check Python version / 检查 Python 版本
python --version  # Needs >= 3.9 / 需要 >= 3.9
```

### Q: Page won't load after starting the server? / 服务启动后页面打不开？

1. Confirm the terminal shows `Uvicorn running on http://0.0.0.0:8000` / 确认终端显示 `Uvicorn running on http://0.0.0.0:8000`
2. Check if the firewall is blocking port 8000 / 检查防火墙是否拦截端口 8000
3. Try `http://127.0.0.1:8000` (instead of localhost) / 尝试 `http://127.0.0.1:8000`（而非 localhost）

### Q: "HY3_API_KEY not set" error? / 提示 "未设置 HY3_API_KEY"？

```bash
# Temporary (current terminal only) / 临时设置（仅当前终端有效）
# Windows CMD:     set HY3_API_KEY=your-key / set HY3_API_KEY=你的密钥
# Windows PowerShell: $env:HY3_API_KEY="your-key" / $env:HY3_API_KEY="你的密钥"
# macOS/Linux:     export HY3_API_KEY=your-key / export HY3_API_KEY=你的密钥

# Or create .env for persistence / 或创建 .env 文件永久生效
echo HY3_API_KEY=your-key > .env    # Windows / echo HY3_API_KEY=你的密钥 > .env
echo "HY3_API_KEY=your-key" > .env  # macOS/Linux / echo "HY3_API_KEY=你的密钥" > .env
```

### Q: How do I provide Hy3 capabilities to other LLM clients? / 如何为其他 LLM 客户端提供 Hy3 能力？

Use the built-in MCP Server: / 使用项目自带的 MCP Server：

```bash
cd hy3-mcp-server
pip install -e .
# Then configure the hy3-mcp command in Claude Desktop / Cursor etc. / 然后在 Claude Desktop / Cursor 中配置 hy3-mcp 命令
```

## Three Core Features / 三大功能

### 🔬 Deep Research / 深度研究

Enter a research topic and Hy3 will automatically: / 输入研究主题，Hy3 将自动完成：

1. **Research Planning** — Break down the topic into sub-questions, generate search keywords / 将主题拆解为子问题，生成搜索关键词
2. **Information Search** — Auto-search relevant web materials / 自动搜索相关网页资料
3. **Report Writing** — Generate a 1500-3000 word professional research report from search results / 基于搜索结果生成 1500-3000 字专业研究报告
4. **Executive Summary** — Concise summary of core findings / 提炼核心发现的简明摘要

### 💻 Code Analysis / 代码分析

Paste code or upload a code file and Hy3 provides: / 粘贴代码或上传代码文件，Hy3 将提供：

- Code overview and core functionality interpretation / 代码概览与核心功能解读
- Execution logic and key flow analysis / 执行逻辑与关键流程分析
- Potential bugs, performance issues, security risks / 潜在 Bug、性能隐患、安全问题诊断
- Specific optimization suggestions and best practices / 具体优化建议与最佳实践
- 1-10 code quality score / 1-10 分代码质量评分

### 📚 Document Q&A / 文档问答

Upload multiple documents (PDF, DOCX, TXT, code files, etc.) and ask Hy3: / 上传多个文档（支持 PDF、DOCX、TXT、代码文件等），向 Hy3 提问：

- Precise answers based on document content / 基于文档内容精准回答
- Citations from original passages as evidence / 引用原始段落作为证据
- Clear indication when information is missing / 明确标注信息缺失情况

## API Endpoints / API 端点

| Endpoint / 端点 | Method / 方法 | Description / 说明 |
|------|------|------|
| `/` | GET | Frontend page / 前端页面 |
| `/health` | GET | Service health check / 服务健康检查 |
| `/api/research` | POST | Deep Research (streaming) / 深度研究（流式） |
| `/api/analyze-code` | POST | Paste code analysis (streaming) / 粘贴代码分析（流式） |
| `/api/analyze-code-file` | POST | Upload code file analysis (streaming) / 上传代码文件分析（流式） |
| `/api/qa-documents` | POST | Multi-document Q&A (streaming) / 多文档问答（流式） |

All intelligent endpoints use **Server-Sent Events (SSE)** for streaming output, supporting real-time frontend rendering.  
所有智能端点均使用 Server-Sent Events (SSE) 实现流式输出，支持前端实时渲染。

## Tech Stack / 技术栈

- **Backend**: FastAPI + OpenAI SDK + Uvicorn / 后端
- **Frontend**: Vanilla HTML/CSS/JS + marked.js (Markdown rendering) / 前端: 原生 HTML/CSS/JS + marked.js（Markdown 渲染）
- **Model**: Tencent Hunyuan Hy3 (via OpenAI-compatible API) / 模型: 腾讯混元 Hy3（通过 OpenAI 兼容接口调用）
- **Tools**: DuckDuckGo web search, PyPDF2, python-docx / 工具: DuckDuckGo 网页搜索、PyPDF2、python-docx

## CodeBuddy Collaboration Notes / CodeBuddy 协作说明

This project was built with the help of the CodeBuddy AI programming assistant: / 本项目借助 CodeBuddy AI 编程助手完成：

- **Collaborative Design**: AI participated in overall architecture planning, feature module breakdown, and frontend-backend interaction design / AI 参与整体架构规划、功能模块拆解、前后端交互设计
- **Code Generation**: AI wrote `backend/main.py` (server and all prompt engineering), `backend/hy3_client.py` (API client wrapper), `backend/tools.py` (search and file parsing), `frontend/index.html` (complete frontend UI) / AI 编写了上述文件
- **Documentation**: AI generated the README, config templates, and launch scripts / AI 生成了 README、配置模板、启动脚本
- **Code Review & Refinement**: AI assisted with syntax checks, Chinese-English translation, and structural optimization / AI 辅助进行了语法检查、中英文翻译、结构优化

---

## Hy3 MCP Server

`hy3-mcp-server` is a standalone Python package that wraps Hy3 capabilities as MCP (Model Context Protocol) tools, enabling direct invocation from clients like Claude Desktop, Cursor, etc.  
`hy3-mcp-server` 是一个独立的 Python 包，将 Hy3 大模型能力封装为 MCP (Model Context Protocol) 工具，让 Claude Desktop、Cursor 等客户端直接调用。

### Install / 安装

```bash
cd hy3-mcp-server
pip install -e .
```

### Configure Claude Desktop / 配置 Claude Desktop

Add to Claude Desktop's `claude_desktop_config.json`: / 在 Claude Desktop 的 `claude_desktop_config.json` 中添加：

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

### Available Tools / 提供的工具

| Tool / 工具名 | Function / 功能 |
|--------|------|
| `hy3_research` | Deep Research: search + analysis + report generation / 深度研究：搜索 + 分析 + 生成报告 |
| `hy3_code_review` | Code Review: bug detection + performance analysis + security audit / 代码评审：Bug 检测 + 性能分析 + 安全审计 |
| `hy3_doc_qa` | Document Q&A: file parsing + precise answers / 文档问答：文件解析 + 精准回答 |
| `hy3_data_analyze` | Data Analysis: CSV/JSON + insights / 数据分析：CSV/JSON + 洞察输出 |
| `hy3_chat` | General Chat: free-form Q&A / 通用对话：自由问答 |
