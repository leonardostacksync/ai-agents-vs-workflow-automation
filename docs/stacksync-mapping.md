# How this maps to Stacksync

If you use Stacksync, the two sides of this guide are two products that share connectors, approvals and logs.

| Idea in this guide | On Stacksync |
|---|---|
| Deterministic workflow | [Workflow Automation](https://www.stacksync.com/workflow-automation): triggers on records created, updated or deleted in configured systems, conditional logic, retries, execution logs and code or visual configuration |
| Human-in-the-loop | Approval gates that pause a run for sign-off, then resume |
| Replay | Replay a whole workflow or only the failed modules and their dependencies |
| Event buffering | [Event queues](https://www.stacksync.com/event-queues) for ordered, durable event processing |
| Agent | [Genies](https://www.stacksync.com/ai-agents): AI agents that read connected ERP, CRM, database and support systems and act across them, with approval steps and a log of every run |
| Build from an assistant | [Stacksync MCP](https://www.stacksync.com/mcp) lets Claude, ChatGPT or Cursor build and run both |
| Fresh data for the agent | [Two-way sync](https://www.stacksync.com/two-way-sync) keeps a current copy of ERP and CRM records in a database the agent can query |
| No-AI path | Two-way sync and workflows run without Copilot or Genies |

Two things to check before you rely on any of it:

- **Triggers depend on the system, connector, event and permissions.** Confirm what your systems support.
- **Replay and retry are different.** Workflow replay reruns a workflow or failed modules. A sync issue retry retries the current source state. Test duplicate handling before using either in production.
