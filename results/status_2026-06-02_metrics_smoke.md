# 2026-06-02 Metrics-Smoke 结果记录

日期：2026-06-02

本报告记录 ADJSCC-Reproduction 项目的 metrics-smoke 结果。本阶段读取本地 CIFAR-10 的 2 张图片，经过 ADJSCC 模型做一次非训练 forward，然后计算 MSE 和 PSNR。当前结论是：MSE/PSNR 指标计算链路已经能跑通，但这不是正式论文 evaluation，也不是论文复现完成。

## 本阶段目标

- 读取本地 CIFAR-10 的 2 张图片。
- 让图片经过 ADJSCC 模型做一次非训练 forward。
- 计算每张图片的 MSE 和 PSNR。
- 计算 batch mean MSE 和 batch mean PSNR。
- 确认指标计算流程能跑通，同时继续保持安全边界：不训练、不保存图片、不保存 checkpoint、不写 run summary、不下载新数据、不修改 `external/ADJSCC`。

对科研新手来说，这一步不是在正式评测模型效果，而是在检查“指标计算这条线能不能接起来”。也就是：模型能不能输出图像，程序能不能比较原图和输出图，再算出 MSE/PSNR。

## 运行命令

```bash
PYTHONDONTWRITEBYTECODE=1 /home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/bin/python -m src.repro.cifar10_smoke --metrics-smoke
```

本次结果记录 Agent 没有运行这条命令，只记录用户提供的已完成实验结果。

## 结果数据

- Metrics-smoke 是否通过：是。
- Input shape: `(2, 32, 32, 3)`。
- Output shape: `(2, 32, 32, 3)`。

Per-image MSE:

- `image_1_mse`: `3279.354736328125`
- `image_2_mse`: `3667.052490234375`

Per-image PSNR:

- `image_1_psnr_db`: `12.972919464111328`
- `image_2_psnr_db`: `12.487631797790527`

Batch mean:

- `batch_mean_mse`: `3473.20361328125`
- `batch_mean_psnr_db`: `12.730276107788086`

`input_shape=(2, 32, 32, 3)` 表示输入是 2 张 32x32 的 RGB 图片。`output_shape=(2, 32, 32, 3)` 表示模型输出仍然是 2 张同样大小的 RGB 图片。这个 shape 对得上，说明这次 forward 的图像形状没有明显跑偏。

## MSE/PSNR 解释

MSE 是“原图和重建图之间的平均平方误差”。可以把它理解成：每个像素都和原图比一下，差多少就记下来，再平方，最后求平均。通常 MSE 越小越好，因为误差越小，说明重建图越接近原图。

PSNR 是由 MSE 换算出来的图像质量分数，单位是 dB。通常 PSNR 越大越好，因为它表示重建图和原图越接近。

这里用 `255` 是因为当前图像像素按 `[0,255]` 范围计算。PSNR 公式需要知道像素的最大可能值，8-bit 图像常用最大值就是 255。

## 指标计算说明

- MSE 按每张图片的 `(H, W, C)` 求均值。
- PSNR 使用公式：`10 * log10(255^2 / MSE)`。
- `batch_mean_mse` 是两张图片 MSE 的平均值。
- `batch_mean_psnr_db` 是两张图片 PSNR 的平均值，不是由 `batch_mean_mse` 再换算得到。

这次只用了 2 张 CIFAR-10 图片，所以不能代表论文结果。正式论文 evaluation 通常需要完整测试集、固定实验设置、更多 SNR 条件，以及更完整的指标汇总。

## 安全边界

本阶段确认：

- 是否训练：否。
- 是否保存图片：否。
- 是否保存 checkpoint：否。
- 是否写 run summary：否。
- 是否下载新数据：否。
- 是否修改 `external/ADJSCC`：否。
- 是否产生正式论文指标：否。
- 当前没有 SSIM。
- 当前没有 MS-SSIM。
- 当前没有完整测试集评估。

这些边界说明：metrics-smoke 只是确认指标计算流程能跑通，不是正式 evaluation。

## 代码复现 Agent 审查结论

代码复现 Agent 已审查：

- `--metrics-smoke` 只有显式传入才会运行。
- 默认模式仍是 `check-only`。
- `run_metrics_smoke` 使用 `training=False`。
- 没有 `GradientTape()`，没有 `model.fit()`。
- 没有保存图片、checkpoint、`.h5`、`.ckpt`。
- 没有调用 `tf.keras.datasets.cifar10.load_data()`。
- 没有调用官方 `adjscc_cifar10.py train/eval`。
- MSE 按每张图片的 `(H, W, C)` 求均值。
- PSNR 使用 `10 * log10(255^2 / MSE)`。
- `batch_mean_psnr_db` 是每张图片 PSNR 的平均值，不是由 batch mean MSE 再换算得到。

## 当前结论

Metrics-smoke 通过。可以记录为：本项目已经能对 2 张 CIFAR-10 图片完成非训练 forward，并计算 MSE 和 PSNR。

但不能记录为：

- 正式论文 evaluation 完成。
- 论文完整复现完成。
- 模型效果达到论文结果。
- 已经完成完整测试集评估。
- 已经产生 SSIM 或 MS-SSIM。

## 下一步建议

- 让 Git 管理 Agent 只接手本次 Markdown 记录。
- 后续可以规划 SSIM/MS-SSIM smoke，或规划更完整的测试集 evaluation。
- 在继续之前，应先单独确认评估范围、是否保存结果、是否写 run summary、是否需要记录更多 SNR 条件。
