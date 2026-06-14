# 2026-06-14 200-Step Tiny Training + 16-Image Eval-Smoke 记录

日期：2026-06-14

本报告记录 ADJSCC-Reproduction 项目的 200-step 受控 tiny training 扩展结果。本阶段运行 200-step tiny training，显式保存 checkpoint，再用 eval-smoke 加载 checkpoint，在 CIFAR-10 `test_batch` 的 16 张图上计算 MSE、PSNR 和 SSIM。当前结论是：训练、保存、加载、16 张测试图小样本评估链路能跑通，但这不是正式训练，不是正式论文 evaluation，也不是论文复现完成。

## 本阶段目标

- 运行 200-step 受控 tiny training。
- 显式保存 checkpoint。
- 用 eval-smoke 加载该 checkpoint。
- 在 CIFAR-10 `test_batch` 的 16 张图上计算 MSE / PSNR / SSIM。
- 继续保持安全边界：不保存图片、不写 run summary、不下载新数据、不修改 `external/ADJSCC`、不运行官方 train/eval、不把 checkpoint 加入 Git。

对科研新手来说，这一步是在 50-step 小测试的基础上，把训练时间再拉长一点，同时把 eval-smoke 从 4 张图扩展到 16 张图。它更像一次更稳一点的小规模抽查，不是正式论文评测。

## 代码改动记录

- `src/repro/cifar10_smoke.py` 中 `MAX_TINY_TRAIN_STEPS` 已从 `50` 改为 `200`。
- Eval-smoke 结束提示文案已修正，不再错误写死 `4 images`。
- `--max-steps` 默认值仍保持 `10`，避免默认长训练。
- `eval-image-count` 上限仍为 `16`。

这些改动说明：虽然允许显式跑到 200 step，但默认仍不会变成长训练，仍需要用户主动指定。

## Checkpoint 路径

- WSL 路径：`/mnt/d/Research/ai-data/checkpoints/ADJSCC/tiny_train_smoke_20260614-191721/ckpt`
- Windows 路径：`D:\Research\ai-data\checkpoints\ADJSCC\tiny_train_smoke_20260614-191721\ckpt`
- Checkpoint 是否进入 Git：否。

Checkpoint 仍然保存在 `D:\Research\ai-data`，没有放入 Git 仓库。Checkpoint 是运行产物，不适合混进代码和笔记的版本历史。

## Tiny Training 设置与 Loss

- Max steps: `200`
- Batch size: `2`
- SNR: `10 dB`
- 是否保存 checkpoint: 是

Loss 关键节点：

- `step_1_loss`: `3473.42236328125`
- `step_10_loss`: `3259.82421875`
- `step_50_loss`: `347.51446533203125`
- `step_100_loss`: `20.420076370239258`
- `step_150_loss`: `11.049098014831543`
- `step_200_loss`: `7.018994331359863`

loss 从约 `3473` 降到约 `7`，说明模型在当前 tiny training 数据链路上优化非常明显。

但要谨慎：`batch_size=2`，训练规模仍然很小，模型可能只是在记住很少的小批量样本。loss 下降不等于模型已经泛化，也不等于论文复现成功。

## Eval-Smoke 设置

- Data split: `test`
- Image count: `16`
- Checkpoint used: `true`
- Input shape: `(16, 32, 32, 3)`
- Output shape: `(16, 32, 32, 3)`

这次 eval-smoke 使用 16 张 CIFAR-10 test 图，比 4 张图稍微更稳，但仍然不是完整测试集 evaluation。

## Eval-Smoke 指标

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

- `mean_mse`: `4121.12109375`
- `mean_psnr_db`: `12.233728408813477`
- `mean_ssim`: `0.18134805560112`

这些指标仍然只是 16 张图的小样本结果，不能代表模型真实性能，也不能和论文表格或曲线比较。

## 与 50-Step Smoke 的谨慎对比

50-step eval-smoke 使用 4 张图，200-step eval-smoke 使用 16 张图，因此二者不能严格公平对比。

可以谨慎观察：

- 200-step loss 比 50-step 更低。
- 200-step eval 使用更多测试图，评估稍微更稳。
- 但 200-step 仍不是完整测试集，不能说明论文级性能。

这只是小样本 smoke 观察，不是论文结论。

## 给科研新手的解释

200-step tiny training 可以理解成：把之前已经跑通的训练链路再多跑一段，看看模型是不是还能继续把训练误差压低。

这次 loss 降得非常明显，说明训练过程确实在优化当前小批量数据。但因为 batch size 只有 2，模型可能只是在记住这些很少的数据，并不代表面对更多新图片也一定好。

16 张 eval-smoke 比 4 张更稳一点，但仍然只是抽查。正式论文 evaluation 通常需要完整测试集、明确 checkpoint、明确 SNR 设置，以及更严谨的统计。

本阶段最稳妥的说法是：200-step 受控 tiny training + checkpoint + 16 张 test 图 eval-smoke 已完成；不能说论文复现成功。

## 安全边界

本阶段确认：

- 是否运行训练：是，仅 200-step tiny training。
- 是否长训练：否，仍是受控 smoke 范围。
- 是否保存 checkpoint：是，保存到 `D:\Research\ai-data`。
- 是否保存图片：否。
- 是否写 run summary：否。
- 是否下载新数据：否。
- 是否修改 `external/ADJSCC`：否。
- 是否运行官方 train/eval：否。
- 是否产生正式论文指标：否。
- Checkpoint 是否加入 Git：否。

## 当前结论

200-step 受控 tiny training 扩展已完成。可以记录为：训练链路能连续跑 200 step，checkpoint 能受控保存，eval-smoke 能加载该 checkpoint，并在 CIFAR-10 test split 的 16 张图片上计算 MSE / PSNR / SSIM。

但不能记录为：

- 正式训练完成。
- 正式论文 evaluation 完成。
- 论文完整复现完成。
- 当前小样本指标可以代表模型真实性能。
- 当前指标可以和论文表格或曲线直接比较。

## 下一步建议

- 把本次 200-step 记录交给 Git 管理 Agent。
- 不要把 checkpoint 加入 Git。
- 后续如继续推进，再单独规划完整 test split evaluation、随机种子或多次传输平均、是否保存 run summary，以及是否需要更长训练。
