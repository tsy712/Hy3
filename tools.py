"""
Utility functions: web search, file parsing, etc.
/ 工具函数：网页搜索、文件解析等

Supports Deep Research and Document Q&A features.
/ 为 Deep Research 和 Document Q&A 提供支撑。
"""

import os
import re
import logging
from typing import Optional
from io import BytesIO

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


# ── .env loading / .env 加载 ────────────────────────────

def load_dotenv(path: Optional[str] = None):
    """Simple .env file loader — no python-dotenv dependency needed. / 简单的 .env 文件加载，无需 python-dotenv 依赖"""
    if path is None:
        # Look for .env in backend/ first, then project root / 优先查找 backend 目录下的 .env，再查找项目根目录
        candidates = [
            os.path.join(os.path.dirname(__file__), ".env"),
            os.path.join(os.path.dirname(__file__), "..", ".env"),
        ]
        for p in candidates:
            if os.path.exists(p):
                path = p
                break

    if path is None or not os.path.exists(path):
        return

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                key = key.strip()
                # Remove inline comments and strip quotes / 去掉行内注释，再清理引号
                value = value.split("#", 1)[0].strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value
    logger.info(".env file loaded / .env 文件已加载: %s", path)


# ── Web Search / 网页搜索 ──────────────────────────────────

async def web_search(query: str, num_results: int = 5) -> str:
    """
    Perform a web search and return formatted results.
    / 执行网页搜索并返回格式化结果。

    Uses DuckDuckGo HTML interface (no API key required), parsed via BeautifulSoup.
    / 使用 DuckDuckGo 的 HTML 接口（无需 API Key），BeautifulSoup 解析。
    """
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(
                "https://html.duckduckgo.com/html/",
                params={"q": query},
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
            )

            if resp.status_code != 200:
                return f"Search failed, status code / 搜索失败，状态码: {resp.status_code}"

            soup = BeautifulSoup(resp.text, "html.parser")
            results = []

            # Parse each search result block / 解析每个搜索结果块
            result_blocks = soup.find_all("div", class_="result")
            if not result_blocks:
                result_blocks = soup.select(".result, .results_links, .web-result")

            for i, block in enumerate(result_blocks[:num_results]):
                # Extract title and link / 提取标题和链接
                link_el = block.find("a", class_="result__a")
                if not link_el:
                    link_el = block.find("a", class_="result__url")
                if not link_el:
                    link_el = block.find("a", href=True)

                title = link_el.get_text(strip=True) if link_el else "No title / 无标题"
                link = link_el.get("href", "") if link_el else ""

                # Extract snippet / 提取摘要
                snippet_el = block.find("a", class_="result__snippet")
                if not snippet_el:
                    snippet_el = block.find(class_="result__snippet")
                snippet = snippet_el.get_text(strip=True) if snippet_el else ""

                if title and title != "No title / 无标题":
                    results.append(f"{i+1}. 【{title}】\n   Link / 链接: {link}\n   Snippet / 摘要: {snippet}")

            if not results:
                return f"No results found for \"{query}\". / 未找到与「{query}」相关的搜索结果。"

            return "\n\n".join(results)

    except Exception as e:
        logger.error("Search exception / 搜索异常: %s", e)
        return f"Error searching for \"{query}\" / 搜索「{query}」时发生错误: {str(e)}"


# ── File Reading / 文件读取 ────────────────────────────────

async def read_file_content(file_bytes: bytes, filename: str) -> Optional[str]:
    """
    Parse content based on file extension.
    / 根据文件扩展名解析内容。

    Supported: .txt, .md, .py, .js, .ts, .html, .css, .json, .xml, .yaml, .pdf, .docx
    / 支持: .txt, .md, .py, .js, .ts, .html, .css, .json, .xml, .yaml, .pdf, .docx
    """
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    # Plain text / 纯文本
    if ext in ("txt", "md", "py", "js", "ts", "jsx", "tsx", "html", "css", "json", "xml", "yaml", "yml", "cfg", "ini"):
        try:
            return file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            try:
                return file_bytes.decode("gbk")
            except UnicodeDecodeError:
                return "[Unable to decode file content / 无法解码文件内容]"

    # PDF
    if ext == "pdf":
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(BytesIO(file_bytes))
            pages = []
            for page in reader.pages[:20]:  # Max 20 pages / 最多读 20 页
                text = page.extract_text()
                if text:
                    pages.append(text)
            return "\n\n".join(pages) if pages else "[PDF contains no text / PDF 无文字内容]"
        except ImportError:
            return "[PyPDF2 is not installed — cannot parse PDF / PyPDF2 未安装，无法解析 PDF]"
        except Exception as e:
            return f"[PDF parse error / PDF 解析错误: {e}]"

    # DOCX
    if ext == "docx":
        try:
            from docx import Document
            doc = Document(BytesIO(file_bytes))
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            return "\n".join(paragraphs) if paragraphs else "[Document is empty / 文档为空]"
        except ImportError:
            return "[python-docx is not installed — cannot parse DOCX / python-docx 未安装，无法解析 DOCX]"
        except Exception as e:
            return f"[DOCX parse error / DOCX 解析错误: {e}]"

    return f"[Unsupported file type / 不支持的文件类型: .{ext}]"


def truncate_text(text: str, max_chars: int = 8000) -> str:
    """Truncate text, appending an ellipsis note when exceeding max_chars. / 截断文本，超过最大字符数时添加省略标记"""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + f"\n\n... [Content truncated, original has {len(text)} chars / 内容已截断，原文共 {len(text)} 字符]"
