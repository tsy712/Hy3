"""
Utility functions: web search, file parsing, etc.
Provides support for Deep Research and Document Q&A.
"""

import os
import re
import logging
from typing import Optional
from io import BytesIO

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


# ── .env Loading ─────────────────────────────────────────

def load_dotenv(path: Optional[str] = None):
    """Simple .env file loader, no python-dotenv dependency required"""
    if path is None:
        # First look for .env in backend directory, then project root
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
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value
    logger.info(".env file loaded: %s", path)


# ── Web Search ────────────────────────────────────────────

async def web_search(query: str, num_results: int = 5) -> str:
    """
    Perform web search and return formatted results.
    Uses DuckDuckGo's HTML interface (no API key required), parsed with BeautifulSoup.
    """
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(
                "https://html.duckduckgo.com/html/",
                params={"q": query},
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
            )

            if resp.status_code != 200:
                return f"Search failed, status code: {resp.status_code}"

            soup = BeautifulSoup(resp.text, "html.parser")
            results = []

            # Parse each search result block
            result_blocks = soup.find_all("div", class_="result")
            if not result_blocks:
                result_blocks = soup.select(".result, .results_links, .web-result")

            for i, block in enumerate(result_blocks[:num_results]):
                # Extract title and link
                link_el = block.find("a", class_="result__a")
                if not link_el:
                    link_el = block.find("a", class_="result__url")
                if not link_el:
                    link_el = block.find("a", href=True)

                title = link_el.get_text(strip=True) if link_el else "Untitled"
                link = link_el.get("href", "") if link_el else ""

                # Extract snippet
                snippet_el = block.find("a", class_="result__snippet")
                if not snippet_el:
                    snippet_el = block.find(class_="result__snippet")
                snippet = snippet_el.get_text(strip=True) if snippet_el else ""

                if title and title != "Untitled":
                    results.append(f"{i+1}. 【{title}】\n   Link: {link}\n   Snippet: {snippet}")

            if not results:
                return f"No results found for '{query}'."

            return "\n\n".join(results)

    except Exception as e:
        logger.error("Search error: %s", e)
        return f"Error while searching '{query}': {str(e)}"


# ── File Reading ────────────────────────────────────────────

async def read_file_content(file_bytes: bytes, filename: str) -> Optional[str]:
    """
    Parse content based on file extension.
    Supports: .txt, .md, .py, .js, .ts, .html, .css, .json, .xml, .yaml, .pdf, .docx
    """
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    # Plain text
    if ext in ("txt", "md", "py", "js", "ts", "jsx", "tsx", "html", "css", "json", "xml", "yaml", "yml", "cfg", "ini"):
        try:
            return file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            try:
                return file_bytes.decode("gbk")
            except UnicodeDecodeError:
                return "[Unable to decode file content]"

    # PDF
    if ext == "pdf":
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(BytesIO(file_bytes))
            pages = []
            for page in reader.pages[:20]:  # Read up to 20 pages
                text = page.extract_text()
                if text:
                    pages.append(text)
            return "\n\n".join(pages) if pages else "[PDF contains no text]"
        except ImportError:
            return "[PyPDF2 not installed, cannot parse PDF]"
        except Exception as e:
            return f"[PDF parsing error: {e}]"

    # DOCX
    if ext == "docx":
        try:
            from docx import Document
            doc = Document(BytesIO(file_bytes))
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            return "\n".join(paragraphs) if paragraphs else "[Document is empty]"
        except ImportError:
            return "[python-docx not installed, cannot parse DOCX]"
        except Exception as e:
            return f"[DOCX parsing error: {e}]"

    return f"[Unsupported file type: .{ext}]"


def truncate_text(text: str, max_chars: int = 8000) -> str:
    """Truncate text, adding ellipsis marker when exceeding max characters"""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + f"\n\n... [Content truncated, original length: {len(text)} characters]"
