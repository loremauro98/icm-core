# `delegation-plan` — Plan & Delegation Gate

> Consulted by `skills-orchestrator` immediately after the pre-flight tag, and by every agent before dispatching a subagent.
> Authority for the planner tier and the subagent model policy.

## The gate

Every task gets a one-line decision. A non-trivial task (3+ steps, or 2+ independent work units) gets the full block:

```text
[Plan: <n> steps | Planner: <tier> (<model>) | Delegation: none|parallel|pipeline|fan-out-fan-in | Subagents: <role×n> (<model>) | Verify: <command/test>]
```

Then 3-6 numbered steps, each with an owner (`main` or the subagent role) and a concrete output.

Trivial (≤2 steps, one file, no independent unit) → skip the block; do the work.

## Planner tier

The user sets it inline: `planner=strong|standard|cheap|<provider/model>`.

| Tier | Example (OpenCode Go, 2026) | Use for |
|---|---|---|
| `strong` | Kimi K3.1 Pro | architecture, hard debugging, science/terminal-heavy runs |
| `standard` | Claude Haiku 5.5 (max) | routine code changes, tests, reviews, mixed work |
| `cheap` | DeepSeek V4.1 Flash (max) or GPT-6 Luna (max) | small edits, lookups, mechanical work |
| `<model>` | exactly what the user named | overrides the tier |

Projects on other providers map the same three tiers to their own models.

- If the token is omitted, the current session model plans and is named in the block.
- Never upgrade or downgrade the planner silently. State it, then use it.
- The planner runs in the main thread. Planning is never delegated to a subagent.

Evidence from AA Intelligence Index v5.0.1: Kimi K3.1 Pro is #1 on Terminal-Bench 4.0 (67.2%) and the best Go model on Terminal-Bench-Science (34.3%); Claude Haiku 5.5 (max) is the best Go model on FrontierCode 2.0 (34.9%).

## Subagent model policy

**Subagents are cheap/flash only.** If a task needs a frontier model, it stays in the main thread.

- **Always pass `model` explicitly.** An omitted model inherits the session's model.
- **Allowed class:** AA cost per task ≤ ~$1. Examples: Claude Haiku 5.5 (high), DeepSeek V4.1 Flash (high), GPT-6 Luna (max), MiMo-V2.6-Pro, GLM-5.3-Flash, Qwen3.8 Flash, MiniMax M3.1 Flash.
- **Never as a subagent:** Kimi K3.1 Pro, Gemini 4 Argon, Claude Sonnet/Opus/Fable, GPT-6 Astra/Sol/Terra, Grok 4.7, Qwen3.8 Max, GLM-5.3, Step 5 Preview, or anything above ~$1 per AA task.
- **Role defaults:** code edits → Claude Haiku 5.5 (high); discovery/reads/test runs → DeepSeek V4.1 Flash (high) or GPT-6 Luna (max); bulk mechanical → GPT-6 Luna (max); final whole-branch review → main thread on the planner.
- **Turn count beats token price.** A cheap model that takes 3× the turns can cost more; use Haiku/DeepSeek as the floor for multi-step work.

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

Standard, one cheap subagent:

```text
[Plan: 3 steps | Planner: standard (Claude Haiku 5.5 max) | Delegation: pipeline 1 → 1 | Subagents: explorer×1 (DeepSeek high) | Verify: pytest tests/test_spatial_bins.py]
1. Explorer: locate the polar-bin authority and its consumers (DeepSeek high, read-only)
2. Main: patch the bin geometry + add the failing test
3. Main: run pytest and report
```

Large, fan-out with approval:

```text
[Plan: 5 steps | Planner: strong (Kimi K3.1 Pro) | Delegation: fan-out 3 → merge | Subagents: explorer×2 (DeepSeek high), test×1 (Haiku high) | Verify: pytest tests/ -k "manifold or glm"]
1. Explorers: map the three pipeline entry points (parallel, read-only)
2. Main: choose the change and the test
3. Test subagent: write the failing test (Haiku high)
4. Main: implement, run, and fix
5. Main: full verify + outcome-first report
```

## Anti-patterns

| Thought | Reality |
|---|---|
| "Two subagents will make this faster" | Only if the units are independent. Otherwise they collide. |
| "The planner is a subagent" | Planning stays in the main thread. |
| "Kimi is cheap enough for a subagent" | It is not. Haiku may be; check the class rule. |
| "I'll omit `model` and let it inherit" | It inherits the session model — the exact thing this gate prevents. |
| "The final review can be a frontier subagent" | Final review runs in the main thread on the planner. |
| "I'll spawn first, plan after" | Plan and delegation are decided before the first spawn. |
