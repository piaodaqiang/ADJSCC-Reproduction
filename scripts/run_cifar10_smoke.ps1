param(
  [ValidateSet("check-only", "build-only", "fake-forward", "cifar10-check", "real-batch-forward", "tiny-train")]
  [string]$Mode = "check-only",
  [string]$Distro = "Ubuntu-ADJSCC",
  [string]$WslProjectPath = "/mnt/d/Cloud/OneDrive/文档/Research/SemanticCommunication/ADJSCC-Reproduction",
  [string]$WslPython = "/home/piaodaqiang/miniforge3-adjscc/envs/adjscc-tf/bin/python"
)

$ErrorActionPreference = "Stop"

Write-Host "ADJSCC CIFAR-10 smoke wrapper launcher"
Write-Host "Safety: no dataset download, no upstream train/eval, no long training, no checkpoint write."
Write-Host "WSL distro: $Distro"
Write-Host "Mode: $Mode"

$modeArg = "--$Mode"
$command = "cd '$WslProjectPath' && '$WslPython' -m src.repro.cifar10_smoke $modeArg"
wsl -d $Distro -- bash -lc $command
