"""
工具函数集合 — 网页搜索、文件解析、文本处理等通用能力。
"""

import io
from typing import Optional

import httpx
from bs4 import BeautifulSoup


class ToolManager:
    """工具管理器：提供搜索、文件解析等工具能力"""

    @staticmethod
    async def duckduckgo_search(
        query: str,
        max_results: int = 10,
    ) -> list[dict]:
        """
        DuckDuckGo 搜索（双层降级策略）

        第一层：DuckDuckGo Instant Answer API（JSON）
        第二层：DuckDuckGo HTML 搜索结果页解析
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
                params = {
                    "q": query,
                    "format": "json",
                    "no_html": 1,
                    "skip_disambig": 1,
                }
                resp = await client.get(api_url, params=params)
                resp.raise_for_status()
                data = resp.json()

                # 提取 Abstract
                if data.get("AbstractText"):
                    results.append({
                        "title": data.get("Heading", query),
                        "snippet": data["AbstractText"],
                        "url": data.get("AbstractURL", ""),
                        "source": "DuckDuckGo Abstract",
                    })

                # 提取 RelatedTopics
                for topic in data.get("RelatedTopics", []):
                    if topic.get("Text") and not topic.get("Topics"):
                        results.append({
                            "title": topic.get("FirstURL", ""),
                            "snippet": topic.get("Text", ""),
                            "url": topic.get("FirstURL", ""),
                            "source": "DuckDuckGo Related",
                        })
            except Exception:
                pass

            # 第二层：HTML 搜索（如果结果不够）
            if len(results) < max_results:
                try:
                    html_url = f"https://html.duckduckgo.com/html/?q={query}"
                    resp = await client.get(html_url)
                    resp.raise_for_status()
                    soup = BeautifulSoup(resp.text, "lxml")

                    for item in soup.select(".result")[: max_results - len(results)]:
                        title_el = item.select_one(".result__title a")
                        snippet_el = item.select_one(".result__snippet")
                        url_el = item.select_one(".result__url")

                        if title_el and snippet_el:
                            results.append({
                                "title": title_el.get_text(strip=True),
                                "snippet": snippet_el.get_text(strip=True),
                                "url": url_el.get_text(strip=True) if url_el else "",
                                "source": "DuckDuckGo HTML",
                            })
                except Exception:
                    pass

        return results[:max_results]

    @staticmethod
    def parse_pdf(file_bytes: bytes) -> str:
        """解析 PDF 文件，返回文本内容"""
        try:
            from PyPDF2 import PdfReader

            reader = PdfReader(io.BytesIO(file_bytes))
            text_parts = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
            return "\n".join(text_parts)
        except Exception as e:
            return f"[PDF 解析失败] {str(e)}"

    @staticmethod
    def parse_docx(file_bytes: bytes) -> str:
        """解析 DOCX 文件，返回文本内容"""
        try:
            from docx import Document

            doc = Document(io.BytesIO(file_bytes))
            text_parts = []
            for para in doc.paragraphs:
                if para.text.strip():
                    text_parts.append(para.text)
            return "\n".join(text_parts)
        except Exception as e:
            return f"[DOCX 解析失败] {str(e)}"

    @staticmethod
    def parse_text(file_bytes: bytes) -> str:
        """解析纯文本文件"""
        try:
            return file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            try:
                return file_bytes.decode("gbk")
            except Exception as e:
                return f"[文本解析失败] {str(e)}"

    @classmethod
    def parse_file(cls, filename: str, file_bytes: bytes) -> str:
        """根据文件扩展名自动选择合适的解析器"""
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

        parsers = {
            "pdf": cls.parse_pdf,
            "docx": cls.parse_docx,
            "doc": cls.parse_docx,
            "txt": cls.parse_text,
            "md": cls.parse_text,
            "py": cls.parse_text,
            "js": cls.parse_text,
            "ts": cls.parse_text,
            "java": cls.parse_text,
            "cpp": cls.parse_text,
            "c": cls.parse_text,
            "html": cls.parse_text,
            "css": cls.parse_text,
            "json": cls.parse_text,
            "yaml": cls.parse_text,
            "yml": cls.parse_text,
            "xml": cls.parse_text,
            "csv": cls.parse_text,
        }

        parser = parsers.get(ext, cls.parse_text)
        return parser(file_bytes)
