# 环境要求与项目结构

> 📖 [返回 README](../README.md)

---

## 硬件要求

| 项目 | 最低配置 | 推荐配置 |
|------|---------|---------|
| CPU | 任意双核处理器 | 四核及以上 |
| 内存 | 512 MB | 1 GB+ |
| 磁盘 | 200 MB | 500 MB+ |
| GPU | **不需要** | **不需要** |
| 网络 | 宽带连接 | 稳定宽带 |

> **重要说明：本项目不需要 GPU 或 CUDA。**
> 所有 AI 推理任务均通过 HTTP 调用腾讯混元 Hy3 云端 API 完成，不涉及本地模型加载、推理或训练。
> 如果你的目标是**本地运行/微调 Hy3 模型本身**，请参考 [本地运行 Hy3 模型指南](local-hy3-model.md)。

## 软件要求

| 依赖 | 版本要求 | 说明 |
|------|---------|------|
| Python | **3.9+**（主项目）/ **3.10+**（MCP Server） | 推荐 3.11 |
| pip | 23.0+ | 随 Python 一起安装 |
| 操作系统 | Windows 10+ / macOS 12+ / Linux（任意发行版） | 均支持 |

## 依赖包总览

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

## 预配置文件一览

| 文件 | 说明 | 你需要做什么 |
|------|------|-------------|
| `.env.example` | 环境变量模板 | 复制为 `.env`，填入 `HY3_API_KEY` |
| `backend/requirements.txt` | 11 个轻量依赖 | 无需修改，pip 自动安装 |
| `docker-compose.yml` | Docker 编排文件 | 无需修改，开箱即用 |
| `Dockerfile` | 容器镜像构建文件 | 无需修改 |
| `start.bat` | Windows 双击启动脚本 | 无需修改 |

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
