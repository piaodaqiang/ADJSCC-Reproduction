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

## 2026-05-31

### Enhanced run summary 验证

Status: enhanced run summary 验证已完成。实验执行 Agent 已运行一次 1-step tiny training，并启用 `--write-run-summary`，生成了更详细的 JSON 摘要。本阶段仍然只是 tiny training smoke，不是正式训练，不是论文完整复现，也没有产生论文评价指标。

Evidence source: 用户提供的实验执行记录、enhanced JSON 字段摘要，以及代码复现 Agent 审查结论。

本阶段目标：

- 验证 enhanced run summary 能否记录比 2026-05-29 更完整的信息。
- 继续只运行 `1 step` tiny training：`max_steps=1`，`batch_size=2`，`snr_db=10.0`。
- 检查 JSON 是否记录环境版本、输入输出 shape、安全标记和输出路径。
- 继续保持边界：不保存 checkpoint，不下载新数据，不修改 `external/ADJSCC`，不把 JSON 运行产物加入 Git。

Enhanced JSON 结果：

- WSL 路径：`/mnt/d/Research/ai-data/runs/ADJSCC/tiny_train_summary_20260531-203648.json`。
- Windows 路径：`D:\Research\ai-data\runs\ADJSCC\tiny_train_summary_20260531-203648.json`。
- 文件大小：`907 bytes`。
- JSON 文件位于 `D:\Research\ai-data\runs\ADJSCC`，属于实验运行产物，不加入 Git。

运行设置和 loss：

- Mode: `tiny-train`。
- Max steps: `1`。
- Batch size: `2`。
- SNR: `10.0 dB`。
- Loss: `3472.816162109375`。
- 这个 loss 只说明 1-step tiny training 能算出误差，不是论文指标。

Enhanced JSON 主要字段：

- `timestamp`: `2026-05-31 20:36:48`。
- `mode`: `tiny-train`。
- `python_executable`。
- `python_version`: `3.10.20`。
- `tensorflow_version`: `2.14.0`。
- `tensorflow_probability_version`: `0.22.0`。
- `numpy_version`: `1.26.4`。
- `input_shape`: `[2, 32, 32, 3]`。
- `snr_shape`: `[2, 1]`。
- `output_shape`: `[2, 32, 32, 3]`。
- `run_root`。
- `summary_path`。
- `batch_size`: `2`。
- `max_steps`: `1`。
- `snr_db`: `10.0`。
- `losses`: `[3472.816162109375]`。
- `cifar10_batch_source`: `cifar-10-batches-py/data_batch_1`。
- `checkpoint_saved`: `false`。
- `data_downloaded`: `false`。
- `official_train_eval_used`: `false`。

Beginner notes:

- enhanced run summary 可以理解成“更详细的一次实验小摘要单”。普通摘要只记几个关键结果；enhanced 版本还会把运行环境、输入输出形状、输出路径和安全标记也记下来，方便以后追踪。
- 记录 Python、TensorFlow、TensorFlow Probability 和 NumPy 版本，是为了以后知道这次实验到底在哪套软件环境里跑出来。深度学习实验很容易受到版本影响，版本不同，报错、数值或行为都可能不一样。
- 记录 `input_shape / output_shape` 是为了确认图片 batch 进模型和出模型时形状正确。这里输入是 `[2, 32, 32, 3]`，输出也是 `[2, 32, 32, 3]`，说明 2 张 32x32 RGB 图片经过模型后仍然是图片形状，没有在数据流中变形或断掉。
- `snr_shape=[2, 1]` 表示每张图片都有一个 SNR 条件值，这和 batch size 2 对得上。
- `official_train_eval_used=false` 很重要，因为它说明这次没有调用官方完整训练或评估入口，只是在本项目安全 wrapper 里做 tiny smoke。这样可以避免误以为已经跑了正式训练或论文评估流程。
- JSON 不进 Git，是因为它是实验运行产物，以后可能越来越多。Git 仓库主要保存代码、笔记和小型总结；运行产物统一放在 `D:\Research\ai-data` 更清楚。
- 这仍然不是论文复现结果，因为只有 `1 step`，没有正式训练，没有 checkpoint，没有 PSNR、SSIM、MS-SSIM，也没有和论文表格结果做对比。

