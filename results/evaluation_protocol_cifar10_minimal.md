# CIFAR-10 最小复现实验 Evaluation Protocol 口径草案

日期：2026-06-02

本文档用于整理 ADJSCC-Reproduction 项目中 CIFAR-10 最小复现实验后续“怎么算指标”的统一规则。它是 evaluation protocol，也就是评价口径草案，不是正式实验结果，不代表已经复现论文表格或曲线。

## 1. 文档目的

Evaluation protocol 可以理解为“以后做评价时大家都按同一套规则算分”。这里的“口径”就是规则：用哪部分数据、像素按什么范围、输出要不要 clip、PSNR 是先每张图算再平均还是先全局平均 MSE 再换算、SSIM 参数是什么。

可以把它想成考试评分细则。如果甲同学按 100 分制算，乙同学按 150 分制算，最后数字就不能公平比较。图像指标也是一样：只要口径不同，数字看起来差一点或好一点，都可能不是模型真的变了，而是计算规则变了。因此，在正式比较前必须先统一口径。

本文档的目标是先把 CIFAR-10 最小闭环阶段的评价规则写清楚，方便后续代码复现 Agent 检查 wrapper 是否一致，也方便以后真正跑 evaluation 时不混淆 smoke 结果和正式论文指标。

## 2. 当前阶段边界

当前项目仍处于 CIFAR-10 最小 smoke / tiny training 阶段。已经完成的是链路验证，不是正式论文复现。

当前已完成：

- MSE / PSNR metrics-smoke。
- SSIM metrics-smoke。
- tiny training 只用于确认训练链路能跑。

当前未完成：

- 未完成正式训练。
- 未保存正式 checkpoint。
- 未完成 CIFAR-10 完整测试集 evaluation。
- 未复现论文表格。
- 未复现论文曲线。
- 未得到可以和论文主结果公平比较的指标。

当前 smoke 结果只能说明“程序链路能跑、指标函数能算”，不能写成“模型达到论文结果”。

## 3. 数据范围

- 数据集：CIFAR-10。
- 当前本地数据位置：
  - Windows：`D:\Research\ai-data\datasets\CIFAR10`
  - WSL：`/mnt/d/Research/ai-data/datasets/CIFAR10`
- 正式 evaluation 应使用 CIFAR-10 `test` split。
- 当前 metrics-smoke / SSIM smoke 只用了 2 张图，样本太少，只能验证链路，不代表正式结果。

正式记录中必须写清楚使用的是 `train`、`test` 还是某个 tiny subset。不同 split 的指标不能混在一起比较。

## 4. 像素范围与 Clip Policy

当前 wrapper 的图像指标按 `[0,255]` 像素范围计算：

- target 图像按 `[0,255]` float 值参与计算。
- model outputs 会先 clip 到 `[0,255]`。
- MSE / PSNR / SSIM 使用 clip 后的 outputs。

clip policy 是重要口径，必须记录。原因是模型输出可能出现小于 0 或大于 255 的值。如果先 clip 再算，和不 clip 直接算，指标可能不同。以后如果别人看到同一个 checkpoint 在同一个 SNR 下有两个不同 PSNR，第一件事就要检查像素范围和 clip policy 是否一致。

当前草案默认：

- pixel range：`[0,255]`
- max pixel value：`255.0`
- output clip：yes，clip 到 `[0,255]`

## 5. PSNR 口径

当前 wrapper 的 PSNR 计算口径如下：

- MSE 按每张图的 `(H, W, C)` 求均值。
- 每张图的 PSNR 使用：

```text
PSNR = 10 * log10(255^2 / MSE)
```

- 当前 `batch_mean_psnr_db` 是 per-image PSNR 的平均值。
- 当前 `batch_mean_psnr_db` 不是先把整个 batch 的 MSE 全局平均后再换算得到的 PSNR。

正式 evaluation 时必须明确 PSNR 平均方式，因为下面两种方法可能给出不同数字：

- 方法 A：先每张图算 PSNR，再对所有图求平均。
- 方法 B：先对所有图算全局平均 MSE，再把这个 MSE 换算成 PSNR。

当前 smoke 使用方法 A。正式 CIFAR-10 evaluation 如果沿用当前 wrapper，应明确记录为“先每张图算 PSNR，再平均”。

## 6. SSIM 口径

当前 wrapper 的 SSIM 计算口径如下：

