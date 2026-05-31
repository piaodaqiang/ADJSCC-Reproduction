# 2026-05-31 Enhanced Run Summary 验证记录

日期：2026-05-31

本报告记录 ADJSCC-Reproduction 项目的 enhanced run summary 验证结果。当前结论是：程序已经能在一次 1-step tiny training 后，生成更详细的 JSON 摘要，把环境版本、输入输出 shape、loss、输出路径和安全标记一起记录下来。它仍然只是 tiny training smoke，不是正式训练，不是论文完整复现，也没有产生 PSNR、SSIM、MS-SSIM 等论文指标。

## 本阶段目标

- 验证 enhanced run summary 是否能安全写入外部运行目录。
- 确认增强版 JSON 是否记录了运行环境、shape、路径、loss 和安全边界字段。
- 继续只运行 `1 step` tiny training，不进入正式训练。
- 继续保持安全边界：不保存 checkpoint，不下载新数据，不修改 `external/ADJSCC`，不把 JSON 运行产物加入 Git。

对科研新手来说，这一步不是为了训练出好模型，而是为了确认“实验小票”更完整了。以后回看时，能知道这次实验在哪个环境里跑、数据形状对不对、loss 是多少、有没有误用官方训练入口。

## Enhanced JSON 路径

- WSL 路径：`/mnt/d/Research/ai-data/runs/ADJSCC/tiny_train_summary_20260531-203648.json`
- Windows 路径：`D:\Research\ai-data\runs\ADJSCC\tiny_train_summary_20260531-203648.json`
- 外部运行目录：`/mnt/d/Research/ai-data/runs/ADJSCC`
- Windows 对应目录：`D:\Research\ai-data\runs\ADJSCC`

这个 JSON 文件在 `D:\Research\ai-data\runs\ADJSCC`，不加入 Git。仓库只记录它的路径和关键事实。

## 文件大小

- `907 bytes`

相比 2026-05-29 的 239 bytes 摘要，这次文件更大，是因为 enhanced run summary 记录了更多上下文，例如环境版本、shape、路径和安全标记。

## 运行设置

- Mode: `tiny-train`
- Max steps: `1`
- Batch size: `2`
- SNR: `10.0 dB`
- CIFAR-10 batch source: `cifar-10-batches-py/data_batch_1`

这次仍然只运行 `1 step` tiny training。`1 step` 只能用来确认训练和记录链路能跑通，不能代表模型已经完成训练。

## Loss

```text
loss: 3472.816162109375
```

这个 loss 不是论文指标。它只是训练过程里的误差数字，说明程序成功算出了一个 loss。论文复现通常需要 PSNR、SSIM、MS-SSIM 等评价指标，而本阶段没有产生这些指标。

## Enhanced JSON 字段

本次 enhanced JSON 包含：

- `timestamp`: `2026-05-31 20:36:48`
- `mode`: `tiny-train`
- `python_executable`
- `python_version`: `3.10.20`
- `tensorflow_version`: `2.14.0`
- `tensorflow_probability_version`: `0.22.0`
- `numpy_version`: `1.26.4`
- `input_shape`: `[2, 32, 32, 3]`
- `snr_shape`: `[2, 1]`
- `output_shape`: `[2, 32, 32, 3]`
- `run_root`
- `summary_path`
- `batch_size`: `2`
- `max_steps`: `1`
- `snr_db`: `10.0`
- `losses`: `[3472.816162109375]`
- `cifar10_batch_source`: `cifar-10-batches-py/data_batch_1`
- `checkpoint_saved`: `false`
- `data_downloaded`: `false`
- `official_train_eval_used`: `false`

## 给科研新手的解释

enhanced run summary 是“更详细的一次实验小摘要单”。它不只是写下 loss 和训练参数，还把 Python、TensorFlow、NumPy 版本、输入输出 shape、输出路径、是否保存 checkpoint、是否下载数据、是否调用官方 train/eval 等信息也记下来。

记录 Python/TensorFlow/numpy 版本，是为了以后能复查实验环境。深度学习代码很依赖软件版本，同一段代码在不同 TensorFlow 或 NumPy 版本下，可能报不同错误，也可能出现细小的数值差异。把版本写进 summary，就像给实验贴上环境标签。

记录 `input_shape / output_shape`，是为了确认数据真的按预期流过模型。这里 `input_shape=[2, 32, 32, 3]` 表示输入是 2 张 32x32 的 RGB 图片；`output_shape=[2, 32, 32, 3]` 表示模型输出仍然是 2 张同样大小的 RGB 图片。这个检查能帮助确认模型没有把图片形状弄乱。

`snr_shape=[2, 1]` 表示每张图片对应一个 SNR 条件值，和 batch size 2 对得上。

`official_train_eval_used=false` 很重要。它说明这次没有调用 ADJSCC 官方完整训练或评估入口，只是在本项目安全 wrapper 中跑了 tiny smoke。这样记录以后，就不会误把这次 1-step 小测试当成官方训练或正式评估。

这个 JSON 不进 Git，因为它是实验运行产物。类似文件以后可能越来越多，如果都放进 Git，版本历史会变得很乱。Git 仓库主要保存代码、笔记和小型总结；运行产物放在 `D:\Research\ai-data` 更合适。

这仍然不是论文复现结果。原因很直接：只跑了 `1 step`，没有正式训练，没有保存 checkpoint，没有 PSNR、SSIM、MS-SSIM，也没有和论文表格或曲线做数值对比。

## 安全边界

本阶段确认：

- 运行了训练，但只有 `1 step` tiny training。
- 没有运行长训练。
- 没有保存 checkpoint。
- 没有下载新数据。
- 没有修改 `external/ADJSCC`。
- 没有调用官方 train/eval。
- 没有把 enhanced JSON 加入 Git。
- 没有产生 PSNR。
- 没有产生 SSIM。
- 没有产生 MS-SSIM。

这些边界说明：当前阶段只是验证记录能力和安全链路，不是开始正式训练。

## 代码复现 Agent 审查结论

代码复现 Agent 已审查通过：

- enhanced summary 字段合理。
- `run_root / summary_path` 安全。
- 输出被限制在 `/mnt/d/Research/ai-data/runs/ADJSCC` 内。
- 未发现保存 checkpoint 风险。
- 未发现自动下载数据风险。
- 未发现官方 train/eval 调用风险。
- 未发现 `external/ADJSCC` 修改风险。
- 未发现 Git 污染风险。
- 当前不建议阻塞性修改。

可选建议：后续可以把文件头注释中 “avoids training” 改得更精确，因为现在代码已经存在显式 `--tiny-train` 模式。

## 当前结论

Enhanced run summary 验证通过。可以记录为：1-step tiny training 后，增强版 JSON 摘要能正确记录环境版本、输入输出 shape、路径、loss 和安全标记。

但不能记录为：

- 正式训练完成。
- 论文完整复现完成。
- 模型效果达到论文结果。
- 已经产生 PSNR、SSIM、MS-SSIM。
- `loss=3472.816162109375` 可以作为论文指标。

## 下一步建议

- 让 Git 管理 Agent 只接手本次 Markdown 记录，以及已有的代码改动。
- 不要把 `D:\Research\ai-data\runs\ADJSCC\tiny_train_summary_20260531-203648.json` 加入 Git。
- 下一步可以考虑 5-step tiny training，但仍需用户单独确认。
- 在用户明确确认前，不要运行更长训练，不要保存 checkpoint，不要下载新数据。
