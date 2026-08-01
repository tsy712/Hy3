# Hy3 MCP Server v2 (Async)

> **版本说明**: 这是 Hy3 MCP Server 的 v2 异步架构版本，与 v1 同步版并存。

## 主要改进 (相比 v1)

| 特性 | v1 (同步) | v2 (异步) |
|------|-----------|-----------|
| **执行模型** | 同步阻塞调用 Hy3 API | 异步 asyncio + httpx AsyncClient |
| **并发能力** | 串行处理，一次一个请求 | 可并发调用，提高吞吐量 |
| **Python 要求** | Python 3.9+ | Python 3.10+ |
| **MCP 工具** | 5 个 Tool | 5 个 Tool (相同功能) |
| **包管理** | 手动 setup.bat | pip install -e . (pyproject.toml) |
| **测试** | 基础测试 | 完整 pytest 测试套件 |

## 项目结构

```
v2-async/
├── src/
│   ├── __init__.py
│   ├── server.py          # 异步 MCP Server (FastMCP)
│   ├── hy3_client.py      # 异步 Hy3 API 客户端 (httpx)
│   └── tools.py           # 异步工具函数
├── configs/
│   └── *.json             # MCP 客户端配置参考
├── tests/                 # pytest 单元测试
│   ├── test_server.py
│   └── test_hy3_client.py
├── pyproject.toml          # pip 安装配置
├── requirements.txt        # Python 依赖
└── README.md
```

## 快速开始

```bash
cd v2-async
pip install -e .

# 设置 API Key
set HY3_API_KEY=你的API密钥  # Windows
# export HY3_API_KEY=你的API密钥  # macOS/Linux

# 运行 MCP Server
hy3-mcp
```

## 技术细节

- **MCP 框架**: Python FastMCP (异步支持)
- **HTTP 客户端**: httpx.AsyncClient
- **Hy3 API**: OpenAI 兼容异步接口
- **传输模式**: stdio (标准 MCP 传输)

## 版本历史

- **v1**: 同步版，适合简单场景，Python 3.9+，更稳定
- **v2**: 异步版，适合高并发场景，Python 3.10+，性能更好

> 📌 **选择建议**: v1 同步版更稳定，兼容性更好，推荐新手使用。v2 异步版适合需要处理大量并发请求的场景。
