"""
Framework Exporter Manifest & Taxonomy.

Defines the classification of portable vs domain-specific skills,
template configurations, and default workspace definitions for the
Interpretable Context Methodology (ICM) Operating System.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set

# Core skills included in any portable ICM installation
CORE_PORTABLE_SKILLS: List[str] = [
    # Orchestration & Lifecycle
    "skills-orchestrator",
    "skills-route",
    "project-checkpoint",
    "icm-maintenance",
    "strict-agent-pipeline",
    "verification-before-completion",
    "goal",
    "lookback",
    "icm-init",
    # Engineering & Quality
    "brainstorming",
    "writing-plans",
    "executing-plans",
    "test-driven-development",
    "systematic-debugging",
    "subagent-driven-development",
    "dispatching-parallel-agents",
    "requesting-code-review",
    "receiving-code-review",
    "finishing-a-development-branch",
    "using-git-worktrees",
    "writing-skills",
    "robustness-audit",
    "diagnosing-superpowers",
    "module-migrator",
    # Data & Analytics Discipline
    "transparent-data-masker",
    "statistical-batch-orchestrator",
    "jupyter-pickle-rescuer",
    "run-experiment",
    "datavis",
    "master-presenter",
    "flavio",
    "scientific-pdf-dashboard",
    # High-level Problem Solving & Debate
    "experts_council",
    "fable-method",
    "fable-loop",
    "fable-judge",
    "fable-domain",
    "prompter",
    "graphify",
    "graphify-agentic-extraction",
]

# Scientific & Research extensions (can be toggled with --profile=science)
SCIENCE_EXTENSION_SKILLS: List[str] = [
    "literature-search",
    "literature-to-algorithm",
    "scientific-bullshit-detector",
    "peri-event-tuning",
]

# Skills strictly domain-specific to the source repo (excluded from export)
REPO_SPECIFIC_SKILLS: Set[str] = {
    # Any custom pipeline-locked scripts not suitable for fresh projects
}


@dataclass
class WorkspaceDefinition:
    name: str
    purpose: str
    inputs: str
    process: str
    outputs: str
    constraints: List[str] = field(default_factory=list)


DEFAULT_WORKSPACES: Dict[str, WorkspaceDefinition] = {
    "src": WorkspaceDefinition(
        name="src",
        purpose="Pure, stateless computational engines and core business/algorithmic logic.",
        inputs="Configuration objects, raw data structures, or explicit mathematical specifications.",
        process="Pure functions, typed classes, vectorized math. Zero global state. Must never import from ops.",
        outputs="Deterministic return values, transformed tensors/dataframes, fitted model objects.",
        constraints=[
            "Strictly stateless and pure functions where possible.",
            "Must never import from /ops (strict one-way dependency: ops -> src).",
            "Must be accompanied by headless unit tests.",
        ],
    ),
    "ops": WorkspaceDefinition(
        name="ops",
        purpose="Pipeline orchestration, workflow runners, evaluation scripts, and reports.",
        inputs="Stable outputs from /data, configuration specs, engines from /src.",
        process="Batch iteration, multiprocessing orchestration, metric aggregation, report generation.",
        outputs="Run artifacts, benchmark metrics, processed datasets into /data, presentation decks.",
        constraints=[
            "One-way dependency on /src.",
            "Must not re-implement core math — call /src engines instead.",
            "Expose all hyperparameters, seeds, and cutoff thresholds in signatures or configs.",
        ],
    ),
    "data": WorkspaceDefinition(
        name="data",
        purpose="Read-only empirical data, reference benchmarks, and stabilized outputs.",
        inputs="External experimental data, raw logs, imported datasets.",
        process="Storage and access only. Agents must never overwrite or delete raw data.",
        outputs="Versioned datasets and stable checkpoints.",
        constraints=[
            "NEVER modify or mutate raw data — treat as strictly immutable.",
            "Intermediate caches go to current_output/ or temporary folders.",
            "Large data files must be ignored by version control.",
        ],
    ),
    "planning": WorkspaceDefinition(
        name="planning",
        purpose="Task tracking, architectural specifications, design documents, and decisions.",
        inputs="User requirements, GitHub issues, experimental hypotheses.",
        process="Design iterations, 80/20 planning phase, implementation specifications.",
        outputs="Task description files under planning/tasks/ (e.g. task_<name>.md).",
        constraints=[
            "All active tasks must have a markdown log in planning/tasks/.",
            "Completed tasks are archived to planning/tasks/archive/ during /project-checkpoint.",
            "Never write ad-hoc task notes to the repository root.",
        ],
    ),
    "docs": WorkspaceDefinition(
        name="docs",
        purpose="Permanent architecture blueprints, scientific literature, guides, and CHANGELOG.",
        inputs="Project milestones, finalized specifications, paper citations.",
        process="Documentation synchronization, literature indexing, version history.",
        outputs="System manuals, architecture diagrams, CHANGELOG.md records.",
        constraints=[
            "Keep structure synchronized via sync_tree / icm-maintenance.",
            "Maintain permanent audit log in docs/CHANGELOG.md.",
        ],
    ),
}
