"""
Hy3 MCP Server — FastMCP 服务端

通过 MCP 协议将腾讯混元 Hy3 大模型的对话能力暴露给
Claude Desktop / Cursor / CodeBuddy 等 MCP 客户端使用。

工具列表:
  - hy3_chat: 通用对话
  - hy3_research: 深度研究（搜索+分析）
  - hy3_code_review: 代码审查
  - hy3_doc_qa: 文档问答
"""

import sys
import os
from pathlib import Path

# 路径设置
sys.path.insert(0, str(Path(__file__).parent))

from fastmcp import FastMCP
from hy3_client import Hy3MCPClient, search_duckduckgo

# 初始化 MCP 服务
mcp = FastMCP(
    name="Hy3 MCP Server",
    description="基于腾讯混元 Hy3 大模型的 MCP 服务——研究、代码分析、文档问答",
    version="1.0.0",
)

# Hy3 客户端（延迟初始化）
_hy3_client = None


def get_client():
    """获取或创建 Hy3 客户端实例"""
    global _hy3_client
    if _hy3_client is None:
        _hy3_client = Hy3MCPClient()
    return _hy3_client


# ==================== MCP Tools ====================


@mcp.tool()
async def hy3_chat(message: str) -> str:
    """
    与腾讯混元 Hy3 大模型进行通用对话。

    Args:
        message: 用户消息内容，可以是任何问题或对话。
        
    Returns:
        Hy3 大模型的回复文本。
    """
    client = get_client()
    return await client.chat(message)


@mcp.tool()
async def hy3_research(topic: str) -> str:
    """
    深度研究：自动搜索相关资料，并由 Hy3 AI 进行分析，生成结构化研究报告。

    Args:
        topic: 研究主题，越具体越好。例如："量子计算最新进展"、"Python 3.12 新特性"。
        
    Returns:
        结构化研究报告（Markdown 格式，包含概述、关键发现、分析和结论）。
    """
    client = get_client()

    # 搜索
    search_results = await search_duckduckgo(topic, max_results=8)
    search_texts = [f"[{i+1}] {r['title']}: {r['snippet']}" for i, r in enumerate(search_results)]

    # AI 分析
    report = await client.deep_research(topic, search_texts)
    return report


@mcp.tool()
async def hy3_code_review(code: str, language: str = "") -> str:
    """
    AI 代码审查：从 Bug 检测、性能、安全、代码质量等多个维度分析代码。

    Args:
        code: 需要审查的代码片段。
        language: 编程语言（选填），如不填则自动检测。
        
    Returns:
        结构化代码审查报告（Markdown 格式）。
    """
    client = get_client()
    return await client.code_review(code, language)


@mcp.tool()
async def hy3_doc_qa(question: str, document: str, doc_name: str = "") -> str:
    """
    基于文档内容进行精准备答。Hy3 会从提供的文档中查找答案。

    Args:
        question: 你要问的问题。
        document: 文档的完整文本内容。
        doc_name: 文档名称（选填）。
        
    Returns:
        基于文档内容的精准回答，如果文档不含相关信息会诚实说明。
    """
    client = get_client()
    return await client.doc_qa(question, document, doc_name)


# ==================== Entry Point ====================


def main():
    """MCP Server 启动入口"""
    import asyncio

    # 检查 API Key
    api_key = os.getenv("HY3_API_KEY")
    if not api_key:
        # 尝试从 .env 文件加载
        dotenv_path = Path(__file__).parent.parent / ".env"
        if dotenv_path.exists():
            try:
                from dotenv import load_dotenv
                load_dotenv(dotenv_path)
            except ImportError:
                pass

        api_key = os.getenv("HY3_API_KEY")
        if not api_key:
            print("[警告] HY3_API_KEY 未设置。请设置环境变量或创建 .env 文件。")
            print("        复制 .env.example -> .env 并填入你的 API 密钥。")

    print("🚀 Hy3 MCP Server 启动中...")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
