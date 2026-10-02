# Compare Two Things

A CUGA-powered demo app that compares any two subjects side by side using Wikipedia as its only source. Ask "Python vs Java" or "Mars vs Venus" and get a structured markdown table, a biggest-difference callout, and a "when to pick which" guide.

## Port

**28833**

## Quick start

```bash
pip install -r requirements.txt

export LLM_PROVIDER=openai
export LLM_MODEL=gpt-4o
export OPENAI_API_KEY=<your-key>
export AGENT_SETTING_CONFIG=/path/to/settings.toml

python main.py --port 28833
open http://127.0.0.1:28833
```

## Example Prompts
- Python vs Java
- Crocodile vs alligator
- Mars vs Venus
- Tea vs coffee
- Baroque vs Renaissance art

## Tools
|Tool | Source | Description |
|---|---|---|
|`search_wikipedia`|`knowledge` MCP server | Search Wikipedia for an article by topic |
|`get_article_summary`|`knowledge` MCP server | Fetch the summary of a Wikipedia article |
