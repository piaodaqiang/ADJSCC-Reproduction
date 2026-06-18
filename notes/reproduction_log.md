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

### CIFAR-10 evaluation protocol 口径草案整理

Status: 已新增 CIFAR-10 最小复现实验 evaluation protocol 口径草案。该文档用于说明后续正式 evaluation 时“怎么算指标、怎么记录条件、哪些数字可以比较”，不是正式实验结果，也不是论文复现完成证明。

Evidence source: 论文理解 Agent 结论、已完成的 MSE/PSNR metrics-smoke、已完成的 SSIM metrics-smoke，以及当前 `src/repro/cifar10_smoke.py` wrapper 的只读审查。

新增文档：

- `results/evaluation_protocol_cifar10_minimal.md`

本阶段整理目标：

- 用小白能懂的话解释 evaluation protocol 和“口径”的含义。
- 明确当前仍处于 CIFAR-10 最小 smoke / tiny training 阶段。
- 区分当前 2 张图 smoke 与正式 CIFAR-10 test split evaluation。
- 记录当前 PSNR、SSIM、pixel range、clip policy、SNR、checkpoint 和信道随机性口径。
- 说明 MS-SSIM 暂缓原因。
- 给出后续正式 evaluation 的结果记录字段建议。

Protocol 主要结论：

- CIFAR-10 正式 evaluation 应使用 `test` split。
- 当前本地数据位置为 Windows `D:\Research\ai-data\datasets\CIFAR10`，WSL `/mnt/d/Research/ai-data/datasets/CIFAR10`。
- 当前 smoke 只使用 2 张图，只能证明指标链路能跑，不能代表正式结果。
- 当前 wrapper 使用 `[0,255]` 像素范围，并在计算指标前将 outputs clip 到 `[0,255]`。
- 当前 MSE 按每张图的 `(H, W, C)` 求均值。
- 当前 per-image PSNR 使用 `10 * log10(255^2 / MSE)`。
- 当前 `batch_mean_psnr_db` 是 per-image PSNR 的平均值，不是由 batch mean MSE 再换算得到。
- 当前 SSIM 使用 `tf.image.ssim(targets, clipped_outputs, max_val=255.0)`，并按 per-image SSIM 再求 batch mean。
- 当前 smoke 使用 SNR `10 dB`；正式 evaluation 需要明确 SNR 列表，不同 SNR 下的指标不能混在一起比较。
- 当前没有正式 checkpoint；没有 checkpoint 时不能声称复现论文指标。
- ADJSCC 涉及信道噪声，正式 evaluation 后续需要考虑固定 random seed 或多次传输平均。

MS-SSIM decision:

- 当前暂缓 MS-SSIM。
- CIFAR-10 只有 `32x32`，默认 MS-SSIM 多尺度下采样可能不适合直接套用。
- 论文理解 Agent 未看到 MS-SSIM 是该论文 CIFAR-10 主指标。
- 后续如果需要加入 MS-SSIM，应单独设计参数和 smoke test。

Safety boundary confirmed:

- No experiment was run.
- No training was run.
- No formal evaluation was run.
- No images were saved.
- No checkpoint was saved.
- No run summary was written.
- No data was downloaded.
- `src/repro/cifar10_smoke.py` was not modified.
- `scripts/run_cifar10_smoke.ps1` was not modified.
- `external/ADJSCC` was not modified.
- No Git commit was created.

Current conclusion:

- Evaluation protocol 口径草案已整理完成。
- 当前仍不能记录为正式 CIFAR-10 evaluation 完成。
- 当前仍不能记录为论文表格或曲线复现完成。
- 当前可以交给代码复现 Agent 审查该 protocol 是否与当前 wrapper 完全一致。

Next step:

- 让代码复现 Agent 审查 `results/evaluation_protocol_cifar10_minimal.md` 与当前 wrapper 的一致性。
- 暂缓 MS-SSIM。
- 暂缓长训练。
- 暂缓正式 evaluation。

## 2026-06-08

### CIFAR-10 test split eval-smoke

Status: `--eval-smoke` 已完成。本阶段从 CIFAR-10 test split 的 `test_batch` 读取 4 张图片，经过 ADJSCC 模型做一次非训练 forward，然后计算 MSE、PSNR 和 SSIM。它只验证“测试集评估入口能跑通”，不是正式论文 evaluation，也不是论文复现完成。

Evidence source: 用户提供的 eval-smoke 运行结果和代码复现 Agent 审查结论。

新增模式和数据来源：

- New mode: `--eval-smoke`。
- Data source: `cifar-10-batches-py/test_batch`。
- Image count: `4`。
- Input shape: `(4, 32, 32, 3)`。
- Output shape: `(4, 32, 32, 3)`。

Per-image MSE:

- `image_1_mse`: `2541.4853515625`。
- `image_2_mse`: `6932.91943359375`。
- `image_3_mse`: `4320.96240234375`。
- `image_4_mse`: `3927.419921875`。

Per-image PSNR:

- `image_1_psnr_db`: `14.079927444458008`。
- `image_2_psnr_db`: `9.72164249420166`。
- `image_3_psnr_db`: `11.774999618530273`。
- `image_4_psnr_db`: `12.189730644226074`。

Per-image SSIM:

- `image_1_ssim`: `0.09230268746614456`。
- `image_2_ssim`: `0.07816802710294724`。
- `image_3_ssim`: `0.09644591808319092`。
- `image_4_ssim`: `0.11792823672294617`。

Mean metrics:

- `mean_mse`: `4430.69677734375`。
- `mean_psnr_db`: `11.941575050354004`。
- `mean_ssim`: `0.09621121734380722`。

Beginner notes:

- `data_batch_1` 是 CIFAR-10 训练集的一部分。之前的 metrics-smoke 主要用于检查 MSE、PSNR、SSIM 这些指标计算链路能不能跑通。
- `test_batch` 是 CIFAR-10 测试集。正式 evaluation 应该在测试集上做，因为测试集更适合用来观察模型在“没参与训练的数据”上的表现。
- 这次只用了 4 张测试集图片，所以仍然只是 smoke test，也就是小规模安全冒烟测试。
- 没有正式训练 checkpoint，所以不能拿这些数字和论文表格或曲线比较。
- 本阶段的意义是确认“测试集评估入口能跑通”：能从 `test_batch` 读图，能非训练 forward，能计算 MSE / PSNR / SSIM。
- 这些 MSE / PSNR / SSIM 都只是 4 张图的小样本结果，不代表模型真实性能，也不能写成论文正式结果。

