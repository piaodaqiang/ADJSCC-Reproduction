# 2026-06-10 Checkpoint Eval-Smoke 最小闭环记录

日期：2026-06-10

本报告记录 ADJSCC-Reproduction 项目的最小“训练-保存-加载-评估”闭环 smoke。本阶段完成了 10-step tiny training，显式保存 checkpoint，然后 eval-smoke 加载这个 checkpoint，并在 CIFAR-10 `test_batch` 的 4 张图上计算 MSE、PSNR 和 SSIM。当前结论是：这条最小闭环已经打通，但它不是正式训练，不是正式论文 evaluation，也不是论文复现完成。

## 本阶段目标

建立一个最小可交付闭环：

```text
tiny training 10 step
-> 显式保存 checkpoint
-> eval-smoke 加载该 checkpoint
-> 在 CIFAR-10 test_batch 的 4 张图上计算 MSE / PSNR / SSIM
```

对科研新手来说，这一步的重点不是“模型效果好不好”，而是确认一条关键流程已经能走完：模型能训练一点点、能把参数存下来、能再加载回来、能在测试集小样本上算指标。

## Checkpoint 路径

- WSL 路径：`/mnt/d/Research/ai-data/checkpoints/ADJSCC/tiny_train_smoke_20260610-111436/ckpt`
- Windows 路径：`D:\Research\ai-data\checkpoints\ADJSCC\tiny_train_smoke_20260610-111436\ckpt`
- Checkpoint 是否在 Git 仓库外：是。
- Checkpoint 是否加入 Git：否。

Checkpoint 是模型训练后的参数存档。可以把它理解成“模型当时学到的参数快照”。本次 checkpoint 放在 `D:\Research\ai-data`，不是放在 Git 仓库里，是为了避免把模型权重这类运行产物混进代码和笔记的版本历史。

## Tiny Training 设置与 Loss

- Max steps: `10`
- Batch size: `2`
- SNR: `10 dB`
- 是否保存 checkpoint: 是

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

这次 10-step tiny training 只是验证训练和保存流程，不是正式训练。10 step 太短，不能说明模型已经训练好，也不能作为论文结果。

## Eval-Smoke 设置

- Data split: `test`
- Image count: `4`
- Checkpoint used: `true`
- Checkpoint path: `/mnt/d/Research/ai-data/checkpoints/ADJSCC/tiny_train_smoke_20260610-111436/ckpt`
- Input shape: `(4, 32, 32, 3)`
- Output shape: `(4, 32, 32, 3)`
- SNR: `10 dB`

Eval-smoke 加载 checkpoint 后，只评估了 CIFAR-10 `test_batch` 的 4 张图片。这是小样本测试集 smoke，不是完整测试集 evaluation。

## Eval-Smoke 指标

Per-image MSE:

- `image_1_mse`: `2502.846435546875`
- `image_2_mse`: `6873.56689453125`
- `image_3_mse`: `4300.40234375`
- `image_4_mse`: `3891.243408203125`

Per-image PSNR:

- `image_1_psnr_db`: `14.14646053314209`
- `image_2_psnr_db`: `9.758981704711914`
- `image_3_psnr_db`: `11.7957124710083`
- `image_4_psnr_db`: `12.229918479919434`

Per-image SSIM:

- `image_1_ssim`: `0.10743298381567001`
- `image_2_ssim`: `0.08025652915239334`
- `image_3_ssim`: `0.09003458172082901`
- `image_4_ssim`: `0.10067815333604813`

Mean metrics:

- `mean_mse`: `4392.0146484375`
- `mean_psnr_db`: `11.982768058776855`
- `mean_ssim`: `0.09460055828094482`

这些 MSE / PSNR / SSIM 数值不能和论文表格或曲线比较。原因是当前只有 10-step tiny training，没有正式训练 checkpoint，也只评估了 4 张测试图片。

## 给科研新手的解释

这个闭环代表：项目已经能从“训练一点点”走到“保存模型参数”，再走到“加载参数做测试集小样本评估”。这对复现实验很重要，因为后面正式训练和正式评估都要依赖这条链路。

这个闭环不能代表：模型已经训练好了，论文结果已经复现了，或者当前指标可以和论文表格对比。它只是一个最小可交付 smoke，证明流程没有断。

如果你最近要准备期末和六级，这个节点很适合先收住：它已经是一个清楚、可交付、能解释的阶段成果。

## 安全边界

本阶段确认：

- 是否运行训练：是，仅 10-step tiny training。
- 是否长训练：否。
- 是否保存 checkpoint：是，受控保存在 `D:\Research\ai-data`。
- 是否保存图片：否。
- 是否写 `.h5` / `.keras`：否。
- 是否写 run summary：否。
- 是否下载新数据：否。
- 是否修改 `external/ADJSCC`：否。
- 是否运行官方 train/eval：否。
- 是否产生正式论文指标：否。
- Checkpoint 是否加入 Git：否。

## 代码复现 Agent 审查结论

代码复现 Agent 已确认：

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

## 非阻塞问题

1. 文件开头和主程序安全提示仍写 “no checkpoint write”，但现在 tiny-train 显式 `--save-checkpoint` 会写 checkpoint。后续建议改成 “no checkpoint write unless explicitly requested for tiny-train”。
2. `MAX_TINY_TRAIN_STEPS` 从 `10` 提到 `50`。当前跑的是 `10 step`，没问题；后续如需极保守，可重新讨论是否改回 `10`。

## 当前结论

最小“训练-保存-加载-评估”闭环 smoke 已完成。可以记录为：当前项目已经能完成 10-step tiny training、受控保存 checkpoint、加载 checkpoint，并在 CIFAR-10 test split 的 4 张图上计算 MSE / PSNR / SSIM。

但不能记录为：

- 正式训练完成。
- 正式论文 evaluation 完成。
- 论文完整复现完成。
- 当前指标可以和论文表格或曲线直接比较。

## 下一步建议

- 先把当前闭环作为期末和六级复习前的最小可交付节点，交给 Git 管理 Agent 处理。
- 不要把 checkpoint 加入 Git。
- 后续如继续推进，再单独规划是否做更长训练、正式 checkpoint、完整 test split evaluation，以及是否保存 run summary。
