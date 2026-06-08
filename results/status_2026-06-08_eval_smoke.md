# 2026-06-08 CIFAR-10 Test Split Eval-Smoke 记录

日期：2026-06-08

本报告记录 ADJSCC-Reproduction 项目的 CIFAR-10 test split eval-smoke 结果。本阶段新增并验证 `--eval-smoke`：只从 CIFAR-10 `test_batch` 读取 4 张图片，经过 ADJSCC 模型做一次非训练 forward，然后计算 MSE、PSNR 和 SSIM。当前结论是：测试集评估入口能跑通，但这不是正式论文 evaluation，也不是论文复现完成。

## 本阶段目标

- 新增并验证 `--eval-smoke` 模式。
- 从 CIFAR-10 test split 的 `test_batch` 读取 4 张图片。
- 对这 4 张图片做非训练 forward。
- 计算每张图片的 MSE、PSNR、SSIM，并记录平均值。
- 继续保持安全边界：不训练、不保存图片、不保存 checkpoint、不写 run summary、不下载新数据、不修改 `external/ADJSCC`、不运行官方 train/eval。

对科研新手来说，这一步像是先把“测试集评估入口”试着打开一下，确认能读测试集图片、能过模型、能算指标。它不是正式评估模型水平。

## 新增模式

- Mode: `--eval-smoke`

`--eval-smoke` 是显式模式，也就是只有手动传入这个参数才会运行。默认模式仍然是 `check-only`，这能避免不小心直接跑评估或训练。

## 数据来源

- Data source: `cifar-10-batches-py/test_batch`
- Image count: `4`
- Input shape: `(4, 32, 32, 3)`
- Output shape: `(4, 32, 32, 3)`

`data_batch_1` 是 CIFAR-10 训练集的一部分。之前 metrics-smoke 主要用它检查 MSE、PSNR、SSIM 这些指标计算链路能不能跑通。

`test_batch` 是 CIFAR-10 测试集。正式 evaluation 应该在测试集上做，因为测试集更适合观察模型在没参与训练的数据上的表现。

这次只用了 4 张测试集图片，所以仍然只是 smoke test。它能说明入口能跑，但不能代表完整测试集结果。

## 结果数据

Per-image MSE:

- `image_1_mse`: `2541.4853515625`
- `image_2_mse`: `6932.91943359375`
- `image_3_mse`: `4320.96240234375`
- `image_4_mse`: `3927.419921875`

Per-image PSNR:

- `image_1_psnr_db`: `14.079927444458008`
- `image_2_psnr_db`: `9.72164249420166`
- `image_3_psnr_db`: `11.774999618530273`
- `image_4_psnr_db`: `12.189730644226074`

Per-image SSIM:

- `image_1_ssim`: `0.09230268746614456`
- `image_2_ssim`: `0.07816802710294724`
- `image_3_ssim`: `0.09644591808319092`
- `image_4_ssim`: `0.11792823672294617`

Mean metrics:

- `mean_mse`: `4430.69677734375`
- `mean_psnr_db`: `11.941575050354004`
- `mean_ssim`: `0.09621121734380722`

## 解释

训练集和测试集不是一回事。训练集更像“练习题”，模型训练时会看它；测试集更像“考试题”，正式评价模型时应该主要看测试集表现。

这次从 `test_batch` 读取图片，是往正式 evaluation 的方向靠了一步。但只读取了 4 张图片，数量太少，所以仍然只是 smoke test，不是正式 evaluation。

没有正式训练 checkpoint，就像还没有一份正式训练好的模型答卷。没有这份答卷，就不能把当前指标拿去和论文表格或曲线比较。

这次的意义是确认“测试集评估入口能跑通”：程序能找到 `test_batch`，能读出图片，能做非训练 forward，能算出 MSE / PSNR / SSIM。

MSE / PSNR / SSIM 都只是这 4 张图的小样本结果，不代表模型真实性能。正式结果需要完整测试集、明确 checkpoint、明确 SNR 设置，并按 evaluation protocol 统一记录。

## 指标口径

- MSE、PSNR、SSIM 的指标口径符合当前 `evaluation_protocol_cifar10_minimal.md`。
- Clip policy 与 protocol 一致。
- 本阶段只记录 smoke 结果，不把这些数值当作正式论文指标。

## 安全边界

本阶段确认：

- 是否训练：否。
- 是否保存图片：否。
- 是否保存 checkpoint：否。
- 是否写 run summary：否。
- 是否下载新数据：否。
- 是否修改 `external/ADJSCC`：否。
- 是否运行官方 train/eval：否。
- 是否产生正式论文指标：否。

这些边界说明：本阶段只验证 eval-smoke 入口和指标链路，不进入正式训练或正式论文评估。

## 代码复现 Agent 审查结论

代码复现 Agent 已确认：

- `--eval-smoke` 是显式模式，默认仍是 `check-only`。
- 读取的是 CIFAR-10 `test_batch`。
- 如果从 `.tar.gz` 读取，也是只读读取，不解压写文件。
- 默认 `image_count=4`。
- 硬上限 `MAX_EVAL_SMOKE_IMAGES=16`，避免误跑完整测试集。
- 使用 `training=False`。
- 没有 `fit()`。
- 没有 eval-smoke 内的 `GradientTape()`。
- 没有保存图片。
- 没有保存 checkpoint。
- 没有写 run summary。
- 没有调用 `tf.keras.datasets.cifar10.load_data()`。
- 没有调用官方 `adjscc_cifar10.py train/eval`。
- 没有修改 `external/ADJSCC`。
- 指标口径符合 evaluation protocol。
- Clip policy 与 protocol 一致。

## 当前结论

CIFAR-10 test split eval-smoke 通过。可以记录为：`--eval-smoke` 已能从 `test_batch` 读取 4 张图片，并完成非训练 forward 和 MSE / PSNR / SSIM 计算。

但不能记录为：

- 正式论文 evaluation 完成。
- 论文完整复现完成。
- 模型效果达到论文结果。
- 已经完成完整测试集评估。
- 这 4 张图的 MSE / PSNR / SSIM 可以代表模型真实性能。

## 下一步建议

- 让 Git 管理 Agent 只接手本次 Markdown 记录，以及已有代码/脚本改动。
- 后续可以规划更完整的 test split evaluation。
- 在继续之前，应先单独确认 checkpoint 来源、评估图片数量、SNR 设置、是否保存结果，以及是否允许写 run summary。
