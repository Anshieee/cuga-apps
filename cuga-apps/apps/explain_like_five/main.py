"""
Explain Like I'm Five — CUGA Demo App

Type any concept, like "black holes", "inflation" or "how vaccines work", and get
it explained at the level you choose: a 5-year-old, a teenager, or an adult new
to the topic. Every explanation is grounded in the Wikipedia article.

Usage:
  python main.py [--port 28830] [--provider anthropic] [--model claude-sonnet-4-6]

Required env vars:
  LLM_PROVIDER          — LLM backend: anthropic | openai | rits | watsonx | litellm | ollama
  LLM_MODEL             — Model name for the chosen provider
  AGENT_SETTING_CONFIG  — Path to the agent settings TOML file

Optional env vars (provider-specific):
  ANTHROPIC_API_KEY     — Required when LLM_PROVIDER=anthropic
  OPENAI_API_KEY        — Required when LLM_PROVIDER=openai
  RITS_API_KEY          — Required when LLM_PROVIDER=rits
"""

import argparse
import logging
import os
import sys
import uuid
from pathlib import Path

# ---------------------------------------------------------------------------
# Path bootstrap — must come before local imports
# ---------------------------------------------------------------------------
_DIR       = Path(__file__).parent
_DEMOS_DIR = _DIR.parent
for _p in [str(_DIR), str(_DEMOS_DIR)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

# Robustness: AGENT_SETTING_CONFIG may arrive as an in-IMAGE absolute path
# (e.g. /app/apps/settings.watsonx.toml from build/.env) while running from a
# local checkout where it doesn't exist. CUGA aborts on a missing config file,
# so remap a non-existent absolute config to a local file of the same name.
_asc = os.environ.get("AGENT_SETTING_CONFIG", "")
if os.path.isabs(_asc) and not os.path.isfile(_asc):
    for _cand in (_DIR / os.path.basename(_asc), _DEMOS_DIR / os.path.basename(_asc)):
        if _cand.is_file():
            os.environ["AGENT_SETTING_CONFIG"] = str(_cand)
            break

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Third-party imports (after path bootstrap)
# ---------------------------------------------------------------------------
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from langchain_core.tools import tool
from pydantic import BaseModel

from ui import _HTML

# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

def _make_tools():
    # Delegated to MCP server(s): knowledge.
    from _mcp_bridge import load_tools
    return load_tools(["knowledge"])


# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

_SYSTEM = """\
You explain concepts simply and accurately.

For every question:
1. Find the topic with search_wikipedia, then read it with get_article_summary.
2. Decide the audience from the question: "like I'm 5" / "kid" → a young child; "teenager" → a teen; otherwise → an adult who is new to the topic.
3. Answer with:
   - **In one sentence:** the idea in the simplest words that are still true.
   - **An everyday picture:** one analogy the audience already knows (toys, cooking, sports…).
   - **Three things to remember:** short bullets.
   - **Source:** the Wikipedia article title and URL you read.
Keep it under 150 words for a child, 250 otherwise. Never invent facts that are not in the article; if the article doesn't cover something, say so.
"""


# ---------------------------------------------------------------------------
# Agent factory
# ---------------------------------------------------------------------------

def make_agent():
    from cuga.sdk import CugaAgent
    from _llm import create_llm

    return CugaAgent(
        model=create_llm(
            provider=os.getenv("LLM_PROVIDER"),
            model=os.getenv("LLM_MODEL"),
        ),
        tools=_make_tools(),
        special_instructions=_SYSTEM,
        cuga_folder=str(_DIR / ".cuga"),
        # Each question is independent — disable the persistent knowledge store
        # and on-disk policy auto-load so nothing carries across questions via
        # the shared .cuga folder.
        enable_knowledge=False,
        auto_load_policies=False,
    )


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

def _web(port: int):
    import uvicorn

    app = FastAPI(title="Explain Like I'm Five", version="1.0.0")

    # Lazy-initialise the agent on first request so startup is instant
    _agent = None

    def _get_agent():
        nonlocal _agent
        if _agent is None:
            log.info("Initialising CugaAgent…")
            _agent = make_agent()
            log.info("CugaAgent ready.")
        return _agent

    class AskRequest(BaseModel):
        question: str

    @app.get("/", response_class=HTMLResponse)
    async def index():
        return HTMLResponse(_HTML)

    @app.post("/ask")
    async def ask(req: AskRequest):
        from _usage import track_utterance; track_utterance(req.question)
        thread_id = str(uuid.uuid4())
        try:
            agent = _get_agent()
            result = await agent.invoke(req.question, thread_id=thread_id)
            # Return the agent's synthesised answer, NOT str(result): the
            # result object's repr dumps the CUGA plan + generated Python code,
            # which is what was leaking into the UI as an unformatted code blob.
            answer = result.answer if hasattr(result, "answer") else str(result)
            return {"answer": answer}
        except Exception as exc:
            log.exception("Agent invocation failed")
            return JSONResponse(status_code=500, content={"answer": f"Error: {exc}"})

    @app.get("/health")
    async def health():
        return {"ok": True}

    # Public deployment: layered, in-memory rate limiting on POST.
    from _ratelimit import install_rate_limit
    install_rate_limit(app)
    from _usage import install_usage
    install_usage(app)
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Explain Like I'm Five — CUGA demo app")
    parser.add_argument("--port", type=int, default=28830)
    parser.add_argument(
        "--provider", "-p", default=None,
        choices=["rits", "watsonx", "openai", "anthropic", "litellm", "ollama"],
    )
    parser.add_argument("--model", "-m", default=None)
    args = parser.parse_args()

    if args.provider:
        os.environ["LLM_PROVIDER"] = args.provider
    if args.model:
        os.environ["LLM_MODEL"] = args.model

    print(f"\n  Explain Like I'm Five  →  http://127.0.0.1:{args.port}\n")
    _web(args.port)