Code review notes:

- `--eval-smoke` 是显式模式，默认仍是 `check-only`。
- 读取的是 CIFAR-10 `test_batch`。
- 如果从 `.tar.gz` 读取，也是只读读取，不解压写文件。
- 默认 `image_count=4`。
- 硬上限 `MAX_EVAL_SMOKE_IMAGES=16`，避免误跑完整测试集。
- 使用 `training=False`。
- 没有 `fit()`。
- 没有 eval-smoke 内的 `GradientTape()`。
- 没有保存图片。
- 没有保存 checkpoint。
- 没有写 run summary。
- 没有调用 `tf.keras.datasets.cifar10.load_data()`。
- 没有调用官方 `adjscc_cifar10.py train/eval`。
- 没有修改 `external/ADJSCC`。
- 指标口径符合 evaluation protocol。
- Clip policy 与 protocol 一致。

Safety boundary confirmed:

- Training was not run。
- No images were saved。
- No checkpoint was saved。
- No run summary was written。
- No new data was downloaded。
- `external/ADJSCC` was not modified。
- Official train/eval was not run。
- No formal paper metrics were produced。

Current conclusion:

- CIFAR-10 test split eval-smoke 通过。
- 可以记录为：`--eval-smoke` 能从 `test_batch` 读取 4 张图，并完成非训练 forward 和 MSE / PSNR / SSIM 计算。
- 不能记录为正式论文 evaluation 完成。
- 不能记录为论文完整复现完成。
- 不能用这 4 张图的指标代表模型真实性能。

Next step:

- 可以让 Git 管理 Agent 接手本次 Markdown 记录。
- 下一步可以规划更完整的 test split evaluation，但必须先单独确认 checkpoint 来源、评估图片数量、SNR 设置、是否保存结果，以及是否允许写 run summary。

## 2026-06-10

### 最小训练-保存-加载-评估闭环 smoke

Status: 最小“训练-保存-加载-评估”闭环 smoke 已完成。本阶段完成了 10-step tiny training，显式保存 checkpoint，再让 eval-smoke 加载该 checkpoint，并在 CIFAR-10 `test_batch` 的 4 张图上计算 MSE、PSNR 和 SSIM。它证明这条最小流程已经打通，但不是正式训练，不是正式论文 evaluation，也不是论文复现完成。

Evidence source: 用户提供的 checkpoint/eval-smoke 运行结果和代码复现 Agent 审查结论。

本阶段闭环：

```text
tiny training 10 step
-> 显式保存 checkpoint
-> eval-smoke 加载该 checkpoint
-> 在 CIFAR-10 test_batch 的 4 张图上计算 MSE / PSNR / SSIM
```

Checkpoint path:

- WSL 路径：`/mnt/d/Research/ai-data/checkpoints/ADJSCC/tiny_train_smoke_20260610-111436/ckpt`。
- Windows 路径：`D:\Research\ai-data\checkpoints\ADJSCC\tiny_train_smoke_20260610-111436\ckpt`。
- Checkpoint 位于 Git 仓库外，没有加入 Git。

Tiny training 设置：

- Max steps: `10`。
- Batch size: `2`。
- SNR: `10 dB`。
- 是否保存 checkpoint: 是。
- Checkpoint 是否在 Git 仓库外: 是。

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

Eval-smoke 设置：

- Data split: `test`。
- Image count: `4`。
- Checkpoint used: `true`。
- Checkpoint path: `/mnt/d/Research/ai-data/checkpoints/ADJSCC/tiny_train_smoke_20260610-111436/ckpt`。
- Input shape: `(4, 32, 32, 3)`。
- Output shape: `(4, 32, 32, 3)`。
- SNR: `10 dB`。

Per-image MSE:

- `image_1_mse`: `2502.846435546875`。
- `image_2_mse`: `6873.56689453125`。
- `image_3_mse`: `4300.40234375`。
- `image_4_mse`: `3891.243408203125`。

Per-image PSNR:

- `image_1_psnr_db`: `14.14646053314209`。
- `image_2_psnr_db`: `9.758981704711914`。
- `image_3_psnr_db`: `11.7957124710083`。
- `image_4_psnr_db`: `12.229918479919434`。

Per-image SSIM:

- `image_1_ssim`: `0.10743298381567001`。
- `image_2_ssim`: `0.08025652915239334`。
- `image_3_ssim`: `0.09003458172082901`。
- `image_4_ssim`: `0.10067815333604813`。

Mean metrics:

- `mean_mse`: `4392.0146484375`。
- `mean_psnr_db`: `11.982768058776855`。
- `mean_ssim`: `0.09460055828094482`。

Beginner notes:

- Checkpoint 是模型训练后的参数存档。可以把它理解成“模型当时学到的参数快照”，以后可以加载它继续评估或继续训练。
- 这次 checkpoint 存在 `D:\Research\ai-data`，不在 Git 仓库里。这样做是为了避免把模型权重这类运行产物混进代码仓库。
- 这次 10-step tiny training 只是验证训练和保存流程，不是正式训练。10 step 太短，只能说明流程能跑，不能说明模型已经学好了。
- Eval-smoke 加载 checkpoint 后，只评估了 CIFAR-10 `test_batch` 的 4 张图片，不是完整测试集 evaluation。
- 这些 MSE / PSNR / SSIM 数值不能和论文表格或曲线比较，因为没有正式训练 checkpoint、没有完整测试集评估，也没有完整论文设置。
- 这次真正有价值的地方是：训练、保存、加载、测试集小样本评估这条链路已经打通。对当前阶段来说，这是一个很好的最小可交付闭环。

Code review notes:

