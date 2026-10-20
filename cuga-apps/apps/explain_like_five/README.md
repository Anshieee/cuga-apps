# Explain Like I'm Five

Type any concept, like "black holes", "inflation" or "how vaccines work", and get it explained at the level you choose: a 5-year-old, a teenager, or an adult new to the topic. Every explanation is grounded in the Wikipedia article.

## Port

**28830**

## Quick start

```bash
# Install dependencies
pip install -r requirements.txt

# Run
python main.py --port 28830

# Open in browser
open http://127.0.0.1:28830
```

## Example prompts

- `Explain black holes like I'm 5`
- `What is inflation? Explain for a teenager`
- `How do vaccines work, in simple words?`
- `Explain blockchain to my grandma`
- `What is photosynthesis? Kid level`

## Tools

All tools are provided via the shared `knowledge` MCP server:

| Tool | Description |
|---|---|
| `search_wikipedia` | Searches Wikipedia for relevant articles by title/query |
| `get_article_summary` | Retrieves the summary text and URL of a Wikipedia article |
