# API Reference & Tech Stack

<p align="center">
  <a href="api-reference.md">🇨🇳 中文</a> · <strong>🇺🇸 English</strong> · <a href="../README_EN.md">⬅ Back to README</a>
</p>

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Frontend page |
| `/health` | GET | Service health check |
| `/api/research` | POST | Deep research (streaming) |
| `/api/analyze-code` | POST | Paste code analysis (streaming) |
| `/api/analyze-code-file` | POST | Upload code file analysis (streaming) |
| `/api/qa-documents` | POST | Multi-document Q&A (streaming) |

All intelligent endpoints use **Server-Sent Events (SSE)** for streaming output, supporting real-time frontend rendering.

### Health Check Example

```bash
curl http://localhost:8000/health
# Expected output: {"status":"healthy","hy3_connected":true}
```

## Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `HY3_API_KEY` | Hy3 API key | - | ✅ |
| `HY3_BASE_URL` | API endpoint | `https://api.hunyuan.cloud.tencent.com/v1` | - |
| `HY3_MODEL` | Model name | `hunyuan-pro` | - |
| `PORT` | Service port | `8000` | - |

## Tech Stack

- **Backend**: FastAPI + OpenAI SDK + Uvicorn
- **Frontend**: Vanilla HTML/CSS/JS + marked.js (Markdown rendering)
- **Model**: Tencent Hunyuan Hy3 (via OpenAI-compatible interface)
- **Tools**: DuckDuckGo web search, PyPDF2, python-docx
