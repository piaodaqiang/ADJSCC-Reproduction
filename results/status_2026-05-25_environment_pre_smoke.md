# ADJSCC Environment Status Before CPU Smoke Test

Date: 2026-05-25

This report records the current preparation state for the ADJSCC-Reproduction project. It is based on user-provided environment information and confirmed import checks. It does not claim that the CPU smoke test, full training, or paper reproduction has been completed.

## Stage Progress Summary

Current stage: environment preparation is complete up to the CPU smoke test prerequisite state.

Completed:

- WSL2 + Ubuntu-ADJSCC + Miniforge runtime stack is prepared.
- Conda environment `adjscc-tf` is available.
- Python and key TensorFlow-family dependencies have been installed.
- Core imports for `numpy`, `tensorflow`, `tensorflow_compression`, and `tensorflow_probability` have succeeded.
- The official ADJSCC import-risk pattern has been identified and a safer project-root import pattern has been tested.

Not completed:

- CIFAR-10 availability has not been confirmed.
- CIFAR-10 has not been downloaded by this step.
- CPU smoke test has not been run.
- Real training has not been run.
- No checkpoint has been saved.
- No paper-level PSNR, SSIM, or MS-SSIM reproduction result has been produced.
- `external/ADJSCC` has not been modified as part of this reporting step.

## Experiment Record Draft

```text
Date: 2026-05-25
Goal: Record ADJSCC CPU smoke test prerequisite environment status.
Code version: Official code is under external/ADJSCC; this report does not modify upstream code.
Environment:
  Runtime: WSL2 + Ubuntu-ADJSCC + Miniforge + conda environment adjscc-tf
  Ubuntu: 22.04
  User: piaodaqiang
  Miniforge: /home/piaodaqiang/miniforge3-adjscc
  Python: /home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/bin/python
  Python version: 3.10.20
  pip version: 26.1.1
Dependencies:
  tensorflow==2.14.0
  tensorflow-compression==2.14.0
  tensorflow-probability==0.22.0
  numpy==1.26.4
  pyyaml, matplotlib, scikit-image installed; exact versions not recorded here.
Dataset path:
  Planned CIFAR-10 path: /mnt/d/Research/ai-data/datasets/CIFAR10
Command:
  No smoke-test command recorded in this report.
Result:
  Environment imports passed for numpy, tensorflow, tensorflow_compression, and tensorflow_probability.
  TensorFlow GPU list is [].
  nvidia-smi in WSL can see RTX 4060 Laptop GPU.
Problem:
  external/ADJSCC contains an old tensorflow_compression/ directory.
  Direct execution from external/ADJSCC can shadow the pip package and trigger a TensorFlow 2.1 requirement error.
Next step:
  Confirm CIFAR-10 availability without automatic download.
  Run only a short CPU smoke test.
  Record the exact command, output path, and success/failure evidence.
```

## Evidence Chain

- User-provided environment record confirms WSL2, Ubuntu 22.04, Miniforge, and `adjscc-tf` as the main runtime environment.
- User-provided version record confirms Python 3.10.20 and pip 26.1.1 in `/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/bin/python`.
- User-provided dependency record confirms `tensorflow==2.14.0`, `tensorflow-compression==2.14.0`, `tensorflow-probability==0.22.0`, and `numpy==1.26.4`.
- User-provided import checks confirm successful imports of `numpy`, `tensorflow`, `tensorflow_compression`, and `tensorflow_probability`.
- User-provided GPU status confirms TensorFlow currently reports no GPU devices, while WSL `nvidia-smi` can see an RTX 4060 Laptop GPU.
- User-provided import-risk check confirms direct execution from `external/ADJSCC` can pick up the old bundled `tensorflow_compression/` and produce a TensorFlow 2.1 requirement error.
- Safer import pattern has been verified: start from the project root, import pip-installed `tensorflow_compression` first, then append `external/ADJSCC` to the end of `sys.path`.

## Pending Items

- Confirm whether CIFAR-10 exists under `/mnt/d/Research/ai-data/datasets/CIFAR10`.
- Confirm whether the next CPU smoke-test command avoids automatic CIFAR-10 download.
- Confirm that the smoke test is short and does not start long training.
- Record exact versions for `pyyaml`, `matplotlib`, and `scikit-image` if they become relevant to a later run.
- Investigate GPU enablement in a later phase; do not block CPU smoke testing on this.
- Keep all large datasets, runs, checkpoints, and caches under `/mnt/d/Research/ai-data`.

## Next Stage Recommendation

The next execution Agent should first perform a read-only data-path check for CIFAR-10. If the dataset is available, run only the planned CPU smoke test and record the command, short log summary, output location, and failure or success evidence. If the dataset is missing, stop and ask for confirmation before any download.
