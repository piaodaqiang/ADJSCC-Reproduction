# 真实 CIFAR-10 数据 Forward Smoke 阶段记录

日期：2026-05-27

本报告记录 ADJSCC-Reproduction 项目的真实 CIFAR-10 数据 forward smoke 阶段。当前结论是：真实 CIFAR-10 数据已经能够进入 smoke wrapper，并得到同尺寸模型输出。它不是训练结果，不是论文完整复现结果，也没有产生 PSNR、SSIM、MS-SSIM 等论文指标。

## 本阶段目标

- 在不训练、不保存 checkpoint、不修改 `external/ADJSCC` 的前提下，确认真实 CIFAR-10 数据能否进入模型。
- 验证模型能对极小 batch 做一次 forward pass，并输出与输入同尺寸的图像张量。
- 为后续 tiny training 规划提供一个更可靠的前置证据。

## 已运行命令

```bash
/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/bin/python -m src.repro.cifar10_smoke --real-batch-forward
```

## 数据与输出结果

数据门禁结果：

- 数据门禁通过。
- 已识别本地 CIFAR-10 压缩包：

```text
/mnt/d/Research/ai-data/datasets/CIFAR10/cifar-10-python.tar.gz
```

Forward smoke 结果：

- 输入 batch shape：`(2, 32, 32, 3)`。
- 输出 shape：`(2, 32, 32, 3)`。
- 输入和输出的图像尺寸一致，说明模型链路可以接收真实 CIFAR-10 小批量数据并完成一次输出计算。

## 给科研新手的解释

`forward pass` 可以理解为“把数据喂给模型，让它从入口走到出口一次”。

在这一步中：

- 模型看到了 2 张 CIFAR-10 图片。
- 每张图片大小是 `32 x 32`，有 3 个颜色通道，也就是 RGB。
- 模型计算后输出了 2 张同样形状的结果。

但这一步不会训练模型：

- 不会根据误差修改模型参数。
- 不会让模型变得更准。
- 不会保存训练权重。
- 不会产生论文中的 PSNR、SSIM、MS-SSIM 指标。

这一步的重要性在于：它证明“真实数据 -> 模型 -> 输出”的最小通路已经跑通。后面如果要做 tiny training，就不是从环境或数据读取问题开始排雷了。

## 安全边界确认

本阶段确认：

- 未运行训练。
- 未保存 checkpoint。
- 未下载新数据。
- 未修改 `external/ADJSCC`。
- 运行前后 `git status --short` 均无输出。

## 当前结论

`--real-batch-forward` 已通过。当前可以说真实 CIFAR-10 数据 forward smoke 成功，但不能说训练成功，也不能说论文复现完成。

尚未产生：

- PSNR
- SSIM
- MS-SSIM
- 训练曲线
- checkpoint
- 论文表格或论文图像级复现结果

## 下一步建议

项目可以进入 tiny training 规划阶段，但不能直接开始训练。

tiny training 规划前应先明确：

- 训练步数或 epoch 数。
- 输出目录。
- 是否允许写入 checkpoint。
- 是否允许写入日志和小型结果文件。
- 如何记录 loss、PSNR、SSIM 或 MS-SSIM。
- 出现 GPU 不可用、显存不足、数据读取失败时如何停止并记录。

在用户确认这些边界之前，仍然不要运行训练。
