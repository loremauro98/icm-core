---
name: literature-to-algorithm
description: >-
  Translates scientific literature and laboratory methodology into a statistically 
  robust Python analytical engine, complete with formal mathematical specifications 
  and null-distribution shuffling.
---

# Literature to Algorithm

## Overview
A workflow protocol for moving from the "Methods" section of a scientific paper to a robust Python class. This skill enforces a structured progression: literature search -> formal mathematical specification -> Python implementation with statistical rigour (parallelized null-shuffling).

## Dependencies
- **research subagent**: Required to search the web and literature for the requested methodologies.

## Quick Start
"Extract the Fenton Lab's spatial tuning methodology for the APA task and implement it as a Python engine."

## Workflow

### 1. Literature Search
- Spawn a `research` subagent to search the web and literature for how the specified lab or author calculates the requested metric.
- Ensure you extract exact mathematical formulas, filtering thresholds, and statistical approaches (e.g., circular statistics vs. standard Skaggs information).

### 2. Formal Specification
- Do NOT jump straight to code.
- Write a formal `math_spec.md` artifact detailing the mathematical formulas, equations, and processing steps extracted from the literature.
- **IMPORTANT**: The reference to the paper(s) or authors MUST be clearly stated at the top of the methodology specification.
- Request user approval on this specification before writing code.

### 3. Implementation
- Translate the approved `math_spec.md` into a modular Python class.
- The Python engine MUST include statistical rigour by default. If the metric requires a null-distribution for significance (as is common in computational neuroscience), implement parallelized shuffling directly into the engine.

### 4. Verification
- Create a testing Jupyter Notebook or script to verify the engine executes correctly on a sample of data.

## Common Mistakes
- **Skipping the Math Spec**: Going straight from web search to code results in hidden assumptions. Always generate the intermediate `math_spec.md`.
- **Ignoring Null Distributions**: Biological metrics require statistical baselines. Do not write a metric without its corresponding null-shuffle logic unless explicitly told otherwise.
