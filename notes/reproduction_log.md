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

## 2026-05-26

### CIFAR-10 data gate check

Status: CIFAR-10 data gate mode has been added and `--cifar10-check` has been run. This is not a paper reproduction result, not a training result, and not a successful real CIFAR-10 smoke result.

Evidence source: experiment execution Agent report and latest Git commit `4e50056 feat: add CIFAR-10 data gate smoke modes`.

Changed files:

- `src/repro/cifar10_smoke.py`
- `scripts/run_cifar10_smoke.ps1`

New wrapper modes:

- `--cifar10-check`
- `--real-batch-forward`

Command run:

```bash
/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/bin/python -m src.repro.cifar10_smoke --cifar10-check
```

Data gate result:

- CIFAR-10 dataset directory exists: `/mnt/d/Research/ai-data/datasets/CIFAR10`.
- No recognizable CIFAR-10 data files were found.
- Missing or unrecognized expected entries:
  - `cifar-10-python.tar.gz`
  - `cifar-10-batches-py`
  - `data_batch_1`
  - `data_batch_2`
  - `data_batch_3`
  - `data_batch_4`
  - `data_batch_5`
  - `test_batch`
  - `batches.meta`

Safety boundary confirmed:

- No `tf.keras.datasets.cifar10.load_data()` call was found.
- No `model.fit()` call was found.
- No `save_weights()` call was found.
- CIFAR-10 was not downloaded.
- ImageNet was not downloaded.
- Model weights were not downloaded.
- Training was not run.
- No checkpoint was saved.
- `external/ADJSCC` was not modified.

Current blocker:

- Local CIFAR-10 data is not present in a recognizable format, so `--real-batch-forward` has not been run and should not be run yet.

Next step:

- Ask the user to confirm whether to download CIFAR-10 or provide an existing local CIFAR-10 copy.
- After CIFAR-10 availability is confirmed, let the experiment execution Agent run `--real-batch-forward` with strict no-training and no-checkpoint boundaries.

## 2026-05-27

### Real CIFAR-10 data forward smoke

Status: `--real-batch-forward` passed with real CIFAR-10 data. This is a real-data forward smoke check only. It is not training, not a full paper reproduction result, and not a paper-metric reproduction.

Evidence source: experiment execution Agent report.

Command run:

```bash
/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/bin/python -m src.repro.cifar10_smoke --real-batch-forward
```

Data gate result:

- CIFAR-10 data gate passed.
- Recognized local CIFAR-10 archive:
  `/mnt/d/Research/ai-data/datasets/CIFAR10/cifar-10-python.tar.gz`

Forward smoke result:

- Input batch shape: `(2, 32, 32, 3)`.
- Output shape: `(2, 32, 32, 3)`.
- The output has the same image shape as the input batch.

Beginner note:

- A forward pass means data flows through the model once, from input to output.
- It does not update model parameters.
- It does not teach or train the model.
- This step is important because it shows that real CIFAR-10 images can enter the ADJSCC smoke wrapper and produce model output with the expected image dimensions.

Safety boundary confirmed:

- Training was not run.
- No checkpoint was saved.
- No new data was downloaded.
- `external/ADJSCC` was not modified.
- `git status --short` had no output before and after the run.

Metrics:

- No PSNR was produced.
- No SSIM was produced.
- No MS-SSIM was produced.
- This cannot be written as a paper result or full reproduction.

Next step:

- The project can enter tiny-training planning, but should not directly start training.
- Before any tiny training, define the training step count, output directory, checkpoint policy, logging format, and confirmation rules for writing training artifacts.

## 2026-05-28

### 1-step tiny training smoke

Status: `--tiny-train` has run for exactly 1 training step. This is a tiny training smoke check for the training pipeline. It is not formal training, not a full paper reproduction, and not a paper-metric result.

Evidence source: experiment execution Agent report and code review Agent report.

