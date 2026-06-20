# 2026-06-20 GPU 50-Step Tiny Training + 100-Image Eval-Smoke 记录

日期：2026-06-20

本报告记录 ADJSCC-Reproduction 项目的第一个 GPU 50-step tiny training 闭环：修复 GPU tiny training 缺少 `ptxas` 的问题后，在 GPU 上运行 50-step tiny training，保存 checkpoint，再加载该 checkpoint 对 100 张 CIFAR-10 `test_batch` 图片运行 eval-smoke。

重要边界：这是 GPU 训练链路验证，不是正式训练，不是正式论文 evaluation，也不是论文复现结果。

## 本阶段目标

- 解决 GPU tiny training 中缺少 `ptxas` 的阻塞问题。
- 运行第一个 GPU 50-step tiny training。
- 显式保存 checkpoint 到 Git 仓库外。
- 使用该 checkpoint 对 100 张 CIFAR-10 `test_batch` 图片运行 eval-smoke。
- 记录 loss 和 100-image mean MSE / PSNR / SSIM。

## ptxas / cuda-nvcc 环境修复

初次 GPU tiny training 因缺少 `ptxas` 失败。

报错核心：

```text
ptxas returned an error
Failed to launch ptxas
Aborted (core dumped)
```

修复方式：

```bash
conda install -c nvidia "cuda-nvcc=11.8.*"
```

安装后：

```text
which ptxas:
/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/bin/ptxas
```

```text
ptxas --version:
Cuda compilation tools, release 11.8, V11.8.89
```

`ptxas` 是 NVIDIA CUDA 编译工具。TensorFlow/XLA 在某些 GPU 图编译时会用到它。对新手来说，可以把它理解成 GPU 运行某些计算图前需要用到的“编译器零件”。

为什么 fake-forward / real-batch-forward 可能通过，但 tiny training 仍可能失败？因为前向 smoke 只验证数据能不能通过模型，而训练会触发更多计算图、梯度和优化相关路径。缺少 `ptxas` 时，简单 forward 可能没踩到这个问题，但 tiny training 会踩到。

## GPU 50-Step Training 设置

- TensorFlow: `2.14.0`
- GPU: RTX 4060
- Batch size: `2`
- SNR: `10 dB`
- Max steps: `50`
- Checkpoint WSL 路径：`/mnt/d/Research/ai-data/checkpoints/ADJSCC/tiny_train_smoke_20260620-210955/ckpt`
- Checkpoint Windows 路径：`D:\Research\ai-data\checkpoints\ADJSCC\tiny_train_smoke_20260620-210955\ckpt`
- Checkpoint 是否加入 Git：否

Checkpoint 是训练后的模型参数存档。本阶段 checkpoint 保存到 `D:\Research\ai-data`，不放进 Git 仓库，避免把运行产物和代码记录混在一起。

## GPU 50-Step Loss

Loss 关键节点：

- Step 1: `3471.749267578125`
- Step 10: `3247.22998046875`
- Step 50: `381.5732421875`

这个 loss 下降说明 GPU tiny training 链路确实完成了训练步骤，并且训练误差在这个 50-step 小训练里下降了。

但 50 step 很短，`batch_size=2` 也很小，所以它不能说明模型已经训练好，不能说明模型泛化能力已经变强，也不能说明论文复现成功。

## Eval-Smoke 设置

- Data split: `test`
- Image count: `100`
- Checkpoint used: `true`
- Input shape: `(100, 32, 32, 3)`
- Output shape: `(100, 32, 32, 3)`

## 100-Image Eval-Smoke Mean 指标

- `mean_mse`: `4709.00732421875`
- `mean_psnr_db`: `11.753862380981445`
- `mean_ssim`: `0.14604239165782928`

这些指标只代表 100 张 CIFAR-10 `test_batch` 图片的小样本 eval-smoke。CIFAR-10 test split 一共有 10000 张图片，所以这不是完整测试集 evaluation。

## 给科研新手的解释

这一步最重要的意义是：GPU 训练链路打通了。

前面 GPU fake-forward 说明 GPU 能跑假数据前向；GPU real-batch-forward 说明 GPU 能跑真实 CIFAR-10 小批量前向；这次 GPU 50-step tiny training 说明 GPU 能进入训练流程、保存 checkpoint，再加载 checkpoint 做 100 张测试图的 eval-smoke。

但是，这仍然只是 tiny training。50 step 太短，100 张测试图也只是完整 CIFAR-10 test split 的一小部分。当前 MSE / PSNR / SSIM 不能作为论文指标，也不能和论文表格直接比较。

也不建议和 CPU 50-step 指标做严格公平对比，因为 GPU/CPU 运行路径、随机性、初始化状态和运行条件都可能不同。当前最稳妥的说法是：GPU 训练链路验证通过。

## 安全边界

本阶段确认：

- 是否运行训练：是，仅 GPU 50-step tiny training。
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

GPU 50-step tiny training + checkpoint + 100-image eval-smoke 已完成。可以记录为：GPU 能完成训练、保存 checkpoint、加载 checkpoint，并在 100 张 CIFAR-10 test split 图片上完成 eval-smoke。

不能记录为：正式训练完成、正式论文 evaluation 完成、论文复现成功，或当前指标可作为论文结果。

## 下一步建议

- 把本次 GPU 50-step 记录交给 Git 管理 Agent。
- 后续可以规划 GPU 200-step 或 500-step 对照实验。
- 下一步仍应保持 smoke/预实验边界：小步数、外部 checkpoint 路径、明确评估样本数量，并继续说明这些结果不是论文正式指标。
