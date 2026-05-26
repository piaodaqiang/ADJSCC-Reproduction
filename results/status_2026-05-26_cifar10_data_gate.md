# CIFAR-10 数据门禁阶段记录

日期：2026-05-26

本报告记录 ADJSCC-Reproduction 项目的 CIFAR-10 数据门禁阶段。当前结论仅表示数据门禁检查已经执行，并确认本地 CIFAR-10 数据尚不存在；这不是论文复现结果，不是训练结果，也不是真实 CIFAR-10 smoke 成功结果。

## 本阶段目标

- 在不下载数据、不训练、不保存 checkpoint 的前提下，检查本地 CIFAR-10 数据是否已经具备运行真实 batch forward 的条件。
- 为后续 `--real-batch-forward` 建立前置门禁，避免 wrapper 隐式触发 Keras 自动下载或长训练流程。
- 将数据状态、安全边界和当前阻塞点记录到项目日志与结果报告中。

## 修改文件

实验执行 Agent 已提交并推送：

```text
4e50056 feat: add CIFAR-10 data gate smoke modes
```

该提交涉及：

- `src/repro/cifar10_smoke.py`
- `scripts/run_cifar10_smoke.ps1`

本结果记录不修改上述代码文件，也不修改 `external/ADJSCC`。

## 新增 Wrapper 模式

- `--cifar10-check`：只检查本地 CIFAR-10 文件是否存在和可识别，不导入训练流程，不下载数据。
- `--real-batch-forward`：计划用于在本地 CIFAR-10 数据存在后运行极小真实 batch forward；当前尚未运行。

## 已运行命令

```bash
/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/bin/python -m src.repro.cifar10_smoke --cifar10-check
```

## 数据检查结果

检查路径：

```text
/mnt/d/Research/ai-data/datasets/CIFAR10
```

结果：

- CIFAR-10 数据目录存在。
- 未识别到可用于真实 batch forward 的 CIFAR-10 数据文件。

未识别到的预期文件或目录：

- `cifar-10-python.tar.gz`
- `cifar-10-batches-py`
- `data_batch_1`
- `data_batch_2`
- `data_batch_3`
- `data_batch_4`
- `data_batch_5`
- `test_batch`
- `batches.meta`

因此，当前不能把本阶段写成真实 CIFAR-10 smoke 成功，也不能运行或记录 `--real-batch-forward` 成功。

## 安全边界确认

本阶段确认：

- 未发现 `tf.keras.datasets.cifar10.load_data()`。
- 未发现 `model.fit()`。
- 未发现 `save_weights()`。
- 未下载 CIFAR-10。
- 未下载 ImageNet。
- 未下载模型权重。
- 未运行训练。
- 未保存 checkpoint。
- 未修改 `external/ADJSCC`。

## 当前阻塞点

本地尚未存在可识别的 CIFAR-10 数据文件，因此 `--real-batch-forward` 尚未运行，当前也不应继续运行。

必须先由用户确认以下二选一：

- 允许下载 CIFAR-10 到 `/mnt/d/Research/ai-data/datasets/CIFAR10` 或项目约定的数据目录。
- 提供已有本地 CIFAR-10 副本，并记录其准确路径。

## 下一步建议

- 由用户确认是否允许下载 CIFAR-10，或提供本地 CIFAR-10 数据路径。
- 确认数据可用后，再由实验执行 Agent 运行 `--real-batch-forward`。
- 下一阶段仍应保持边界：不训练、不保存 checkpoint、不修改 `external/ADJSCC`，只记录真实 batch forward 的命令、输出摘要和失败或成功证据。
