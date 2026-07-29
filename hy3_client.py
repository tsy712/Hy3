"""
Hy3 MCP Server — Hy3 API 客户端

基于 OpenAI 兼容接口调用腾讯混元 Hy3 大模型。
"""

import os
import asyncio
from typing import Optional

import httpx
from openai import AsyncOpenAI


class Hy3MCPClient:
    """Hy3 API 异步客户端（用于 MCP Server）"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
    ):
        self.api_key = api_key or os.getenv("HY3_API_KEY")
        self.base_url = base_url or os.getenv(
            "HY3_BASE_URL", "https://api.hunyuan.cloud.tencent.com/v1"
        )
        self.model = model or os.getenv("HY3_MODEL", "hunyuan-pro")

        if not self.api_key:
            raise ValueError(
                "HY3_API_KEY 未设置。请设置环境变量或在 .env 文件中配置。"
            )

        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

    async def chat(self, message: str, temperature: float = 0.7) -> str:
        """通用对话"""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": message}],
            temperature=temperature,
            max_tokens=4096,
        )
        return response.choices[0].message.content

    async def deep_research(
        self,
        topic: str,
        search_results: list[str],
    ) -> str:
        """深度研究"""
        context = "\n".join(search_results)

        system_prompt = (
            "你是一个专业的研究助手。基于提供的搜索资料生成深度研究报告。\n"
            "格式：\n"
            "## 概述\n## 关键发现\n## 多角度分析\n## 结论与建议\n"
            "请引用来源编号，保持客观中立。"
        )

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"主题：{topic}\n\n资料：\n{context}"},
            ],
            temperature=0.5,
            max_tokens=8192,
        )
        return response.choices[0].message.content

    async def code_review(self, code: str, language: str = "") -> str:
        """代码审查"""
        lang_hint = f"（语言：{language}）" if language else ""
        system_prompt = (
            "你是一个资深代码审查专家。请从以下维度分析：\n"
            "1. Bug 检测\n2. 性能分析\n3. 安全审计\n4. 代码质量\n5. 改进建议\n"
            "要求：具体、建设性。"
        )

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"审查以下代码{lang_hint}：\n\n```\n{code}\n```"},
            ],
            temperature=0.3,
            max_tokens=8192,
        )
        return response.choices[0].message.content

    async def doc_qa(
        self,
        question: str,
        doc_content: str,
        doc_name: str = "",
    ) -> str:
        """文档问答"""
        name_hint = f'"{doc_name}"' if doc_name else "上传的文档"
        system_prompt = (
            "你是一个文档分析助手。基于提供的文档内容回答问题。\n"
            "如果答案在文档中，请引用原文。如果不在，请诚实说明。"
        )

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": (
                        f"文档：{name_hint}\n"
                        f"内容：\n{doc_content}\n\n"
                        f"问题：{question}"
                    ),
                },
            ],
            temperature=0.3,
            max_tokens=4096,
        )
        return response.choices[0].message.content


async def search_duckduckgo(query: str, max_results: int = 8) -> list[dict]:
    """
    DuckDuckGo 搜索（异步）
    
    双层降级：Instant Answer API → HTML 搜索结果页
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    results = []

    async with httpx.AsyncClient(timeout=15.0, headers=headers) as client:
        # 第一层：Instant Answer API
        try:
            api_url = "https://api.duckduckgo.com/"
            params = {"q": query, "format": "json", "no_html": 1, "skip_disambig": 1}
            resp = await client.get(api_url, params=params)
            resp.raise_for_status()
            data = resp.json()

            if data.get("AbstractText"):
                results.append({
                    "title": data.get("Heading", query),
                    "snippet": data["AbstractText"],
                    "url": data.get("AbstractURL", ""),
                })

            for topic in data.get("RelatedTopics", []):
                if topic.get("Text") and not topic.get("Topics"):
                    results.append({
                        "title": topic.get("FirstURL", ""),
                        "snippet": topic.get("Text", ""),
                        "url": topic.get("FirstURL", ""),
                    })
        except Exception:
            pass

        # 第二层：HTML 搜索
        if len(results) < max_results:
            try:
                html_url = f"https://html.duckduckgo.com/html/?q={query}"
                resp = await client.get(html_url)
                resp.raise_for_status()

                from bs4 import BeautifulSoup
                soup = BeautifulSoup(resp.text, "lxml")

                for item in soup.select(".result")[: max_results - len(results)]:
                    title_el = item.select_one(".result__title a")
                    snippet_el = item.select_one(".result__snippet")
                    if title_el and snippet_el:
                        results.append({
                            "title": title_el.get_text(strip=True),
                            "snippet": snippet_el.get_text(strip=True),
                            "url": "",
                        })
            except Exception:
                pass

    return results[:max_results]
