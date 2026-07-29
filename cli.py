"""
API 路由定义 — 提供 RESTful 端点，连接前端与 Hy3 大模型。
"""

import sys
import os
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel

# 确保 backend 在 sys.path 中
sys.path.insert(0, str(Path(__file__).parent))

from hy3_client import Hy3Client
from tools import ToolManager

router = APIRouter(prefix="/api", tags=["API"])

# ——— 数据模型 ———


class ChatRequest(BaseModel):
    messages: list[dict]
    temperature: float = 0.7
    max_tokens: int = 4096


class ResearchRequest(BaseModel):
    topic: str
    search_depth: int = 10


class CodeReviewRequest(BaseModel):
    code: str
    language: str = ""


class DocQARequest(BaseModel):
    question: str
    doc_content: Optional[str] = None


# ——— 端点 ———


@router.post("/chat")
async def chat(request: ChatRequest):
    """通用对话"""
    try:
        client = Hy3Client()
        result = client.chat_sync(
            messages=request.messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        return {"status": "ok", "content": result}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"API 调用失败: {str(e)}")


@router.post("/research")
async def deep_research(request: ResearchRequest):
    """深度研究：搜索 + AI 分析 → 结构化报告"""
    try:
        # 1. 搜索
        search_results_raw = await ToolManager.duckduckgo_search(
            query=request.topic,
            max_results=request.search_depth,
        )
        search_texts = [
            f"{r['title']}: {r['snippet']}"
            for r in search_results_raw
        ]

        # 2. AI 分析
        client = Hy3Client()
        report = client.deep_research(
            topic=request.topic,
            search_results=search_texts,
        )

        return {
            "status": "ok",
            "topic": request.topic,
            "sources": search_results_raw,
            "report": report,
        }
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"研究失败: {str(e)}")


@router.post("/code-review")
async def code_review(request: CodeReviewRequest):
    """代码分析"""
    try:
        client = Hy3Client()
        result = client.code_review(
            code=request.code,
            language=request.language,
        )
        return {"status": "ok", "review": result}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"代码分析失败: {str(e)}")


@router.post("/doc-qa")
async def doc_qa(
    question: str = Form(...),
    file: Optional[UploadFile] = File(None),
    doc_content: Optional[str] = Form(None),
    doc_name: Optional[str] = Form(None),
):
    """文档问答：支持上传文件或直接粘贴文本"""
    try:
        content = doc_content or ""

        # 如果上传了文件，解析内容
        if file:
            file_bytes = await file.read()
            content = ToolManager.parse_file(
                filename=file.filename or "unknown",
                file_bytes=file_bytes,
            )
            doc_name = doc_name or file.filename

        if not content:
            raise HTTPException(status_code=400, detail="请提供文档内容或上传文件")

        client = Hy3Client()
        answer = client.doc_qa(
            question=question,
            doc_content=content,
            doc_name=doc_name or "",
        )

        return {"status": "ok", "answer": answer, "doc_name": doc_name}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文档问答失败: {str(e)}")


# ——— CLI 入口 ———


def main():
    """CLI 启动入口"""
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
