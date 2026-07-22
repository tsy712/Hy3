# Hy3 研究助手

> 基于 **腾讯混元 Hy3**（295B MoE 模型）的端到端研究助手应用。
>
> 🏷️ 腾讯犀牛鸟开源人才培养计划 2026 · Issue [#4](https://github.com/Tencent-Hunyuan/Hy3/issues/4)

---

## 项目概述

Hy3 研究助手是一个全栈 Web 应用，展示了 **Hy3 在实际场景中的强大能力**：

| 功能 | 描述 | Hy3 扮演的角色 |
|------|------|---------------|
| 🔬 **深度研究** | 规划 → 搜索 → 长文报告（带引用来源） | 规划智能体、信息综合、报告撰写 |
| 💻 **代码分析** | Bug 检测、性能优化、代码解释 | 代码理解、逻辑分析、重构建议 |
| 📄 **文档问答** | 多文档上传与智能问答 | 阅读理解、基于证据的回答 |

所有 LLM 能力**完全通过 Hy3 API 实现**——无需训练、微调或本地推理。

---

## 演示流程

### 演示一：「MoE 架构效率」深度研究

1. 输入主题：「MoE 架构对 LLM 推理效率的影响」
2. Hy3 生成包含 4 个关键问题和搜索查询的研究计划
3. 系统执行网页搜索并收集来源
4. Hy3 撰写带有引用标注（[来源 1], [来源 2], ...）的全面报告
5. 生成中英文双语执行摘要

### 演示二：技术论文多文档问答

1. 上传 2-3 个技术 PDF/TXT 文件
2. 提问：「比较这些文档中描述的方法，关键区别是什么？」
3. Hy3 读取所有文档并提供跨文档的综合分析

---

## 架构

```
hy3-research-assistant/
├── backend/
│   ├── main.py            # FastAPI 服务器（6 个 API 端点）
│   ├── hy3_client.py      # Hy3 API 客户端（OpenAI 兼容）
│   ├── tools.py            # 网页搜索、文件解析工具
│   └── requirements.txt   # Python 依赖
├── frontend/
│   └── index.html          # 现代化单页应用（纯 HTML/CSS/JS）
├── .env.example            # 环境变量模板
└── README.md               # 项目文档
```

**技术栈：**
- **后端**：Python 3.10+ · FastAPI · OpenAI SDK（Hy3 兼容）
- **前端**：纯 HTML5/CSS3/JavaScript（零依赖）
- **大模型**：腾讯混元 Hy3（295B MoE，21B 活跃参数）
- **搜索**：DuckDuckGo（无需 API 密钥）
- **文件解析**：PyPDF2、python-docx

---

## 快速开始

### 前提条件

- Python 3.10+
- 从 [腾讯云控制台](https://console.cloud.tencent.com/hunyuan) 获取 Hy3 API 密钥

### 安装运行

```bash
# 1. 进入项目目录
cd hy3-research-assistant

# 2. 设置 Hy3 API 密钥
export HY3_API_KEY="你的 API 密钥"

# Windows 系统使用:
set HY3_API_KEY=你的 API 密钥

# 3. 安装依赖
cd backend
pip install -r requirements.txt

# 4. 启动服务器
python main.py
```

在浏览器中访问 http://localhost:8000 即可使用。

### API 端点

| 方法 | 端点 | 描述 |
|------|------|------|
| `GET` | `/api/health` | 健康检查 |
| `POST` | `/api/research` | 深度研究（完整版） |
| `POST` | `/api/research/stream` | 深度研究（流式 SSE） |
| `POST` | `/api/analyze-code` | 代码分析 |
| `POST` | `/api/upload-documents` | 上传文档 |
| `POST` | `/api/qa` | 文档问答 |

---

## Hy3 API 配置

Hy3 提供了 **OpenAI 兼容的 API**。本项目使用标准的 `openai` Python SDK 配合 Hy3 的接口地址：

```python
from openai import OpenAI

client = OpenAI(
    api_key="你的 Hy3 API 密钥",
    base_url="https://api.hunyuan.cloud.tencent.com/v1",
)

response = client.chat.completions.create(
    model="hunyuan-hy3-295b-a21b",
    messages=[{"role": "user", "content": "你好！"}],
)
```

环境变量说明：
- `HY3_API_KEY` — 腾讯云 API 密钥 **（必填）**
- `HY3_BASE_URL` — API 基础地址（默认：`https://api.hunyuan.cloud.tencent.com/v1`）
- `HY3_MODEL` — 模型名称（默认：`hunyuan-hy3-295b-a21b`）

---

## 开发说明

### CodeBuddy 协作

本项目使用 **CodeBuddy** 作为主要开发环境。以下是由 CodeBuddy 生成或大幅协助完成的代码模块：

| 文件 | CodeBuddy 贡献 |
|------|---------------|
| `backend/hy3_client.py` | 完整文件 — Hy3 API 客户端封装，含流式支持 |
| `backend/tools.py` | 完整文件 — 网页搜索爬虫、多格式文件解析器 |
| `backend/main.py` | 完整文件 — FastAPI 服务器及所有端点（含流式） |
| `frontend/index.html` | 完整文件 — 单页应用（暗色主题、SSE 流式、Markdown 渲染） |
| `README.md` | 完整文件 — 项目文档和配置指南 |

开发者的主要工作：
- 设计应用架构
- 选择技术栈
- 配置 Hy3 API 凭证
- 测试和迭代提示词工程
- 制作演示录屏

### 提示词工程

系统使用精心设计的提示词来最大化 Hy3 的能力：

1. **研究规划器**：结构化 JSON 输出，用于制定研究计划
2. **研究报告撰写器**：学术风格的写作，带来源引用
3. **代码分析器**：领域专用分析（Bug 检测/优化/解释）
4. **文档问答器**：基于证据的回答，支持段落引用

---

## 许可证

MIT License — 模型许可参见 [Hy3 仓库](https://github.com/Tencent-Hunyuan/Hy3)

---

## 致谢

- [腾讯混元 Hy3](https://github.com/Tencent-Hunyuan/Hy3) — 驱动本应用的 295B MoE 模型
- 腾讯犀牛鸟开源人才培养计划 2026
- 使用 [CodeBuddy](https://www.codebuddy.ai/) 构建
