"""
Hy3 MCP Server 的 API 客户端
与主项目的 hy3_client.py 类似，但增加 web_search 能力
"""

import os
import logging
from typing import Optional

from openai import AsyncOpenAI
import httpx

logger = logging.getLogger(__name__)


class Hy3MCPClient:
    """Hy3 API 客户端（MCP Server 专用）"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
    ):
        self.api_key = api_key or os.getenv("HY3_API_KEY", "")
        self.base_url = base_url or os.getenv("HY3_BASE_URL", "https://api.hunyuan.cloud.tencent.com/v1")
        self.model = model or os.getenv("HY3_MODEL", "hunyuan-pro")

        self.client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)
        logger.info("Hy3 MCP 客户端初始化: 模型=%s 端点=%s", self.model, self.base_url)

    async def chat(self, messages: list[dict], temperature: float = 0.7, max_tokens: int = 4096, **kwargs):
        """调用 Hy3 API 对话接口"""
        if not self.api_key:
            raise ValueError("未设置 HY3_API_KEY")

        resp = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )
        return resp

    async def agenerate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 4096) -> str:
        """发送单条消息并返回文本"""
        messages = [{"role": "user", "content": prompt}]
        resp = await self.chat(messages, temperature=temperature, max_tokens=max_tokens)
        return resp.choices[0].message.content or ""

    async def web_search(self, query: str, num_results: int = 5) -> str:
        """执行网页搜索并返回格式化结果"""
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.get(
                    "https://html.duckduckgo.com/html/",
                    params={"q": query},
                    headers={"User-Agent": "Mozilla/5.0 (compatible; Hy3MCP/1.0)"},
                )
                if resp.status_code != 200:
                    return f"搜索失败: HTTP {resp.status_code}"

                from bs4 import BeautifulSoup
                soup = BeautifulSoup(resp.text, "html.parser")
                results = []
                for block in soup.find_all("div", class_="result")[:num_results]:
                    link_el = block.find("a", class_="result__a")
                    title = link_el.get_text(strip=True) if link_el else "(无标题)"
                    snippet_el = block.find("a", class_="result__snippet")
                    snippet = snippet_el.get_text(strip=True) if snippet_el else ""
                    results.append(f"- **{title}**: {snippet}")

                return "\n".join(results) if results else "无相关搜索结果"
        except Exception as e:
            logger.error("搜索异常: %s", e)
            return f"搜索出错: {e}"
