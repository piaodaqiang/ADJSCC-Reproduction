# ADJSCC Smoke Wrapper Checks

Date: 2026-05-25

This report records the safe wrapper checks completed before any CIFAR-10 download or real training. It is not a paper reproduction result.

## Summary

The CIFAR-10 smoke wrapper in `src/repro/cifar10_smoke.py` passed three safe modes:

- `--check-only`
- `--build-only`
- `--fake-forward`

All commands were run from the project root in WSL distribution `Ubuntu-ADJSCC` with:

```text
/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/bin/python
```

## Commands

```bash
cd /mnt/d/Cloud/OneDrive/文档/Research/SemanticCommunication/ADJSCC-Reproduction
/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/bin/python -m src.repro.cifar10_smoke --check-only
/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/bin/python -m src.repro.cifar10_smoke --build-only
/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/bin/python -m src.repro.cifar10_smoke --fake-forward
```

## Evidence Summary

Runtime and imports:

- Python executable: `/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/bin/python`
- Python version: 3.10.20
- TensorFlow version: 2.14.0
- TensorFlow Probability version: 0.22.0
- NumPy version: 1.26.4
- TensorFlow GPU list: `[]`
- `tensorflow_compression` loaded from the conda environment, not from `external/ADJSCC`.
- `util_module.py` and `util_channel.py` loaded from `external/ADJSCC`.

CIFAR-10 data check:

- Checked path: `/mnt/d/Research/ai-data/datasets/CIFAR10`
- Directory exists: yes
- Recognizable CIFAR-10 files found: no
- The wrapper did not call `tf.keras.datasets.cifar10.load_data()`.
- The wrapper did not download CIFAR-10.

Model build:

- Model name: `adjscc_cifar10_smoke`
- Inputs: `(None, 32, 32, 3)` and `(None, 1)`
- Output: `(None, 32, 32, 3)`
- Trainable parameters: 12,779,055

Fake forward:

- Fake image input shape: `(2, 32, 32, 3)`
- SNR input shape: `(2, 1)`
- Fake output shape: `(2, 32, 32, 3)`
- Output dtype: `float32`

## Boundaries Confirmed

- CIFAR-10 download: no
- ImageNet download: no
- Model weight download: no
- Official `adjscc_cifar10.py train/eval`: not run
- Training: no
- Checkpoint or `.h5` write: no
- Modification to `external/ADJSCC`: no

## Notes For Beginners

- `--check-only` means checking the lab bench: Python, TensorFlow, paths, and imports.
- `--build-only` means assembling the model structure, like confirming the circuit diagram can be built.
- `--fake-forward` means sending two random fake images through the model once. This checks that the pipeline flows, but it does not prove the paper result.
- A real CIFAR-10 smoke test is still pending because no recognizable CIFAR-10 files are available yet.

## Next Confirmation Point

Before the next stage, the user must explicitly confirm one of these:

- Allow downloading CIFAR-10 into `/mnt/d/Research/ai-data/datasets/CIFAR10` or the Keras cache under `/mnt/d/Research/ai-data`.
- Provide an existing local CIFAR-10 copy and document its exact path.

After CIFAR-10 availability is confirmed, the next plan should define a tiny real-data smoke test with strict limits and no long training.
