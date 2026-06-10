# Phase Summary: CIFAR-10 Minimal Checkpoint Evaluation Loop

Date: 2026-06-10

## Current stage

This stage closes the first usable CIFAR-10 reproduction loop for the ADJSCC reproduction project. The project is no longer only preparing the environment or checking imports. It can now run a very small training job, save a controlled checkpoint, load that checkpoint, and evaluate a few CIFAR-10 test images with MSE, PSNR, and SSIM.

This is still a smoke-stage result. It is not formal training, not full test-set evaluation, and not a completed reproduction of the paper.

## Completed work so far

- Prepared WSL2, Conda, TensorFlow 2.14, TensorFlow Compression, TensorFlow Probability, and NumPy environment.
- Added safe CIFAR-10 wrapper modes without modifying `external/ADJSCC`.
- Verified local CIFAR-10 data gate.
- Ran real CIFAR-10 forward smoke.
- Ran 1-step and 5-step tiny training smoke.
- Verified external run summary writing.
- Added MSE / PSNR metrics smoke.
- Added SSIM metrics smoke.
- Added CIFAR-10 `test_batch` `--eval-smoke`.
- Drafted CIFAR-10 minimal evaluation protocol.
- Completed the minimal checkpoint evaluation loop described below.

## Minimal loop

The current minimum closed loop is:

```text
tiny training 10 steps
-> explicitly save checkpoint
-> load checkpoint with eval-smoke
-> evaluate 4 CIFAR-10 test_batch images
-> print MSE / PSNR / SSIM
```

This proves that training, checkpoint saving, checkpoint loading, and small test-split evaluation are connected end to end.

## Key run details

Tiny training settings:

- `max_steps`: `10`
- `batch_size`: `2`
- `SNR`: `10 dB`
- checkpoint saved: yes
- checkpoint location: outside the Git repository

Checkpoint path:

- WSL: `/mnt/d/Research/ai-data/checkpoints/ADJSCC/tiny_train_smoke_20260610-111436/ckpt`
- Windows: `D:\Research\ai-data\checkpoints\ADJSCC\tiny_train_smoke_20260610-111436\ckpt`

Tiny training loss:

```json
[
  3473.37353515625,
  3467.616455078125,
  3460.36767578125,
  3450.755859375,
  3438.58447265625,
  3419.8203125,
  3396.435546875,
  3366.81689453125,
  3323.211181640625,
  3266.85498046875
]
```

Eval-smoke settings:

- data split: `test`
- image count: `4`
- checkpoint used: `true`
- input shape: `(4, 32, 32, 3)`
- output shape: `(4, 32, 32, 3)`
- `SNR`: `10 dB`

Mean eval-smoke metrics:

- `mean_mse`: `4392.0146484375`
- `mean_psnr_db`: `11.982768058776855`
- `mean_ssim`: `0.09460055828094482`

## Boundaries

- This is not formal paper training.
- This is not full CIFAR-10 test-set evaluation.
- This is not a paper-table or paper-curve result.
- The checkpoint was not committed to Git.
- No CIFAR-10 data, checkpoint, image, run summary JSON, run cache, `.h5`, `.ckpt`, or `.keras` artifact should enter Git.
- `external/ADJSCC` remains a reference implementation and was not modified.

## Beginner explanation

A checkpoint is a saved copy of model parameters after training. In this stage, the model trained for only 10 tiny steps, saved those parameters outside the repository, then loaded them again for a tiny test-set evaluation.

The important result is not that the metrics are good. The important result is that the workflow is now connected: train, save, load, and evaluate. The numbers are useful as evidence that the pipeline runs, but they cannot be compared with the paper because the training is too short and the evaluation uses only 4 test images.

## Suggested next steps

- Pause here as a clean pre-exam milestone if needed.
- If continuing, prefer one controlled extension at a time:
  - a longer but still bounded tiny training run,
  - a larger but still bounded test-split evaluation,
  - optional run summary for checkpoint eval.
- Keep MS-SSIM, GPU setup, and full training deferred until the current loop is documented and stable.
