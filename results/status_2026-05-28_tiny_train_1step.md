# 1-Step Tiny Training Smoke 阶段记录

日期：2026-05-28

本报告记录 ADJSCC-Reproduction 项目的 1-step tiny training smoke。当前结论是：训练链路已经能用真实 CIFAR-10 小 batch 跑通 1 个训练 step，并算出一个 loss。它不是正式训练结果，不是论文完整复现结果，也没有产生 PSNR、SSIM、MS-SSIM 等论文指标。

## 本阶段目标

- 验证 `--tiny-train` 入口能否安全启动。
- 验证真实 CIFAR-10 数据能进入训练链路。
- 验证模型能完成一次前向计算、loss 计算和一次极小训练更新。
- 继续保持不下载新数据、不保存 checkpoint、不修改 `external/ADJSCC` 的边界。

## 已运行命令

```bash
PYTHONDONTWRITEBYTECODE=1 /home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/bin/python -m src.repro.cifar10_smoke --tiny-train --max-steps 1 --batch-size 2
```

## 训练结果

- 训练模式：`--tiny-train`。
- 最大训练步数：`1`。
- Batch size：`2`。
- CIFAR-10 数据门禁：通过。
- 输入 batch shape：`(2, 32, 32, 3)`。
- 输出 shape：`(2, 32, 32, 3)`。
- 记录到的 loss：

```text
tiny_train_step_1_loss: 3471.53759765625
```

## 给科研新手的解释

### tiny training 是什么

`tiny training` 是一次超小规模训练试跑。可以把它理解成：真正上路前，先轻轻踩一下油门，确认车能动、方向盘能转、刹车也还在。

在这里，它的作用不是训练出好模型，而是确认这些环节能连起来：

- 读取 CIFAR-10 数据。
- 把数据送进模型。
- 模型算出输出。
- 程序根据输出算出 loss。
- 训练代码能完成一次很小的参数更新。

### loss 是什么

`loss` 可以理解成模型当前输出和目标之间的误差数字。一般来说，训练时程序会尝试让 loss 变小。

但这次的 `loss=3471.53759765625` 只说明：训练链路能算出损失值。它不代表论文效果，也不能说明模型已经学好了。

### 为什么 1 step training 不等于正式训练

`1 step` 只表示模型用一个很小的 batch 做了一次训练更新。它太短了，不能代表模型真的学到了稳定规律。

正式训练通常需要很多 step 或很多 epoch，还要保存日志、评估指标、对比不同 SNR、比较 PSNR/SSIM/MS-SSIM 等结果。当前阶段还没有做这些。

### 为什么这不是论文完整复现

论文复现至少需要可重复的训练设置、足够训练时间、评价指标、对比实验和结果分析。

当前阶段没有：

- 长训练。
- checkpoint。
- PSNR。
- SSIM。
- MS-SSIM。
- 论文表格或曲线。
- 与论文结果的数值对比。

所以它只能写成 training smoke，不能写成论文复现完成。

### 为什么没有 checkpoint 也可以记录这个阶段

Checkpoint 是保存下来的模型权重，方便以后继续训练或评估。

这次不保存 checkpoint 是合理的，因为目标只是确认训练链路能不能跑通。记录命令、loss、shape 和安全边界，就足够说明这个阶段完成了。

等以后进入更长的 tiny training 或正式训练规划时，再决定是否允许保存 checkpoint。

## 安全边界确认

本阶段确认：

- 训练确实发生了，但只训练 1 step。
- 未运行长训练。
- 未保存 checkpoint。
- 未下载新数据。
- 未修改 `external/ADJSCC`。
- 未运行官方 train/eval。
- 未产生 PSNR、SSIM、MS-SSIM。

## 代码审查结论

代码复现 Agent 已审查：

- Tiny training 只在显式传入 `--tiny-train` 时运行。
- 默认模式仍是 `check-only`。
- 未发现 `save_weights`、`model.save`、`.save()`。
- `--save-checkpoint` 参数存在，但当前阶段会直接报错停止，不会保存 checkpoint。
- 未发现 `tf.keras.datasets.cifar10.load_data()`。
- `max_steps` 限制合理：1 到 10，默认 1。
- Run summary 只有显式传入 `--write-run-summary` 才写，并且必须位于 `/mnt/d/Research/ai-data/runs/ADJSCC` 内。

## 当前结论

1-step tiny training smoke 已完成。可以说训练链路已经跑通 1 step，并记录到一个 loss。

不能说：

- 正式训练完成。
- 论文复现完成。
- 模型效果达到论文结果。
- 已经产生 PSNR、SSIM、MS-SSIM。

## 下一步建议

下一步可以规划：

- 5-step tiny training。
- 或一次带 `--write-run-summary` 的 run summary 测试。

但不能直接进入正式训练。下一阶段开始前，应先确认：

- 最大训练 step 数。
- 是否允许写 run summary。
- 是否继续禁止 checkpoint。
- 输出目录是否仍限定在 `/mnt/d/Research/ai-data/runs/ADJSCC`。
- 要记录哪些证据，例如 loss 列表、shape、耗时和安全边界。
