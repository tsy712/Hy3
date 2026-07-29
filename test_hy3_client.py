"""
Hy3 MCP Server — Hy3 API 客户端单元测试

测试覆盖：
  - 客户端初始化（含 API Key 校验）
  - 通用对话 (chat)
  - 深度研究 (deep_research)
  - 代码审查 (code_review)
  - 文档问答 (doc_qa)
  - DuckDuckGo 搜索
"""

import os
import sys
import asyncio
from pathlib import Path

import pytest

# 路径设置
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from hy3_client import Hy3MCPClient, search_duckduckgo


# ==================== Fixtures ====================


@pytest.fixture
def api_key():
    """获取测试 API Key"""
    key = os.getenv("HY3_API_KEY")
    if not key:
        pytest.skip("HY3_API_KEY not set — skipping integration test")
    return key


@pytest.fixture
def client(api_key):
    """创建 Hy3MCPClient 实例"""
    return Hy3MCPClient(api_key=api_key)


# ==================== Unit Tests ====================


class TestClientInit:
    """客户端初始化测试"""

    def test_init_with_api_key(self, api_key):
        """测试使用显式 API Key 初始化"""
        client = Hy3MCPClient(api_key=api_key)
        assert client.api_key == api_key
        assert client.client is not None

    def test_init_without_api_key_raises(self, monkeypatch):
        """测试无 API Key 时抛出异常"""
        monkeypatch.delenv("HY3_API_KEY", raising=False)
        with pytest.raises(ValueError, match="HY3_API_KEY"):
            Hy3MCPClient(api_key=None)

    def test_default_model(self, api_key):
        """测试默认模型"""
        client = Hy3MCPClient(api_key=api_key)
        assert client.model in ("hunyuan-pro", "")

    def test_custom_model(self, api_key):
        """测试自定义模型"""
        client = Hy3MCPClient(api_key=api_key, model="hunyuan-lite")
        assert client.model == "hunyuan-lite"


# ==================== Integration Tests ====================


@pytest.mark.asyncio
class TestChat:
    """对话功能集成测试"""

    async def test_basic_chat(self, client):
        """测试基本对话"""
        response = await client.chat("你好，请用一句话介绍你自己。")
        assert response
        assert len(response) > 0
        assert isinstance(response, str)

    async def test_chat_with_math(self, client):
        """测试数学问题"""
        response = await client.chat("1+1等于几？")
        assert response
        assert "2" in response or "二" in response


@pytest.mark.asyncio
class TestCodeReview:
    """代码审查集成测试"""

    async def test_basic_code_review(self, client):
        """测试基本代码审查"""
        code = """
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
"""
        response = await client.code_review(code, "python")
        assert response
        assert len(response) > 0


@pytest.mark.asyncio
class TestDocQA:
    """文档问答集成测试"""

    async def test_doc_qa(self, client):
        """测试文档问答"""
        doc = "北京是中国的首都。上海是中国最大的城市。"
        question = "中国的首都是哪里？"
        response = await client.doc_qa(question, doc, "test.txt")
        assert response
        assert "北京" in response


@pytest.mark.asyncio
class TestSearch:
    """搜索功能测试"""

    async def test_duckduckgo_search(self):
        """测试 DuckDuckGo 搜索"""
        results = await search_duckduckgo("Python programming", max_results=5)
        assert len(results) > 0
        assert all("title" in r and "snippet" in r for r in results)

    async def test_search_empty_query(self):
        """测试空查询"""
        results = await search_duckduckgo("", max_results=3)
        assert isinstance(results, list)


# ==================== Run ====================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
