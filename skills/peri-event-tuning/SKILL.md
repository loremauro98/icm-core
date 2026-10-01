---
name: peri-event-tuning
description: >-
  Strict architectural and mathematical specifications for analyzing single-cell neural tuning to discrete, time-locked behavioral events (peri-event tuning). Enforces boundary handling, out-of-window sampling, FDR correction, and bootstrapped Bayesian decoding.
---

# Peri-Event Tuning Architecture

## Overview
This skill dictates the formal mathematical pipeline requirements for any script analyzing single-cell tuning aligned to discrete time-locked events (e.g., action bouts, stimuli). It ensures that statistical engine generation rigorously controls for edge-case boundaries, event contamination, and small-sample biases.

## Dependencies
- `statistical-batch-orchestrator`: For standardizing parallelization and FDR correction parameters.
- `transparent-data-masker`: For explicitly tracking and logging any boundary bouts that are dropped.

## Workflow

### 1. Data Integrity & Boundary Exclusion
Before extracting peri-event matrices, you **MUST** validate every single behavioral bout against the edges of the recording session.
- Calculate `window_frames = window_seconds * FPS`.
- For each bout `[start_frame, end_frame]`, verify that `start_frame - window_frames >= 0` and `start_frame + window_frames < total_frames`.
- Any bout that violates this boundary **MUST BE RIGOROUSLY DROPPED**. Do not interpolate or pad with `NaN`s, as this will crash downstream statistical estimators and decoders.
- Use the `transparent-data-masker` logic to log exactly how many bouts were discarded due to boundary restrictions.

### 2. Out-of-Window Null Sampling
Because events are temporally discrete, the null distribution for significance testing MUST be drawn exclusively from **inter-bout intervals** (non-action frames).
- You MUST calculate `valid_centers`: a list of frame indices where the entire surrounding `[-window, +window]` block does not overlap with any behavioral bout.
- Do NOT use standard circular permutations (which simply shift the real events into the baseline, causing contamination).
- Draw random `[-window, +window]` matrices from `valid_centers` across `N_SHUFFLES` iterations to construct the empirical null distribution.

### 3. Z-Scoring & Significance Testing
- **Z-Scoring**: Raw firing probabilities must be z-scored against the null baseline to normalize traces prior to plotting or Bayesian decoding.
- **FDR Correction**: Calculate two-tailed p-values by comparing the real mean to the empirical null distribution. You MUST apply Benjamini-Hochberg False Discovery Rate (FDR) correction (e.g., `alpha=0.01`).
- **Consecutive Frames Rule**: To declare genuine temporal tuning, enforce a contiguous block requirement (e.g., 3 consecutive frames must be significant post-FDR).

### 4. Bout Reliability Assessment
- Calculate **Precision/Recall** for each tuned neuron per bout using raw spike counts, bypassing the smoothed matrix, to ensure the temporal tuning is consistent across multiple occurrences rather than driven by a single massive outlier bout.

### 5. Bootstrapped Bayesian Decoding
If predicting temporal windows (e.g., Predictive `[-3s, 0s]`, Reactive `[0s, +3s]`):
- Use Gaussian Naive Bayes classification.
- Because discrete actions often have very small sample sizes (low `n_bouts`), standard cross-validation is highly unstable.
- You **MUST** bootstrap the baseline sampling (`N_DECODER_ITERATIONS = 500`) and evaluate the decoder using Leave-One-Out (LOO) cross-validation on each iteration to provide a statistically robust `mean` and `std` accuracy score.

## Common Mistakes
- **Padding with NaNs**: Extracting matrices that overlap the 0th frame or max frame and padding the missing time with `NaN`s. This is an invalid scientific approach and will crash `GaussianNB` (`ValueError: Input X contains NaN`). Always drop edge-case bouts.
- **Circular Shuffling**: Using standard circular shifts on the entire spike array. This smears the actual neural response into the baseline. Always use targeted *Out-of-Window Null Sampling*.
- **Hardcoding Parameters**: Hardcoding temporal windows (e.g., `[-3s, +3s]`) into raw indices without factoring in `FPS`. Always calculate slicing indices dynamically: `int(seconds * FPS)`.
