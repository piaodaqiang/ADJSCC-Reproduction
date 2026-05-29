# 2026-05-29 Run Summary 写入测试记录

日期：2026-05-29

本报告记录 ADJSCC-Reproduction 项目的 1-step tiny training + run summary 写入测试。当前结论是：程序已经能在一次极小训练后，把本次运行的小型 JSON 摘要安全写入外部实验输出目录。它仍然只是 smoke test，不是正式训练，不是论文完整复现，也没有产生 PSNR、SSIM、MS-SSIM 等论文指标。

## 本阶段目标

- 运行一次 `1 step` tiny training。
- 启用 `--write-run-summary`。
- 验证程序能把本次运行的摘要 JSON 写到外部实验输出目录。
- 继续确认安全边界：不保存 checkpoint，不下载新数据，不修改 `external/ADJSCC`，不把 JSON 运行产物加入 Git。

对科研新手来说，可以把这一步理解成：不是正式训练模型，而是检查“训练能不能启动一下、loss 能不能算出来、实验小摘要能不能写出去”。这更像是检查实验流水线有没有接通。

## 运行目录

- WSL 运行目录：`/mnt/d/Research/ai-data/runs/ADJSCC`
- Windows 对应目录：`D:\Research\ai-data\runs\ADJSCC`

run summary 放在 `D:\Research\ai-data`，而不是放进 Git 仓库，是因为它属于实验运行产物。以后每次实验都可能生成类似文件，数量可能越来越多。Git 仓库更适合保存代码、笔记和小型总结，避免把大量运行产物混进版本历史。

## 实际 JSON 文件路径

- WSL 路径：`/mnt/d/Research/ai-data/runs/ADJSCC/tiny_train_summary_20260529-210910.json`
- Windows 路径：`D:\Research\ai-data\runs\ADJSCC\tiny_train_summary_20260529-210910.json`

这个 JSON 文件本身不加入 Git。仓库只记录它的路径、大小和关键内容，方便以后回看这次实验发生了什么。

## 文件大小

- `239 bytes`

这个大小很小，说明它只是一个简短摘要，不是模型权重、数据集或大型训练输出。

## 训练设置

- Mode: `tiny-train`
- Max steps: `1`
- Batch size: `2`
- SNR: `10.0 dB`
- CIFAR-10 batch source: `cifar-10-batches-py/data_batch_1`

这次只训练 `1 step`，所以它仍然只是 tiny training smoke。`1 step` 的作用是确认训练链路能跑通，不足以说明模型已经学好了，也不能代表正式训练效果。

## Loss

```text
tiny_train_step_1_loss: 3472.2255859375
```

JSON 中记录的 loss 列表为：

```json
[3472.2255859375]
```

loss 可以理解成训练过程中模型输出和目标之间的误差数字。本阶段的 loss 只能说明程序成功算出了误差，不能当作论文复现指标。论文复现通常要看 PSNR、SSIM、MS-SSIM 等评价指标，但这次没有产生这些指标。

## JSON 主要字段

```json
{
  "mode": "tiny-train",
  "batch_size": 2,
  "max_steps": 1,
  "snr_db": 10.0,
  "losses": [
    3472.2255859375
  ],
  "cifar10_batch_source": "cifar-10-batches-py/data_batch_1",
  "checkpoint_saved": false,
  "data_downloaded": false
}
```

run summary 可以理解成“一次实验的小摘要单”。它记录这次怎么跑、用了什么参数、loss 是多少、有没有保存 checkpoint、有没有下载数据等。这样以后回看实验记录时，不需要只靠记忆猜当时发生了什么。

## 安全边界

本阶段确认：

- 运行了训练，但只有 `1 step` tiny training。
- 没有运行长训练。
- 没有保存 checkpoint。
- 没有下载新数据。
- 没有修改 `external/ADJSCC`。
- 没有把 run summary JSON 加入 Git。
- 没有产生 PSNR。
- 没有产生 SSIM。
- 没有产生 MS-SSIM。
- 提供的记录中 `git status --short` 是干净的。

这些边界很重要，因为当前阶段目标只是验证流程，不是开始消耗大量时间、磁盘空间或产生正式模型。

## 命令拼写注意事项

用户实际命令里写成了：

```bash
PYTHONDONTWRITECODE=1
--max-step 1
```

其中 `PYTHONDONTWRITECODE` 拼写不完整，正确写法应为：

```bash
PYTHONDONTWRITEBYTECODE=1
```

这个拼写错误不影响本次实验的核心结果。原因是它只影响是否禁止 Python 生成 `.pyc` 缓存文件，不影响 Python 运行训练代码、计算 loss 或写入 JSON 摘要。

另外，`--max-step 1` 被 `argparse` 解析成了 `--max-steps`，所以本次仍然按 `1 step` 执行。为了避免以后误解，后续统一使用正确写法：

```bash
PYTHONDONTWRITEBYTECODE=1
--max-steps 1
```

## 当前结论

本阶段可以记录为：1-step tiny training + run summary 写入测试通过。训练链路至少能跑 1 step，loss 能被记录，JSON 摘要也能写入外部运行目录。

但不能记录为：

- 正式训练完成。
- 论文完整复现完成。
- 模型效果达到论文结果。
- 已经产生 PSNR、SSIM、MS-SSIM。

## 下一步建议

- 让 Git 管理 Agent 只接手本次 Markdown 记录文件，不要加入外部 JSON 运行产物。
- 如果继续推进实验，建议先规划 5-step tiny training 或更完整的 run summary 字段检查。
- 在用户明确授权前，不要运行长训练，不要保存 checkpoint，不要下载新数据。
