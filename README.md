# Hy3 研究助手

基于腾讯混元 Hy3 大模型的智能研究助手，提供**深度研究**、**代码分析**、**文档问答**三大核心功能。

> ⚡ **本项目不需要 GPU、不需要 CUDA、不需要安装 PyTorch / DeepSpeed / Flash-Attention。**  
> 所有 AI 能力通过云端 API 调用，本地只需 Python 3.9+ 即可运行。

---

## 🚀 一键运行指南

**别跑！先花 30 秒把项目跑起来再说——后续内容随时能看，卡在环境上就亏了。**

### 方式一：Docker（零配置，三行命令）

```bash
git clone https://github.com/Tencent-Hunyuan/Hy3.git && cd hy3-research-assistant
cp .env.example .env                          # 然后用记事本打开 .env，填入 HY3_API_KEY
docker-compose up -d                          # 打开 http://localhost:8000
```

> **[安装 Docker Desktop](https://docs.docker.com/get-docker/) 即可，不需要 NVIDIA Container Toolkit。**

### 方式二：pip（一行安装）

```bash
pip install -e . && hy3-research               # 访问 http://localhost:8000
```

### 方式三：Windows 双击

```bash
.\start.bat                                    # 双击或终端运行即可
```

---

### 常见问题 30 秒速查

<details>
<summary><b>我没 GPU 能跑吗？</b></summary>

**能！** 本项目不跑本地模型，只发 HTTP 请求调用云端 API。核显笔记本完全够用。
</details>

<details>
<summary><b>需要装 CUDA / PyTorch 吗？</b></summary>

**不需要。** 11 个轻量依赖（FastAPI + OpenAI SDK + 文件解析），总计 ~80 MB。跟 deepspeed / flash-attn 没关系。
</details>

<details>
<summary><b>docker-compose 报错？</b></summary>

试 `docker compose up -d`（无横杠），新版 Docker 内置。
</details>

---

## 项目简介

本项目是腾讯犀牛鸟实战计划 [Issue #4](https://github.com/Tencent-Hunyuan/Hy3/issues/4) 的完整实现。所有智能任务（研究规划、报告生成、代码分析、文档问答）均通过调用 **Hy3 API**（OpenAI 兼容接口）完成，不涉及模型训练、微调或本地推理。

### Hy3 在项目中的角色

| 功能模块 | Hy3 的角色 |
|---------|-----------|
| 深度研究 | 研究计划制定 → 搜索关键词生成 → 长文报告撰写 → 执行摘要提炼 |
| 代码分析 | 代码理解、Bug 检测、性能优化建议、安全审计、质量评分 |
| 文档问答 | 多文档阅读理解、证据驱动的精准问答 |

---

## 预配置文件一览

| 文件 | 说明 | 你需要做什么 |
|------|------|-------------|
| `.env.example` | [环境变量模板](.env.example) | 复制为 `.env`，填入 `HY3_API_KEY` |
| `backend/requirements.txt` | [11 个轻量依赖](backend/requirements.txt) | 无需修改，pip 自动安装 |
| `docker-compose.yml` | Docker 编排文件 | 无需修改，开箱即用 |
| `Dockerfile` | 容器镜像构建文件 | 无需修改 |
| `start.bat` | Windows 双击启动脚本 | 无需修改 |

---

## 项目结构

```
hy3-research-assistant/
├── Dockerfile              # 容器镜像构建文件
├── docker-compose.yml      # Docker 一键编排文件
├── backend/
│   ├── main.py            # FastAPI 服务器（6 个 API 端点，全部支持 SSE 流式输出）
│   ├── hy3_client.py      # Hy3 API 客户端封装（OpenAI 兼容接口）
│   ├── tools.py            # 工具函数（网页搜索、PDF/DOCX/代码文件解析）
│   ├── cli.py              # 命令行启动入口（pip 安装后可用 hy3-research 命令）
│   └── requirements.txt   # Python 依赖
├── hy3-mcp-server/         # MCP Server 子项目（可独立安装）
│   ├── src/                # 源代码
│   │   ├── server.py       # FastMCP 服务端（5 个 Tool）
│   │   └── hy3_client.py  # Hy3 API 客户端
│   ├── pyproject.toml      # pip 安装配置
│   └── requirements.txt   # Python 依赖
├── frontend/
│   └── index.html          # 现代化 Web 前端（暗色主题、流式渲染、Markdown 展示）
├── pyproject.toml          # 主项目 pip 安装配置
├── .env.example            # 环境变量配置模板
├── .gitignore
├── start.bat               # Windows 一键启动脚本
└── README.md
```

---

> 🚨 **【新人必读】环境配置避坑指南**
> 
> 由于 Hy3 官方仓库依赖 `deepspeed` + `flash-attn`，对 CUDA 版本有严格要求，**请先确认你属于哪种情况**：
> 
> **方案 A（推荐）**：如果你用的是学校服务器、个人笔记本，且 **没有 NVIDIA GPU (≥24GB)** → 请**跳过模型微调模块**，仅运行 `python server.py` 体验基础功能。本项目通过 HTTP 调用云端 API，不需要 GPU / CUDA / 本地模型。
> 
> **方案 B（硬核）**：如果你有 NVIDIA GPU 且想本地运行 Hy3 模型 → 请务必确保 **PyTorch 版本与 CUDA 驱动匹配**。强烈建议在 Docker 环境下运行（下方有版本对照表和 Docker 指南）。
> 
> 详细风险说明见下方 ⚠️ 章节 →

---

## 环境要求

### 硬件要求

| 项目 | 最低配置 | 推荐配置 |
|------|---------|---------|
| CPU | 任意双核处理器 | 四核及以上 |
| 内存 | 512 MB | 1 GB+ |
| 磁盘 | 200 MB | 500 MB+ |
| GPU | **不需要** | **不需要** |
| 网络 | 宽带连接 | 稳定宽带 |

> **重要说明：本项目不需要 GPU 或 CUDA。**  
> 所有 AI 推理任务均通过 HTTP 调用腾讯混元 Hy3 云端 API 完成，不涉及本地模型加载、推理或训练。  
> 如果你的目标是 **本地运行/微调 Hy3 模型本身**，请参考 [Hy3 官方仓库](https://github.com/Tencent-Hunyuan/Hy3) 的硬件要求（需要 NVIDIA GPU + CUDA 11.8+）。

### 软件要求

| 依赖 | 版本要求 | 说明 |
|------|---------|------|
| Python | **3.9+**（主项目）/ **3.10+**（MCP Server） | 推荐 3.11 |
| pip | 23.0+ | 随 Python 一起安装 |
| 操作系统 | Windows 10+ / macOS 12+ / Linux（任意发行版） | 均支持 |

### 依赖包总览

本项目**不依赖** PyTorch、Transformers、CUDA 等深度学习框架。全部依赖仅 11 个轻量级包：

```
fastapi>=0.115.0        # Web 框架
uvicorn>=0.34.0         # ASGI 服务器
openai>=1.50.0          # Hy3 API 调用（OpenAI 兼容接口）
python-multipart        # 文件上传支持
aiofiles                # 异步文件读写
PyPDF2>=3.0.0           # PDF 解析
python-docx>=1.1.0      # Word 文档解析
httpx>=0.28.0           # HTTP 客户端（网页搜索）
beautifulsoup4>=4.12.0  # HTML 解析
lxml>=5.3.0             # XML/HTML 高性能解析器
```

> 总安装大小约 **80 MB**，无需下载数 GB 的模型权重文件。

---

## ⚠️ 风险提示：两种运行模式的巨大差异

很多第一次接触 Hy3 的开发者会混淆以下两种场景。**请务必确认你属于哪一种：**

| 维度 | 🟢 模式 A：本应用（推荐） | 🔴 模式 B：本地运行 Hy3 模型 |
|------|--------------------------|------------------------------|
| 做什么 | 通过 HTTP 调用腾讯云端 API | 在本地 GPU 上加载并推理模型 |
| 需要 GPU？ | **不需要** | **必须**（NVIDIA GPU） |
| 需要 CUDA？ | **不需要** | **必须**（CUDA 11.8 或 12.1） |
| 安装大小 | ~80 MB | ~20 GB+（含模型权重） |
| 安装时间 | < 2 分钟 | 30 分钟 ~ 2 小时 |
| 一次能跑通？ | ✅ 几乎不会出问题 | ❌ 高概率踩坑 |

> **如果你只是想使用 Hy3 的智能能力做研究、写代码、问答 → 模式 A，本文档完全覆盖。**  
> **如果你想在自己的 GPU 服务器上部署 Hy3 模型本身 → 模式 B，请继续阅读下方风险说明。**

### 🔴 模式 B：本地运行 Hy3 模型的已知陷阱

Hy3 官方模型仓库依赖 `deepspeed` + `flash-attn` 两个以"安装困难"著称的深度学习组件，**不正确的版本组合会导致编译失败或运行时崩溃**。

#### 1. DeepSpeed + Flash-Attention 版本兼容对照表

| Torch 版本 | CUDA 版本 | DeepSpeed | Flash-Attn | 说明 |
|-----------|----------|-----------|------------|------|
| 2.1.x | 11.8 | 0.12.x | 2.5.x | 稳定组合，推荐先尝试 |
| 2.2.x | 12.1 | 0.13.x | 2.5.x | 较新组合 |
| 2.3.x | 12.1 | 0.14.x | 2.6.x | 最新组合，可能有兼容问题 |
| 2.4.x+ | 12.4+ | 0.15.x+ | 2.7.x+ | 前沿组合，稳定性未充分验证 |

> **关键教训**: 不要用 `pip install deepspeed` 直接安装，必须先确认你的 `torch.__version__` 和 `nvcc --version`，再按上表选择版本。
> ```bash
> # 先查版本
> python -c "import torch; print(torch.__version__)"
> nvcc --version  # 或 nvidia-smi 查看 CUDA Driver 版本
> 
> # 再精确安装（示例：CUDA 11.8 + Torch 2.1.x）
> pip install torch==2.1.2 torchvision==0.16.2 --index-url https://download.pytorch.org/whl/cu118
> pip install deepspeed==0.12.6
> pip install flash-attn==2.5.8 --no-build-isolation
> ```

#### 2. flash-attn 编译失败的常见原因

- **Ninja 未安装**: `pip install ninja`
- **GCC/G++ 版本过低**: 需要 GCC 9+（Linux）或 Visual Studio Build Tools 2022+（Windows）
- **CUDA Toolkit 未安装或路径不对**: 确保 `nvcc` 可执行且在 PATH 中
- **RAM 不足**: `flash-attn` 编译峰值内存可达 **32 GB+**，内存不足会导致编译被 OOM Killer 终止
- **Windows 兼容性**: `flash-attn` 对 Windows 支持有限，强烈建议在 WSL2 或 Linux 原生环境下编译

#### 3. 显存最低要求

| 模型规模 | 半精度 (FP16) | 全精度 (FP32) | INT8 量化 |
|---------|-------------|-------------|----------|
| 7B | ~14 GB | ~28 GB | ~8 GB |
| 13B | ~26 GB | ~52 GB | ~14 GB |
| 34B | ~68 GB | ~136 GB | ~35 GB |

> **⚠️ 如果你用 MacBook / 轻薄本 / 核显台式机评审本仓库**：模式 B 不可能跑通。  
> **⚠️ 如果你只有单张 8GB/12GB 消费级显卡（如 RTX 3060/4060）**：只能跑 7B 量化版，且需要 CPU offload。  
> **推荐评审环境**: NVIDIA GPU ≥ 24 GB 显存（如 RTX 3090/4090, A5000, A100）。

#### 4. 推荐：使用 Docker 一键部署（跳过编译地狱）

如果必须本地运行 Hy3 模型，**强烈建议使用官方 Docker 镜像**，避免手动编译 `deepspeed` + `flash-attn`：

```bash
# 拉取 Hy3 官方镜像（如可用）
docker pull tencent-hunyuan/hy3:latest

# 启动（挂载模型目录）
docker run --gpus all \
  -v /path/to/models:/models \
  -p 7860:7860 \
  tencent-hunyuan/hy3:latest
```

> 如官方尚未发布 Docker 镜像，可在 Hy3 官方仓库提交 Issue 请求，或参考 `Dockerfile` 模板自行构建。

---

## 快速开始

### 零、获取 Hy3 API Key

使用前需要有效的 Hy3 API 密钥。获取方式请参考 [Hy3 官方文档](https://github.com/Tencent-Hunyuan/Hy3)。

### 一、克隆项目

```bash
git clone https://github.com/Tencent-Hunyuan/Hy3.git
cd hy3-research-assistant
```

### 二、配置 API 密钥

**方式 A：环境变量（推荐）**

| 操作系统 | 命令 |
|---------|------|
| Windows (CMD) | `set HY3_API_KEY=你的API密钥` |
| Windows (PowerShell) | `$env:HY3_API_KEY="你的API密钥"` |
| macOS / Linux | `export HY3_API_KEY=你的API密钥` |

**方式 B：.env 文件（持久化）**

```bash
# 复制模板
copy .env.example .env        # Windows CMD
cp .env.example .env          # macOS / Linux

# 用任意文本编辑器打开 .env，填入密钥：
# HY3_API_KEY=你的API密钥
```

### 三、安装与启动

<details open>
<summary><b>方式一：pip 安装（推荐，支持命令行启动）</b></summary>

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

# 服务运行在 http://localhost:8000
```

</details>

<details>
<summary><b>方式二：手动安装（不创建命令行入口）</b></summary>

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

# 服务运行在 http://localhost:8000
```

</details>

<details>
<summary><b>方式三：一键脚本（Windows）</b></summary>

```bash
# 双击 start.bat 或在终端中运行：
.\start.bat
```

</details>

安装完成后，打开浏览器访问 `http://localhost:8000` 即可使用。

### 四、验证安装

```bash
# 健康检查
curl http://localhost:8000/health
# 预期输出: {"status":"healthy","hy3_connected":true}

# 或直接浏览器打开 http://localhost:8000/health
```

### 可选环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `HY3_API_KEY` | Hy3 API 密钥（**必填**） | - |
| `HY3_BASE_URL` | API 端点地址 | `https://api.hunyuan.cloud.tencent.com/v1` |
| `HY3_MODEL` | 模型名称 | `hunyuan-pro` |
| `PORT` | 服务端口 | `8000` |

---

## 常见问题 (FAQ)

### Q: 需要 GPU 吗？需要安装 CUDA 吗？

**不需要。** 本项目所有 AI 能力通过云端 API 调用实现，本地仅运行轻量级 Web 服务器。一台普通笔记本即可运行。

### Q: 和 Hy3 官方仓库的 requirements.txt 有何区别？

Hy3 官方仓库包含模型训练/微调依赖（`torch`、`transformers`、`deepspeed`、`flash-attn` 等），需要 NVIDIA GPU + CUDA。本项目是 Hy3 的上层应用，只依赖 Web 框架和 HTTP 客户端，**两者互不冲突**。

### Q: 我想本地运行 Hy3 模型，有什么坑？

请完整阅读上方的 **⚠️ 风险提示** 章节。核心要点：
- `deepspeed` + `flash-attn` 安装极其容易失败，必须按 Torch→CUDA→Deepspeed→Flash-Attn 的顺序精确匹配版本
- 需要 NVIDIA GPU ≥ 24 GB 显存 + 32 GB 系统内存（编译 flash-attn）
- 强烈建议用 Docker 部署而非手动编译
- 如果你用的是普通笔记本（集成显卡或 < 8GB 显存），请放弃本地运行，使用本应用的云端 API 模式即可

### Q: pip install 报错怎么办？

```bash
# 1. 升级 pip
python -m pip install --upgrade pip

# 2. 如果在 Windows 上遇到 lxml 编译错误，安装预编译版：
pip install lxml --only-binary=lxml

# 3. 检查 Python 版本
python --version  # 需要 >= 3.9
```

### Q: 服务启动后页面打不开？

1. 确认终端显示 `Uvicorn running on http://0.0.0.0:8000`
2. 检查防火墙是否拦截端口 8000
3. 尝试 `http://127.0.0.1:8000`（而非 localhost）

### Q: 提示 "未设置 HY3_API_KEY"？

```bash
# 临时设置（仅当前终端有效）
# Windows CMD:     set HY3_API_KEY=你的密钥
# Windows PowerShell: $env:HY3_API_KEY="你的密钥"
# macOS/Linux:     export HY3_API_KEY=你的密钥

# 或创建 .env 文件永久生效
echo HY3_API_KEY=你的密钥 > .env    # Windows
echo "HY3_API_KEY=你的密钥" > .env  # macOS/Linux
```

### Q: 如何为其他 LLM 客户端提供 Hy3 能力？

使用项目自带的 MCP Server：

```bash
cd hy3-mcp-server
pip install -e .
# 然后在 Claude Desktop / Cursor 中配置 hy3-mcp 命令
```

## 三大功能

### 🔬 深度研究 (Deep Research)

输入研究主题，Hy3 将自动完成：

1. **研究规划** — 将主题拆解为子问题，生成搜索关键词
2. **资料搜索** — 自动搜索相关网页资料
3. **报告撰写** — 基于搜索结果生成 1500-3000 字专业研究报告
4. **执行摘要** — 提炼核心发现的简明摘要

### 💻 代码分析 (Code Analysis)

粘贴代码或上传代码文件，Hy3 将提供：

- 代码概览与核心功能解读
- 执行逻辑与关键流程分析
- 潜在 Bug、性能隐患、安全问题诊断
- 具体优化建议与最佳实践
- 1-10 分代码质量评分

### 📚 文档问答 (Document Q&A)

上传多个文档（支持 PDF、DOCX、TXT、代码文件等），向 Hy3 提问：

- 基于文档内容精准回答
- 引用原始段落作为证据
- 明确标注信息缺失情况

## API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 前端页面 |
| `/health` | GET | 服务健康检查 |
| `/api/research` | POST | 深度研究（流式） |
| `/api/analyze-code` | POST | 粘贴代码分析（流式） |
| `/api/analyze-code-file` | POST | 上传代码文件分析（流式） |
| `/api/qa-documents` | POST | 多文档问答（流式） |

所有智能端点均使用 Server-Sent Events (SSE) 实现流式输出，支持前端实时渲染。

## 技术栈

- **后端**: FastAPI + OpenAI SDK + Uvicorn
- **前端**: 原生 HTML/CSS/JS + marked.js（Markdown 渲染）
- **模型**: 腾讯混元 Hy3（通过 OpenAI 兼容接口调用）
- **工具**: DuckDuckGo 网页搜索、PyPDF2、python-docx

## CodeBuddy 协作说明

本项目借助 CodeBuddy AI 编程助手完成：

- **协同设计**：AI 参与整体架构规划、功能模块拆解、前后端交互设计
- **代码生成**：AI 编写了 `backend/main.py`（服务器和所有提示词工程）、`backend/hy3_client.py`（API 客户端封装）、`backend/tools.py`（搜索和文件解析）、`frontend/index.html`（完整前端界面）
- **文档撰写**：AI 生成了 README、配置模板、启动脚本
- **代码审查与打磨**：AI 辅助进行了语法检查、中英文翻译、结构优化

---

## Hy3 MCP Server

`hy3-mcp-server` 是一个独立的 Python 包，将 Hy3 大模型能力封装为 MCP (Model Context Protocol) 工具，让 Claude Desktop、Cursor 等客户端直接调用。

### 安装

```bash
cd hy3-mcp-server
pip install -e .
```

### 配置 Claude Desktop

在 Claude Desktop 的 `claude_desktop_config.json` 中添加：

```json
{
  "mcpServers": {
    "hy3": {
      "command": "hy3-mcp",
      "env": {
        "HY3_API_KEY": "你的API密钥"
      }
    }
  }
}
```

### 提供的工具

| 工具名 | 功能 |
|--------|------|
| `hy3_research` | 深度研究：搜索 + 分析 + 生成报告 |
| `hy3_code_review` | 代码评审：Bug 检测 + 性能分析 + 安全审计 |
| `hy3_doc_qa` | 文档问答：文件解析 + 精准回答 |
| `hy3_data_analyze` | 数据分析：CSV/JSON + 洞察输出 |
| `hy3_chat` | 通用对话：自由问答 |