Command run:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/bin/python -m src.repro.cifar10_smoke --tiny-train --max-steps 1 --batch-size 2
```

Training smoke result:

- Training mode: `--tiny-train`.
- Max steps: `1`.
- Batch size: `2`.
- Recorded loss: `tiny_train_step_1_loss: 3471.53759765625`.
- CIFAR-10 data gate passed.
- Input batch shape: `(2, 32, 32, 3)`.
- Output shape: `(2, 32, 32, 3)`.

Beginner notes:

- Tiny training means a very small training trial. It is like lightly pressing the gas pedal once to confirm the car can move, not driving the full route.
- Loss is an error number computed from the model output and the target. In this stage, the loss only proves that the training code can compute an error value.
- `loss=3471.53759765625` does not mean the model quality is good or bad for the paper. It is only a pipeline smoke value.
- One training step means the model only performs one tiny update. This checks whether the training path works, but it is far from formal training.
- No checkpoint is still acceptable here because this stage is meant to verify the training link, not to save a reusable model.

Safety boundary confirmed:

- Training was run, but only for 1 step.
- No long training was run.
- No checkpoint was saved.
- No new data was downloaded.
- `external/ADJSCC` was not modified.
- Official train/eval entrypoints were not run.
- No PSNR was produced.
- No SSIM was produced.
- No MS-SSIM was produced.

Code review notes:

- Tiny training only runs when `--tiny-train` is explicitly passed.
- Default mode is still `check-only`.
- No `save_weights`, `model.save`, or `.save()` checkpoint write path was found for this stage.
- `--save-checkpoint` exists, but currently stops with an error in this stage instead of saving a checkpoint.
- No `tf.keras.datasets.cifar10.load_data()` call was found.
- `max_steps` is limited from 1 to 10, and defaults to 1.
- Run summary is written only when `--write-run-summary` is explicitly passed, and must stay under `/mnt/d/Research/ai-data/runs/ADJSCC`.

Next step:

- The project can plan a 5-step tiny training run or a run summary test.
- Do not directly start formal training.
- Before the next run, define whether run summaries are allowed, where outputs go, what evidence to collect, and whether checkpoint writing remains disabled.

## 2026-05-29

### 1-step tiny training + run summary 写入测试

Status: 1-step tiny training 已经运行，并且启用了 `--write-run-summary`。本阶段确认小型 JSON 摘要可以安全写入外部实验输出目录。它仍然只是 tiny training smoke，不是正式训练，不是论文完整复现，也没有产生论文评价指标。

Evidence source: 用户提供的实验执行记录和已读取到的 run summary JSON 内容。

本阶段目标：

- 运行一次非常小的训练测试：`max_steps=1`，`batch_size=2`。
- 启用 `--write-run-summary`，确认程序能把本次运行的小摘要写到外部实验目录。
- 继续保持安全边界：不保存 checkpoint，不下载新数据，不修改 `external/ADJSCC`，不把运行产物混进 Git 仓库。

Run summary 结果：

- 外部运行目录：`/mnt/d/Research/ai-data/runs/ADJSCC`。
- 实际生成 JSON：`/mnt/d/Research/ai-data/runs/ADJSCC/tiny_train_summary_20260529-210910.json`。
- Windows 路径：`D:\Research\ai-data\runs\ADJSCC\tiny_train_summary_20260529-210910.json`。
- 文件大小：`239 bytes`。
- JSON 文件本身是实验运行产物，不提交 Git。

JSON 主要字段：

```json
{
  "mode": "tiny-train",
  "batch_size": 2,
  "max_steps": 1,
  "snr_db": 10.0,
  "losses": [
    3472.2255859375
  ],
  "cifar10_batch_source": "cifar-10-batches-py/data_batch_1",
  "checkpoint_saved": false,
  "data_downloaded": false
}
```

Training smoke result:

- Training mode: `tiny-train`。
- Max steps: `1`。
- Batch size: `2`。
- SNR: `10.0 dB`。
- Recorded loss: `3472.2255859375`。
- JSON losses: `[3472.2255859375]`。

Beginner notes:

- run summary 可以理解成“一次实验的小摘要单”。它记录这次怎么跑、batch size 是多少、训练了几步、loss 是多少、有没有保存 checkpoint、有没有下载数据等。
- run summary 放在 `D:\Research\ai-data`，不是放进 Git，是因为它属于实验运行产物。以后这种 JSON 可能会越来越多；Git 仓库主要用来保存代码、笔记和小型总结，避免把运行产物塞进版本历史。
- 这次仍然只是 tiny training smoke，因为只跑了 `1 step`。它的意义是确认训练链路和摘要写入链路能跑通，不是训练出可用模型。
- `loss=3472.2255859375` 只能说明训练过程算出了一个误差数字，不能当作论文复现指标。本阶段没有 PSNR、SSIM、MS-SSIM。

Safety boundary confirmed:

- Training was run, but only for 1 step tiny training。
- No long training was run。
- No checkpoint was saved。
- No new data was downloaded。
- `external/ADJSCC` was not modified。
- No PSNR was produced。
- No SSIM was produced。
- No MS-SSIM was produced。
- Run summary JSON itself was not added to Git。
- `git status --short` was clean in the provided record。

命令拼写注意事项：

- 用户实际命令里写成了 `PYTHONDONTWRITECODE=1`，少了 `BYTE`。
- 这个拼写错误只影响是否禁用 `.pyc` 缓存文件写入，不影响 Python 执行训练、loss 计算和 JSON 写入。
- 用户实际命令里写成了 `--max-step 1`，`argparse` 将它解析为 `--max-steps`，所以本次仍然按 1 step 执行。
- 后续统一使用正确写法：

```bash
PYTHONDONTWRITEBYTECODE=1
--max-steps 1
```

Current conclusion:

- 1-step tiny training + run summary 写入测试已经通过。
- 可以记录为“训练 smoke + JSON 摘要写入链路已跑通”。
- 不能记录为正式训练完成。
- 不能记录为论文完整复现完成。
- 不能用这个 loss 代替 PSNR、SSIM、MS-SSIM 等论文指标。

Next step:

- 可以让 Git 管理 Agent 接手，把 `notes/reproduction_log.md` 和 `results/status_2026-05-29_run_summary_check.md` 纳入版本管理。
- 下一阶段如果继续实验，建议先规划 5-step tiny training 或更完整的 run summary 字段检查；在明确授权前不要运行长训练、不要保存 checkpoint、不要下载新数据。

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
