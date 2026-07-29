"""
Hy3 Research Assistant — FastAPI backend server
/ Hy3 Research Assistant —— FastAPI 后端服务器

Provides API endpoints for three features: Deep Research, Code Analysis, and Document Q&A.
/ 提供三大功能的 API 端点：深度研究、代码分析、文档问答

All intelligent tasks are completed via the Hy3 large model.
/ 所有智能任务均通过 Hy3 大模型完成。
"""

import os
import re
import json
import logging
import asyncio
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse, HTMLResponse
import uvicorn

from hy3_client import get_hy3_client
from tools import web_search, read_file_content, truncate_text, load_dotenv

# Load .env file / 加载 .env 文件
load_dotenv()

# Logging / 日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Hy3 Research Assistant / Hy3 研究助手", version="1.0.0")

# Frontend directory / 前端目录
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")


# ━━━━━ Home Page / 首页 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.get("/", response_class=HTMLResponse)
async def index():
    """Serve the frontend page. / 返回前端页面"""
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):

        async def _read():
            with open(index_path, "r", encoding="utf-8") as f:
                return f.read()

        content = await asyncio.to_thread(_read)
        return HTMLResponse(content)
    return HTMLResponse("<h1>Frontend file not found / 前端文件未找到</h1>", status_code=404)


@app.get("/health")
async def health():
    """Health check endpoint. / 健康检查"""
    client = get_hy3_client()
    return {"status": "ok", "model": client.model, "base_url": client.base_url}


# ━━━━━ Feature 1: Deep Research / 功能一：深度研究 ━━━━━━━━━

# Hy3 prompt: Research planning / Hy3 提示词：研究规划
RESEARCH_PLAN_PROMPT = """你是一位资深的研究分析师。请根据用户的研究主题，制定一个详细的研究计划。

要求：
1. 将研究主题分解为 3-5 个核心子问题
2. 为每个子问题提供具体的搜索关键词建议
3. 以 JSON 格式输出，结构如下：
{
  "topic": "研究主题",
  "sub_questions": [
    {"question": "子问题", "search_keywords": ["关键词1", "关键词2"]}
  ],
  "approach": "整体研究方法说明"
}

用户研究主题：{topic}

请仅输出 JSON，不要有任何其他内容。"""

# Hy3 prompt: Research report writing / Hy3 提示词：研究报告撰写
RESEARCH_REPORT_PROMPT = """你是一位资深的研究分析师。请根据以下搜索资料，撰写一份全面深入的研究报告。

要求：
1. 报告长度：1500-3000 字
2. 结构清晰：包含摘要、背景、核心分析（分章节）、结论、参考文献
3. 使用 Markdown 格式
4. 基于提供的搜索资料，标注引用来源
5. 语言专业但通俗易懂

研究主题：{topic}

搜索资料：
{search_results}

请撰写研究报告："""

# Hy3 prompt: Executive summary / Hy3 提示词：执行摘要
RESEARCH_SUMMARY_PROMPT = """请为以下研究报告撰写一个 200-300 字的执行摘要。用简洁的语言概括核心发现和关键结论。

研究报告：
{report}

执行摘要："""


def _parse_plan(plan_raw: str, topic: str) -> dict:
    """Robustly parse the research plan JSON. / 鲁棒地解析研究计划 JSON"""
    default = {"sub_questions": [{"question": topic, "search_keywords": [topic]}]}

    cleaned = plan_raw.strip()
    # Strip markdown code blocks / 移除 markdown 代码块包裹
    cleaned = re.sub(r'^```(?:json)?\s*', '', cleaned)
    cleaned = re.sub(r'\s*```$', '', cleaned)
    cleaned = cleaned.strip()

    # Method 1: Direct parse / 方式1：直接解析
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Method 2: Regex-extract first JSON object (supports nesting) / 方式2：正则提取第一个 JSON 对象（支持嵌套）
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

    logger.warning("Unable to parse research plan JSON, using default strategy / 无法解析研究计划 JSON，使用默认策略")
    return default