- Checkpoint 保存基本受控。
- 只有显式传入 `--save-checkpoint` 才会保存。
- Checkpoint 路径被限制在 `/mnt/d/Research/ai-data/checkpoints/ADJSCC`。
- Eval-smoke 只有显式传入 `--eval-checkpoint` 才加载 checkpoint。
- Eval-smoke 不训练，使用 `training=False`。
- 没有自动下载数据。
- 没有保存图片。
- 没有写 run summary。
- 没有修改 `external/ADJSCC`。
- 没有调用官方 `adjscc_cifar10.py train/eval`。
- 当前 checkpoint 没有进入 Git。
- 这是最小闭环 smoke，不是论文正式结果。

Non-blocking notes:

- 文件开头和主程序安全提示仍写 “no checkpoint write”，但现在 tiny-train 显式 `--save-checkpoint` 会写 checkpoint。后续建议改成 “no checkpoint write unless explicitly requested for tiny-train”。
- `MAX_TINY_TRAIN_STEPS` 从 `10` 提到 `50`。当前跑的是 `10 step`，没问题；后续如需极保守，可重新讨论是否改回 `10`。

Safety boundary confirmed:

- Training was run, but only for 10-step tiny training。
- No long training was run。
- Checkpoint was saved, controlled under `D:\Research\ai-data`。
- No images were saved。
- No `.h5` or `.keras` file was written。
- No run summary was written。
- No new data was downloaded。
- `external/ADJSCC` was not modified。
- Official train/eval was not run。
- No formal paper metrics were produced。
- Checkpoint was not added to Git。

Current conclusion:

- 最小“训练-保存-加载-评估”闭环 smoke 已打通。
- 可以记录为：当前项目已经能完成 10-step tiny training、受控保存 checkpoint、加载 checkpoint，并在 CIFAR-10 test split 的 4 张图上计算 MSE / PSNR / SSIM。
- 不能记录为正式训练完成。
- 不能记录为正式论文 evaluation 完成。
- 不能记录为论文复现完成。
- 不能把本次指标和论文表格或曲线直接比较。

Next step:

- 可以把当前闭环作为期末和六级复习前的最小可交付节点，交给 Git 管理 Agent 处理 Markdown 记录和已有代码改动。
- 后续如继续推进，再单独规划是否做更长训练、正式 checkpoint、完整 test split evaluation，以及是否保存 run summary。

## 2026-06-14

### 50-step tiny training + checkpoint + eval-smoke

Status: 50-step 受控 tiny training 扩展结果已完成。本阶段运行 50-step tiny training，显式保存 checkpoint，再用 eval-smoke 加载 checkpoint，在 CIFAR-10 `test_batch` 的 4 张图上计算 MSE、PSNR 和 SSIM。它是在 10-step 最小闭环基础上的小幅扩展，不是正式训练，不是正式论文 evaluation，也不是论文复现完成。

Evidence source: 用户提供的 50-step tiny training、checkpoint 和 eval-smoke 结果。

Checkpoint path:

- WSL 路径：`/mnt/d/Research/ai-data/checkpoints/ADJSCC/tiny_train_smoke_20260614-170644/ckpt`。
- Windows 路径：`D:\Research\ai-data\checkpoints\ADJSCC\tiny_train_smoke_20260614-170644\ckpt`。
- Checkpoint 保存到 `D:\Research\ai-data`，没有加入 Git。

Tiny training 设置：

- Max steps: `50`。
- Batch size: `2`。
- SNR: `10 dB`。
- 是否保存 checkpoint: 是。
- Checkpoint 是否进入 Git: 否。

Loss 关键变化：

- `step_1_loss`: `3472.87646484375`。
- `step_10_loss`: `3279.12841796875`。
- `step_20_loss`: `2268.64892578125`。
- `step_30_loss`: `1317.4755859375`。
- `step_40_loss`: `652.4791259765625`。
- `step_50_loss`: `306.04559326171875`。

Loss interpretation:

- Loss 明显下降，说明模型在这次 tiny training 的小批量训练链路上确实发生了优化。
- 但这不等于模型已经泛化，也不等于论文复现成功。
- 这里的 loss 主要证明训练链路可以连续工作 50 step，并且能把训练误差压下来；它不能替代完整测试集指标。

Eval-smoke 设置：

- Data split: `test`。
- Image count: `4`。
- Checkpoint used: `true`。
- Input shape: `(4, 32, 32, 3)`。
- Output shape: `(4, 32, 32, 3)`。

Per-image MSE:

- `image_1_mse`: `3531.161865234375`。
- `image_2_mse`: `6643.31640625`。
- `image_3_mse`: `3506.180419921875`。
- `image_4_mse`: `4169.91796875`。

Per-image PSNR:

- `image_1_psnr_db`: `12.651627540588379`。
- `image_2_psnr_db`: `9.906953811645508`。
- `image_3_psnr_db`: `12.682459831237793`。
- `image_4_psnr_db`: `11.929529190063477`。

Per-image SSIM:

- `image_1_ssim`: `0.14745713770389557`。
- `image_2_ssim`: `0.08354467153549194`。
- `image_3_ssim`: `0.25806406140327454`。
- `image_4_ssim`: `0.14494939148426056`。

Mean metrics:

- `mean_mse`: `4462.64453125`。
- `mean_psnr_db`: `11.792642593383789`。
- `mean_ssim`: `0.15850381553173065`。

Comparison with 10-step smoke:

- 10-step `mean_mse`: `4392.0146484375`。
- 10-step `mean_psnr_db`: `11.982768058776855`。
- 10-step `mean_ssim`: `0.09460055828094482`。
- 50-step 的 `mean_ssim` 高于 10-step。
- 但 50-step 的 `mean_mse` 和 `mean_psnr_db` 并没有明显优于 10-step。
- 因为只评估了 4 张图，所以不能说 50-step 模型整体更好。这只是小样本 smoke 观察，不是论文结论。

Beginner notes:

