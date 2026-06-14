# 2026-06-14 100-Image Expanded Eval-Smoke 记录

日期：2026-06-14

本报告记录 ADJSCC-Reproduction 项目的 100-image expanded eval-smoke。这个阶段没有重新训练，只是使用已有 200-step checkpoint，把 eval-smoke 的 CIFAR-10 `test_batch` 图片数量从 16 扩大到 100，并计算 MSE、PSNR 和 SSIM 的 mean 指标。当前结论是：expanded eval-smoke 成功，但这不是正式论文 evaluation，也不是论文复现完成。

## 本阶段目标

- 让 eval-smoke 支持最多 100 张 CIFAR-10 `test_batch` 图片。
- 使用已有 200-step checkpoint 运行一次 100 张 evaluation smoke。
- 记录 100 张小样本上的 mean MSE、mean PSNR 和 mean SSIM。
- 继续保持安全边界：不重新训练、不保存新 checkpoint、不保存图片、不写 run summary、不下载新数据、不修改 `external/ADJSCC`、不运行官方 train/eval。

对科研新手来说，这一步像是把“小测验”的题目从 16 道增加到 100 道。它比 16 张图更稳一点，但还不是完整考试。

## 代码改动记录

- `src/repro/cifar10_smoke.py` 中 `MAX_EVAL_SMOKE_IMAGES` 从 `16` 改为 `100`。
- `DEFAULT_EVAL_SMOKE_IMAGES` 仍保持 `4`。
- 未修改 `MAX_TINY_TRAIN_STEPS`。
- 未修改训练逻辑。
- 未修改 checkpoint 逻辑。
- 未修改指标计算逻辑。

这说明：允许手动把 eval-smoke 扩展到 100 张，但默认仍然只跑 4 张，避免默认行为突然变重。

## Checkpoint 使用情况

- WSL 路径：`/mnt/d/Research/ai-data/checkpoints/ADJSCC/tiny_train_smoke_20260614-191721/ckpt`
- Windows 路径：`D:\Research\ai-data\checkpoints\ADJSCC\tiny_train_smoke_20260614-191721\ckpt`
- 使用已有 200-step checkpoint：是。
- 本阶段是否重新训练：否。
- 本阶段是否保存新 checkpoint：否。
- Checkpoint 是否加入 Git：否。

本阶段只是复用已有 checkpoint 做更大一点的小样本 eval-smoke，不是重新训练一个新模型。

## Eval-Smoke 设置

- Data split: `test`
- Image count: `100`
- Checkpoint used: `true`
- Input shape: `(100, 32, 32, 3)`
- Output shape: `(100, 32, 32, 3)`

`input_shape` 和 `output_shape` 都是 `(100, 32, 32, 3)`，说明这次一次性读入 100 张 32x32 RGB 图片，模型输出也保持同样的图片形状。

## Mean 指标

- `mean_mse`: `4599.38916015625`
- `mean_psnr_db`: `11.864448547363281`
- `mean_ssim`: `0.15781359374523163`

这些数值只代表这 100 张 test_batch 小样本上的平均结果。它们不能当作论文正式指标。

## 给科研新手的解释

100 张比 16 张更能观察指标稳定性，因为样本多一些，单张图片特别难或特别简单造成的影响会小一点。

但 CIFAR-10 test split 一共有 10000 张图片，100 张只占很小一部分。所以这仍然只是 smoke test，不是完整测试集 evaluation。

本阶段没有重新训练，只是复用已有 200-step checkpoint。它的意义是确认：这个 checkpoint 可以加载，并且 eval-smoke 可以在更多测试图上完成指标计算。

当前指标不能写成论文正式指标，也不能直接和论文表格比较。稳妥说法是：100-image expanded eval-smoke 成功；不能说正式 evaluation 完成。

## 安全边界

本阶段确认：

- 是否运行训练：否。
- 是否保存 checkpoint：否，本阶段没有新 checkpoint。
- 是否使用已有 checkpoint：是。
- 是否保存图片：否。
- 是否写 run summary：否。
- 是否下载新数据：否。
- 是否修改 `external/ADJSCC`：否。
- 是否运行官方 train/eval：否。
- 是否产生正式论文指标：否。
- Checkpoint 是否加入 Git：否。

## 当前结论

100-image expanded eval-smoke 已完成。可以记录为：已有 200-step checkpoint 能被 eval-smoke 加载，并在 100 张 CIFAR-10 `test_batch` 图片上完成 mean MSE / PSNR / SSIM 计算。

但不能记录为：

- 正式论文 evaluation 完成。
- 论文完整复现完成。
- 当前指标可以代表完整 CIFAR-10 test split。
- 当前指标可以和论文表格或曲线直接比较。

## 下一步建议

- 把本次 100-image expanded eval-smoke 记录交给 Git 管理 Agent。
- 不要把 checkpoint、数据、图片或 run summary JSON 加入 Git。
- 后续如继续推进，再单独规划完整 10000 张 test split evaluation、随机种子或多次传输平均、是否保存 run summary，以及是否需要更正式的 checkpoint。
