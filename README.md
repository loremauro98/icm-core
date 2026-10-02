# ICM Core — Interpretable Context Methodology & Skills workflow

> A workflow pairing **Interpretable context methodology (ICM)**
> with **Executive Skills Routing** for Python and multi-language projects.
> Works out of the box 

## Quickstart

### 1. Initialize a new project in the current directory:
```bash
python bootstrap.py init --name "My Project" --env myenv
```

### 2. Or using `uvx` (no installation needed):
```bash
uvx --from git+https://github.com/your-username/icm-core icm init
```

## Architecture Summary
- **Layer 1 Map (`AGENTS.md`):** Root routing map, NEVER rules, and intent routing table.
- **Layer 2 Contracts (`CONTEXT.md`):** Room-by-room contracts in `/src`, `/ops`, `/data`, `/planning`, `/docs`.
- **Skills Suite (`.agents/skills/`):** 35+ skills for TDD, systematic debugging, data masking, multi-agent expert councils, and automated checkpoints.
- **Cross-Agent Junction:** Automatically mirrors `.agents/skills` to `.claude/skills` via zero-copy junctions.

## How to use
- Start each session by typing: "read agents.md ... task you want to tackle"
- Example:"hei read agents.md and then look at the arm ... we need to do a control based on this document I just added in docs". The agent will proceed by reading the CONTEXT.md of the specific arm, reading the document, selecting the appropriate skill or skills to achieve the task. The first part of the output will be a short [Intent: .... | Skill Stack: ..... | Env: ....], followed by the action plan.

