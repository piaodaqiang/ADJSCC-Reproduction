# 2026-06-16 500-Step Tiny Training + 100-Image Eval-Smoke 记录

日期：2026-06-16

本报告记录 ADJSCC-Reproduction 项目的 500-step 受控 tiny training + checkpoint + 100-image eval-smoke 结果。本阶段跨 2026-06-15/16 完成：先运行 500-step tiny training 并保存 checkpoint，再用这个 checkpoint 在 CIFAR-10 `test_batch` 的 100 张图片上计算 MSE、PSNR 和 SSIM。

当前结论是：训练、保存、加载和 100 张小样本评估链路继续跑通；但这不是正式训练，不是正式论文 evaluation，也不是论文复现完成。

## 本阶段目标

- 将 tiny training 上限提高到 `500`。
- 运行 500-step 受控 tiny training。
- 显式保存 checkpoint 到 Git 仓库外。
- 使用该 checkpoint 对 100 张 CIFAR-10 `test_batch` 图片运行 eval-smoke。
- 记录 100-image mean MSE、mean PSNR 和 mean SSIM。

## 代码改动记录

- `src/repro/cifar10_smoke.py` 中 `MAX_TINY_TRAIN_STEPS` 从 `200` 改为 `500`。
- 默认 `--max-steps` 仍为 `10`。
- `MAX_EVAL_SMOKE_IMAGES` 仍为 `100`。
- 未修改 checkpoint 逻辑。
- 未修改指标计算逻辑。
- 未修改数据读取逻辑。

这表示：手动指定时允许跑到 500 step，但默认命令仍然很保守，不会一不小心变成长训练。

## Checkpoint 路径

- WSL 路径：`/mnt/d/Research/ai-data/checkpoints/ADJSCC/tiny_train_smoke_20260615-235340/ckpt`
- Windows 路径：`D:\Research\ai-data\checkpoints\ADJSCC\tiny_train_smoke_20260615-235340\ckpt`
- Checkpoint 是否进入 Git：否。

Checkpoint 是模型训练后的参数存档。它放在 `D:\Research\ai-data`，而不是 Git 仓库里，是为了避免把模型权重这类运行产物混进版本历史。

## Tiny Training 设置与 Loss

- `max_steps`: `500`
- `batch_size`: `2`
- `SNR`: `10 dB`
- 是否保存 checkpoint: 是
- checkpoint 是否进入 Git: 否

Loss 关键节点：

- Step 1: `3471.86181640625`
- Step 10: `3247.29345703125`
- Step 50: `325.57470703125`
- Step 100: `23.40330696105957`
- Step 200: `7.393202304840088`
- Step 300: `3.482886791229248`
- Step 400: `4.400880336761475`
- Step 500: `6.220396518707275`

Loss 从约 `3471` 降到个位数，说明模型在 tiny training 小批量上优化明显。更直白地说，训练程序确实在更新模型参数，并且让训练误差大幅变小。

但这里不能夸大：`step 300` 到 `step 500` 有波动，不是一路严格下降；而且 `batch_size=2`，训练样本极少，模型可能只是在继续拟合很小的一批样本。Loss 下降不等于模型泛化提升，也不等于论文复现成功。

## Eval-Smoke 设置

- `data_split`: `test`
- `image_count`: `100`
- `checkpoint_used`: `true`
- `input_shape`: `(100, 32, 32, 3)`
- `output_shape`: `(100, 32, 32, 3)`

`input_shape` 和 `output_shape` 都是 `(100, 32, 32, 3)`，说明这次一次读入 100 张 32x32 RGB 测试图，模型输出也保持同样的图片形状。

## 100-Image Eval-Smoke Mean 指标

- `mean_mse`: `4700.11083984375`
- `mean_psnr_db`: `11.812779426574707`
- `mean_ssim`: `0.14577139914035797`

这些指标只代表 100 张测试图片的小样本 smoke 结果。CIFAR-10 test split 一共有 10000 张图片，所以当前结果不能当作完整测试集 evaluation，更不能当作论文正式指标。

## 与 200-Step + 100-Image Eval-Smoke 对比

200-step + 100-image eval-smoke 的参考结果：

- `mean_mse`: `4599.38916015625`
- `mean_psnr_db`: `11.864448547363281`
- `mean_ssim`: `0.15781359374523163`

谨慎观察：

- 500-step 的 100-image `mean_mse` 没有低于 200-step。
- 500-step 的 100-image `mean_psnr_db` 没有高于 200-step。
- 500-step 的 100-image `mean_ssim` 也没有高于 200-step。

这不能简单说训练失败。更合理的说法是：在当前 tiny training 和 100-image eval-smoke 设置下，继续从 200 step 增加到 500 step，没有观察到测试小样本指标提升。

可能原因包括：`batch_size` 太小、训练样本太少、信道随机性、评估样本仍有限，以及当前还没有采用正式训练设置。

## 给科研新手的解释

这一步像是把前面的“小训练”延长了一些，看看模型在训练 loss 上会不会继续下降，并确认保存出来的 checkpoint 还能继续用于测试集小样本评估。

训练 loss 下降，说明模型在训练过程中确实在变得更会处理当前小批量训练数据。但科研复现更关心的是：模型在没见过的测试图片上表现如何。这里 100 张测试图比 4 张、16 张更有参考价值，但仍然远小于完整测试集的 10000 张。

所以本阶段最稳妥的说法是：500-step tiny training + checkpoint + 100-image eval-smoke 链路跑通，并且在当前设置下没有观察到比 200-step 更好的 100-image mean 指标。不能写成论文复现成功。

## 安全边界

本阶段确认：

- 是否运行训练：是，仅 500-step tiny training。
- 是否长训练：否，仍是受控 smoke/预实验范围。
- 是否保存 checkpoint：是，保存到 `D:\Research\ai-data`。
- 是否保存图片：否。
- 是否写 run summary：否。
- 是否下载新数据：否。
- 是否修改 `external/ADJSCC`：否。
- 是否运行官方 train/eval：否。
- 是否产生正式论文指标：否。
- Checkpoint 是否加入 Git：否。

## 当前结论

500-step 受控 tiny training + checkpoint + 100-image eval-smoke 已完成。训练 loss 在 tiny training 小批量上明显下降，但 100-image eval-smoke mean 指标没有优于 200-step 结果。

这说明当前链路可以继续推进，但还不能说明模型已经泛化，也不能说明论文复现成功。

## 下一步建议

- 把本次记录交给 Git 管理 Agent。
- 不要把 checkpoint、数据、图片或 run summary JSON 加入 Git。
- 后续如继续推进，建议先规划更合理的训练数据循环、固定随机种子、多次传输平均、完整 10000 张 test split evaluation，以及是否保存更完整的 run summary。
