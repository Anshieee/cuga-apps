# On This Day

Ask about any calendar date and the agent reads Wikipedia's date article to return
5 notable events, 3 famous birthdays, and a fun fact for that date.

## Run

```bash
cd apps/on_this_day
python main.py --port 28834
# open http://localhost:28834
```

## Example prompts

- What happened on this day?
- On this day: July 20
- Famous birthdays on March 14
- What happened on December 25 in history?
- Give me a fun fact for February 29

## Tools used

Both tools come from the shared **knowledge** MCP server (port 29101):

| Tool | Purpose |
|---|---|
| `get_article_summary` | Fetches the intro/summary of a Wikipedia date article |
| `get_article_sections` | Fetches the Events and Births sections of the article |

## Environment

Set the same env vars as every other app — see `build/.env.example`. No extra
API keys are needed: the knowledge MCP server uses Wikipedia (public, no key).
