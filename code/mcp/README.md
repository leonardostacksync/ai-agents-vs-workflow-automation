# Build both from an AI assistant (MCP)

The Stacksync MCP server lets Claude, ChatGPT, Cursor and other assistants build and run workflows and Genies in a Stacksync workspace, with exactly your permissions.

- [`mcp.json`](mcp.json): project config for Claude Code (`.mcp.json`). Other clients: see the [setup guide](https://docs.stacksync.com/mcp).
- [`build-prompts.md`](build-prompts.md): prompts for the workflow, agent and hybrid patterns.

Server URL: `https://mcp.stacksync.com/mcp`. Sign in with OAuth. To limit an assistant to reading, clear "Make changes" on the sign-in page.
