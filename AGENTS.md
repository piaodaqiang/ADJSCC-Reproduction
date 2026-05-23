# Project Instructions

禁止批量删除文件或目录。

不要使用：

- `del /s`
- `rd /s`
- `rmdir /s`
- `Remove-Item -Recurse`
- `rm -rf`

需要删除文件时，只能一次删除一个明确路径的文件。

正确示例：

```powershell
Remove-Item "C:\path\to\file.txt"
```

如果需要批量删除文件，应停止操作，并向用户请求，让用户手动删除。

## Reproduction Rules

- Do not download ImageNet or other large datasets without explicit confirmation.
- Do not download model weights without explicit confirmation.
- Do not run long training jobs without explicit confirmation.
- Keep project code in this repository.
- Keep large datasets, checkpoints, caches, and training outputs under `D:\Research\ai-data`.
