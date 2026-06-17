# 2026-06-17 TensorFlow GPU 审计与最小修复结果

日期：2026-06-17

本报告整理环境数据配置 Agent 关于 TensorFlow GPU 可用性的审计与最小修复结果。本阶段只验证 WSL2 + `adjscc-tf` 环境下 TensorFlow 2.14 是否能识别并使用 GPU。

重要边界：这只是环境验证 / GPU smoke test，不是 ADJSCC 训练，不是真实数据复现，也不是论文复现完成。

## 本阶段目标

- 验证 TensorFlow 2.14 在 `adjscc-tf` 环境中是否能看到 GPU。
- 在 TensorFlow 初始无法识别 GPU 时，尝试最小修复。
- 验证修复后 TensorFlow 是否能完成一个小型 GPU 计算。
- 明确记录仍未进入 ADJSCC 正式训练或论文 evaluation。

本阶段没有运行 ADJSCC 训练，没有运行 `external/ADJSCC/adjscc_cifar10.py`，没有下载数据，没有修改 `external/ADJSCC`，也没有提交 Git。

## 执行环境

- WSL 发行版：`Ubuntu-ADJSCC`
- 系统：Ubuntu 22.04.5 LTS
- Conda 环境：`adjscc-tf`
- Python 环境路径：`/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf`
- GPU：NVIDIA GeForce RTX 4060 Laptop GPU
- Windows 驱动版本：`560.94`
- 驱动报告 CUDA Version：`12.6`
- TensorFlow 版本：`2.14.0`
- TensorFlow CUDA build:
  - `cuda_version`: `11.8`
  - `cudnn_version`: `8`

## 初始问题

WSL2 中 `nvidia-smi` 可以看到 NVIDIA GeForce RTX 4060 Laptop GPU，说明 Windows 驱动和 WSL GPU 映射大体正常。

但是 TensorFlow 初始检查：

```python
tf.config.list_physical_devices("GPU")
```

返回空列表。这说明系统层面能看到 GPU，但 TensorFlow 当时还没有成功识别 GPU。

## 原因判断

初步判断原因是：`adjscc-tf` conda 环境中缺少 TensorFlow 2.14 所需的 CUDA 11.8 / cuDNN 8 用户态动态库。

对新手来说，可以这样理解：

- `nvidia-smi` 能看到 GPU，说明“电脑和驱动知道显卡在这里”。
- TensorFlow 要用 GPU，还需要自己运行时能找到合适版本的 CUDA/cuDNN 库。
- 当这些库缺失或路径没有配置好时，TensorFlow 就可能返回空 GPU 列表。

## 最小修复动作

用户在 `adjscc-tf` 环境中执行：

```bash
mamba install -c conda-forge cudatoolkit=11.8 cudnn=8
```

安装后，在当前终端临时设置：

```bash
export LD_LIBRARY_PATH="$CONDA_PREFIX/lib:$LD_LIBRARY_PATH"
```

这个环境变量的作用是告诉 TensorFlow：优先从当前 conda 环境的 `lib` 目录里找 CUDA/cuDNN 相关动态库。

## 验证结果

修复后再次检查：

```python
tf.config.list_physical_devices("GPU")
```

返回：

```python
[PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]
```

进一步运行 `1024 x 1024` 矩阵乘法后，TensorFlow 成功创建 GPU 设备：

```text
NVIDIA GeForce RTX 4060 Laptop GPU
```

输出形状：

```text
(1024, 1024)
```

这说明 TensorFlow 不只是“看到了 GPU”，而且已经能把实际计算放到 GPU 设备上执行。

## 当前结论

WSL2 + `adjscc-tf` 环境下，TensorFlow 2.14 的 GPU 可用性验证成功。

但需要明确区分：

- 可以说：TensorFlow GPU 环境验证成功。
- 可以说：TensorFlow 能识别 RTX 4060 Laptop GPU，并完成矩阵计算。
- 不能说：ADJSCC 已经完成 GPU 训练。
- 不能说：真实数据复现已经完成。
- 不能说：论文结果已经复现成功。

## 非阻塞警告说明

验证过程中仍存在一些日志提示：

- `Unable to register cuDNN/cuFFT/cuBLAS factory`
- `TF-TRT Warning: Could not find TensorRT`
- `could not open file to read NUMA node`

当前判断：这些不是本阶段阻塞项。

理由是 TensorFlow 已经成功识别 GPU，并完成了矩阵计算验证。后续如果进入更正式训练或性能调优阶段，可以再单独评估这些 warning 是否影响稳定性或性能。

## 重要限制

当前 GPU 生效依赖当前终端中的临时环境变量：

```bash
export LD_LIBRARY_PATH="$CONDA_PREFIX/lib:$LD_LIBRARY_PATH"
```

新开终端后可能需要重新设置。

后续可以规划把这个设置写入 conda activate 脚本，让进入 `adjscc-tf` 环境时自动配置。但本次记录不直接修改脚本，先保持“最小修复、可验证、可回退”的状态。

## 未做事项

本阶段没有做以下事情：

- 没有运行 ADJSCC 训练。
- 没有运行 `external/ADJSCC/adjscc_cifar10.py`。
- 没有下载 CIFAR-10 或其他数据。
- 没有修改 `external/ADJSCC`。
- 没有修改项目源码。
- 没有保存 checkpoint。
- 没有产生 PSNR、SSIM、MS-SSIM 等论文指标。
- 没有提交 Git。

## 后续建议

- 后续新开终端后，如果 TensorFlow 又看不到 GPU，先检查是否设置了 `LD_LIBRARY_PATH`。
- 可以单独规划一个小任务，把 `LD_LIBRARY_PATH` 写入 conda activate 脚本，但不要和训练任务混在一起做。
- 进入 ADJSCC 实验时，仍应从小规模 smoke 开始，例如 GPU 环境下的安全 wrapper 检查、小 batch forward 或 tiny training。
- 不要因为 GPU 验证成功就直接启动长训练；GPU 可用只代表环境准备更进一步，模型复现仍需要单独规划和验证。