```python
tf.image.ssim(targets, clipped_outputs, max_val=255.0)
```

当前 SSIM 是每张图计算一次，然后再求 batch 平均。

正式 evaluation 需要固定并记录 SSIM 参数，至少包括：

- `max_val`
- `filter_size`
- `filter_sigma`
- `k1`
- `k2`
- 是否使用 TensorFlow 默认参数
- 输入是否已经 clip 到 `[0,255]`

当前阶段只完成 SSIM smoke。它只说明 SSIM 计算链路能跑，不代表正式感知质量结果，也不能作为论文结论。

## 7. MS-SSIM 暂缓

当前不把 MS-SSIM 纳入 CIFAR-10 最小闭环硬要求。

原因：

- CIFAR-10 图像只有 `32x32`。
- 默认 MS-SSIM 会做多尺度下采样，小图在多次下采样后空间尺寸很小，可能不适合直接套默认参数。
- 论文理解 Agent 结论中未看到 MS-SSIM 是该论文 CIFAR-10 主指标。
- CIFAR-10 主实验更关注 average MSE 和 average PSNR，结果曲线主要展示 PSNR。
- SSIM 可作为感知质量参考，但不是当前 CIFAR-10 主曲线核心指标。

后续如果确实需要加入 MS-SSIM，应单独设计参数、单独写 smoke test，并在文档中说明为什么这些参数适合 `32x32` CIFAR-10。

## 8. SNR 条件

当前 smoke 使用：

- SNR：`10 dB`

正式 evaluation 必须明确 SNR 列表，例如每个 SNR 单独记录一行或一个结果块。

不同 SNR 下的指标不能混在一起比较。原因是 ADJSCC 模型会经过信道，SNR 越低，信道噪声通常越强，重建图像更难；SNR 越高，信道条件更好。因此，`SNR=1 dB` 的 PSNR 和 `SNR=10 dB` 的 PSNR 不能直接放在一起说谁更好，除非明确它们是在不同信道条件下。

## 9. Checkpoint 策略

当前项目没有正式 checkpoint。

当前 tiny training 不保存 checkpoint，目的只是验证训练链路，不是产出可复用模型。

正式 evaluation 必须指定使用哪个 checkpoint，至少记录：

- checkpoint 路径。
- checkpoint 来自哪次训练。
- 训练数据和训练设置摘要。
- 对应 commit hash。
- 是否修改过 `external/ADJSCC`。

没有正式 checkpoint 时，不能声称复现论文指标。因为正式 evaluation 应该评价一个确定的模型权重；如果权重没有保存、来源不清楚，结果就无法复查，也无法公平比较。

## 10. 信道随机性

ADJSCC 涉及信道噪声。即使输入图像和模型 checkpoint 一样，信道随机性也可能让输出略有变化。

正式 evaluation 需要选择并记录统计策略：

- 固定 random seed 后评价一次。
- 或者同一图像在同一 SNR 下传输多次，再对结果求平均。

当前 smoke 只验证链路能跑，不处理统计稳定性，也不声称结果具有正式统计意义。

## 11. 结果记录格式建议

后续正式 evaluation 至少记录以下字段：

- commit hash。
- Python 版本。
- TensorFlow 版本。
- TensorFlow Compression 版本。
- TensorFlow Probability 版本。
- NumPy 版本。
- checkpoint 路径。
- data split，例如 CIFAR-10 `test`。
- SNR。
- batch size。
- image count。
- pixel range。
- clip policy。
- PSNR average method。
- SSIM parameters。
- 是否保存图片。
- 是否保存 run summary。
- 是否修改 `external/ADJSCC`。
- 是否使用官方 train/eval entrypoint。
- 是否下载新数据。

建议正式结果表中每个 SNR 单独成行，避免把不同信道条件下的指标混在一起。

## 12. 下一步建议

下一阶段建议：

- 先让代码复现 Agent 审查本文档中的 evaluation protocol 是否与当前 wrapper 完全一致。
- 暂缓 MS-SSIM。
- 暂缓长训练。
- 暂缓正式 evaluation。
- 在正式 evaluation 前，先确定 checkpoint 策略、SNR 列表、test split 读取方式、run summary 字段和是否保存重建图片。

当前最重要的不是马上追求更大的实验，而是先保证“以后怎么算指标”这件事讲清楚、写清楚、查得清楚。
