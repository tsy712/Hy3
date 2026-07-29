"""
Hy3 API Client — OpenAI-compatible interface wrapper.
/ Hy3 API 客户端 —— 基于 OpenAI 兼容接口封装

Points base_url to the Hy3 endpoint and uses the OpenAI SDK to call the Hunyuan model.
/ 通过自定义 base_url 指向 Hy3 端点，使用 OpenAI SDK 调用混元大模型。
"""

import os
import json
import logging
from typing import Optional, AsyncGenerator, Dict, Any

from openai import AsyncOpenAI

logger = logging.getLogger(__name__)


class Hy3Client:
    """OpenAI-compatible client wrapper for the Hunyuan Hy3 model.
    / 混元 Hy3 模型的 OpenAI 兼容客户端封装"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
    ):
        self.api_key = api_key or os.getenv("HY3_API_KEY", "")
        self.base_url = base_url or os.getenv("HY3_BASE_URL", "https://api.hunyuan.cloud.tencent.com/v1")
        self.model = model or os.getenv("HY3_MODEL", "hunyuan-pro")

        if not self.api_key:
            logger.warning("⚠️ HY3_API_KEY is not set! / HY3_API_KEY 未设置！"
                           "Please configure via environment variable or .env file / 请设置环境变量或在 .env 文件中配置")

        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )
        logger.info("Hy3 client initialized, model: %s, endpoint: %s / Hy3 客户端已初始化，模型: %s，端点: %s",
                    self.model, self.base_url)

    async def chat(
        self,
        messages: list[Dict[str, Any]],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False,
        **kwargs,
    ):
        """
        General-purpose chat endpoint, OpenAI chat/completions compatible.
        / 通用对话接口，兼容 OpenAI chat/completions。

        Returns a full response or a streaming generator.
        / 返回完整响应或流式生成器。
        """
        if not self.api_key:
            raise ValueError(
                "HY3_API_KEY is not set — configure in .env file or environment variable. "
                "/ HY3_API_KEY 未设置，请在 .env 文件或环境变量中配置"
            )

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream,
            **kwargs,
        )
        return response

    async def agenerate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 4096, **kwargs) -> str:
        """
        Convenience method: send a single user message and return full text.
        / 便捷方法：发送单条 user 消息并返回完整文本。

        Used for research planning, search and other non-streaming scenarios.
        / 用于研究规划、搜索等非流式场景。
        """
        messages = [self.build_message("user", prompt)]
        response = await self.chat(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=False,
            **kwargs,
        )
        return response.choices[0].message.content or ""

    async def chat_stream(
        self,
        messages: list[Dict[str, Any]],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs,
    ) -> AsyncGenerator[str, None]:
        """
        Streaming chat endpoint — yields tokens one by one for real-time frontend display.
        / 流式对话接口 —— 逐 token 返回内容，用于实时前端展示。
        """
        if not self.api_key:
            yield (
                "\n\n> ⚠️ Error: HY3_API_KEY is not set — configure in .env file or environment variable. "
                "/ ⚠️ 错误：HY3_API_KEY 未设置，请在 .env 文件或环境变量中配置"
            )
            return

        try:
            stream_resp = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
                **kwargs,
            )
            async for chunk in stream_resp:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "Unauthorized" in error_msg:
                error_msg = (
                    "API Key authentication failed (401) — check HY3_API_KEY. "
                    "/ API Key 认证失败（401），请检查 HY3_API_KEY 是否正确"
                )
            elif "429" in error_msg or "Rate limit" in error_msg:
                error_msg = (
                    "API rate limit exceeded (429) — please retry later. "
                    "/ API 请求频率过高（429），请稍后重试"
                )
            elif "timeout" in error_msg.lower():
                error_msg = "Request timed out — check network connection. / 请求超时，请检查网络连接"
            logger.error("Hy3 streaming call failed / Hy3 流式调用失败: %s", e)
            yield f"\n\n> ❌ Error: {error_msg} / ❌ 错误：{error_msg}"

    @staticmethod
    def build_message(role: str, content: str) -> Dict[str, str]:
        """Build a single chat message. / 构造单条消息"""
        return {"role": role, "content": content}


# Global singleton / 全局单例
_hy3_client: Optional[Hy3Client] = None


def get_hy3_client() -> Hy3Client:
    """Get the global Hy3 client singleton. / 获取全局 Hy3 客户端单例"""
    global _hy3_client
    if _hy3_client is None:
        _hy3_client = Hy3Client()
    return _hy3_client
