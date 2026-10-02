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
