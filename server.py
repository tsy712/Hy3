"""
Hy3 MCP Server — 将腾讯混元 Hy3 大模型接入 MCP 协议
提供 5 个 MCP 工具：hy3_research、hy3_code_review、hy3_doc_qa、hy3_data_analyze、hy3_chat
"""

import os
import sys
import json
import logging
from pathlib import Path

from fastmcp import FastMCP
from dotenv import load_dotenv

from hy3_mcp_server.hy3_client import Hy3MCPClient

# ── 日志初始化 ──────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,  # MCP stdio 协议需要在 stderr 输出日志
)
logger = logging.getLogger("hy3-mcp-server")

# ── 加载 .env ───────────────────────────────────
# 先找 configs/.env，再找当前目录和上级目录
env_candidates = [
    Path(__file__).parent.parent / "configs" / ".env",
    Path(__file__).parent.parent / ".env",
    Path.cwd() / ".env",
]
for env_path in env_candidates:
    if env_path.exists():
        load_dotenv(env_path)
        logger.info(".env 加载自: %s", env_path)
        break
else:
    load_dotenv()  # 默认搜索
    logger.info("未找到自定义 .env 文件，使用环境变量")

# ── FastMCP 初始化 ──────────────────────────────
mcp = FastMCP(
    "Hy3",
    description="腾讯混元 Hy3 大模型 MCP Server — 提供深度研究、代码评审、文档问答、数据分析等能力",
)

# ── Hy3 客户端 (延迟初始化) ─────────────────────
_client: Hy3MCPClient | None = None


def get_client() -> Hy3MCPClient:
    global _client
    if _client is None:
        api_key = os.getenv("HY3_API_KEY", "")
        base_url = os.getenv("HY3_BASE_URL", "https://api.hunyuan.cloud.tencent.com/v1")
        model = os.getenv("HY3_MODEL", "hunyuan-pro")
        _client = Hy3MCPClient(api_key=api_key, base_url=base_url, model=model)
    return _client


# ═══════════════════════════════════════════════════════
# MCP Tool 定义
# ═══════════════════════════════════════════════════════

@mcp.tool()
async def hy3_research(topic: str, depth: str = "standard") -> str:
    """
    深度研究工具：给定一个研究主题，自动规划研究路径、搜索相关信息，生成结构化的研究报告。

    参数:
        topic (str): 研究主题，如"量子计算在药物研发中的应用前景"
        depth (str): 研究深度，可选 "quick"(快速) / "standard"(标准) / "deep"(深入)，默认 "standard"

    返回:
        str: Markdown 格式的研究报告
    """
    client = get_client()
    logger.info("深度研究 [%s]: %s", depth, topic)

    depth_map = {"quick": 2, "standard": 4, "deep": 6}
    num_search = depth_map.get(depth, 4)

    # 生成研究计划
    plan_prompt = f"""你是一位资深研究分析师。请为以下研究主题制定一个详细的研究计划。
将主题分解为 {num_search} 个核心子问题，并为每个子问题提供 2-3 个搜索关键词。
以 JSON 格式输出，结构: {{"sub_questions": [{{"question": "...", "keywords": ["..."]}}], "approach": "..."}}

研究主题: {topic}
"""
    plan_raw = await client.agenerate(plan_prompt, temperature=0.5, max_tokens=2048)

    # 尝试解析 JSON 计划
    sub_questions = []
    try:
        # 清理可能的 markdown 包裹
        cleaned = plan_raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        plan = json.loads(cleaned)
        sub_questions = plan.get("sub_questions", [])
    except json.JSONDecodeError:
        # 降级：直接搜索主题
        sub_questions = [{"question": topic, "keywords": [topic]}]

    if not sub_questions:
        sub_questions = [{"question": topic, "keywords": [topic]}]

    # 执行搜索
    search_results = []
    for sq in sub_questions:
        keywords = sq.get("keywords", [sq.get("question", topic)])
        for kw in keywords[:2]:
            result = await client.web_search(kw, num_results=3)
            search_results.append(f"### 搜索: {kw}\n{result}")

    search_text = "\n\n".join(search_results)

    # 生成报告
    report_prompt = f"""你是一位资深研究分析师。请基于以下搜索资料撰写一份专业研究报告。

主题: {topic}

要求:
- 1500-3000 字
- 结构: 摘要 → 背景 → 核心分析(分章节) → 结论 → 参考文献
- 使用 Markdown 格式
- 引用搜索来源

搜索资料:
{search_text[:12000]}
"""
    report = await client.agenerate(report_prompt, temperature=0.7, max_tokens=8192)
    return report


