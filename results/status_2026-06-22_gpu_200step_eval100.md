# 2026-06-22 GPU 200-Step Tiny Training + 100-Image Eval-Smoke 记录

日期：2026-06-22

本报告记录 ADJSCC-Reproduction 项目的 GPU 200-step tiny training + checkpoint + 100-image eval-smoke 结果。本阶段运行 GPU 200-step tiny training，保存 checkpoint，然后用该 checkpoint 在 100 张 CIFAR-10 `test_batch` 图片上运行 eval-smoke。

重要边界：这是 GPU 受控 smoke 结果，不是正式训练，不是完整测试集 evaluation，也不是论文复现结果。

## 本阶段目标

- 运行 GPU 200-step tiny training。
- 显式保存 checkpoint 到 Git 仓库外。
- 使用该 checkpoint 对 100 张 CIFAR-10 `test_batch` 图片运行 eval-smoke。
- 对比 GPU 50-step 与 GPU 200-step 的 100-image smoke 指标。
- 谨慎解释观察到的轻微改善。

## 环境状态

- TensorFlow 能识别 GPU。
- `ptxas` 可用。
- Git 运行前后均干净。
- 未修改 `external/ADJSCC`。
- 未下载新数据。

这些说明 GPU 训练环境已经从 fake-forward、real-batch-forward、50-step tiny training 继续推进到 200-step tiny training。但这仍然只是受控 smoke 阶段。

## Checkpoint 路径

- WSL 路径：`/mnt/d/Research/ai-data/checkpoints/ADJSCC/tiny_train_smoke_20260622-214536/ckpt`
- Windows 路径：`D:\Research\ai-data\checkpoints\ADJSCC\tiny_train_smoke_20260622-214536\ckpt`
- Checkpoint saved: `true`
- Checkpoint 是否进入 Git：否

Checkpoint 是模型训练后的参数存档。本阶段 checkpoint 仍放在 `D:\Research\ai-data`，不放进 Git 仓库，避免把运行产物混进版本历史。

## GPU 200-Step Training 设置

- Batch size: `2`
- SNR: `10 dB`
- Max steps: `200`
- Checkpoint saved: `true`

## GPU 200-Step Loss

Loss 关键节点：

- Step 1: `3474.34716796875`
- Step 10: `3312.654296875`
- Step 50: `304.3578796386719`
- Step 100: `13.667617797851562`
- Step 200: `5.290384769439697`

Loss 明显下降，说明 GPU tiny training 链路继续有效。更直白地说，模型在这个小训练过程中确实在更新参数，并把训练误差压低。

但要注意：`batch_size=2` 很小，200 step 仍然属于 tiny training，不是正式训练。Loss 下降不能直接说明模型已经泛化，也不能说明论文复现成功。

## 100-Image Eval-Smoke 设置

- Data split: `test`
- Image count: `100`
- Checkpoint used: `true`
- Input shape: `(100, 32, 32, 3)`
- Output shape: `(100, 32, 32, 3)`

## 100-Image Eval-Smoke Mean 指标

- `mean_mse`: `4613.39599609375`
- `mean_psnr_db`: `11.875377655029297`
- `mean_ssim`: `0.15711666643619537`

这些指标只代表 100 张 CIFAR-10 `test_batch` 图片的小样本 eval-smoke。CIFAR-10 test split 一共有 10000 张图片，所以这不是完整测试集 evaluation。

## GPU 50-Step 与 GPU 200-Step 对比

GPU 50-step：

- `mean_mse`: `4709.0073`
- `mean_psnr_db`: `11.7539`
- `mean_ssim`: `0.1460`

GPU 200-step：

- `mean_mse`: `4613.3960`
- `mean_psnr_db`: `11.8754`
- `mean_ssim`: `0.1571`

谨慎解释：

- GPU 200-step 的 `mean_mse` 比 GPU 50-step 略低。
- GPU 200-step 的 `mean_psnr_db` 比 GPU 50-step 略高。
- GPU 200-step 的 `mean_ssim` 比 GPU 50-step 略高。
- 因此可以说：在当前 GPU smoke 设置下，200-step 相比 50-step 在 100-image 小样本评估中指标略好。

不能说：

- 不能说论文复现成功。
- 不能说模型已经正式训练完成。
- 不能说已经完成完整 CIFAR-10 test split evaluation。
- 不能把这些指标写成论文正式结果。

## 给科研新手的解释

这一步像是把 GPU 上的小训练从 50 step 延长到 200 step，看看训练链路是否还能继续稳定工作。

Loss 从约 `3474` 降到约 `5.29`，说明模型在 tiny training 的训练样本上误差明显变小。100 张测试图上的 MSE / PSNR / SSIM 相比 50-step 略有改善，说明这个小样本 smoke 里观察到了一点更好的趋势。

但是这里的训练规模和评估规模都还很小：`batch_size=2`，测试图片只有 `100` 张，而完整 CIFAR-10 test split 有 `10000` 张。所以这一步最准确的结论是：GPU 200-step 受控 smoke 通过，并且相对 GPU 50-step 有轻微改善；不是论文复现结果。

## 安全边界

本阶段确认：

- 是否运行训练：是，仅 GPU 200-step tiny training。
- 是否长训练：否。
- 是否保存 checkpoint：是，保存到 `D:\Research\ai-data`。
- Checkpoint 是否进入 Git：否。
- 是否保存图片：否。
- 是否写 run summary：否。
- 是否下载新数据：否。
- 是否修改 `external/ADJSCC`：否。
- 是否运行官方 train/eval：否。
- 是否产生正式论文指标：否。

## 当前结论

GPU 200-step tiny training + checkpoint + 100-image eval-smoke 已完成。可以记录为：GPU tiny training 链路继续有效，并且在当前 100-image smoke eval 中，相比 GPU 50-step 观察到轻微指标改善。

不能记录为：正式训练完成、正式论文 evaluation 完成、论文复现成功，或当前指标可作为论文正式结果。

## 下一步建议

- 把本次 GPU 200-step 记录交给 Git 管理 Agent。
- 后续可以规划 GPU 500-step 对照实验，或先整理 GPU smoke 阶段对比表。
- 如果继续扩大训练或 evaluation，应提前明确训练步数、checkpoint 策略、评估样本数量、随机性控制和是否保存 run summary。