- 50-step tiny training 可以理解成比 10-step 多踩几下油门，看看训练链路能不能更久地稳定跑下去。
- 这次 loss 从 `3472.87646484375` 降到 `306.04559326171875`，说明这批 tiny training 确实在减小训练误差。
- 但是训练误差下降，不等于模型在新图片上都表现更好。模型可能只是更适应当前小批量训练数据。
- Eval-smoke 只用了 4 张 CIFAR-10 测试图，所以 MSE / PSNR / SSIM 只是小样本观察，不能代表模型真实性能。
- 这次结果最适合写成“50-step 受控 tiny training + checkpoint + 小样本 eval-smoke 已跑通”，不能写成“论文结果复现成功”。

Safety boundary confirmed:

- Training was run, but only for 50-step tiny training。
- No long training was run。
- Checkpoint was saved under `D:\Research\ai-data`。
- No images were saved。
- No run summary was written。
- No new data was downloaded。
- `external/ADJSCC` was not modified。
- Official train/eval was not run。
- No formal paper metrics were produced。
- Checkpoint was not added to Git。

Current conclusion:

- 50-step 受控 tiny training 扩展已完成。
- 可以记录为：训练链路可以连续跑 50 step，受控保存 checkpoint，并用该 checkpoint 完成 4 张 CIFAR-10 test split 图片的 eval-smoke。
- 不能记录为正式训练完成。
- 不能记录为正式论文 evaluation 完成。
- 不能记录为论文复现完成。
- 不能把本次小样本指标和论文表格或曲线直接比较。

Next step:

- 可以把本次 50-step 结果作为期末和六级复习前的扩展记录节点，交给 Git 管理 Agent 处理 Markdown 记录和已有代码改动。
- 后续如果继续推进，应先单独规划是否做完整 test split evaluation、是否固定随机种子、是否多次传输平均、是否保存 run summary。

### 200-step tiny training + checkpoint + 16-image eval-smoke

Status: 200-step 受控 tiny training 扩展结果已完成。本阶段运行 200-step tiny training，显式保存 checkpoint，再用 eval-smoke 加载 checkpoint，在 CIFAR-10 `test_batch` 的 16 张图上计算 MSE、PSNR 和 SSIM。它比 50-step smoke 更进一步，但仍然是受控 tiny training smoke，不是正式训练，不是正式论文 evaluation，也不是论文复现完成。

Evidence source: 用户提供的 200-step tiny training、checkpoint、16-image eval-smoke 结果，以及代码改动说明。

Code change notes:

- `src/repro/cifar10_smoke.py` 中 `MAX_TINY_TRAIN_STEPS` 已从 `50` 改为 `200`。
- Eval-smoke 结束提示文案已修正，不再错误写死 `4 images`。
- `--max-steps` 默认值仍保持 `10`，避免默认长训练。
- `eval-image-count` 上限仍为 `16`。

Checkpoint path:

- WSL 路径：`/mnt/d/Research/ai-data/checkpoints/ADJSCC/tiny_train_smoke_20260614-191721/ckpt`。
- Windows 路径：`D:\Research\ai-data\checkpoints\ADJSCC\tiny_train_smoke_20260614-191721\ckpt`。
- Checkpoint 保存到 `D:\Research\ai-data`，没有加入 Git。

Tiny training 设置：

- Max steps: `200`。
- Batch size: `2`。
- SNR: `10 dB`。
- 是否保存 checkpoint: 是。
- Checkpoint 是否进入 Git: 否。

Loss 关键节点：

- `step_1_loss`: `3473.42236328125`。
- `step_10_loss`: `3259.82421875`。
- `step_50_loss`: `347.51446533203125`。
- `step_100_loss`: `20.420076370239258`。
- `step_150_loss`: `11.049098014831543`。
- `step_200_loss`: `7.018994331359863`。

Loss interpretation:

- Loss 从约 `3473` 降到约 `7`，说明模型在当前 tiny training 数据链路上优化非常明显。
- 但 `batch_size=2`，训练规模仍小，可能存在记住小批量样本的情况。
- Loss 下降不等于模型已经泛化，也不等于论文复现成功。

Eval-smoke 设置：

- Data split: `test`。
- Image count: `16`。
- Checkpoint used: `true`。
- Input shape: `(16, 32, 32, 3)`。
- Output shape: `(16, 32, 32, 3)`。

Per-image MSE:

```text
[3680.9246, 7926.2642, 4025.0342, 5229.5400, 2229.2458, 2720.7056, 5195.3091, 2973.6316, 4047.8770, 4950.3491, 2832.6008, 5063.9155, 2245.2974, 5396.0581, 4124.9199, 3296.2627]
```

Per-image PSNR:

```text
[12.4712, 9.1401, 12.0831, 10.9462, 14.6492, 13.7840, 10.9747, 13.3979, 12.0585, 11.1844, 13.6089, 11.0859, 14.6181, 10.8100, 11.9766, 12.9506]
```

Per-image SSIM:

```text
[0.1090, 0.0575, 0.2684, 0.1547, 0.1845, 0.1427, 0.1650, 0.2014, 0.0942, 0.1133, 0.2096, 0.2072, 0.3329, 0.3022, 0.1036, 0.2554]
```

Mean metrics:

- `mean_mse`: `4121.12109375`。
- `mean_psnr_db`: `12.233728408813477`。
- `mean_ssim`: `0.18134805560112`。

Comparison with 50-step smoke:

- 50-step eval-smoke 使用 `4` 张图，200-step eval-smoke 使用 `16` 张图，因此二者不能严格公平对比。
- 可以谨慎观察：200-step loss 比 50-step 更低。
- 200-step eval 使用更多测试图，评估稍微更稳。
- 但它仍然不是完整测试集，不能说明论文级性能。

Beginner notes:

- 200-step tiny training 可以理解成把之前的 50-step 小测试再延长一点，看训练链路能否继续稳定下降。
- Loss 大幅下降说明模型在当前训练小批量上“学得很快”，但也可能是在记住这些很少的训练样本。
- Eval-smoke 从 4 张图扩展到 16 张图，比之前稍微稳一点，但仍然只是抽查，不是完整考试。
- 本阶段最稳妥的说法是：200-step 受控 tiny training + checkpoint + 16 张 test 图 eval-smoke 已完成。不能说论文复现成功。

