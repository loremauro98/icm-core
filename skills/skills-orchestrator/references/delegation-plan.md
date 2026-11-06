# `delegation-plan` — Plan & Delegation Gate

> Consulted by `skills-orchestrator` immediately after the pre-flight tag, and by every agent before dispatching a subagent.
> Authority for the harness declaration, the plan mode, and the executor model per harness.

## The gate

Every task gets a one-line decision. A non-trivial task (3+ steps, or 2+ independent work units) gets the full block:

```text
[Plan: <n> steps | Harness: antigravity|opencode | Plan: local|delegate (<model>) | Executors: <model> | Delegation: none|parallel|pipeline|fan-out-fan-in | Verify: <command/test>]
```

Then 3-6 numbered steps, each with an owner (`main` or the subagent role) and a concrete output.

Trivial (≤2 steps, one file, no independent unit) → skip the block; do the work.

## 1. Harness

Declared in the pre-flight tag and never assumed:

```text
[Intent: <Category 1-7> | Skill Stack: <skills> | Env: <conda-env> | Harness: antigravity|opencode]
```

The harness decides the executor model. If it cannot be told, ask one line and stop.

## 2. Plan mode

The user sets it inline: `plan=local|delegate`. Default `local`.

| Mode | Who plans | Output |
|---|---|---|
| `local` | the model already selected in this harness | the plan, in the main thread |
| `delegate` | an external worker (Argon in Antigravity or the Gemini app) | a copy-paste prompt plus the exact file paths to attach; nothing else |

- The local selected model drafts the delegate prompt. Planning is never delegated to a subagent.
- In `local`, never swap the selected model silently.
- In `delegate`, the local thread still owns acceptance: it checks the returned plan against the repo before any subagent runs.

### Delegate output

In `delegate`, the answer in the chat is exactly two things:

1. one copy-paste prompt for the external worker;
2. the exact file paths to attach alongside it.

No plan, no context folder, no ad hoc documents.

The prompt must require the external worker to answer with:

- **a concise answer**, in the form of a single copy-paste prompt;
- **no verbose explanation** of what or why outside that prompt;
- **a final `Expected outputs` list** that the local run fills and the user pastes back.

### Return loop

1. The user pastes the external answer back.
2. The local thread checks every path, symbol, and parameter against the repo; reject or fix before dispatch.
3. Execute with local subagents.
4. Collect the expected outputs and present them for the user to paste back.

## 3. Executors

Subagents are cheap/flash only and always receive an explicit `model`.

| Harness | Executor |
|---|---|
| Antigravity | Gemini 3.8 Flash |
| OpenCode | DeepSeek V4.1 Flash |

- The executor is fixed per harness; the user does not pick it per task.
- Frontier models are never subagents. If a task needs one, it stays in the main thread on the selected model.
- The final whole-branch review runs in the main thread on the selected model.
- Turn count beats token price. A cheap model that takes 3× the turns can cost more.

## Delegation patterns

| Pattern | When | Shape |
|---|---|---|
| `none` | shared state, sequential reasoning, one file, or the work needs the conversation | main thread does it |
| `parallel` | independent reads/lookups/tests with disjoint scopes | N subagents in one batch, then merge |
| `pipeline` | stages depend on each other (explore → implement → review) | one subagent per stage, explicit handoff artifact |
| `fan-out-fan-in` | broad exploration, one synthesis | N scouts, main thread merges |

Preconditions for any delegation: disjoint files/scopes, no shared mutable state, a required return format, and a named verification step.

Do **not** delegate: raw-data decisions, statistical parameter choices, final merges, or anything that needs the conversation context.

## Approval

- **Trivial** → no gate.
- **Standard** → emit the block and proceed.
- **Large, ambiguous, or irreversible** → emit the block and wait for the user's explicit yes before spawning or editing.
- The user can say "just do it" to skip the wait; the block is still recorded.

## Verification

Every plan ends with `Verify:` — a command, test, or artifact. Work is not done until that check passes. This is the same gate as `verification-before-completion`.

## Examples

Local planning, one cheap subagent:

```text
[Plan: 3 steps | Harness: opencode | Plan: local (selected) | Executors: DeepSeek V4.1 Flash | Delegation: pipeline 1 → 1 | Verify: pytest tests/test_spatial_bins.py]
1. Explorer: locate the polar-bin authority and its consumers (DeepSeek Flash, read-only)
2. Main: patch the bin geometry + add the failing test
3. Main: run pytest and report
```

Delegated planning, fan-out context:

```text
[Plan: 3 steps | Harness: opencode | Plan: delegate → Argon | Executors: DeepSeek V4.1 Flash | Delegation: context×2 | Verify: pytest tests/test_spatial_bins.py]
1. Context subagents: map the bin authority and its consumers (read-only)
2. Main: return the copy-paste prompt + the file list
3. (after return) Main: validate against the repo, dispatch, collect the expected outputs
```

## Anti-patterns

| Thought | Reality |
|---|---|
| "The harness can be inferred" | Declare it in the pre-flight tag. The executor depends on it. |
| "Two subagents will make this faster" | Only if the units are independent. Otherwise they collide. |
| "The planner is a subagent" | Planning stays in the main thread. |
| "Delegate can write a context folder" | No. Prompt plus file paths in the chat, nothing else. |
| "The external plan runs as-is" | Validate every path and symbol against the repo first. |
| "I'll omit `model` and let it inherit" | It inherits the session model — the exact thing this gate prevents. |
| "The final review can be a frontier subagent" | Final review runs in the main thread on the selected model. |
| "I'll spawn first, plan after" | Plan and delegation are decided before the first spawn. |
