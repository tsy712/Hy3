# Hy3 Research Assistant

基于腾讯混元 **Hy3** 大模型的智能研究助手，提供 **深度研究**、**代码分析**、**文档问答** 三大核心能力。

## 项目定位

这是一个 **Hy3 的上层应用项目**，通过 HTTP API 调用腾讯混元 Hy3 大模型——不需要 GPU、不需要 CUDA、不需要下载模型权重。

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

### 1. 环境要求

- **Python 3.10+**
- **Windows / macOS / Linux**（无需 GPU、无需 CUDA）
- **Hy3 API Key**（从腾讯混元平台申请）

### 2. 安装

```bash
# 克隆仓库
git clone <this-repo>
cd hy3-research-assistant

# 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 安装主项目（pip install -e .）
pip install -e .
```

### 3. 配置

```bash
# 复制环境变量模板
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux

# 编辑 .env，填入你的 API Key
```

`.env` 示例：

```env
HY3_API_KEY=sk-your-api-key-here
HY3_BASE_URL=https://api.hunyuan.cloud.tencent.com/v1
HY3_MODEL=hunyuan-pro
PORT=8000
```

### 4. 启动

**方式一：一键启动（Windows）**

```bash
start.bat
```

**方式二：命令行启动**

```bash
# 启动 Web 服务（API + 前端）
hy3-research

# 或直接运行
python backend/main.py
```

### 5. 使用

- **Web 界面**：打开浏览器访问 http://localhost:8000
- **API 文档**：http://localhost:8000/docs
- **CLI 模式**：`hy3-research --cli`

## 核心功能

### 1. 深度研究 (Deep Research)

输入研究主题，自动执行多角度搜索 + Hy3 AI 分析 → 输出结构化研究报告。

### 2. 代码分析 (Code Review)

上传代码文件 / 粘贴代码片段，Hy3 进行多维度代码审查：
- Bug 检测
- 性能分析
- 安全审计
- 代码质量评分

### 3. 文档问答 (Document Q&A)

上传文档文件（PDF / DOCX / TXT / MD），基于文档内容精准备答。

## 项目结构

```
hy3-research-assistant/
├── backend/
│   ├── __init__.py        # 包信息
│   ├── main.py            # FastAPI 主应用
│   ├── hy3_client.py      # Hy3 API 客户端
│   ├── tools.py           # 工具函数（搜索、文件解析）
│   ├── cli.py             # 命令行入口
│   └── requirements.txt   # Python 依赖
├── frontend/
│   └── index.html         # Web 前端界面
├── hy3-mcp-server/        # MCP Server 子项目
├── pyproject.toml          # 主项目配置
├── start.bat               # Windows 一键启动
├── .env.example            # 环境变量模板
└── README.md
```

## 子项目：Hy3 MCP Server

本项目包含一个独立的 **MCP Server** 子项目，可将 Hy3 大模型接入 Claude Desktop / Cursor / CodeBuddy 等 MCP 客户端。

详见 [`hy3-mcp-server/README.md`](hy3-mcp-server/README.md)。

## 依赖说明

主项目依赖轻量级 Web 框架和 API 客户端库：

| 库 | 版本 | 用途 |
|----|------|------|
| FastAPI | 0.115.x | Web API 框架 |
| Uvicorn | 0.34.x | ASGI 服务器 |
| OpenAI SDK | 1.58.x | Hy3 API 调用（OpenAI 兼容） |
| httpx | 0.28.x | HTTP 客户端（搜索请求） |
| PyPDF2 | 3.0.x | PDF 解析 |
| python-docx | 1.1.x | DOCX 解析 |
| beautifulsoup4 | 4.12.x | HTML 解析 |

> **不需要**: `torch`、`transformers`、`deepspeed`、`flash-attn` 等 GPU/训练相关依赖。

## API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | Web 前端界面 |
| POST | `/api/research` | 深度研究 |
| POST | `/api/code-review` | 代码分析 |
| POST | `/api/doc-qa` | 文档问答 |
| POST | `/api/chat` | 通用对话 |
| GET | `/docs` | Swagger API 文档 |

## FAQ

### Q: 和 Hy3 官方仓库的 requirements.txt 有何区别？

Hy3 官方仓库包含模型训练/微调依赖（`torch`、`transformers`、`deepspeed`、`flash-attn` 等），需要 NVIDIA GPU + CUDA。本项目是 Hy3 的上层应用，只依赖 Web 框架和 HTTP 客户端，**两者互不冲突**。

### Q: 我想本地运行 Hy3 模型，有什么坑？

请完整阅读上方的 **⚠️ 风险提示** 章节。核心要点：
- `deepspeed` + `flash-attn` 安装极其容易失败，必须按 Torch→CUDA→Deepspeed→Flash-Attn 的顺序精确匹配版本
- 需要 NVIDIA GPU ≥ 24 GB 显存 + 32 GB 系统内存（编译 flash-attn）
- 强烈建议用 Docker 部署而非手动编译
- 如果你用的是普通笔记本（集成显卡或 < 8GB 显存），请放弃本地运行，使用本应用的云端 API 模式即可

### Q: API Key 从哪里获取？

从腾讯混元大模型平台申请。具体流程请参考腾讯云官方文档。

## 技术栈

- **后端**: FastAPI (Python)
- **前端**: 原生 HTML/CSS/JS（单文件 SPA）
- **AI 推理**: 腾讯混元 Hy3（OpenAI 兼容接口）
- **搜索**: DuckDuckGo（双层搜索降级）
- **MCP**: FastMCP（子项目）

## 许可证

MIT License
