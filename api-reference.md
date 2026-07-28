# API 参考与技术栈

> 📖 [返回 README](../README.md)

---

## API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 前端页面 |
| `/health` | GET | 服务健康检查 |
| `/api/research` | POST | 深度研究（流式） |
| `/api/analyze-code` | POST | 粘贴代码分析（流式） |
| `/api/analyze-code-file` | POST | 上传代码文件分析（流式） |
| `/api/qa-documents` | POST | 多文档问答（流式） |

所有智能端点均使用 **Server-Sent Events (SSE)** 实现流式输出，支持前端实时渲染。

### 健康检查示例

```bash
curl http://localhost:8000/health
# 预期输出: {"status":"healthy","hy3_connected":true}
```

## 环境变量参考

| 变量名 | 说明 | 默认值 | 必填 |
|--------|------|--------|------|
| `HY3_API_KEY` | Hy3 API 密钥 | - | ✅ |
| `HY3_BASE_URL` | API 端点地址 | `https://api.hunyuan.cloud.tencent.com/v1` | - |
| `HY3_MODEL` | 模型名称 | `hunyuan-pro` | - |
| `PORT` | 服务端口 | `8000` | - |

## 技术栈

- **后端**: FastAPI + OpenAI SDK + Uvicorn
- **前端**: 原生 HTML/CSS/JS + marked.js（Markdown 渲染）
- **模型**: 腾讯混元 Hy3（通过 OpenAI 兼容接口调用）
- **工具**: DuckDuckGo 网页搜索、PyPDF2、python-docx
