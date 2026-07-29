"""
Hy3 Research Assistant — FastAPI Backend Server
Provides API endpoints for three core features: Deep Research, Code Analysis, Document Q&A
All intelligent tasks are powered by the Hy3 large language model.
"""

import os
import re
import json
import logging
import asyncio
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse, HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from hy3_client import get_hy3_client
from tools import web_search, read_file_content, truncate_text, load_dotenv

# Load .env file
load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Hy3 Research Assistant", version="1.0.0")

# Mount frontend static files
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.isdir(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Homepage
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.get("/", response_class=HTMLResponse)
async def index():
    """Return the frontend page"""
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    return HTMLResponse("<h1>Frontend file not found</h1>", status_code=404)


@app.get("/health")
async def health():
    """Health check"""
    client = get_hy3_client()
    return {"status": "ok", "model": client.model, "base_url": client.base_url}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Feature 1: Deep Research
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Hy3 Prompt: Research Planning
RESEARCH_PLAN_PROMPT = """You are a senior research analyst. Based on the user's research topic, create a detailed research plan.

Requirements:
1. Decompose the research topic into 3-5 core sub-questions
2. Provide specific search keyword suggestions for each sub-question
3. Output in JSON format with the following structure:
{
  "topic": "research topic",
  "sub_questions": [
    {"question": "sub-question", "search_keywords": ["keyword1", "keyword2"]}
  ],
  "approach": "overall research methodology description"
}

User's research topic: {topic}

Please output JSON only, nothing else."""

# Hy3 Prompt: Research Report Writing
RESEARCH_REPORT_PROMPT = """You are a senior research analyst. Based on the following search materials, write a comprehensive and in-depth research report.

Requirements:
1. Report length: 1500-3000 words
2. Clear structure: including abstract, background, core analysis (by chapters), conclusion, and references
3. Use Markdown format
4. Based on the provided search materials, cite sources
5. Professional yet accessible language

Research topic: {topic}

Search materials:
{search_results}

Please write the research report:"""

# Hy3 Prompt: Executive Summary
RESEARCH_SUMMARY_PROMPT = """Please write a 200-300 word executive summary for the following research report. Summarize the core findings and key conclusions concisely.

Research report:
{report}

Executive summary:"""


def _parse_plan(plan_raw: str, topic: str) -> dict:
    """Robustly parse the research plan JSON"""
    default = {"sub_questions": [{"question": topic, "search_keywords": [topic]}]}

    cleaned = plan_raw.strip()
    # Remove markdown code block wrapping
    cleaned = re.sub(r'^```(?:json)?\s*', '', cleaned)
    cleaned = re.sub(r'\s*```$', '', cleaned)
    cleaned = cleaned.strip()

    # Method 1: Direct parsing
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Method 2: Regex extract first JSON object (supports nesting)
    depth = 0
    start = -1
    for i, ch in enumerate(cleaned):
        if ch == '{':
            if depth == 0:
                start = i
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0 and start >= 0:
                try:
                    return json.loads(cleaned[start:i+1])
                except json.JSONDecodeError:
                    break

    logger.warning("Unable to parse research plan JSON, using default strategy")
    return default


@app.post("/api/research")
async def deep_research(topic: str = Form(...)):
    """Deep research: planning → search → report → summary (streaming response)"""
    client = get_hy3_client()
    logger.info("Starting deep research: %s", topic)

    async def event_stream():
        # Phase 1: Generate research plan
        yield f"data: {json.dumps({'phase': 'planning', 'msg': '📋 Generating research plan...'}, ensure_ascii=False)}\n\n"
        plan_prompt = RESEARCH_PLAN_PROMPT.format(topic=topic)
        plan_raw = ""
        async for token in client.chat_stream(
            messages=[client.build_message("user", plan_prompt)],
            temperature=0.5,
            max_tokens=2048,
        ):
            plan_raw += token
        yield f"data: {json.dumps({'phase': 'planning', 'msg': '✅ Research plan generated', 'plan': plan_raw}, ensure_ascii=False)}\n\n"

        # Phase 2: Parse plan and execute search
        yield f"data: {json.dumps({'phase': 'searching', 'msg': '🔍 Searching for relevant materials...'}, ensure_ascii=False)}\n\n"

        search_results = []
        plan = _parse_plan(plan_raw, topic)
        sub_questions = plan.get("sub_questions", [{"question": topic, "search_keywords": [topic]}])
        if not sub_questions:
            sub_questions = [{"question": topic, "search_keywords": [topic]}]

        for i, sq in enumerate(sub_questions):
            keywords = sq.get("search_keywords", [sq.get("question", topic)])
            for kw in keywords[:2]:  # Up to 2 keywords per sub-question
                result = await web_search(kw, num_results=3)
                search_results.append(f"## Search: {kw}\n{result}")
                yield f"data: {json.dumps({'phase': 'searching', 'msg': f'🔍 Searched: {kw} ({i+1}/{len(sub_questions)})'}, ensure_ascii=False)}\n\n"
                await asyncio.sleep(0.5)

        search_text = "\n\n---\n\n".join(search_results)
        yield f"data: {json.dumps({'phase': 'searching', 'msg': '✅ Search complete', 'search_data': search_text[:2000]}, ensure_ascii=False)}\n\n"

        # Phase 3: Write report (streaming)
        yield f"data: {json.dumps({'phase': 'reporting', 'msg': '✍️ Writing research report...'}, ensure_ascii=False)}\n\n"

        report_prompt = RESEARCH_REPORT_PROMPT.format(
            topic=topic,
            search_results=truncate_text(search_text, max_chars=12000),
        )
        report_text = ""
        async for token in client.chat_stream(
            messages=[client.build_message("user", report_prompt)],
            temperature=0.7,
            max_tokens=8192,
        ):
            report_text += token
            yield f"data: {json.dumps({'phase': 'reporting', 'token': token}, ensure_ascii=False)}\n\n"

        # Phase 4: Generate summary
        yield f"data: {json.dumps({'phase': 'summarizing', 'msg': '📝 Generating executive summary...'}, ensure_ascii=False)}\n\n"

        summary_prompt = RESEARCH_SUMMARY_PROMPT.format(report=truncate_text(report_text, max_chars=5000))
        summary_text = ""
        async for token in client.chat_stream(
            messages=[client.build_message("user", summary_prompt)],
            temperature=0.5,
            max_tokens=1024,
        ):
            summary_text += token
            yield f"data: {json.dumps({'phase': 'summarizing', 'token': token}, ensure_ascii=False)}\n\n"

        yield f"data: {json.dumps({'phase': 'done', 'msg': '🎉 Research complete!'}, ensure_ascii=False)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Feature 2: Code Analysis
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Hy3 Prompt: Code Analysis
CODE_ANALYSIS_PROMPT = """You are a senior software engineer and code review expert. Please conduct an in-depth analysis of the following code.

Analysis dimensions:
1. **Code Overview**: What is the core functionality of this code?
2. **Logic Analysis**: Execution logic and key flow
3. **Potential Issues**: Bugs, performance issues, security concerns
4. **Optimization Suggestions**: Specific improvement plans and best practices
5. **Code Quality Score**: 1-10 rating with justification

User intent: {intent}

Code content:
```
{code}
```

Please output a detailed analysis report in Markdown format."""


@app.post("/api/analyze-code")
async def analyze_code(
    code: str = Form(...),
    intent: str = Form(default="Please provide a comprehensive analysis of this code"),
):
    """Code analysis: streaming output of analysis results"""
    client = get_hy3_client()
    logger.info("Starting code analysis, code length: %d", len(code))

    prompt = CODE_ANALYSIS_PROMPT.format(
        intent=intent,
        code=truncate_text(code, max_chars=15000),
    )

    async def event_stream():
        yield f"data: {json.dumps({'phase': 'analyzing', 'msg': '🔬 Analyzing code...'}, ensure_ascii=False)}\n\n"
        async for token in client.chat_stream(
            messages=[client.build_message("user", prompt)],
            temperature=0.3,
            max_tokens=8192,
        ):
            yield f"data: {json.dumps({'phase': 'analyzing', 'token': token}, ensure_ascii=False)}\n\n"
        yield f"data: {json.dumps({'phase': 'done', 'msg': '✅ Analysis complete!'}, ensure_ascii=False)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.post("/api/analyze-code-file")
async def analyze_code_file(
    file: UploadFile = File(...),
    intent: str = Form(default="Please provide a comprehensive analysis of this code"),
):
    """Upload a code file for analysis"""
    code_bytes = await file.read()
    code = await read_file_content(code_bytes, file.filename or "code.txt")

    if code is None or code.startswith("[Unable") or code.startswith("[Unsupported"):
        return StreamingResponse(
            iter([f"data: {json.dumps({'phase': 'error', 'msg': code or 'File parsing failed'}, ensure_ascii=False)}\n\n"]),
            media_type="text/event-stream",
        )

    prompt = CODE_ANALYSIS_PROMPT.format(
        intent=intent,
        code=truncate_text(code, max_chars=15000),
    )

    client = get_hy3_client()

    async def event_stream():
        yield f"data: {json.dumps({'phase': 'analyzing', 'msg': f'🔬 Analyzing {file.filename}...'}, ensure_ascii=False)}\n\n"
        async for token in client.chat_stream(
            messages=[client.build_message("user", prompt)],
            temperature=0.3,
            max_tokens=8192,
        ):
            yield f"data: {json.dumps({'phase': 'analyzing', 'token': token}, ensure_ascii=False)}\n\n"
        yield f"data: {json.dumps({'phase': 'done', 'msg': '✅ Analysis complete!'}, ensure_ascii=False)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Feature 3: Document Q&A
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Hy3 Prompt: Document Q&A
DOC_QA_PROMPT = """You are a professional document analysis assistant. Please answer the user's question based on the following document content.

Requirements:
1. Answers must be based on the provided document content; do not fabricate information
2. Cite specific passages from the documents as evidence
3. If relevant information cannot be found in the documents, clearly state so
4. Use Markdown format to organize the answer for readability

Document content:
{document_text}

User question: {question}

Please answer:"""


@app.post("/api/qa-documents")
async def qa_documents(
    question: str = Form(...),
    files: list[UploadFile] = File(...),
):
    """Multi-document Q&A: upload documents + ask question, Hy3 answers based on document content"""
    client = get_hy3_client()
    logger.info("Document Q&A: %s, file count: %d", question, len(files))

    # Parse all documents
    doc_contents = []
    for f in files:
        content = await read_file_content(await f.read(), f.filename or "document")
        if content:
            doc_contents.append(f"### File: {f.filename}\n{content}")

    if not doc_contents:
        async def error_stream():
            yield f"data: {json.dumps({'phase': 'error', 'msg': 'All files failed to parse, please check file format'}, ensure_ascii=False)}\n\n"
        return StreamingResponse(error_stream(), media_type="text/event-stream")

    combined_text = "\n\n---\n\n".join(doc_contents)
    prompt = DOC_QA_PROMPT.format(
        document_text=truncate_text(combined_text, max_chars=20000),
        question=question,
    )

    async def event_stream():
        yield f"data: {json.dumps({'phase': 'analyzing', 'msg': f'📚 Read {len(files)} documents, analyzing...'}, ensure_ascii=False)}\n\n"
        async for token in client.chat_stream(
            messages=[client.build_message("user", prompt)],
            temperature=0.5,
            max_tokens=4096,
        ):
            yield f"data: {json.dumps({'phase': 'analyzing', 'token': token}, ensure_ascii=False)}\n\n"
        yield f"data: {json.dumps({'phase': 'done', 'msg': '✅ Answer complete!'}, ensure_ascii=False)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Entry Point
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    logger.info("Starting Hy3 Research Assistant server on port %d", port)
    uvicorn.run(app, host="0.0.0.0", port=port)
