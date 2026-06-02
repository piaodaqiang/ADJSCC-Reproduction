# 2026-06-02 SSIM Smoke 结果记录

日期：2026-06-02

本报告记录 ADJSCC-Reproduction 项目的 SSIM smoke 结果。本阶段是在已有 `--metrics-smoke` 中加入 SSIM，用 2 张 CIFAR-10 图片验证 SSIM 指标计算链路。当前结论是：SSIM 计算流程能跑通，但这不是正式论文 evaluation，也不是论文复现完成。

## 本阶段目标

- 在已有 `--metrics-smoke` 中加入 SSIM 计算。
- 用 2 张 CIFAR-10 图片验证 SSIM 指标计算链路。
- 确认计算时先把模型输出 clip 到 `[0,255]`。
- 继续保持安全边界：不训练、不保存图片、不保存 checkpoint、不写 run summary、不下载新数据、不修改 `external/ADJSCC`。

这一步还是“小规模安全冒烟测试”。它像是先点一下开关，确认 SSIM 这条指标计算线有电，而不是正式评测模型质量。

## SSIM 结果

- `image_1_ssim`: `0.0835731998`
- `image_2_ssim`: `0.0400035866`
- `batch_mean_ssim`: `0.0617883950`

这次只用了 2 张 CIFAR-10 图片，所以这些 SSIM 数值只能说明链路能跑，不能代表论文正式结果。

## SSIM 计算方式

本阶段使用 TensorFlow API：

```python
tf.image.ssim(targets, clipped_outputs, max_val=255.0)
```

其中 `outputs` 会先 clip 到 `[0,255]`。这样做是因为图像指标通常要求像素值在合法图像范围内；如果输出图像数值跑到范围外，直接计算指标会让口径变得不清楚。

正式 evaluation 时必须明确记录是否 clip。是否 clip 会影响指标数值，所以它是一个重要评估口径，不能含糊带过。

## 给科研新手的解释

SSIM 是结构相似度指标。通常越接近 `1`，说明两张图的结构越相似；越低，说明结构差异越大。

PSNR 更偏“逐像素误差”，也就是一个像素一个像素地比较差多少。SSIM 更偏“结构和纹理像不像”，更接近看图片时关心的边缘、纹理和局部结构。

这次 SSIM smoke 只用了 2 张 CIFAR-10 图片，所以只能说明 SSIM 计算链路能跑。它不能说明模型已经达到论文效果，也不能代表完整测试集表现。

当前没有完整测试集 evaluation，没有 MS-SSIM，也没有正式训练 checkpoint。因此，当前 SSIM 数值不能写成论文正式结果。

## 安全边界

本阶段确认：

- 是否训练：否。
- 是否保存图片：否。
- 是否保存 checkpoint：否。
- 是否写 run summary：否。
- 是否下载新数据：否。
- 是否修改 `external/ADJSCC`：否。
- 是否产生正式论文指标：否。
- 是否有完整测试集 evaluation：否。
- 是否有 MS-SSIM：否。
- 是否有正式训练 checkpoint：否。

这些边界说明：这次仍然属于 smoke test，只验证指标计算流程，不进入正式评估或论文复现结论。

## 代码复现 Agent 审查结论

代码复现 Agent 已确认：

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

## 当前结论

SSIM smoke 通过。可以记录为：本项目已经能在 metrics-smoke 中对 2 张 CIFAR-10 图片计算 SSIM，并且记录了 clip 到 `[0,255]` 的计算口径。

但不能记录为：

- 正式论文 evaluation 完成。
- 论文完整复现完成。
- 模型效果达到论文结果。
- 已经完成完整测试集评估。
- 已经产生 MS-SSIM。
- 当前 SSIM 数值可以代表论文正式结果。

## 下一步建议

- 让 Git 管理 Agent 只接手本次 Markdown 记录。
- 后续可以规划 MS-SSIM smoke，或规划更完整的测试集 evaluation。
- 在继续之前，应先单独确认评估范围、checkpoint 策略、是否保存结果，以及是否记录 clip 等评估口径。