Safety boundary confirmed:

- Training was run, but only for 200-step tiny training。
- No long training was run; this is still controlled smoke scope。
- Checkpoint was saved under `D:\Research\ai-data`。
- No images were saved。
- No run summary was written。
- No new data was downloaded。
- `external/ADJSCC` was not modified。
- Official train/eval was not run。
- No formal paper metrics were produced。
- Checkpoint was not added to Git。

Current conclusion:

- 200-step 受控 tiny training 扩展已完成。
- 可以记录为：训练链路可以连续跑 200 step，受控保存 checkpoint，并用该 checkpoint 完成 16 张 CIFAR-10 test split 图片的 eval-smoke。
- 不能记录为正式训练完成。
- 不能记录为正式论文 evaluation 完成。
- 不能记录为论文复现完成。
- 不能把本次小样本指标和论文表格或曲线直接比较。

Next step:

- 可以把本次 200-step 结果交给 Git 管理 Agent 处理 Markdown 记录和已有代码改动。
- 后续如果继续推进，建议先规划完整 test split evaluation、随机种子或多次传输平均，以及是否保存 run summary。

### 100-image expanded eval-smoke

Status: 100-image expanded eval-smoke 已完成。本阶段没有重新训练，而是复用已有 200-step checkpoint，把 eval-smoke 的 CIFAR-10 `test_batch` 图片数量从 16 扩大到 100，并计算 MSE、PSNR 和 SSIM 的 mean 指标。它可以记录为 expanded eval-smoke 成功，不能记录为正式 evaluation 完成。

Evidence source: 用户提供的 100-image eval-smoke 结果和代码改动说明。

Code change notes:

- `src/repro/cifar10_smoke.py` 中 `MAX_EVAL_SMOKE_IMAGES` 从 `16` 改为 `100`。
- `DEFAULT_EVAL_SMOKE_IMAGES` 仍保持 `4`。
- 未修改 `MAX_TINY_TRAIN_STEPS`。
- 未修改训练逻辑。
- 未修改 checkpoint 逻辑。
- 未修改指标计算逻辑。

Checkpoint used:

- WSL 路径：`/mnt/d/Research/ai-data/checkpoints/ADJSCC/tiny_train_smoke_20260614-191721/ckpt`。
- Windows 路径：`D:\Research\ai-data\checkpoints\ADJSCC\tiny_train_smoke_20260614-191721\ckpt`。
- 使用的是已有 200-step checkpoint。
- 本阶段没有保存新 checkpoint。
- Checkpoint 没有加入 Git。

Eval-smoke 设置：

- Data split: `test`。
- Image count: `100`。
- Checkpoint used: `true`。
- Input shape: `(100, 32, 32, 3)`。
- Output shape: `(100, 32, 32, 3)`。
- 是否重新训练：否。

Mean metrics:

- `mean_mse`: `4599.38916015625`。
- `mean_psnr_db`: `11.864448547363281`。
- `mean_ssim`: `0.15781359374523163`。

Beginner notes:

- 100 张图片比 16 张图片更能观察指标是否稳定，因为样本更多，单张图片的偶然影响会稍微小一些。
- 但 CIFAR-10 test split 一共有 10000 张图片，100 张仍然只是小样本 smoke，不是完整测试集 evaluation。
- 本阶段没有重新训练，只是复用已有 200-step checkpoint，所以它验证的是“这个 checkpoint 能在更多测试图上跑 eval-smoke”。
- 当前 MSE / PSNR / SSIM 不能当作论文正式指标，也不能和论文表格直接比较。
- 更稳妥的说法是：expanded eval-smoke 成功；不能说正式 evaluation 完成。

Safety boundary confirmed:

- Training was not run。
- No new checkpoint was saved。
- Existing 200-step checkpoint was used。
- No images were saved。
- No run summary was written。
- No new data was downloaded。
- `external/ADJSCC` was not modified。
- Official train/eval was not run。
- No formal paper metrics were produced。
- Checkpoint was not added to Git。

Current conclusion:

- 100-image expanded eval-smoke 已完成。
- 可以记录为：已有 200-step checkpoint 能加载，并在 100 张 CIFAR-10 test split 图片上完成 MSE / PSNR / SSIM mean 指标计算。
- 不能记录为正式论文 evaluation 完成。
- 不能记录为论文复现完成。
- 不能把当前 100 张小样本指标当作论文正式指标。

Next step:

- 可以把本次 expanded eval-smoke 记录交给 Git 管理 Agent。
- 后续如继续推进，建议单独规划完整 10000 张 test split evaluation、随机种子或多次传输平均、是否保存 run summary，以及是否需要更正式的 checkpoint。

## 2026-06-16

### 500-step tiny training + checkpoint + 100-image eval-smoke

Status: 500-step 受控 tiny training 和 100-image eval-smoke 已完成。本阶段把 tiny training 上限提高到 500，运行 500-step 受控训练，显式保存 checkpoint，再用该 checkpoint 在 CIFAR-10 `test_batch` 的 100 张图片上计算 MSE、PSNR 和 SSIM。它仍然是 smoke/预实验范围，不是正式训练，不是正式论文 evaluation，也不是论文复现完成。

Evidence source: 用户提供的 500-step tiny training、checkpoint 和 100-image eval-smoke 结果。

Code change notes:

- `src/repro/cifar10_smoke.py` 中 `MAX_TINY_TRAIN_STEPS` 从 `200` 改为 `500`。
- 默认 `--max-steps` 仍为 `10`，避免默认命令变成长训练。
- `MAX_EVAL_SMOKE_IMAGES` 仍为 `100`。
- 未修改 checkpoint 逻辑。
- 未修改指标计算逻辑。
- 未修改数据读取逻辑。

Checkpoint path:

- WSL 路径：`/mnt/d/Research/ai-data/checkpoints/ADJSCC/tiny_train_smoke_20260615-235340/ckpt`。
- Windows 路径：`D:\Research\ai-data\checkpoints\ADJSCC\tiny_train_smoke_20260615-235340\ckpt`。
- Checkpoint 保存到 `D:\Research\ai-data`，没有加入 Git。

