#!/usr/bin/env python3
"""
ICM & Skills Operating System — Standalone Turnkey Bootstrapper.

Initializes, scaffolds, and verifies the Interpretable Context Methodology (ICM)
architecture and Skills Orchestration framework for any project on any computer.
Works across Windows, macOS, and Linux without requiring external dependencies.
"""

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set

# Attempt import from local package if running within repo; fallback to bundled defaults
try:
    from manifest import (
        CORE_PORTABLE_SKILLS,
        DEFAULT_WORKSPACES,
        SCIENCE_EXTENSION_SKILLS,
        WorkspaceDefinition,
    )
except ImportError:
    # Embedded fallback definitions when distributed as standalone file
    CORE_PORTABLE_SKILLS = [
        "skills-orchestrator",
        "skills-route",
        "project-checkpoint",
        "icm-maintenance",
        "strict-agent-pipeline",
        "verification-before-completion",
        "goal",
        "lookback",
        "icm-init",
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
        "transparent-data-masker",
        "statistical-batch-orchestrator",
        "jupyter-pickle-rescuer",
        "run-experiment",
        "datavis",
        "master-presenter",
        "flavio",
        "scientific-pdf-dashboard",
        "experts_council",
        "fable-method",
        "fable-loop",
        "fable-judge",
        "fable-domain",
        "prompter",
        "graphify",
        "graphify-agentic-extraction",
    ]
    SCIENCE_EXTENSION_SKILLS = [
        "literature-search",
        "literature-to-algorithm",
        "scientific-bullshit-detector",
        "peri-event-tuning",
    ]
    DEFAULT_WORKSPACES = {}


def render_template(content: str, variables: Dict[str, str]) -> str:
    """Simple string template substitution replacing {{ KEY }} with value."""
    result = content
    for key, val in variables.items():
        result = result.replace(f"{{{{ {key} }}}}", str(val))
        result = result.replace(f"{{{{{key}}}}}", str(val))
    return result


def setup_skills_junction(target_dir: Path) -> bool:
    """Creates cross-agent junction/symlink from .claude/skills to .agents/skills."""
    agents_skills = target_dir / ".agents" / "skills"
    claude_dir = target_dir / ".claude"
    claude_skills = claude_dir / "skills"

    claude_dir.mkdir(parents=True, exist_ok=True)
    agents_skills.mkdir(parents=True, exist_ok=True)

    if claude_skills.exists() or claude_skills.is_symlink():
        return True

    is_windows = platform.system().lower() == "windows"

    if is_windows:
        # Use Windows directory junction (mklink /J) - requires NO administrator privileges
        cmd = f'cmd /c mklink /J "{claude_skills.resolve()}" "{agents_skills.resolve()}"'
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if res.returncode != 0:
            # Fallback to standard symlink if junction fails
            try:
                os.symlink(agents_skills.resolve(), claude_skills, target_is_directory=True)
                return True
            except OSError as err:
                print(f"[WARN] Failed to link .claude/skills: {res.stderr or err}")
                return False
        return True
    else:
        # POSIX relative symlink
        try:
            rel_path = Path("..") / ".agents" / "skills"
            os.symlink(rel_path, claude_skills, target_is_directory=True)
            return True
        except OSError as err:
            print(f"[WARN] Failed to create symlink: {err}")
            return False


def copy_skills(
    source_skills_dir: Path, target_dir: Path, skill_names: List[str]
) -> List[str]:
    """Copies designated skills from source skills directory to project .agents/skills."""
    dest_skills_dir = target_dir / ".agents" / "skills"
    dest_skills_dir.mkdir(parents=True, exist_ok=True)

    copied: List[str] = []
    for skill_name in skill_names:
        src = source_skills_dir / skill_name
        dest = dest_skills_dir / skill_name
        if src.exists() and src.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest)
            copied.append(skill_name)
    return copied


