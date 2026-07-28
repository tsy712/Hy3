# Hy3 MCP Server

> 📖 [返回 README](../README.md)

---

`hy3-mcp-server` 是一个独立的 Python 包，将 Hy3 大模型能力封装为 MCP (Model Context Protocol) 工具，让 Claude Desktop、Cursor 等客户端直接调用。

## 安装

```bash
cd hy3-mcp-server
pip install -e .
```

## 配置 Claude Desktop

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

## 提供的工具

| 工具名 | 功能 |
|--------|------|
| `hy3_research` | 深度研究：搜索 + 分析 + 生成报告 |
| `hy3_code_review` | 代码评审：Bug 检测 + 性能分析 + 安全审计 |
| `hy3_doc_qa` | 文档问答：文件解析 + 精准回答 |
| `hy3_data_analyze` | 数据分析：CSV/JSON + 洞察输出 |
| `hy3_chat` | 通用对话：自由问答 |
