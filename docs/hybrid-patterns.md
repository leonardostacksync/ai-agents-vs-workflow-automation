# Five hybrid patterns

Most real jobs are not purely one or the other. These five combinations cover most of them.

## 1. Workflow with one model step

The flow is fixed, but one step needs language understanding (classify a message, extract fields from a document). The model returns a value, the workflow does everything else.

**Use when:** the sequence never changes but one input is messy.

## 2. Workflow first, agent for exceptions

Rules handle the known cases. Only what fails the rules goes to an agent, which proposes. See [`hybrid_pipeline.py`](../code/patterns/hybrid_pipeline.py).

**Use when:** most cases are routine and a minority need judgment.

## 3. Agent that calls workflows as tools

The agent decides what to do, but each action is a vetted workflow with its own approvals and retries. The agent never touches the raw API.

**Use when:** you want judgment on what to do, and determinism in how it is done.

## 4. Approval gate between the two

The agent proposes, a person approves, the workflow executes. The decision is logged with who made it.

**Use when:** a write is hard to undo.

## 5. Agent that graduates to a workflow

Run an agent while the problem is new. When its decisions become identical run after run, replace them with a workflow and keep the agent for what still varies.

**Use when:** you are still learning the rules.

## Choosing

| If you know... | Start with |
|---|---|
| The rule and the steps | Workflow |
| The goal but not the steps | Agent with guardrails |
| The rule for most cases | Pattern 2 |
| The risky actions | Pattern 3 or 4 |
| Neither yet | Pattern 5 |
