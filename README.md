# Grok Bot Marketplace archive

Public recipes archived from the [Grok Bot marketplace](https://x.ai/bot/marketplace).

## Layout

- `catalog.json`: index of currently listed bots, all archived bots (with `categories` and `creator`), and `pluginReferences` keyed by marketplace `pluginId`.
- `bots/<slug>/recipe.json`: published profile, `memory`, `gettingStarted`, `plugins`, `listing` metadata (categories, creator, timestamps, `shareId`), and references to skill and routine files.
- `bots/<slug>/skills/<name>.md`: verbatim skill markdown bodies (omitted when a bot has no skills).
- `bots/<slug>/routines/<name>.md`: verbatim routine markdown bodies (omitted when a bot has no routines).

Paths in `catalog.json` are relative to the repository root; `contentFile` paths inside each `recipe.json` are relative to that bot's directory.

## Update

Run `python3 sync.py` with Python 3.9+ (standard library only, no external dependencies). Pass `--output DIR` to write to another directory.

The script discovers bot links from `https://x.ai/bot/marketplace` and fetches each recipe through `api2.cursor.sh` (`aiserver.v1.GrokBotService/GetPublicGrokBotMarketplaceListing`) and its signed template URL. Each bot is validated before writing; stale skill or routine files are pruned per synced bot, while bots that leave the marketplace or fail to download remain intact. The command reports individual failures and exits nonzero if any bot fails. An unchanged upstream recipe produces no diff.

## Scope & plugins

Plugins in Grok Bot are platform-hosted SaaS/MCP connectors (such as Slack, Notion, Linear, Figma, and Google Workspace), not files bundled with a bot recipe. Each bot's `recipe.json` stores only the connector reference (`pluginId`, `name`, and bot-specific `description`), which is also indexed in `catalog.json`. Plugin implementations and built-in tool schemas are not exposed by the public recipe API, and this archive does not install or run any bot or plugin.