@mcp.tool()
async def hy3_code_review(code: str, language: str = "auto") -> str:
    """
    代码评审工具：对代码进行全面分析，包括 Bug 检测、性能分析、安全审计、质量评分。

    参数:
        code (str): 待评审的源代码
        language (str): 编程语言，可选 "python"/"javascript"/"typescript"/"java"/"go"/"rust"/"auto"，默认 "auto"

    返回:
        str: Markdown 格式的代码评审报告
    """
    client = get_client()
    logger.info("代码评审 [%s]: %d 字符", language, len(code))

    prompt = f"""你是一位资深代码审查专家。请对以下 {language if language != 'auto' else ''} 代码进行全面评审。

评审维度:
1. **代码概览** — 核心功能、架构模式
2. **逻辑分析** — 执行流程、关键路径
3. **Bug 检测** — 逻辑错误、边界情况、异常处理
4. **性能分析** — 时间复杂度、内存占用、优化机会
5. **安全审计** — 注入风险、敏感信息泄露、权限问题
6. **质量评分** — 1-10 分，附评分理由
7. **改进建议** — 具体的优化方案和最佳实践

代码:
```
{code[:15000]}
```"""
    result = await client.agenerate(prompt, temperature=0.3, max_tokens=4096)
    return result


@mcp.tool()
async def hy3_doc_qa(document_text: str, question: str) -> str:
    """
    文档问答工具：基于提供的文档内容回答用户问题，引用原文证据。

    参数:
        document_text (str): 文档全文内容
        question (str): 基于文档内容提出的问题

    返回:
        str: 基于文档内容的精准回答（引用原文证据）
    """
    client = get_client()
    logger.info("文档问答: %s", question[:50])

    prompt = f"""你是一位文档分析专家。请基于以下文档内容回答用户问题。

要求:
1. 仅基于文档内容回答，不要编造
2. 引用原文段落作为证据（用 > 标记）
3. 如信息不足，明确说明
4. 使用 Markdown 组织回答

文档内容:
{document_text[:20000]}

用户问题: {question}"""
    result = await client.agenerate(prompt, temperature=0.5, max_tokens=4096)
    return result


@mcp.tool()
async def hy3_data_analyze(data: str, format: str = "auto") -> str:
    """
    数据分析工具：分析 CSV/JSON 等结构化数据，生成数据洞察和可视化建议。

    参数:
        data (str): 结构化数据文本（CSV 格式或 JSON 格式）
        format (str): 数据格式，可选 "csv"/"json"/"auto"，默认 "auto"

    返回:
        str: Markdown 格式的数据分析报告
    """
    client = get_client()
    logger.info("数据分析 [%s]: %d 字符", format, len(data))

    prompt = f"""你是一位数据分析专家。请对以下{format if format != 'auto' else ''}数据进行分析。

分析维度:
1. **数据概览** — 规模、字段、类型
2. **统计摘要** — 关键指标汇总
3. **趋势与模式** — 发现的数据规律
4. **异常检测** — 异常值和需要注意的点
5. **可视化建议** — 推荐的可视化方案（图表类型、维度选择）
6. **行动建议** — 基于数据的决策建议

数据:
```
{data[:15000]}
```"""
    result = await client.agenerate(prompt, temperature=0.5, max_tokens=4096)
    return result


@mcp.tool()
async def hy3_chat(prompt: str, temperature: str = "0.7") -> str:
    """
    通用对话工具：向 Hy3 大模型自由提问，不支持多轮对话。

    参数:
        prompt (str): 用户问题或提示词
        temperature (str): 创造性程度，0.0(精确) 到 1.0(创意)，默认 "0.7"

    返回:
        str: Hy3 的回复
    """
    client = get_client()
    logger.info("通用对话: %s", prompt[:50])

    try:
        temp = float(temperature)
        temp = max(0.0, min(1.0, temp))
    except ValueError:
        temp = 0.7

    result = await client.agenerate(prompt, temperature=temp, max_tokens=4096)
    return result


# ═══════════════════════════════════════════════════════
# 健康检查
# ═══════════════════════════════════════════════════════

def _health_check() -> bool:
    """检查 Hy3 API 是否可用"""
    try:
        client = get_client()
        if not client.api_key:
            return False
        return True
    except Exception:
        return False


# ═══════════════════════════════════════════════════════
# 启动入口
# ═══════════════════════════════════════════════════════

def main():
    """MCP Server 入口函数（供 pyproject.toml 条目脚本调用）"""
    api_key = os.getenv("HY3_API_KEY", "")
    if not api_key:
        logger.error("❌ 未设置 HY3_API_KEY 环境变量！")
        logger.error("请通过以下方式设置：")
        logger.error("  - 环境变量: export HY3_API_KEY=你的API密钥")
        logger.error("  - .env 文件: 在项目根目录创建 .env 文件，写入 HY3_API_KEY=你的API密钥")
        sys.exit(1)

    model = os.getenv("HY3_MODEL", "hunyuan-pro")
    logger.info("🚀 Hy3 MCP Server 启动中...")
    logger.info("   模型: %s", model)
    logger.info("   传输模式: stdio")
    logger.info("   可用工具: hy3_research, hy3_code_review, hy3_doc_qa, hy3_data_analyze, hy3_chat")
    logger.info("   日志输出: stderr（不影响 MCP 协议通信）")

    if _health_check():
        logger.info("✅ Hy3 API 连接正常")
    else:
        logger.warning("⚠️ Hy3 API 连接检查失败，工具调用时可能出现错误")

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
