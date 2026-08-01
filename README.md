# Hy3 MCP Server

封装腾讯混元 Hy3 大模型能力的 MCP 工具集，一键安装、即插即用到任何支持 MCP 的 AI 客户端。

---

## 快速安装

### Windows
```bat
install.bat
```

### Linux/macOS
```bash
chmod +x install.sh && ./install.sh
```

### 手动安装
```bash
pip install -e .
```

### 设置 API Key

复制并编辑 `.env` 文件：
```bash
cp ../.env.example .env
# 编辑 .env，填入 HY3_API_KEY
```

---

## MCP 工具

| 工具 | 功能 |
|------|------|
| `hy3_chat` | Hy3 大模型对话 |
| `hy3_search` | 互联网搜索 (DuckDuckGo) |
| `hy3_fetch_web` | 网页内容抓取 |
| `hy3_code_review` | 代码审查 (5维度) |
| `hy3_parse_file` | 文件解析 (PDF/DOCX/TXT) |
| `hy3_execute_code` | 安全 Python 代码执行 |
| `hy3_embed` | 文本向量化 |

---

## 客户端配置

### CodeBuddy
复制 `configs/codebuddy-mcp.json` 配置到 CodeBuddy MCP 设置。

### Claude Desktop
复制 `configs/claude-desktop-mcp.json` 配置到 `claude_desktop_config.json`。

### Cursor
复制 `configs/cursor-mcp.json` 配置到 Cursor MCP 设置。

---

## 手动测试
```bash
python -m src.server
```
