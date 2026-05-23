# ADJSCC Reproduction

本项目用于从零复现论文 **Wireless Image Transmission Using Deep Source Channel Coding With Attention Modules**。

当前阶段目标是先完成 CIFAR-10 最小实验闭环，而不是一次性复现论文中的全部实验结果。

## Project Layout

```text
ADJSCC-Reproduction/
├─ external/        # Third-party or official source code
├─ configs/         # Experiment configs and local path templates
├─ environment/     # Environment notes and dependency records
├─ notes/           # Paper reading notes and reproduction logs
├─ results/         # Small result summaries and figures tracked by Git
├─ scripts/         # Helper scripts
└─ src/             # Our own reproduction helpers
```

## Data And Outputs

Large files are kept outside this OneDrive/GitHub project:

```text
D:/Research/ai-data
```

Recommended mapping:

```text
D:/Research/ai-data/datasets/CIFAR10
D:/Research/ai-data/runs/ADJSCC
D:/Research/ai-data/checkpoints/ADJSCC
D:/Research/ai-data/cache/ADJSCC
```

Do not commit datasets, checkpoints, long training logs, or large generated files.

## Phase 1 Goal

The first phase focuses on CIFAR-10 only:

1. Record the paper background and reproduction target.
2. Import the official ADJSCC code under `external/ADJSCC`.
3. Check Python, Conda, TensorFlow, CUDA, and GPU availability.
4. Load CIFAR-10 from the external data directory.
5. Run a tiny smoke test before any long training.
6. Record every experiment in `notes/reproduction_log.md`.

## Upstream Code

Official repository:

<https://github.com/alexxu1988/ADJSCC>

Current upstream commit:

```text
e5332e95faf592aab9f440992de96029162dc7dd
```

The upstream code should be treated as reference implementation first. Prefer adding small wrappers or notes before modifying upstream files.