def scaffold_project(
    target_dir: Path,
    project_name: str,
    project_description: str,
    conda_env: str,
    author: str,
    profile: str = "core",
    custom_skills_source: Optional[Path] = None,
    templates_dir: Optional[Path] = None,
) -> Dict[str, any]:
    """Scaffolds a complete ICM project into target_dir."""
    target_dir = target_dir.resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    # Locate templates directory
    if templates_dir is None or not templates_dir.exists():
        module_dir = Path(__file__).parent.resolve()
        candidates = [
            module_dir / "templates",
            module_dir / ".." / "templates",
            module_dir.parent / "framework_exporter" / "templates",
        ]
        for c in candidates:
            if c.exists() and (c / "AGENTS.md.template").exists():
                templates_dir = c
                break

    if not templates_dir or not templates_dir.exists():
        raise FileNotFoundError("Could not locate framework templates directory.")

    variables = {
        "PROJECT_NAME": project_name,
        "PROJECT_DESCRIPTION": project_description,
        "CONDA_ENV": conda_env,
        "AUTHOR": author,
    }

    # 1. Create Workspace Directories
    workspaces = ["src", "ops", "data", "planning", "docs"]
    for ws in workspaces:
        (target_dir / ws).mkdir(parents=True, exist_ok=True)
    (target_dir / "planning" / "tasks").mkdir(parents=True, exist_ok=True)
    (target_dir / "planning" / "tasks" / "archive").mkdir(parents=True, exist_ok=True)

    # 2. Render AGENTS.md
    agents_tmpl = (templates_dir / "AGENTS.md.template").read_text(encoding="utf-8")
    (target_dir / "AGENTS.md").write_text(
        render_template(agents_tmpl, variables), encoding="utf-8"
    )

    # 3. Render CODE_PIPELINE.md
    pipeline_tmpl = (templates_dir / "CODE_PIPELINE.md.template").read_text(
        encoding="utf-8"
    )
    (target_dir / "CODE_PIPELINE.md").write_text(pipeline_tmpl, encoding="utf-8")

    # 4. Render Workspace CONTEXT.md files
    context_tmpl = (templates_dir / "CONTEXT.md.template").read_text(encoding="utf-8")
    for ws in workspaces:
        ws_def = DEFAULT_WORKSPACES.get(ws) if DEFAULT_WORKSPACES else None
        purpose = (
            ws_def.purpose
            if ws_def
            else f"Workspace for {ws} components and procedures."
        )
        inputs = (
            ws_def.inputs
            if ws_def
            else f"Authorized upstream inputs designated for {ws}."
        )
        process = (
            ws_def.process
            if ws_def
            else f"Procedures and transformations belonging to {ws}."
        )
        outputs = (
            ws_def.outputs if ws_def else f"Artifacts produced under /{ws}."
        )
        constraints = (
            ws_def.constraints
            if ws_def
            else [f"Follow 9-step pipeline before making edits in /{ws}."]
        )

        ws_vars = {
            "WORKSPACE_NAME": ws,
            "WORKSPACE_PURPOSE": purpose,
            "WORKSPACE_INPUTS": inputs,
            "WORKSPACE_PROCESS": process,
            "WORKSPACE_OUTPUTS": outputs,
        }
        content = render_template(context_tmpl, ws_vars)
        # Render constraint items
        constraint_block = "\n".join(f"- **{c}**" for c in constraints)
        content = content.replace(
            "{% for constraint in WORKSPACE_CONSTRAINTS %}\n- **{{ constraint }}**\n{% endfor %}",
            constraint_block,
        )
        (target_dir / ws / "CONTEXT.md").write_text(content, encoding="utf-8")

    # 5. Render Documentation & Changelog
    skills_tmpl = (templates_dir / "CUSTOM_SKILLS.md.template").read_text(
        encoding="utf-8"
    )
    (target_dir / "docs" / "CUSTOM_SKILLS.md").write_text(
        render_template(skills_tmpl, variables), encoding="utf-8"
    )

    changelog_tmpl = (templates_dir / "CHANGELOG.md.template").read_text(
        encoding="utf-8"
    )
    (target_dir / "docs" / "CHANGELOG.md").write_text(
        render_template(changelog_tmpl, variables), encoding="utf-8"
    )

    # 6. Configure .claude settings & output styles
    claude_dir = target_dir / ".claude"
    (claude_dir / "output-styles").mkdir(parents=True, exist_ok=True)

    bluf_content = (templates_dir / "bluf.md").read_text(encoding="utf-8")
    (claude_dir / "output-styles" / "bluf.md").write_text(
        bluf_content, encoding="utf-8"
    )

    settings_content = (templates_dir / "settings.json").read_text(encoding="utf-8")
    (claude_dir / "settings.json").write_text(settings_content, encoding="utf-8")

    # 7. Configure ignores
    gitignore_tmpl = (templates_dir / "gitignore.template").read_text(encoding="utf-8")
    (target_dir / ".gitignore").write_text(gitignore_tmpl, encoding="utf-8")

    graphify_tmpl = (templates_dir / "graphifyignore.template").read_text(
        encoding="utf-8"
    )
    (target_dir / ".graphifyignore").write_text(graphify_tmpl, encoding="utf-8")

    # 8. Copy Skills Bundle
    skills_source = custom_skills_source
    if skills_source is None or not skills_source.exists():
        # Check standard locations
        curr = Path(__file__).parent.resolve()
        candidates = [
            curr / "skills",
            curr / ".." / ".." / ".agents" / "skills",
            curr / ".." / "skills",
            Path.cwd() / ".agents" / "skills",
        ]
        for c in candidates:
            if c.exists() and (c / "skills-orchestrator").exists():
                skills_source = c
                break

    selected_skills = list(CORE_PORTABLE_SKILLS)
    if profile in ("science", "all"):
        selected_skills.extend(SCIENCE_EXTENSION_SKILLS)

    copied_skills: List[str] = []
    if skills_source and skills_source.exists():
        copied_skills = copy_skills(skills_source, target_dir, selected_skills)

    # 9. Establish Cross-Agent Junction
    junction_ok = setup_skills_junction(target_dir)

    # 10. Deploy Rules Bundle
    rules_source = None
    curr = Path(__file__).parent.resolve()
    candidates_rules = [
        curr / "rules",
        templates_dir.parent / "rules",
        templates_dir / "rules",
    ]
    for c in candidates_rules:
        if c.exists() and c.is_dir():
            rules_source = c
            break

    rules_copied = 0
    if rules_source and rules_source.exists():
        dest_rules_dir = target_dir / ".agents" / "rules"
        dest_rules_dir.mkdir(parents=True, exist_ok=True)
        for r_file in rules_source.glob("*.md"):
            shutil.copy2(r_file, dest_rules_dir / r_file.name)
            rules_copied += 1

    return {
        "target_dir": str(target_dir),
        "project_name": project_name,
        "skills_copied": len(copied_skills),
        "rules_copied": rules_copied,
        "junction_created": junction_ok,
    }


