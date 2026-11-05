# Prompts to build each pattern from your AI assistant

Connect the Stacksync MCP server first (`https://mcp.stacksync.com/mcp`, OAuth, no API key in the chat), then ask "List my Stacksync workspaces." Every prompt asks the assistant to inspect first and wait for your confirmation.

## A workflow (the deterministic pattern)

```text
List my connections, syncs and workflows first so nothing is built twice. Then propose a scheduled workflow that matches payment payouts to bank deposits and ERP records on payout ID, amount and date window, and writes unmatched items to an exceptions table. Use a workflow only, no AI agent. Show each step and the matching keys, and wait for my confirmation before creating anything.
```

## An agent (the judgment pattern)

```text
Inspect my connections for Slack, Shopify and the fulfillment system. Propose a read-only Genie that answers order status questions in one Slack channel. It must ask for the order number instead of guessing, and it must not change any order. Confirm the channel and the scope before creating anything.
```

## A hybrid (workflow plus an agent for exceptions)

```text
Inspect my ERP and the system that holds purchase orders. Propose a workflow that matches invoices to purchase orders on vendor, invoice number and amount, plus a Genie that handles only the invoices that do not match. The Genie may propose, never write. Add a duplicate check before every write and an approval step before the ERP write. Wait for my confirmation before creating or deploying anything.
```

## Turn an agent into a workflow

When an agent keeps doing the same thing the same way, make it deterministic:

```text
Look at the runs of my Genie <name>. Which of its decisions were identical every time? Propose a workflow that replaces those steps, and keep the Genie only for the cases that varied. Show the rules you inferred and wait for my confirmation.
```

## Check it works

```text
Show me the last runs of <workflow or Genie>. Where did any fail, and can a failed run be replayed? Do not change anything.
```