Code review notes:

- 代码复现 Agent 已审查 enhanced summary 字段合理。
- `run_root / summary_path` 安全。
- 输出被限制在 `/mnt/d/Research/ai-data/runs/ADJSCC` 内。
- 未发现保存 checkpoint 风险。
- 未发现自动下载数据风险。
- 未发现官方 train/eval 调用风险。
- 未发现 `external/ADJSCC` 修改风险。
- 未发现 Git 污染风险。
- 当前不建议阻塞性修改。
- 可选后续建议：以后可以把文件头注释中 “avoids training” 改得更精确，因为现在已经存在显式 `--tiny-train` 模式。

Safety boundary confirmed:

- Training was run, but only for 1-step tiny training。
- No long training was run。
- No checkpoint was saved。
- No new data was downloaded。
- `external/ADJSCC` was not modified。
- Official train/eval entrypoints were not used。
- No PSNR was produced。
- No SSIM was produced。
- No MS-SSIM was produced。
- Enhanced JSON itself was not added to Git。

Current conclusion:

- Enhanced run summary 验证通过。
- 本阶段可以记录为：1-step tiny training 后，增强版 JSON 摘要能正确记录环境版本、shape、路径、loss 和安全标记。
- 不能记录为正式训练完成。
- 不能记录为论文完整复现完成。
- 不能把 `loss=3472.816162109375` 当作论文指标。

Next step:

- 可以让 Git 管理 Agent 接手本次 Markdown 记录。
- 下一步可以考虑 5-step tiny training，但仍需用户单独确认；在确认前不要运行更长训练、不要保存 checkpoint、不要下载新数据。

### 5-step tiny training + enhanced run summary

Status: 5-step tiny training smoke 已完成，并生成 enhanced run summary。本阶段比 1-step 多跑了 4 个 step，用来观察训练链路能否连续跑几步、loss 列表能否被完整写入 JSON。它仍然不是正式训练，不是论文完整复现，也没有产生论文评价指标。

Evidence source: 用户提供的实验执行记录和 enhanced run summary 信息。

Command run:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/bin/python -m src.repro.cifar10_smoke --tiny-train --max-steps 5 --batch-size 2 --write-run-summary
```

Run summary 结果：

- WSL 路径：`/mnt/d/Research/ai-data/runs/ADJSCC/tiny_train_summary_20260531-212309.json`。
- Windows 路径：`D:\Research\ai-data\runs\ADJSCC\tiny_train_summary_20260531-212309.json`。
- 文件大小：`993 bytes`。
- JSON 文件位于 `D:\Research\ai-data\runs\ADJSCC`，属于实验运行产物，不加入 Git。

训练设置：

- Mode: `tiny-train`。
- Max steps: `5`。
- Batch size: `2`。
- Input shape: `[2, 32, 32, 3]`。
- Output shape: `[2, 32, 32, 3]`。

Loss 列表：

```json
[
  3472.5771484375,
  3467.310302734375,
  3459.9541015625,
  3450.0517578125,
  3437.323486328125
]
```

- Loss 数量：`5`。
- 这 5 个 loss 对应 5 个 tiny training step。
- loss 从 `3472.5771484375` 到 `3437.323486328125`，说明这个极小训练过程中误差数字有下降趋势。
- 但 loss 下降不能直接当作论文复现成功。它只是 smoke 阶段训练链路证据，不能代替 PSNR、SSIM、MS-SSIM 等论文指标。

Beginner notes:

- 5-step tiny training 可以理解成让模型连续做 5 次很小的训练更新，比 1-step 更能检查训练循环是否稳定，但规模仍然非常小。
- 5 step 仍然不是正式训练，因为正式训练通常需要大量 step 或 epoch，还需要保存与评估模型，并和论文指标做对比。
- loss 列表就是每一步训练后记录下来的误差数字。列表里有 5 个数，表示这次 5-step tiny training 每一步都有记录。
- loss 下降看起来是好信号，说明这几步里训练代码在尝试减小误差；但它不等于模型达到了论文效果，因为本阶段没有跑正式评估，也没有 PSNR、SSIM、MS-SSIM。
- run summary JSON 不加入 Git，是因为它是实验运行产物，以后可能越来越多。Git 仓库主要保存代码、笔记和小型总结。
- 仍然不保存 checkpoint，是因为 tiny training 的目标是验证训练链路和记录链路，不是产出可复用模型。保存 checkpoint 会引入额外产物和管理负担，应该留到更正式的训练规划阶段再单独确认。

Safety boundary confirmed:

- Training was run, but only for 5-step tiny training。
- No formal training was run。
- No checkpoint was saved。
- No new data was downloaded。
- `external/ADJSCC` was not modified。
- No PSNR was produced。
- No SSIM was produced。
- No MS-SSIM was produced。
- `checkpoint_saved`: `false`。
- `data_downloaded`: `false`。
- `official_train_eval_used`: `false`。
- External JSON itself was not added to Git。
- `git status --short` was clean in the provided record。

Current conclusion:

- 5-step tiny training smoke + enhanced run summary 已通过。
- 可以记录为：训练循环能连续跑 5 个 tiny step，并把 5 个 loss、安全字段和 shape 信息写入外部 JSON。
- 不能记录为正式训练完成。
- 不能记录为论文完整复现完成。
- 不能把 loss 下降写成论文复现成功。

Next step:

- 可以让 Git 管理 Agent 接手本次 Markdown 记录。
- 下一步如果继续推进，应先单独确认是否允许更长 tiny training、是否仍然禁止 checkpoint、是否需要开始规划 PSNR/SSIM/MS-SSIM 评估。

## 2026-06-02

### Metrics-smoke MSE/PSNR 指标链路验证

Status: `--metrics-smoke` 已通过。本阶段读取本地 CIFAR-10 的 2 张图片，让它们经过 ADJSCC 模型做一次非训练 forward，然后计算 MSE 和 PSNR。它只验证 MSE/PSNR 指标计算流程能跑通，不是正式论文 evaluation，也不是论文复现完成。

Evidence source: 用户提供的 metrics-smoke 运行结果和代码复现 Agent 审查结论。

Command run:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/bin/python -m src.repro.cifar10_smoke --metrics-smoke
```

