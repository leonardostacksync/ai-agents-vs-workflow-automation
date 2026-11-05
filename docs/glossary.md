# Glossary

**Workflow automation.** A fixed sequence of steps that runs on a trigger (an event or a schedule). The same input gives the same output.

**Deterministic.** Predictable: no randomness in what it does for a given input.

**AI agent.** Software that uses a model to decide which steps to take and which tools to call to reach a goal, within limits you set.

**Agentic workflow.** A workflow in which one or more steps are decided by a model. Often used loosely. See [hybrid patterns](hybrid-patterns.md).

**Tool calling.** A model asking the surrounding code to run a function, such as reading a record.

**MCP (Model Context Protocol).** An open protocol that lets an assistant call tools on an external server. Stacksync runs one at `https://mcp.stacksync.com/mcp`.

**Human-in-the-loop.** A person approves, rejects or edits before the run continues.

**Idempotency.** Running the same operation twice has the same effect as running it once.

**RPA.** Robotic process automation: scripted software that imitates clicks and keystrokes in a user interface. Closer to a workflow than to an agent.

**Two-way sync.** Records stay matched in both systems, with matching keys and conflict handling. A different job from either of the above: it keeps data consistent, and workflows and agents then act on it.

**Genie.** A Stacksync AI agent that reads and acts across connected systems, with approval steps and a run log.
