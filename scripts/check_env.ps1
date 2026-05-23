$ErrorActionPreference = "Continue"

Write-Host "== Basic tools =="
python --version
pip --version
conda --version
git --version

Write-Host ""
Write-Host "== Python package probe =="
python -c "import sys; print('python_executable:', sys.executable)"
python -c "import numpy; print('numpy:', numpy.__version__)" 2>$null
python -c "import tensorflow as tf; print('tensorflow:', tf.__version__); print('gpus:', tf.config.list_physical_devices('GPU'))" 2>$null

Write-Host ""
Write-Host "== Data directories =="
$paths = @(
  "D:\Research\ai-data",
  "D:\Research\ai-data\datasets",
  "D:\Research\ai-data\datasets\CIFAR10",
  "D:\Research\ai-data\runs\ADJSCC",
  "D:\Research\ai-data\checkpoints\ADJSCC",
  "D:\Research\ai-data\cache\ADJSCC"
)

foreach ($path in $paths) {
  if (Test-Path $path) {
    Write-Host "[OK] $path"
  } else {
    Write-Host "[MISSING] $path"
  }
}
