"""
Hy3 Research Assistant — FastAPI 主应用

提供 Web 前端界面 + RESTful API 端点。
"""

import os
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

# 确保 backend 在 sys.path 中
sys.path.insert(0, str(Path(__file__).parent))

from hy3_client import Hy3Client
from tools import ToolManager
from cli import router as api_router

app = FastAPI(
    title="Hy3 Research Assistant",
    description="基于腾讯混元 Hy3 大模型的智能研究助手 — 深度研究 · 代码分析 · 文档问答",
    version="1.0.0",
)

# 初始化核心组件
hy3_client = Hy3Client()
tool_manager = ToolManager()

# 注入到路由
app.dependency_overrides = {}  # 后续可注入配置

# 注册 API 路由
app.include_router(api_router)

# 前端静态文件
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")


@app.get("/")
async def root():
    """Web 前端入口"""
    index_path = Path(__file__).parent.parent / "frontend" / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "Hy3 Research Assistant API is running", "docs": "/docs"}


@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "ok", "version": "1.0.0"}


def main():
    """启动入口"""
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
