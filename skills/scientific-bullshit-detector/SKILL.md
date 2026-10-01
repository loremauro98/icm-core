---
name: scientific-bullshit-detector
description: >-
  A heavy, standalone research skill to assess the appropriateness of statistical methods 
  against current literature using arXiv, spotting inconsistencies and proposing validations.
---

# Scientific Bullshit Detector

## Overview
This is a deep, standalone academic research skill. When you invoke this skill, the agent will cross-reference the project's statistical methodology against the latest scientific literature to actively hunt for inconsistencies, hidden assumptions, or outdated practices.

## Dependencies
- **literature-search-arxiv**: Used to query arXiv for papers performing the same analysis.
- **literature-to-algorithm**: Used in concert to map academic math back to Python engines.

## Workflow

### 1. Methodology Extraction
- Read the project's `math_spec.md` or the `CONTEXT.md` of the target analytical pipeline (e.g., `src/apa_spatial_tuning`).
- Extract the core statistical methods being used (e.g., Pearson correlation, FDR correction, shuffling distributions, Skaggs information).

### 2. Deep Literature Review
- Use the `literature-search-arxiv` skill to query recent neuroscientific literature addressing the same or similar problems.
- Download and read the abstracts/methodology sections of relevant papers.

### 3. Cross-Referencing & Auditing
- Compare our methodology against the literature.
- **Spot Differences**: Are we using a different null-distribution shuffling method than the standard?
- **Spot Inconsistencies**: Are there hidden assumptions in our methods, or flaws in theirs?
- **Assess Appropriateness**: Is the FDR correction method appropriate for this specific type of single-cell data?

### 4. Redact Final Recap
- Generate a comprehensive Markdown report detailing the findings.
- Explicitly propose changes to the code, or scientifically validate the current method.
- Save this report permanently in `/docs/` (e.g., `docs/bullshit_detector_report_[topic].md`) and present it to the user.
