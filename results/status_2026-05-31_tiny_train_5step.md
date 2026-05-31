# 2026-05-31 5-Step Tiny Training Smoke 记录

日期：2026-05-31

本报告记录 ADJSCC-Reproduction 项目的 5-step tiny training + enhanced run summary 结果。当前结论是：训练链路可以连续跑 5 个很小的 step，并把 5 个 loss、shape 和安全字段写入外部 JSON。它仍然只是 tiny training smoke，不是正式训练，不是论文完整复现，也没有产生 PSNR、SSIM、MS-SSIM 等论文指标。

## 本阶段目标

- 运行一次 5-step tiny training。
- 启用 `--write-run-summary`，生成 enhanced run summary。
- 确认 loss 列表能记录 5 个 step。
- 确认 input/output shape 仍然正确。
- 继续保持安全边界：不保存 checkpoint，不下载新数据，不修改 `external/ADJSCC`，不把外部 JSON 加入 Git。

对科研新手来说，这一步像是把之前“轻轻踩一下油门”的 1-step 测试，变成连续轻踩 5 下。它能更好地检查训练循环是不是能连续工作，但还远远不是正式开车跑完整路线。

## 已运行命令

```bash
PYTHONDONTWRITEBYTECODE=1 /home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/bin/python -m src.repro.cifar10_smoke --tiny-train --max-steps 5 --batch-size 2 --write-run-summary
```

本次结果记录 Agent 没有运行这条命令，只记录用户提供的已完成实验结果。

## Enhanced Run Summary 路径

- WSL 路径：`/mnt/d/Research/ai-data/runs/ADJSCC/tiny_train_summary_20260531-212309.json`
- Windows 路径：`D:\Research\ai-data\runs\ADJSCC\tiny_train_summary_20260531-212309.json`
- JSON 文件大小：`993 bytes`

这个 JSON 文件在 `D:\Research\ai-data\runs\ADJSCC`，不加入 Git。仓库只记录它的路径、大小和关键事实。

## 训练设置

- Mode: `tiny-train`
- Max steps: `5`
- Batch size: `2`
- Input shape: `[2, 32, 32, 3]`
- Output shape: `[2, 32, 32, 3]`

`input_shape=[2, 32, 32, 3]` 表示输入是 2 张 32x32 的 RGB 图片。`output_shape=[2, 32, 32, 3]` 表示模型输出仍然是 2 张同样大小的 RGB 图片。这说明数据形状在这次 tiny training 中没有明显跑偏。

## Loss 列表

```json
[
  3472.5771484375,
  3467.310302734375,
  3459.9541015625,
  3450.0517578125,
  3437.323486328125
]
```

- Loss 数量：`5`
- 第 1 step loss：`3472.5771484375`
- 第 2 step loss：`3467.310302734375`
- 第 3 step loss：`3459.9541015625`
- 第 4 step loss：`3450.0517578125`
- 第 5 step loss：`3437.323486328125`

loss 列表可以理解成“每一步训练后测到的误差记录”。这里有 5 个数，是因为这次 tiny training 跑了 5 个 step。

这组 loss 从第一步到第五步下降了，这是一个有用的 smoke 信号：说明训练循环确实在计算 loss，并且这几步里 loss 有变小。但它不能直接当作论文复现成功。

## 给科研新手的解释

5-step tiny training 是一次很小规模的训练试跑。它比 1-step 多跑几步，能检查训练循环、loss 记录和 run summary 写入是否能连续工作。

5 step 仍然不是正式训练。正式训练通常需要大量 step 或 epoch，还需要更完整的日志、checkpoint、评估指标和结果对比。5 step 太短，只能证明流程能动起来，不能证明模型训练好了。

loss 列表记录的是每个训练 step 的误差数字。一般来说，训练希望 loss 变小；这次 loss 确实下降了，但这只能说明 smoke 阶段训练链路看起来正常。

loss 下降不能直接当作论文复现成功，因为论文复现通常要看 PSNR、SSIM、MS-SSIM 这类评价指标，还要在规定数据、规定 SNR 和足够训练条件下做对比。本阶段没有这些指标。

run summary JSON 不加入 Git，是因为它是实验运行产物。以后每次实验都可能生成一个 JSON，如果都提交到 Git，版本历史会越来越乱。Git 仓库主要保存代码、笔记和小型总结；运行产物放在 `D:\Research\ai-data` 更合适。

这次仍然不保存 checkpoint，是因为 tiny training 的目标只是确认训练链路能连续跑几步，不是产出可复用模型。保存 checkpoint 会产生额外模型文件，也会带来“这个模型能不能用”的管理问题，所以要留到更正式的训练阶段再单独确认。

## 安全字段

本次 enhanced run summary 中的安全字段为：

- `checkpoint_saved`: `false`
- `data_downloaded`: `false`
- `official_train_eval_used`: `false`

这些字段很重要：它们说明这次没有保存模型权重，没有下载新数据，也没有调用官方完整 train/eval 入口。

## 安全边界

本阶段确认：

- 是否训练：是，仅 5-step tiny training。
- 是否保存 checkpoint：否。
- 是否下载新数据：否。
- 是否修改 `external/ADJSCC`：否。
- 是否产生论文指标：否。
- 没有 PSNR。
- 没有 SSIM。
- 没有 MS-SSIM。
- 外部 JSON 不加入 Git。
- 用户提供记录中 `git status --short` 干净。

## 当前结论

5-step tiny training smoke + enhanced run summary 已完成。可以记录为：训练循环能连续跑 5 个 tiny step，loss 列表被完整写入，input/output shape 符合预期，安全字段显示没有保存 checkpoint、没有下载数据、没有调用官方 train/eval。

但不能记录为：

- 正式训练完成。
- 论文完整复现完成。
- 模型效果达到论文结果。
- loss 下降等于论文复现成功。
- 已经产生 PSNR、SSIM、MS-SSIM。

## 下一步建议

- 让 Git 管理 Agent 只接手本次 Markdown 记录。
- 不要把 `D:\Research\ai-data\runs\ADJSCC\tiny_train_summary_20260531-212309.json` 加入 Git。
- 下一步可以规划更长 tiny training 或评估指标流程，但必须先单独确认训练步数、checkpoint 策略和是否开始 PSNR/SSIM/MS-SSIM 评估。