@app.post("/api/research")
async def deep_research(topic: str = Form(...)):
    """Deep Research: Plan → Search → Report → Summary (streaming). / 深度研究：规划 → 搜索 → 报告 → 摘要（流式返回）"""
    client = get_hy3_client()
    logger.info("Starting deep research / 开始深度研究: %s", topic)

    async def event_stream():
        # Phase 1: Generate research plan / 阶段1：生成研究计划
        yield f"data: {json.dumps({'phase': 'planning', 'msg': '📋 Generating research plan... / 正在制定研究计划...'}, ensure_ascii=False)}\n\n"
        plan_prompt = RESEARCH_PLAN_PROMPT.format(topic=topic)
        plan_raw = ""
        async for token in client.chat_stream(
            messages=[client.build_message("user", plan_prompt)],
            temperature=0.5,
            max_tokens=2048,
        ):
            plan_raw += token
        yield f"data: {json.dumps({'phase': 'planning', 'msg': '✅ Research plan generated / 研究计划已生成', 'plan': plan_raw}, ensure_ascii=False)}\n\n"

        # Phase 2: Parse plan and execute search / 阶段2：解析计划并执行搜索
        yield f"data: {json.dumps({'phase': 'searching', 'msg': '🔍 Searching for relevant materials... / 正在搜索相关资料...'}, ensure_ascii=False)}\n\n"

        search_results = []
        plan = _parse_plan(plan_raw, topic)
        sub_questions = plan.get("sub_questions", [{"question": topic, "search_keywords": [topic]}])
        if not sub_questions:
            sub_questions = [{"question": topic, "search_keywords": [topic]}]

        for i, sq in enumerate(sub_questions):
            keywords = sq.get("search_keywords", [sq.get("question", topic)])
            for kw in keywords[:2]:  # Max 2 keywords per sub-question / 每个子问题最多搜2个关键词
                result = await web_search(kw, num_results=3)
                search_results.append(f"## Search / 搜索: {kw}\n{result}")
                yield f"data: {json.dumps({'phase': 'searching', 'msg': f'🔍 Searched: {kw} ({i+1}/{len(sub_questions)})'}, ensure_ascii=False)}\n\n"
                await asyncio.sleep(0.5)

        search_text = "\n\n---\n\n".join(search_results)
        yield f"data: {json.dumps({'phase': 'searching', 'msg': '✅ Search completed / 搜索完成', 'search_data': search_text[:2000]}, ensure_ascii=False)}\n\n"

        # Phase 3: Write report (streaming) / 阶段3：撰写报告（流式）
        yield f"data: {json.dumps({'phase': 'reporting', 'msg': '✍️ Writing research report... / 正在撰写研究报告...'}, ensure_ascii=False)}\n\n"

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

        # Phase 4: Generate summary / 阶段4：生成摘要
        yield f"data: {json.dumps({'phase': 'summarizing', 'msg': '📝 Generating executive summary... / 正在生成执行摘要...'}, ensure_ascii=False)}\n\n"

        summary_prompt = RESEARCH_SUMMARY_PROMPT.format(report=truncate_text(report_text, max_chars=5000))
        summary_text = ""
        async for token in client.chat_stream(
            messages=[client.build_message("user", summary_prompt)],
            temperature=0.5,
            max_tokens=1024,
        ):
            summary_text += token
            yield f"data: {json.dumps({'phase': 'summarizing', 'token': token}, ensure_ascii=False)}\n\n"

        yield f"data: {json.dumps({'phase': 'done', 'msg': '🎉 Research completed! / 研究完成！'}, ensure_ascii=False)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


# ━━━━━ Feature 2: Code Analysis / 功能二：代码分析 ━━━━━━━━━━

# Hy3 prompt: Code analysis / Hy3 提示词：代码分析
CODE_ANALYSIS_PROMPT = """你是一位资深软件工程师和代码审查专家。请对以下代码进行深入分析。

分析维度：
1. **代码概览**：这段代码的核心功能是什么？
2. **逻辑分析**：代码的执行逻辑和关键流程
3. **潜在问题**：Bug、性能隐患、安全问题
4. **优化建议**：具体的改进方案和最佳实践
5. **代码质量评分**：1-10 分，并说明理由

用户意图：{intent}

代码内容：
```
{code}
```

请使用 Markdown 格式输出详细的分析报告。"""


@app.post("/api/analyze-code")
async def analyze_code(
    code: str = Form(...),
    intent: str = Form(default="Please provide a comprehensive analysis of this code / 请对这段代码进行全面分析"),
):
    """Code Analysis: Stream analysis results. / 代码分析：流式返回分析结果"""
    client = get_hy3_client()
    logger.info("Starting code analysis, code length / 开始代码分析，代码长度: %d", len(code))

    prompt = CODE_ANALYSIS_PROMPT.format(
        intent=intent,
        code=truncate_text(code, max_chars=15000),
    )

    async def event_stream():
        yield f"data: {json.dumps({'phase': 'analyzing', 'msg': '🔬 Analyzing code... / 正在分析代码...'}, ensure_ascii=False)}\n\n"
        async for token in client.chat_stream(
            messages=[client.build_message("user", prompt)],
            temperature=0.3,
            max_tokens=8192,
        ):
            yield f"data: {json.dumps({'phase': 'analyzing', 'token': token}, ensure_ascii=False)}\n\n"
        yield f"data: {json.dumps({'phase': 'done', 'msg': '✅ Analysis completed! / 分析完成！'}, ensure_ascii=False)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.post("/api/analyze-code-file")