Tiny training 设置：

- Max steps: `500`。
- Batch size: `2`。
- SNR: `10 dB`。
- 是否保存 checkpoint: 是。
- Checkpoint 是否进入 Git: 否。

Loss 关键节点：

- `step_1_loss`: `3471.86181640625`。
- `step_10_loss`: `3247.29345703125`。
- `step_50_loss`: `325.57470703125`。
- `step_100_loss`: `23.40330696105957`。
- `step_200_loss`: `7.393202304840088`。
- `step_300_loss`: `3.482886791229248`。
- `step_400_loss`: `4.400880336761475`。
- `step_500_loss`: `6.220396518707275`。

Loss interpretation:

- Loss 从约 `3471` 降到个位数，说明模型在当前 tiny training 的小批量训练链路上优化明显。
- 但是 `step 300` 到 `step 500` 有波动，不是严格单调下降。
- 因为 `batch_size=2`，训练样本极少，模型可能只是在继续拟合很小的一批样本。
- Loss 下降不等于模型泛化能力提升，也不等于论文复现成功。

Eval-smoke 设置：

- Data split: `test`。
- Image count: `100`。
- Checkpoint used: `true`。
- Input shape: `(100, 32, 32, 3)`。
- Output shape: `(100, 32, 32, 3)`。

100-image eval-smoke mean:

- `mean_mse`: `4700.11083984375`。
- `mean_psnr_db`: `11.812779426574707`。
- `mean_ssim`: `0.14577139914035797`。

Comparison with 200-step + 100-image eval-smoke:

- 200-step `mean_mse`: `4599.38916015625`。
- 200-step `mean_psnr_db`: `11.864448547363281`。
- 200-step `mean_ssim`: `0.15781359374523163`。
- 500-step 的 100-image `mean_mse`、`mean_psnr_db` 和 `mean_ssim` 没有优于 200-step。
- 这不能简单写成训练失败。更合理的说法是：在当前 tiny training 和 100-image eval-smoke 设置下，继续从 200 step 增加到 500 step，没有观察到测试小样本指标提升。
- 可能原因包括：`batch_size` 太小、训练样本太少、信道随机性、评估样本仍有限，以及当前还没有采用正式训练设置。

Beginner notes:

- 500-step tiny training 可以理解成把前面的受控小训练再延长一些，看看训练 loss 会不会继续变小。
- 这次训练 loss 明显下降，说明训练流程确实在更新模型参数；但模型可能只是更会处理训练中见到的极少量样本。
- Eval-smoke 用的是 100 张测试图，比 4 张或 16 张更有参考价值，但 CIFAR-10 测试集一共有 10000 张，所以它仍然只是小样本 smoke。
- 本阶段的稳妥结论是：500-step 训练、checkpoint 保存、checkpoint 加载和 100-image eval-smoke 链路已经跑通；不能说论文结果复现成功。

Safety boundary confirmed:

- Training was run, but only for 500-step tiny training。
- No long training was run; this is still controlled smoke/pre-experiment scope。
- Checkpoint was saved under `D:\Research\ai-data`。
- No images were saved。
- No run summary was written。
- No new data was downloaded。
- `external/ADJSCC` was not modified。
- Official train/eval was not run。
- No formal paper metrics were produced。
- Checkpoint was not added to Git。

Current conclusion:

- 500-step 受控 tiny training + checkpoint + 100-image eval-smoke 已完成。
- 可以记录为：训练 loss 在 tiny training 小批量上明显下降，并且保存出的 checkpoint 可以用于 100 张 CIFAR-10 test split 图片的 eval-smoke。
- 不能记录为正式训练完成。
- 不能记录为正式论文 evaluation 完成。
- 不能记录为论文复现完成。
- 不能把当前 100 张小样本指标当作论文正式指标。

Next step:

- 可以把本次 500-step 记录交给 Git 管理 Agent。
- 后续如果继续推进，建议先复盘是否需要更合理的训练数据循环、固定随机种子、多次传输平均、完整 10000 张 test split evaluation，以及是否保存更完整的 run summary。

## 2026-06-17

### TensorFlow GPU 审计与最小修复结果

Status: TensorFlow GPU 可用性验证成功。本阶段只验证 WSL2 + `adjscc-tf` 环境中 TensorFlow 2.14 是否能识别并使用 GPU，并记录环境数据配置 Agent 的最小修复结果。它是环境层面的 GPU smoke test，不是 ADJSCC 训练，不是真实数据复现，也不是论文复现完成。

Evidence source: 环境数据配置 Agent 汇报。

环境范围：

- WSL 发行版：`Ubuntu-ADJSCC`。
- 系统：Ubuntu 22.04.5 LTS。
- Conda 环境：`adjscc-tf`。
- Python 环境路径：`/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf`。
- GPU：NVIDIA GeForce RTX 4060 Laptop GPU。
- Windows Driver Version: `560.94`。
- Driver reported CUDA Version: `12.6`。
- TensorFlow 版本：`2.14.0`。
- TensorFlow CUDA build:
  - `cuda_version`: `11.8`。
  - `cudnn_version`: `8`。

初始问题：

- WSL2 中 `nvidia-smi` 可见 NVIDIA GeForce RTX 4060 Laptop GPU，说明 Windows 驱动和 WSL GPU 映射大体正常。
- 但初始 `tf.config.list_physical_devices('GPU')` 返回空列表。
- 初步判断原因是：`adjscc-tf` 环境中缺少 TensorFlow 2.14 所需的 CUDA 11.8 / cuDNN 8 用户态动态库。

最小修复动作：

```bash
mamba install -c conda-forge cudatoolkit=11.8 cudnn=8
```

安装后，在当前终端临时设置：

```bash
export LD_LIBRARY_PATH="$CONDA_PREFIX/lib:$LD_LIBRARY_PATH"
```

Beginner notes:

