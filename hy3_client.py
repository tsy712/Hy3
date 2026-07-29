"""
Hy3 API Client — OpenAI-compatible interface wrapper.
Calls Hunyuan large language model via custom base_url pointing to Hy3 endpoint, using OpenAI SDK.
"""

import os
import json
import logging
from typing import Optional, AsyncGenerator, Dict, Any

from openai import AsyncOpenAI

logger = logging.getLogger(__name__)


class Hy3Error(Exception):
    """Hy3 client exception"""
    pass


class Hy3Client:
    """OpenAI-compatible client wrapper for Hunyuan Hy3 model"""

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
            logger.warning("HY3_API_KEY not set! Please set the environment variable or configure in .env file")

        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )
        logger.info("Hy3 client initialized, model: %s, endpoint: %s", self.model, self.base_url)

    async def chat(
        self,
        messages: list[Dict[str, Any]],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False,
        **kwargs,
    ):
        """
        Universal chat interface, compatible with OpenAI chat/completions.
        Returns full response or streaming generator.
        """
        if not self.api_key:
            raise ValueError("HY3_API_KEY not set. Please configure in .env file or environment variable")

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
        Convenience method: sends a single user message and returns the complete text.
        Used for non-streaming scenarios like research planning and search.
        """
        messages = [self.build_message("user", prompt)]
        if stream := kwargs.pop("stream", None):
            pass  # ignored, agenerate is always non-streaming
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
        Streaming chat interface — returns content token by token for real-time frontend display.
        """
        if not self.api_key:
            yield f"\n\n> ⚠️ Error: HY3_API_KEY not set. Please configure in .env file or environment variable"
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
                error_msg = "API Key authentication failed (401). Please check if HY3_API_KEY is correct"
            elif "429" in error_msg or "Rate limit" in error_msg:
                error_msg = "API rate limit exceeded (429). Please try again later"
            elif "timeout" in error_msg.lower():
                error_msg = "Request timeout. Please check network connection"
            logger.error("Hy3 streaming call failed: %s", e)
            yield f"\n\n> ❌ Error: {error_msg}"

    @staticmethod
    def build_message(role: str, content: str) -> Dict[str, str]:
        """Construct a single message"""
        return {"role": role, "content": content}


# Global singleton
_hy3_client: Optional[Hy3Client] = None


def get_hy3_client() -> Hy3Client:
    """Get the global Hy3 client singleton"""
    global _hy3_client
    if _hy3_client is None:
        _hy3_client = Hy3Client()
    return _hy3_client
