# Code Explainer

Paste a snippet of code in any language and get a beginner-friendly walkthrough:
which language it is, what it does in one sentence, a line-by-line explanation,
and (for Python) whether it even runs.

## Port

**28838**

## Quick start

```bash
pip install -r requirements.txt

# Set required env vars (example: OpenAI), or use Ollama for free local answers
export LLM_PROVIDER=openai
export LLM_MODEL=gpt-4o
export OPENAI_API_KEY=sk-…
export AGENT_SETTING_CONFIG=settings.openai.toml
export MODEL_NAME=gpt-4o

python main.py --port 28838
# open http://127.0.0.1:28838
```

## Example prompts

1. `Explain: for i in range(3): print(i * i)`
2. `What does this do? const add = (a, b) => a + b;`
3. `Explain this SQL: SELECT name FROM users WHERE age > 30`
4. `Is this valid Python? def f(x) return x`
5. `Walk me through a list comprehension: [x for x in range(10) if x % 2 == 0]`

## Tools

All tools come from the hosted **code** MCP server (no extra API keys):

| Tool | Description |
|---|---|
| `detect_language` | Identifies the programming language of a snippet |
| `check_python_syntax` | Validates Python syntax and reports line numbers on errors |
| `extract_code_metrics` | Basic metrics (lines, complexity hints) for longer snippets |