- `nvidia-smi` 能看到 GPU，只说明系统和驱动层面能看到显卡。
- TensorFlow 要真正用上 GPU，还需要在当前 Python/conda 环境里找到匹配版本的 CUDA/cuDNN 动态库。
- 这次安装 `cudatoolkit=11.8` 和 `cudnn=8`，是为了匹配 TensorFlow 2.14 的 CUDA build。
- `LD_LIBRARY_PATH` 可以理解成告诉程序“去哪里找这些动态库”。这次是临时设置，新开终端后可能需要重新设置。

验证结果：

- 修复后 `tf.config.list_physical_devices('GPU')` 返回：

```python
[PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]
```

- 进一步运行 `1024 x 1024` 矩阵乘法后，TensorFlow 成功创建 GPU 设备：

```text
NVIDIA GeForce RTX 4060 Laptop GPU
```

- 输出形状：

```text
(1024, 1024)
```

Current conclusion:

- WSL2 + `adjscc-tf` 环境下，TensorFlow 2.14 GPU 可用性验证成功。
- 这说明 TensorFlow 不只是能看到 GPU，也能把实际矩阵计算放到 GPU 上执行。
- 但这仍然只是环境验证成功，不代表 ADJSCC 模型训练成功，不代表真实数据复现完成，也不能写成论文复现成功。

Non-blocking warnings:

- `Unable to register cuDNN/cuFFT/cuBLAS factory`。
- `TF-TRT Warning: Could not find TensorRT`。
- `could not open file to read NUMA node`。

当前判断：

- 这些日志提示需要记录，但本阶段不作为阻塞项。
- 原因是 TensorFlow 已经成功识别 GPU，并完成矩阵计算验证。
- 后续如果进入更正式训练或性能调优阶段，可以再单独评估这些 warning 是否影响稳定性或性能。

Safety boundary confirmed:

- ADJSCC training was not run。
- `external/ADJSCC/adjscc_cifar10.py` was not run。
- No data was downloaded。
- `external/ADJSCC` was not modified。
- Project source code was not modified for this record。
- No checkpoint was saved by this record。
- No paper metrics were produced。
- Git was not committed。

Next step:

- 如果后续继续使用 GPU，新开终端后可能需要重新执行：

```bash
export LD_LIBRARY_PATH="$CONDA_PREFIX/lib:$LD_LIBRARY_PATH"
```

- 后续可以单独规划是否把该设置写入 conda activate 脚本，但本阶段先不直接修改。
- 进入 ADJSCC 实验时仍应从小规模 smoke 开始，例如 GPU 环境下的安全 wrapper 检查、小 batch forward 或 tiny training，不要因为 GPU 验证成功就直接启动长训练。

## 2026-06-18

### WSL2 + adjscc-tf TensorFlow GPU fake-forward 验证

Status: GPU 环境下 ADJSCC smoke wrapper 的 `--fake-forward` 已通过。本阶段记录 conda activate/deactivate 脚本已经固化 CUDA/cuDNN 和 XLA 相关环境变量，新 shell 中无需手动 export `LD_LIBRARY_PATH` / `XLA_FLAGS`。这仍然只是 GPU 环境下的 fake-forward smoke，不是真实 CIFAR-10 forward，不是训练，也不是论文复现完成。

Evidence source: 用户提供的 GPU 环境修复和 fake-forward 验证结果。

环境基础状态：

- WSL 发行版：`Ubuntu-ADJSCC`。
- Conda 环境：`adjscc-tf`。
- TensorFlow: `2.14.0`。
- GPU: NVIDIA GeForce RTX 4060 Laptop GPU。
- WSL 中 `nvidia-smi` 可见 GPU。
- 已安装 `cudatoolkit=11.8` 和 `cudnn=8`。
- TensorFlow GPU 列表非空：

```python
[PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]
```

Conda activate/deactivate scripts:

- Activate 脚本：`/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/etc/conda/activate.d/adjscc_cuda_libs.sh`。
- Deactivate 脚本：`/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/etc/conda/deactivate.d/adjscc_cuda_libs.sh`。
- Activate 脚本负责自动设置 `LD_LIBRARY_PATH` 和 `XLA_FLAGS`。

关键路径：

- `LD_LIBRARY_PATH` 包含：`/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/lib`。
- `XLA_FLAGS` 指向：`--xla_gpu_cuda_data_dir=/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf`。
- `libdevice` 路径：`/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/nvvm/libdevice/libdevice.10.bc`。

Beginner notes:

- `LD_LIBRARY_PATH` 可以理解成“动态库搜索路线图”。它告诉 TensorFlow 去哪里找 CUDA/cuDNN 这些 GPU 运行需要的库文件。
- `XLA_FLAGS` 是给 TensorFlow/XLA 的提示，告诉它去哪里找 `libdevice`。`libdevice` 是一些 GPU 编译/执行时会用到的底层数学和设备函数。
- 把这些设置写进 conda activate 脚本后，以后进入 `adjscc-tf` 环境时会自动设置，不需要每次新开 shell 都手动 export。