def package_distribution(
    export_dir: Path,
    source_root: Path,
    templates_dir: Path,
) -> Path:
    """Builds a complete, standalone distribution package in export_dir ready to push to GitHub."""
    export_dir = export_dir.resolve()
    if export_dir.exists():
        shutil.rmtree(export_dir)
    export_dir.mkdir(parents=True, exist_ok=True)

    # 1. Copy templates
    dest_templates = export_dir / "templates"
    shutil.copytree(templates_dir, dest_templates)

    # 2. Copy portable skills
    source_skills = source_root / ".agents" / "skills"
    dest_skills = export_dir / "skills"
    dest_skills.mkdir(parents=True, exist_ok=True)

    all_export_skills = set(CORE_PORTABLE_SKILLS + SCIENCE_EXTENSION_SKILLS)
    for skill_name in all_export_skills:
        src = source_skills / skill_name
        if src.exists() and src.is_dir():
            shutil.copytree(src, dest_skills / skill_name)

    # 2b. Copy rules
    source_rules = source_root / ".agents" / "rules"
    if not source_rules.exists():
        source_rules = Path(__file__).parent / "rules"
    dest_rules = export_dir / "rules"
    if source_rules.exists() and source_rules.is_dir():
        dest_rules.mkdir(parents=True, exist_ok=True)
        for r_file in source_rules.glob("*.md"):
            shutil.copy2(r_file, dest_rules / r_file.name)

    # 3. Copy bootstrap script itself
    shutil.copy2(__file__, export_dir / "bootstrap.py")

    # 4. Copy manifest
    manifest_src = Path(__file__).parent / "manifest.py"
    if manifest_src.exists():
        shutil.copy2(manifest_src, export_dir / "manifest.py")

    # 5. Write pyproject.toml
    pyproject_content = """[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "icm-core"
version = "1.0.0"
description = "Interpretable Context Methodology (ICM) & Skills Operating System"
readme = "README.md"
requires-python = ">=3.8"
authors = [{ name = "ICM Framework Team" }]
license = { text = "MIT" }

[project.scripts]
icm = "bootstrap:cli"
"""
    (export_dir / "pyproject.toml").write_text(pyproject_content, encoding="utf-8")

    # 6. Write standalone README.md
    readme_content = """# ICM Core — Interpretable Context Methodology & Skills OS

> A turnkey, agentic operating system that pairs **Spatial Context Architecture (ICM)**
> with **Executive Skills Routing** for Python and multi-language projects.
> Works out of the box with Claude Code, Gemini CLI, Antigravity, and Cursor.

## Quickstart

### 1. Initialize a new project in the current directory:
```bash
python bootstrap.py init --name "My Awesome Project" --env myenv
```

### 2. Or using `uvx` (no installation needed):
```bash
uvx --from git+https://github.com/your-username/icm-core icm init
```

## Architecture Summary
- **Layer 1 Map (`AGENTS.md`):** Root routing map, NEVER rules, and intent routing table.
- **Layer 2 Contracts (`CONTEXT.md`):** Room-by-room contracts in `/src`, `/ops`, `/data`, `/planning`, `/docs`.
- **Skills Suite (`.agents/skills/`):** 35+ battle-tested skills for TDD, systematic debugging, data masking, multi-agent expert councils, and automated checkpoints.
- **Cross-Agent Junction:** Automatically mirrors `.agents/skills` to `.claude/skills` via zero-copy junctions.
"""
    (export_dir / "README.md").write_text(readme_content, encoding="utf-8")

    return export_dir