Metrics-smoke result:

- Metrics-smoke passed: yes.
- Input shape: `(2, 32, 32, 3)`。
- Output shape: `(2, 32, 32, 3)`。

Per-image MSE:

- `image_1_mse`: `3279.354736328125`。
- `image_2_mse`: `3667.052490234375`。

Per-image PSNR:

- `image_1_psnr_db`: `12.972919464111328`。
- `image_2_psnr_db`: `12.487631797790527`。

Batch mean:

- `batch_mean_mse`: `3473.20361328125`。
- `batch_mean_psnr_db`: `12.730276107788086`。

Beginner notes:

- MSE 可以理解成“原图和重建图之间的平均平方误差”。每个像素都比较一次，差得越多，平方误差越大。通常 MSE 越小越好。
- PSNR 是由 MSE 换算出来的图像质量分数，单位是 dB。通常 PSNR 越大，表示重建图和原图越接近。
- 这里用 `255` 是因为当前图像像素按 `[0,255]` 范围计算。PSNR 公式里需要知道像素最大值，所以使用 `255`。
- 这次只用了 2 张 CIFAR-10 图片，样本太少，不能代表论文结果。
- Metrics-smoke 的意义是确认“指标计算流程能跑通”：模型能输出图像，程序能按每张图计算 MSE，再把 MSE 换算成 PSNR。
- 当前还没有 SSIM、MS-SSIM，也没有完整测试集评估，所以不能写成正式 evaluation。

Metric calculation notes:

- MSE 按每张图片的 `(H, W, C)` 求均值。
- PSNR 使用 `10 * log10(255^2 / MSE)`。
- `batch_mean_psnr_db` 是两张图片 PSNR 的平均值，不是由 `batch_mean_mse` 再换算得到。

Code review notes:

- `--metrics-smoke` 只有显式传入才会运行。
- 默认模式仍是 `check-only`。
- `run_metrics_smoke` 使用 `training=False`。
- 没有 `GradientTape()`，没有 `model.fit()`。
- 没有保存图片、checkpoint、`.h5`、`.ckpt`。
- 没有调用 `tf.keras.datasets.cifar10.load_data()`。
- 没有调用官方 `adjscc_cifar10.py train/eval`。
- 未发现自动下载数据、保存产物或官方训练/评估入口风险。

