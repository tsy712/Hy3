"""
Hy3 API 客户端 — 基于 OpenAI 兼容接口调用腾讯混元 Hy3 大模型。

支持：
- 通用对话 (chat)
- 深度研究 (deep_research) — 搜索 + AI 分析
- 代码审查 (code_review)
- 文档问答 (doc_qa)
"""

import os
from typing import Optional, Generator

from openai import OpenAI


class Hy3Client:
    """腾讯混元 Hy3 大模型 API 客户端（OpenAI 兼容接口）"""

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
                "HY3_API_KEY 未设置。请在 .env 文件中配置或设置环境变量 HY3_API_KEY。"
            )

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

    def chat(
        self,
        messages: list[dict],
        stream: bool = False,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> dict | Generator:
        """通用对话"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=stream,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response

    def chat_sync(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> str:
        """同步对话，返回文本内容"""
        response = self.chat(
            messages=messages,
            stream=False,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    def deep_research(
        self,
        topic: str,
        search_results: list[str],
        stream: bool = False,
    ) -> str:
        """
        深度研究：基于搜索结果进行 AI 分析，生成结构化研究报告。
        
        Args:
            topic: 研究主题
            search_results: DuckDuckGo 搜索结果摘要列表
            stream: 是否流式输出
        """
        context = "\n".join(
            f"[来源 {i+1}] {r}" for i, r in enumerate(search_results)
        )

        system_prompt = (
            "你是一个专业的研究助手，基于提供的搜索资料生成深度研究报告。\n"
            "报告结构：\n"
            "1. **概述** - 主题背景与核心发现\n"
            "2. **关键信息** - 分点提取重要事实和数据\n"
            "3. **多角度分析** - 从不同视角解读信息\n"
            "4. **结论与建议** - 总结 + 下一步研究方向\n"
            "要求：引用来源标注编号，保持客观中立。"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"研究主题：{topic}\n\n参考资料：\n{context}",
            },
        ]

        return self.chat_sync(messages, temperature=0.5, max_tokens=8192)

    def code_review(
        self,
        code: str,
        language: str = "",
    ) -> str:
        """
        代码审查：多维度分析代码。

        Args:
            code: 代码内容
            language: 编程语言（自动检测或手动指定）
        """
        system_prompt = (
            "你是一个资深代码审查专家。请从以下维度分析代码：\n"
            "1. **Bug 检测** - 逻辑错误、边界情况\n"
            "2. **性能分析** - 时间复杂度、空间使用、可优化点\n"
            "3. **安全审计** - SQL 注入、XSS、凭据泄露等\n"
            "4. **代码质量** - 命名规范、可读性、DRY 原则\n"
            "5. **改进建议** - 提供具体的优化代码\n"
            "点评风格：建设性、具体、给出修改方案。"
        )

        lang_hint = f"（编程语言：{language}）" if language else ""
        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"请审查以下代码{lang_hint}：\n\n```\n{code}\n```",
            },
        ]

        return self.chat_sync(messages, temperature=0.3, max_tokens=8192)

    def doc_qa(
        self,
        question: str,
        doc_content: str,
        doc_name: str = "",
    ) -> str:
        """
        文档问答：基于文档内容精准回答用户问题。

        Args:
            question: 用户问题
            doc_content: 文档文本内容
            doc_name: 文档名称
        """
        name_hint = f""{doc_name}"" if doc_name else "上传的文档"
        system_prompt = (
            "你是一个文档分析助手。基于提供的文档内容回答用户问题。\n"
            "要求：\n"
            "- 如果答案在文档中，请引用原文段落\n"
            "- 如果文档不包含相关信息，请诚实说明\n"
            "- 回答简洁、准确，避免不必要的延伸"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    f"文档：{name_hint}\n\n"
                    f"文档内容：\n{doc_content}\n\n"
                    f"问题：{question}"
                ),
            },
        ]

        return self.chat_sync(messages, temperature=0.3, max_tokens=4096)
