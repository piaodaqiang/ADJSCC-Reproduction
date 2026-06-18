# 2026-06-18 WSL2 + adjscc-tf TensorFlow GPU Real-Batch-Forward 记录

日期：2026-06-18

本报告记录 ADJSCC-Reproduction 项目的 GPU real-batch-forward 自动环境验证结果。本阶段在新 shell 中激活 `adjscc-tf` 后，不再手动 export `LD_LIBRARY_PATH` / `XLA_FLAGS`，直接运行真实 CIFAR-10 小批量 forward，并成功完成。

重要边界：这不是训练，不保存 checkpoint，不产生论文指标，也不是论文复现完成。

## 本阶段目标

- 验证 conda activate 脚本自动设置 CUDA/XLA 环境变量是否生效。
- 验证 GPU 环境不只可以跑 `fake-forward`，也可以读取真实 CIFAR-10 小批量并完成 ADJSCC forward。
- 记录 real-batch-forward 的输入、SNR 和输出 shape。
- 明确说明它证明了什么、不能代表什么。

## 环境基础状态

- WSL 发行版：`Ubuntu-ADJSCC`
- Conda 环境：`adjscc-tf`
- Conda 环境路径：`/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf`
- TensorFlow GPU 环境已经稳定到 real-batch-forward 级别。
- 新 shell 激活 `adjscc-tf` 后，无需手动 export `LD_LIBRARY_PATH` / `XLA_FLAGS`。

## Conda Activate/Deactivate 脚本

- Activate 脚本：`/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/etc/conda/activate.d/adjscc_cuda_libs.sh`
- Deactivate 脚本：`/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/etc/conda/deactivate.d/adjscc_cuda_libs.sh`

自动环境变量：

- `LD_LIBRARY_PATH` 自动包含：`$CONDA_PREFIX/lib`
- `XLA_FLAGS` 自动包含：`--xla_gpu_cuda_data_dir=$CONDA_PREFIX`
- `libdevice` 标准路径存在：`$CONDA_PREFIX/nvvm/libdevice/libdevice.10.bc`

对新手来说，`LD_LIBRARY_PATH` 是告诉 TensorFlow 去哪里找 CUDA/cuDNN 动态库，`XLA_FLAGS` 是告诉 TensorFlow/XLA 去哪里找 GPU 编译和执行时需要的 `libdevice`。现在这些设置已经跟随 conda 环境自动生效，减少了每次手动配置时出错的机会。

## GPU Real-Batch-Forward 运行命令

```bash
PYTHONDONTWRITEBYTECODE=1 python -m src.repro.cifar10_smoke --real-batch-forward
```

## 关键输出

- `cifar10_batch_source`: `cifar-10-batches-py/data_batch_1`
- `real_input_shape`: `(2, 32, 32, 3)`
- `snr_shape`: `(2, 1)`
- `real_output_shape`: `(2, 32, 32, 3)`
- `real_output_dtype`: `float32`
- `Real-batch-forward completed. No training was run, no checkpoint was written, and no data was downloaded.`

## Fake-Forward 与 Real-Batch-Forward 的区别

`fake-forward` 用的是随机假图。它适合用来确认模型结构、TensorFlow 和 GPU 环境能不能跑通一次最基础的前向计算。

`real-batch-forward` 用的是真实 CIFAR-10 小批量。本阶段的数据来源是 `cifar-10-batches-py/data_batch_1`，输入 shape 是 `(2, 32, 32, 3)`，也就是 2 张真实的 32x32 RGB 图片。

所以，real-batch-forward 比 fake-forward 更进一步：它说明 GPU 环境不仅能跑模型，还能读取真实 CIFAR-10 batch，并完成 ADJSCC forward。

## 这一步证明了什么

本阶段可以证明：

- 新 shell 中 conda 自动环境变量生效。
- GPU 环境下真实 CIFAR-10 小批量可以被读取。
- ADJSCC smoke wrapper 可以在真实小批量输入上完成 forward。
- 模型输出 shape `(2, 32, 32, 3)` 与输入图片 shape 对齐。
- 本次运行没有训练、没有 checkpoint、没有下载数据。

## 这一步不能代表什么

本阶段不能代表：

- 不能代表模型已经训练。
- 不能代表 GPU tiny training 已通过。
- 不能代表 checkpoint 保存或加载已验证。
- 不能代表 PSNR、SSIM、MS-SSIM 等论文指标。
- 不能代表正式 evaluation。
- 不能代表论文复现成功。

Forward 只是“图片经过模型走一遍”。它不会像训练那样更新参数，也不会说明模型质量好坏。

## 安全边界

本阶段确认：

- 是否运行训练：否。
- 是否保存 checkpoint：否。
- 是否保存图片：否。
- 是否写 run summary：否。
- 是否下载新数据：否。
- 是否修改 `external/ADJSCC`：否。
- 是否提交 Git：否。
- 是否产生论文指标：否。

## 当前结论

GPU real-batch-forward 自动环境验证已通过。可以记录为：`adjscc-tf` 的自动 CUDA/XLA 环境变量在新 shell 中生效，真实 CIFAR-10 小批量可以在 GPU 环境下进入 ADJSCC smoke wrapper 并完成 forward。

但是，这仍然只是 smoke 阶段的 forward 验证，不是训练，不是评估，也不是论文复现结果。

## 下一步建议

- 把本次 GPU real-batch-forward 记录交给 Git 管理 Agent。
- 下一步可以单独规划 GPU tiny training 对照实验。
- GPU tiny training 仍应保持严格限制，例如小步数、明确 checkpoint 策略、外部输出目录和“不是论文结果”的记录边界。
