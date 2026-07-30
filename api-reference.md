# API Reference & Tech Stack / API 参考与技术栈

> 📖 [Back to README / 返回 README](../README.md)

---

## API Endpoints / API 端点

| Endpoint / 端点 | Method / 方法 | Description / 说明 |
|------|------|------|
| `/` | GET | Frontend page / 前端页面 |
| `/health` | GET | Service health check / 服务健康检查 |
| `/api/research` | POST | Deep Research (streaming) / 深度研究（流式） |
| `/api/analyze-code` | POST | Paste code analysis (streaming) / 粘贴代码分析（流式） |
| `/api/analyze-code-file` | POST | Upload code file analysis (streaming) / 上传代码文件分析（流式） |
| `/api/qa-documents` | POST | Multi-document Q&A (streaming) / 多文档问答（流式） |

All intelligent endpoints use **Server-Sent Events (SSE)** for streaming output, with real-time frontend rendering.  
所有智能端点均使用 **Server-Sent Events (SSE)** 实现流式输出，支持前端实时渲染。

### Health Check Example / 健康检查示例

```bash
curl http://localhost:8000/health
# Expected output / 预期输出: {"status":"healthy","hy3_connected":true}
```

## Environment Variable Reference / 环境变量参考

| Variable / 变量名 | Description / 说明 | Default / 默认值 | Required / 必填 |
|--------|------|--------|------|
| `HY3_API_KEY` | Hy3 API key / Hy3 API 密钥 | - | ✅ |
| `HY3_BASE_URL` | API endpoint / API 端点地址 | `https://api.hunyuan.cloud.tencent.com/v1` | - |
| `HY3_MODEL` | Model name / 模型名称 | `hunyuan-pro` | - |
| `PORT` | Server port / 服务端口 | `8000` | - |

## Tech Stack / 技术栈

- **Backend / 后端**: FastAPI + OpenAI SDK + Uvicorn
- **Frontend / 前端**: Vanilla HTML/CSS/JS + marked.js (Markdown rendering / Markdown 渲染)
- **Model / 模型**: Tencent Hunyuan Hy3 (via OpenAI-compatible API / 通过 OpenAI 兼容接口调用)
- **Tools / 工具**: DuckDuckGo web search, PyPDF2, python-docx / DuckDuckGo 网页搜索、PyPDF2、python-docx
