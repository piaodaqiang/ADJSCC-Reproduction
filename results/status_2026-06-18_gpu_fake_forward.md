# 2026-06-18 WSL2 + adjscc-tf TensorFlow GPU Fake-Forward 记录

日期：2026-06-18

本报告记录 ADJSCC-Reproduction 项目的 GPU fake-forward 验证结果。本阶段在 WSL2 + `adjscc-tf` 环境中，确认 TensorFlow 能看到 GPU，并进一步确认 ADJSCC smoke wrapper 的 `--fake-forward` 能在 GPU 环境下跑通。

重要边界：这只是 GPU 环境下的 fake-forward smoke test，不是真实 CIFAR-10 forward，不是训练，不保存 checkpoint，也不是论文复现结果。

## 本阶段目标

- 记录 GPU 环境修复后，`adjscc-tf` 中 TensorFlow GPU 列表已经非空。
- 记录 CUDA/cuDNN 和 XLA 相关环境变量已经固化到 conda activate/deactivate 脚本。
- 记录 `--fake-forward` 在 GPU 环境下通过。
- 说明 fake-forward 能代表什么、不能代表什么。

## GPU 基础状态

- WSL 发行版：`Ubuntu-ADJSCC`
- Conda 环境：`adjscc-tf`
- TensorFlow: `2.14.0`
- GPU: NVIDIA GeForce RTX 4060 Laptop GPU
- WSL 中 `nvidia-smi` 可见 GPU
- 已安装 `cudatoolkit=11.8` 和 `cudnn=8`
- TensorFlow GPU 列表非空：

```python
[PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]
```

这说明 TensorFlow 已经能识别 GPU。相比 2026-06-17 的 GPU 审计，本阶段更进一步：不只做 TensorFlow 级别检查，还验证了项目 smoke wrapper 的 fake-forward。

## Conda Activate/Deactivate 脚本

已固化到 conda activate/deactivate 脚本：

- Activate 脚本：`/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/etc/conda/activate.d/adjscc_cuda_libs.sh`
- Deactivate 脚本：`/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/etc/conda/deactivate.d/adjscc_cuda_libs.sh`

Activate 脚本负责自动设置：

- `LD_LIBRARY_PATH`
- `XLA_FLAGS`

关键路径：

- `LD_LIBRARY_PATH` 包含：`/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/lib`
- `XLA_FLAGS` 指向：`--xla_gpu_cuda_data_dir=/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf`
- `libdevice` 路径：`/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/nvvm/libdevice/libdevice.10.bc`

## 给科研新手的解释

`LD_LIBRARY_PATH` 可以理解成“动态库搜索路线图”。TensorFlow 要用 GPU，就要找到 CUDA/cuDNN 这些 GPU 运行需要的库文件。这个变量就是告诉 TensorFlow：先去当前 conda 环境的 `lib` 目录里找。

`XLA_FLAGS` 是给 TensorFlow/XLA 的提示。XLA 在做 GPU 相关编译或执行时，需要找到 `libdevice`。这里把 `XLA_FLAGS` 指向 conda 环境，是为了让 TensorFlow/XLA 能找到对应的 GPU 设备库文件。

把这些设置写进 conda activate 脚本后，新开 shell 再进入 `adjscc-tf` 环境时，会自动配置这些路径，不需要每次手动输入 `export LD_LIBRARY_PATH` 或 `export XLA_FLAGS`。

## GPU Fake-Forward 运行结果

运行命令：

```bash
PYTHONDONTWRITEBYTECODE=1 python -m src.repro.cifar10_smoke --fake-forward
```

关键输出：

- `fake_input_shape`: `(2, 32, 32, 3)`
- `snr_shape`: `(2, 1)`
- `fake_output_shape`: `(2, 32, 32, 3)`
- `fake_output_dtype`: `float32`
- `Fake-forward completed`

## Fake-Forward 含义

`--fake-forward` 只用假的输入数据做一次模型前向计算。它的意义是确认：模型结构、TensorFlow、GPU 环境和项目 smoke wrapper 能配合起来跑通一次前向链路。

这里的输入 shape 是 `(2, 32, 32, 3)`，可以理解成 2 张假的 32x32 RGB 图片；输出 shape 仍是 `(2, 32, 32, 3)`，说明模型输出仍保持图片形状；输出 dtype 是 `float32`，说明输出张量类型正常。

但 fake-forward 不能代表真实实验结果。它不加载真实 CIFAR-10，不训练模型，不保存 checkpoint，不计算 PSNR/SSIM/MS-SSIM，也不能和论文结果比较。

## 当前结论

GPU 环境下 ADJSCC smoke wrapper 的 fake-forward 已通过，且新 shell 中无需手动 export `LD_LIBRARY_PATH` / `XLA_FLAGS`。

这说明 GPU 环境修复已经从“TensorFlow 能看到 GPU”推进到“项目安全 wrapper 的 fake-forward 能跑通”。但是当前还没有验证 GPU real-batch-forward，也没有验证 GPU tiny training。

## 仍需注意的警告

仍有 NUMA、`ptxas` / `nvlink` 等警告。

当前判断：这些 warning 需要记录，但 fake-forward 已经通过，暂时不阻塞 smoke 阶段。后续如果进入真实数据 forward、tiny training 或更长训练，再继续观察它们是否影响稳定性或性能。

## 安全边界

本阶段确认：

- 是否运行 real-batch-forward：否。
- 是否运行 tiny-train：否。
- 是否运行长训练：否。
- 是否下载新数据：否。
- 是否保存 checkpoint：否。
- 是否保存图片：否。
- 是否写 run summary：否。
- 是否修改 `external/ADJSCC`：否。
- 是否产生论文指标：否。

## 未做事项

- 没有运行真实 CIFAR-10 forward。
- 没有运行 GPU tiny training。
- 没有运行长训练。
- 没有下载数据。
- 没有保存 checkpoint。
- 没有修改项目源码。
- 没有修改 `external/ADJSCC`。
- 没有提交 Git。

## 下一步建议

- 可以把本次 GPU fake-forward 记录交给 Git 管理 Agent。
- 后续建议先单独规划 GPU real-batch-forward，确认真实 CIFAR-10 batch 在 GPU 环境下能跑通。
- GPU real-batch-forward 通过后，再规划 GPU tiny training。
- 每一步继续保持 smoke 边界，不要因为 fake-forward 通过就直接启动长训练。