Safety boundary confirmed:

- Training was not run。
- No images were saved。
- No checkpoint was saved。
- No run summary was written。
- No new data was downloaded。
- `external/ADJSCC` was not modified。
- No formal paper metrics were produced。
- No SSIM was produced。
- No MS-SSIM was produced。
- No full test-set evaluation was run。

Current conclusion:

- Metrics-smoke MSE/PSNR 指标链路验证通过。
- 可以记录为：2 张 CIFAR-10 图片的非训练 forward、MSE 计算和 PSNR 计算流程能跑通。
- 不能记录为正式论文 evaluation。
- 不能记录为论文完整复现完成。
- 不能用这 2 张图片的 MSE/PSNR 代表论文结果。

Next step:

- 可以让 Git 管理 Agent 接手本次 Markdown 记录。
- 下一步可以考虑规划 SSIM/MS-SSIM smoke 或更完整的测试集评估，但必须先单独确认评估范围、是否保存结果、是否允许写 run summary 或其他输出。

### SSIM smoke 指标链路验证

Status: SSIM smoke 已完成。本阶段是在已有 `--metrics-smoke` 中加入 SSIM 计算，用同样的 2 张 CIFAR-10 图片验证 SSIM 指标计算链路。它仍然只是 smoke test，也就是“小规模安全冒烟测试”，不是正式论文 evaluation，也不是论文复现完成。

Evidence source: 用户提供的 SSIM smoke 结果和代码复现 Agent 审查结论。

SSIM results:

- `image_1_ssim`: `0.0835731998`。
- `image_2_ssim`: `0.0400035866`。
- `batch_mean_ssim`: `0.0617883950`。

SSIM calculation notes:

- 使用 TensorFlow API：`tf.image.ssim(targets, clipped_outputs, max_val=255.0)`。
- `outputs` 先 clip 到 `[0,255]`。
- 这样做是因为图像指标通常要求像素值在合法图像范围内。
- 正式 evaluation 时需要明确记录是否 clip，因为这是重要评估口径。

Beginner notes:

- SSIM 是结构相似度指标。通常越接近 `1`，说明两张图的结构越相似。
- PSNR 更偏“逐像素误差”，也就是一个像素一个像素地比差多少；SSIM 更偏“结构和纹理像不像”，更接近人眼看图时关心的局部结构。
- 这次只用了 2 张 CIFAR-10 图片，所以只能说明 SSIM 计算链路能跑，不能代表论文正式结果。
- 当前 SSIM 数值不能写成论文指标，因为没有完整测试集 evaluation，也没有正式训练 checkpoint。
- 当前还没有 MS-SSIM。

Code review notes:

- `--metrics-smoke` 仍然只有显式传入才会运行。
- 默认模式仍是 `check-only`。
- `run_metrics_smoke` 使用 `training=False`。
- 没有 `fit()`。
- 没有 `GradientTape()`。
- 没有保存图片。
- 没有保存 checkpoint。
- 没有调用 `save_weights` 或 `.save()`。
- 没有调用 `tf.keras.datasets.cifar10.load_data()`。
- 没有调用官方 `adjscc_cifar10.py train/eval`。
- 没有修改 `external/ADJSCC`。

Safety boundary confirmed:

- Training was not run。
- No images were saved。
- No checkpoint was saved。
- No run summary was written。
- No new data was downloaded。
- `external/ADJSCC` was not modified。
- No formal paper metrics were produced。
- No full test-set evaluation was run。
- No MS-SSIM was produced。
- No formal training checkpoint exists for this result。

Current conclusion:

- SSIM smoke 指标链路验证通过。
- 可以记录为：在 metrics-smoke 中，2 张 CIFAR-10 图片的 SSIM 计算流程能跑通。
- 不能记录为正式论文 evaluation。
- 不能记录为论文完整复现完成。
- 不能用这 2 张图片的 SSIM 数值代表论文结果。

Next step:

- 可以让 Git 管理 Agent 接手本次 Markdown 记录。
- 下一步可以考虑 MS-SSIM smoke 或更完整的测试集 evaluation，但必须先单独确认评估范围、checkpoint 策略、是否保存结果，以及是否记录 clip 等评估口径。

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
