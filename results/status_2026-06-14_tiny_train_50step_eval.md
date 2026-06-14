# 2026-06-14 50-Step Tiny Training + Eval-Smoke 记录

日期：2026-06-14

本报告记录 ADJSCC-Reproduction 项目的 50-step 受控 tiny training 扩展结果。本阶段运行 50-step tiny training，显式保存 checkpoint，再用 eval-smoke 加载 checkpoint，在 CIFAR-10 `test_batch` 的 4 张图上计算 MSE、PSNR 和 SSIM。当前结论是：50-step 训练、保存、加载、小样本测试集评估这条链路能跑通，但这不是正式训练，不是正式论文 evaluation，也不是论文复现完成。

## 本阶段目标

- 运行 50-step tiny training。
- 显式保存 checkpoint。
- 用 eval-smoke 加载该 checkpoint。
- 在 CIFAR-10 `test_batch` 的 4 张图上计算 MSE / PSNR / SSIM。
- 继续保持安全边界：不保存图片、不写 run summary、不下载新数据、不修改 `external/ADJSCC`、不运行官方 train/eval、不把 checkpoint 加入 Git。

这一步是在 10-step 最小闭环基础上，把训练步数稍微拉长，看看训练误差会不会继续下降，以及保存后的 checkpoint 能不能继续被 eval-smoke 使用。

## Checkpoint 路径

- WSL 路径：`/mnt/d/Research/ai-data/checkpoints/ADJSCC/tiny_train_smoke_20260614-170644/ckpt`
- Windows 路径：`D:\Research\ai-data\checkpoints\ADJSCC\tiny_train_smoke_20260614-170644\ckpt`
- Checkpoint 是否进入 Git：否。

Checkpoint 仍然放在 `D:\Research\ai-data`，不放进 Git 仓库。Checkpoint 是运行产物，通常会越来越多、越来越大，不适合混进代码和笔记的版本历史。

## Tiny Training 设置与 Loss

- Max steps: `50`
- Batch size: `2`
- SNR: `10 dB`
- 是否保存 checkpoint: 是

Loss 关键变化：

- `step_1_loss`: `3472.87646484375`
- `step_10_loss`: `3279.12841796875`
- `step_20_loss`: `2268.64892578125`
- `step_30_loss`: `1317.4755859375`
- `step_40_loss`: `652.4791259765625`
- `step_50_loss`: `306.04559326171875`

loss 明显下降，说明模型在这次 tiny training 的小批量训练链路上确实发生了优化。换句话说，程序不只是“跑了一下”，而是在训练误差上往下降。

但要小心：loss 下降不等于模型已经泛化，也不等于论文复现成功。它只能说明这次 tiny training 的训练链路能连续工作，并且训练误差能被压下来。

## Eval-Smoke 设置

- Data split: `test`
- Image count: `4`
- Checkpoint used: `true`
- Input shape: `(4, 32, 32, 3)`
- Output shape: `(4, 32, 32, 3)`

Eval-smoke 加载 50-step checkpoint 后，只评估了 CIFAR-10 `test_batch` 的 4 张图片。这仍然是小样本 smoke，不是完整测试集 evaluation。

## Eval-Smoke 指标

Per-image MSE:

- `image_1_mse`: `3531.161865234375`
- `image_2_mse`: `6643.31640625`
- `image_3_mse`: `3506.180419921875`
- `image_4_mse`: `4169.91796875`

Per-image PSNR:

- `image_1_psnr_db`: `12.651627540588379`
- `image_2_psnr_db`: `9.906953811645508`
- `image_3_psnr_db`: `12.682459831237793`
- `image_4_psnr_db`: `11.929529190063477`

Per-image SSIM:

- `image_1_ssim`: `0.14745713770389557`
- `image_2_ssim`: `0.08354467153549194`
- `image_3_ssim`: `0.25806406140327454`
- `image_4_ssim`: `0.14494939148426056`

Mean metrics:

- `mean_mse`: `4462.64453125`
- `mean_psnr_db`: `11.792642593383789`
- `mean_ssim`: `0.15850381553173065`

这些指标只是 4 张图的小样本结果，不能代表模型真实性能，也不能和论文表格或曲线比较。

## 与 10-Step Smoke 的谨慎对比

10-step eval-smoke mean:

- `mean_mse`: `4392.0146484375`
- `mean_psnr_db`: `11.982768058776855`
- `mean_ssim`: `0.09460055828094482`

50-step eval-smoke mean:

- `mean_mse`: `4462.64453125`
- `mean_psnr_db`: `11.792642593383789`
- `mean_ssim`: `0.15850381553173065`

可以观察到：50-step 的 `mean_ssim` 高于 10-step。SSIM 更偏结构相似度，所以这个变化说明 4 张图上的结构相似度平均值更高。

但 50-step 的 `mean_mse` 和 `mean_psnr_db` 并没有明显优于 10-step。因为只评估 4 张图，这个对比很容易受样本影响，不能说明 50-step 模型整体更好。

这只是小样本 smoke 观察，不是论文结论。

## 解释

50-step tiny training 可以理解成：在最小闭环已经跑通之后，把训练稍微延长一点，看看训练过程是不是还能稳定下降。

本次训练 loss 下降很明显，说明训练代码确实在优化当前小批量数据。但模型是否真的学到通用规律，要靠更完整的测试集评估来判断。

eval-smoke 只看 4 张测试图，就像只抽查了 4 道题。抽查能帮助确认流程没坏，但不能代表整张试卷成绩。

所以本阶段最稳妥的说法是：50-step 受控 tiny training + checkpoint + 小样本 eval-smoke 已完成；不能说论文复现成功。

## 安全边界

本阶段确认：

- 是否运行训练：是，仅 50-step tiny training。
- 是否长训练：否。
- 是否保存 checkpoint：是，保存到 `D:\Research\ai-data`。
- 是否保存图片：否。
- 是否写 run summary：否。
- 是否下载新数据：否。
- 是否修改 `external/ADJSCC`：否。
- 是否运行官方 train/eval：否。
- 是否产生正式论文指标：否。
- Checkpoint 是否加入 Git：否。

## 当前结论

50-step 受控 tiny training 扩展已完成。可以记录为：训练链路能连续跑 50 step，checkpoint 能受控保存，eval-smoke 能加载该 checkpoint，并在 CIFAR-10 test split 的 4 张图片上计算 MSE / PSNR / SSIM。

但不能记录为：

- 正式训练完成。
- 正式论文 evaluation 完成。
- 论文完整复现完成。
- 当前小样本指标可以代表模型真实性能。
- 当前指标可以和论文表格或曲线直接比较。

## 下一步建议

- 后续如继续推进，再单独规划完整 test split evaluation、随机种子或多次传输平均、是否保存 run summary，以及是否需要更长训练。