async def analyze_code_file(
    file: UploadFile = File(...),
    intent: str = Form(default="Please provide a comprehensive analysis of this code / 请对这段代码进行全面分析"),
):
    """Upload a code file for analysis. / 上传代码文件进行分析"""
    code_bytes = await file.read()
    code = await read_file_content(code_bytes, file.filename or "code.txt")

    if code is None or code.startswith("[无法") or code.startswith("[不支持"):
        return StreamingResponse(
            iter([f"data: {json.dumps({'phase': 'error', 'msg': code or 'File parsing failed / 文件解析失败'}, ensure_ascii=False)}\n\n"]),
            media_type="text/event-stream",
        )

    prompt = CODE_ANALYSIS_PROMPT.format(
        intent=intent,
        code=truncate_text(code, max_chars=15000),
    )

    client = get_hy3_client()

    async def event_stream():
        yield f"data: {json.dumps({'phase': 'analyzing', 'msg': f'🔬 Analyzing {file.filename}... / 正在分析 {file.filename}...'}, ensure_ascii=False)}\n\n"
        async for token in client.chat_stream(
            messages=[client.build_message("user", prompt)],
            temperature=0.3,
            max_tokens=8192,
        ):
            yield f"data: {json.dumps({'phase': 'analyzing', 'token': token}, ensure_ascii=False)}\n\n"
        yield f"data: {json.dumps({'phase': 'done', 'msg': '✅ Analysis completed! / 分析完成！'}, ensure_ascii=False)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


# ━━━━━ Feature 3: Document Q&A / 功能三：文档问答 ━━━━━━━━━

# Hy3 prompt: Document Q&A / Hy3 提示词：文档问答
DOC_QA_PROMPT = """你是一位专业的文档分析助手。请根据以下文档内容回答用户的问题。

要求：
1. 回答必须基于提供的文档内容，不要编造信息
2. 引用文档中的具体段落作为证据
3. 如果文档中找不到相关信息，请明确说明
4. 使用 Markdown 格式组织回答，使其易读

文档内容：
{document_text}

用户问题：{question}

请回答："""


@app.post("/api/qa-documents")
async def qa_documents(
    question: str = Form(...),
    files: list[UploadFile] = File(...),
):
    """Multi-document Q&A: Upload docs + ask questions, Hy3 answers based on document content. / 多文档问答：上传文档 + 提问，Hy3 基于文档内容回答"""
    client = get_hy3_client()
    logger.info("Document Q&A / 文档问答: %s, file count / 文件数: %d", question, len(files))

    # Parse all documents / 解析所有文档
    doc_contents = []
    for f in files:
        content = await read_file_content(await f.read(), f.filename or "document")
        if content:
            doc_contents.append(f"### File / 文件: {f.filename}\n{content}")

    if not doc_contents:
        async def error_stream():
            yield f"data: {json.dumps({'phase': 'error', 'msg': 'All files failed to parse — check file format / 所有文件解析失败，请检查文件格式'}, ensure_ascii=False)}\n\n"
        return StreamingResponse(error_stream(), media_type="text/event-stream")

    combined_text = "\n\n---\n\n".join(doc_contents)
    prompt = DOC_QA_PROMPT.format(
        document_text=truncate_text(combined_text, max_chars=20000),
        question=question,
    )

    async def event_stream():
        yield f"data: {json.dumps({'phase': 'analyzing', 'msg': f'📚 Loaded {len(files)} document(s), analyzing... / 已读取 {len(files)} 个文档，正在分析...'}, ensure_ascii=False)}\n\n"
        async for token in client.chat_stream(
            messages=[client.build_message("user", prompt)],
            temperature=0.5,
            max_tokens=4096,
        ):
            yield f"data: {json.dumps({'phase': 'analyzing', 'token': token}, ensure_ascii=False)}\n\n"
        yield f"data: {json.dumps({'phase': 'done', 'msg': '✅ Answer completed! / 回答完成！'}, ensure_ascii=False)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


# ━━━━━ Entry Point / 启动入口 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    logger.info("Starting Hy3 Research Assistant server on port / 启动 Hy3 研究助手服务器，端口: %d", port)
    uvicorn.run(app, host="0.0.0.0", port=port)
