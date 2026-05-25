# Reproduction Log

Use this file to record every important step, including failed attempts.

## 2026-05-23

- Created project plan for ADJSCC reproduction.
- Decided to keep code under OneDrive/GitHub and large files under `D:\Research\ai-data`.
- Phase 1 target: CIFAR-10 minimal experiment loop only.

## 2026-05-25

### Environment preparation before CPU smoke test

Status: environment preparation is complete up to the CPU smoke test prerequisite state.

Evidence source: user-provided environment record and confirmed import checks. This entry records setup status only. It is not a completed smoke test and not a full paper reproduction result.

Completed:

- Main runtime stack: WSL2 + Ubuntu-ADJSCC + Miniforge + conda environment `adjscc-tf`.
- WSL distribution: Ubuntu 22.04.
- WSL user: `piaodaqiang`.
- Miniforge path: `/home/piaodaqiang/miniforge3-adjscc`.
- Python path: `/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/bin/python`.
- Python version: 3.10.20.
- pip version: 26.1.1.
- Confirmed key dependencies:
  - `tensorflow==2.14.0`
  - `tensorflow-compression==2.14.0`
  - `tensorflow-probability==0.22.0`
  - `numpy==1.26.4`
- `pyyaml`, `matplotlib`, and `scikit-image` are installed, but exact versions were not recorded in this entry.
- `numpy`, `tensorflow`, `tensorflow_compression`, and `tensorflow_probability` imported successfully.
- TensorFlow GPU device list is currently `[]`.
- `nvidia-smi` inside WSL can see an RTX 4060 Laptop GPU.
- Current execution decision: run CPU smoke test first; leave GPU enablement for a later phase.

Failed or risky with evidence:

- `external/ADJSCC` contains an old bundled `tensorflow_compression/` directory.
- Running directly from `external/ADJSCC` can shadow the pip-installed `tensorflow-compression` package and trigger a TensorFlow 2.1 version requirement error.
- Safer import pattern: start from the project root, import the pip-installed `tensorflow_compression` first, then append `external/ADJSCC` to the end of `sys.path`.
- This safer pattern has passed the official core-module import test.

Data and output paths:

- CIFAR-10 dataset path plan: `/mnt/d/Research/ai-data/datasets/CIFAR10`.
- Run output path plan: `/mnt/d/Research/ai-data/runs/ADJSCC`.
- Checkpoint path plan: `/mnt/d/Research/ai-data/checkpoints/ADJSCC`.
- Cache path plan: `/mnt/d/Research/ai-data/cache/ADJSCC`.

Pending confirmation:

- CIFAR-10 has not been confirmed available.
- CIFAR-10 has not been downloaded by this project step.
- CPU smoke test has not been run.
- Real training has not been run.
- No checkpoint has been saved.
- `external/ADJSCC` has not been modified for this environment-preparation record.

Next step:

- Check whether the CIFAR-10 path exists and is readable without automatic download.
- Run the CPU smoke test only after confirming that the command is short and does not start long training.
- Record the exact command, short log summary, output path, and success or failure evidence after the smoke test.

### Safe wrapper checks before CIFAR-10 download

Status: the safe CIFAR-10 smoke wrapper passed its pre-dataset checks.

Evidence source: commands run from the project root through WSL distribution `Ubuntu-ADJSCC` using `/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/bin/python`.

Commands:

```bash
/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/bin/python -m src.repro.cifar10_smoke --check-only
/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/bin/python -m src.repro.cifar10_smoke --build-only
/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/bin/python -m src.repro.cifar10_smoke --fake-forward
```

Results:

- `--check-only` completed successfully.
- Runtime stack reported Python 3.10.20, TensorFlow 2.14.0, TensorFlow Probability 0.22.0, and NumPy 1.26.4.
- `tensorflow_compression` was imported from the conda environment, not from `external/ADJSCC`.
- Official `util_module.py` and `util_channel.py` imported successfully from `external/ADJSCC`.
- CIFAR-10 directory `/mnt/d/Research/ai-data/datasets/CIFAR10` exists, but no recognizable CIFAR-10 files were found.
- `--build-only` completed successfully and built model `adjscc_cifar10_smoke`.
- Model inputs were `(None, 32, 32, 3)` and `(None, 1)`; model output was `(None, 32, 32, 3)`.
- Trainable parameter count was 12,779,055.
- `--fake-forward` completed successfully with random fake input shape `(2, 32, 32, 3)`, SNR shape `(2, 1)`, and output shape `(2, 32, 32, 3)`.

Important boundaries:

- No CIFAR-10 data was downloaded.
- No ImageNet data was downloaded.
- No model weights were downloaded.
- No official `train` or `eval` entrypoint was run.
- No training was run.
- No checkpoint or `.h5` file was written.
- `external/ADJSCC` was not modified.

Notes:

- TensorFlow still reports no usable GPU devices in this environment; this is acceptable for the current CPU-only smoke stage.
- TensorFlow printed CUDA/GPU library warnings, but the three CPU-safe wrapper checks completed.
- This is not a paper reproduction result. It only proves that the safe wrapper can import dependencies, build the model, and run one fake-data forward pass.

Next step:

- Ask the user whether to allow CIFAR-10 download or provide an existing local CIFAR-10 copy under `/mnt/d/Research/ai-data/datasets/CIFAR10`.
- Only after that confirmation, plan a tiny real-data smoke test with explicit limits and logging.

## Experiment Template

```text
Date:
Goal:
Code version:
Environment:
Dataset path:
Command:
Result:
Problem:
Next step:
```