def check_doctor(target_dir: Path) -> Dict[str, bool]:
    """Audits health and integrity of an ICM installation."""
    target_dir = target_dir.resolve()
    results = {
        "agents_map": (target_dir / "AGENTS.md").exists(),
        "code_pipeline": (target_dir / "CODE_PIPELINE.md").exists(),
        "src_context": (target_dir / "src" / "CONTEXT.md").exists(),
        "ops_context": (target_dir / "ops" / "CONTEXT.md").exists(),
        "data_context": (target_dir / "data" / "CONTEXT.md").exists(),
        "planning_context": (target_dir / "planning" / "CONTEXT.md").exists(),
        "docs_context": (target_dir / "docs" / "CONTEXT.md").exists(),
        "agents_skills_dir": (target_dir / ".agents" / "skills").is_dir(),
        "agents_rules_dir": (target_dir / ".agents" / "rules").is_dir(),
        "claude_skills_link": (target_dir / ".claude" / "skills").exists(),
        "output_style_bluf": (
            target_dir / ".claude" / "output-styles" / "bluf.md"
        ).exists(),
    }
    return results


def cli():
    parser = argparse.ArgumentParser(
        description="ICM & Skills Operating System Turnkey Bootstrapper"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # init command
    init_parser = subparsers.add_parser(
        "init", help="Scaffold a new ICM project in target directory"
    )
    init_parser.add_argument(
        "--target",
        "-t",
        default=".",
        help="Target project directory (default: current dir)",
    )
    init_parser.add_argument(
        "--name",
        "-n",
        default=None,
        help="Project display name (default: directory name)",
    )
    init_parser.add_argument(
        "--description",
        "-d",
        default="Modular project built with the ICM architecture.",
        help="Project description",
    )
    init_parser.add_argument(
        "--env",
        "-e",
        default="base",
        help="Primary execution environment name (e.g. conda env)",
    )
    init_parser.add_argument(
        "--author", "-a", default="Author", help="Project author"
    )
    init_parser.add_argument(
        "--profile",
        "-p",
        choices=["core", "science", "all"],
        default="core",
        help="Skill bundle profile to deploy",
    )

    # export command
    export_parser = subparsers.add_parser(
        "export", help="Package ICM framework into a standalone distribution bundle"
    )
    export_parser.add_argument(
        "--dest",
        "-o",
        default="dist/icm-core",
        help="Destination directory for distribution package",
    )

    # doctor command
    doctor_parser = subparsers.add_parser(
        "doctor", help="Audit integrity of an existing ICM installation"
    )
    doctor_parser.add_argument(
        "--target",
        "-t",
        default=".",
        help="Target project directory to audit",
    )

    args = parser.parse_args()

    if args.command == "init":
        target_path = Path(args.target)
        p_name = args.name or target_path.resolve().name.capitalize()
        res = scaffold_project(
            target_dir=target_path,
            project_name=p_name,
            project_description=args.description,
            conda_env=args.env,
            author=args.author,
            profile=args.profile,
        )
        print(f"[SUCCESS] Initialized ICM Project '{p_name}' at {res['target_dir']}")
        print(f" - Skills deployed: {res['skills_copied']}")
        print(f" - Rules deployed: {res.get('rules_copied', 0)}")
        print(f" - Cross-agent junction created: {res['junction_created']}")

    elif args.command == "export":
        script_dir = Path(__file__).parent.resolve()
        source_root = script_dir.parent.parent.resolve()
        tmpl_dir = script_dir / "templates"
        dest_path = Path(args.dest)
        out_dir = package_distribution(dest_path, source_root, tmpl_dir)
        print(f"[SUCCESS] Standalone ICM distribution packaged at: {out_dir}")

    elif args.command == "doctor":
        results = check_doctor(Path(args.target))
        passed = sum(results.values())
        total = len(results)
        print(f"ICM Integrity Healthcheck: {passed}/{total} checks passed.")
        for check, ok in results.items():
            status = "✅ PASS" if ok else "❌ FAIL"
            print(f"  {status} - {check}")


if __name__ == "__main__":
    cli()