GPU fake-forward command:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m src.repro.cifar10_smoke --fake-forward
```

关键输出：

- `fake_input_shape`: `(2, 32, 32, 3)`。
- `snr_shape`: `(2, 1)`。
- `fake_output_shape`: `(2, 32, 32, 3)`。
- `fake_output_dtype`: `float32`。
- `Fake-forward completed`。

Fake-forward interpretation:

- `--fake-forward` 只使用假输入检查模型前向链路能不能跑通。
- 输入 shape 是 `(2, 32, 32, 3)`，表示 2 张假的 32x32 RGB 图片。
- 输出 shape 仍是 `(2, 32, 32, 3)`，说明模型输出保持了图片形状。
- 这说明 GPU 环境下 ADJSCC smoke wrapper 的前向链路已经跑通。
- 但它不加载真实 CIFAR-10，不训练，不保存 checkpoint，也不产生论文指标。

Current conclusion:

- GPU 环境下 ADJSCC smoke wrapper 的 fake-forward 已通过。
- 新 shell 中无需手动 export `LD_LIBRARY_PATH` / `XLA_FLAGS`。
- 这说明 GPU 环境修复已经从“TensorFlow 能看到 GPU”推进到“项目安全 wrapper 的 fake-forward 能跑通”。
- 但当前还没有验证 GPU real-batch-forward，也没有验证 GPU tiny training。

Warnings:

- 仍有 NUMA、`ptxas` / `nvlink` 等警告。
- 当前判断：这些警告需要记录，但 fake-forward 已通过，暂时不阻塞 smoke 阶段。
- 后续如果进入真实数据 forward、tiny training 或更长训练，再继续观察这些 warning 是否影响稳定性或性能。

Safety boundary confirmed:

- Real-batch-forward was not run。
- Tiny-train was not run。
- Long training was not run。
- No new data was downloaded。
- No checkpoint was saved。
- No images were saved。
- No run summary was written。
- `external/ADJSCC` was not modified。
- No paper metrics were produced。

Next step:

- 可以把本次 GPU fake-forward 记录交给 Git 管理 Agent。
- 后续如果继续推进，建议单独规划 GPU real-batch-forward，再规划 GPU tiny training；每一步继续保持明确边界，不要直接跳到长训练。

### WSL2 + adjscc-tf TensorFlow GPU real-batch-forward 验证

Status: GPU 环境下 ADJSCC smoke wrapper 的 `--real-batch-forward` 已通过。本阶段验证新 shell 激活 `adjscc-tf` 后，无需手动 export `LD_LIBRARY_PATH` / `XLA_FLAGS`，即可读取真实 CIFAR-10 小批量并完成 ADJSCC forward。它仍然不是训练，不保存 checkpoint，也不产生论文指标。

Evidence source: 用户提供的 GPU real-batch-forward 自动环境验证结果。

环境基础状态：

- WSL 发行版：`Ubuntu-ADJSCC`。
- Conda 环境：`adjscc-tf`。
- Conda 环境路径：`/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf`。
- TensorFlow GPU 环境已经稳定到 real-batch-forward 级别。
- 新 shell 激活 `adjscc-tf` 后，无需手动 export `LD_LIBRARY_PATH` / `XLA_FLAGS`。

Conda activate/deactivate scripts:

- Activate 脚本：`/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/etc/conda/activate.d/adjscc_cuda_libs.sh`。
- Deactivate 脚本：`/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/etc/conda/deactivate.d/adjscc_cuda_libs.sh`。

自动环境变量：

- `LD_LIBRARY_PATH` 自动包含：`$CONDA_PREFIX/lib`。
- `XLA_FLAGS` 自动包含：`--xla_gpu_cuda_data_dir=$CONDA_PREFIX`。
- `libdevice` 标准路径存在：`$CONDA_PREFIX/nvvm/libdevice/libdevice.10.bc`。

GPU real-batch-forward command:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m src.repro.cifar10_smoke --real-batch-forward
```

关键输出：

- `cifar10_batch_source`: `cifar-10-batches-py/data_batch_1`。
- `real_input_shape`: `(2, 32, 32, 3)`。
- `snr_shape`: `(2, 1)`。
- `real_output_shape`: `(2, 32, 32, 3)`。
- `real_output_dtype`: `float32`。
- `Real-batch-forward completed. No training was run, no checkpoint was written, and no data was downloaded.`。

Beginner notes:

- `fake-forward` 用的是随机假图，主要检查模型结构和 GPU 环境能不能跑一次前向。
- `real-batch-forward` 用的是真实 CIFAR-10 小批量，所以它比 fake-forward 更接近真实实验入口。
- 这一步说明 GPU 环境不仅能跑模型，还能读取真实 CIFAR-10 batch，并完成 ADJSCC forward。
- 这里的 forward 只是“把图片送进模型，再拿到输出”，不会更新模型参数。
- 因此它仍然不是训练，没有保存 checkpoint，也没有产生 PSNR、SSIM、MS-SSIM 等论文指标。

Current conclusion:

- GPU real-batch-forward 已通过。
- 可以记录为：自动 CUDA/XLA 环境变量在新 shell 中生效，真实 CIFAR-10 小批量可以在 GPU 环境下进入 ADJSCC smoke wrapper 并完成 forward。
- 不能记录为：GPU training 已完成。
- 不能记录为：论文 evaluation 已完成。
- 不能记录为：论文复现成功。

Safety boundary confirmed:

- Training was not run。
- No checkpoint was saved。
- No images were saved。
- No run summary was written。
- No new data was downloaded。
- `external/ADJSCC` was not modified。
- Git was not committed。
- No paper metrics were produced。

Next step:

- 可以把本次 GPU real-batch-forward 记录交给 Git 管理 Agent。
- 下一步可以单独规划 GPU tiny training 对照实验，继续使用严格步数限制、外部 checkpoint 路径和明确的 no-paper-result 边界。

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

## 2026-06-10 Phase Summary: Minimal Checkpoint Evaluation Loop

Status: added a phase-level summary for the first usable CIFAR-10 minimal loop. The project can now perform a tiny training run, save a controlled checkpoint, load that checkpoint, and run `eval-smoke` on 4 images from CIFAR-10 `test_batch`.

New summary document:

- `results/phase_summary_2026-06-10_minimal_loop.md`

Key evidence:

- Tiny training ran for `10` steps with `batch_size=2` and `SNR=10 dB`.
- Checkpoint path: `/mnt/d/Research/ai-data/checkpoints/ADJSCC/tiny_train_smoke_20260610-111436/ckpt`.
- Eval-smoke loaded that checkpoint and evaluated 4 CIFAR-10 `test_batch` images.
- Mean eval-smoke metrics:
  - `mean_mse`: `4392.0146484375`
  - `mean_psnr_db`: `11.982768058776855`
  - `mean_ssim`: `0.09460055828094482`

Boundary:

- This is a minimal smoke-stage loop, not formal paper training.
- This is not full test-set evaluation.
- These metrics cannot be compared with the paper table or curves.
- The checkpoint remains outside Git under `D:\Research\ai-data`.
- No dataset, checkpoint, image, run summary JSON, cache, `.h5`, `.ckpt`, or `.keras` artifact should be committed.

Code note:

- Updated the wrapper safety wording so it no longer says checkpoint writes never happen. The wording now states that checkpoint writes require explicit tiny-train `--save-checkpoint` and are restricted to the external checkpoint root.
