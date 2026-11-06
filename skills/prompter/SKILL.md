---
name: prompter
description: Builds an external-planner request — one copy-paste prompt plus the exact file paths to attach — for outsourcing planning to an external LLM or human expert.
---

# `prompter` — External Planning Prompt Generator

Invoked via `/prompter`, "use prompter", "outsource planning for...", "delegate planning", or when the Plan & Delegation Gate selects `plan=delegate`.

The output lives in the chat. Do not write a prompt document, a context folder, or any other artifact.

---

## Workflow

### 1. Receive & clarify

Identify the problem. If the statement lacks essential detail, ask brief clarifying questions before gathering context.

### 2. Gather context

Spawn a read-only context subagent with the harness's native subagent tool. Name it `prompter_context_gatherer` and give it this protocol:

```text
You are a context extraction specialist for the project.
Gather complete, precise context for a given analytical or coding problem so it can be outsourced to an external LLM or human expert.

1. Serena & code search: locate exact functions, data structures, variables, and module boundaries.
2. Graphify: run `graphify query "<problem keywords>"`, `graphify path`, and `graphify explain` to map dependencies.
3. Local context: read `CONTEXT.md` files in the relevant directories, `AGENTS.md`, and any relevant `math_spec.md` or `REFERENCES.md`.
4. Domain constraints: extract key parameters (frame rates, sampling rates, normalization rules, cell counts, shuffle numbers).

Return a structured summary of code references, equations, input/output schemas, and project rules. Also return the exact file paths the external worker needs, ranked by importance.
```

### 3. Write the prompt

Draft a standalone, copy-pasteable Markdown prompt with four sections:

1. **Role** — the expert persona.
2. **Problem** — a clear statement, goals, edge cases, known failure modes.
3. **Context** — a compact summary of the gathered facts and the exact attached file paths; tell the worker to read the attachments first.
4. **Expected output** — the answer contract below.

The answer contract is mandatory. The prompt must require:

- a concise answer, in the form of a single copy-paste prompt;
- no verbose explanation of what or why outside that prompt;
- a final `Expected outputs` section listing the artifacts the local run will fill and the user will paste back.

### 4. Output in the chat

Reply with exactly two things and nothing else:

1. the prompt in one fenced block;
2. an `Attach:` list of the exact file paths.

No preamble, no explanation of the prompt, no saved file.
