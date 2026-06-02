"""Safe CIFAR-10 smoke wrapper for the ADJSCC reproduction project.

This module intentionally avoids dataset downloads, long training, checkpoint
writes, image writes, and direct execution of the upstream adjscc_cifar10.py
train/eval entrypoints.
"""

from __future__ import annotations

import argparse
import importlib
import json
import pickle
import sys
import tarfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
UPSTREAM_ROOT = PROJECT_ROOT / "external" / "ADJSCC"
DEFAULT_CIFAR10_DIR = Path("/mnt/d/Research/ai-data/datasets/CIFAR10")
DEFAULT_RUN_ROOT = Path("/mnt/d/Research/ai-data/runs/ADJSCC")
MAX_TINY_TRAIN_STEPS = 10
CIFAR10_BATCH_DIR = "cifar-10-batches-py"
CIFAR10_ARCHIVE = "cifar-10-python.tar.gz"
CIFAR10_REQUIRED_FILES = (
    "data_batch_1",
    "data_batch_2",
    "data_batch_3",
    "data_batch_4",
    "data_batch_5",
    "test_batch",
    "batches.meta",
)


@dataclass(frozen=True)
class RuntimeModules:
    tf: object
    tfc: object
    tfp: object
    np: object
    util_module: object
    util_channel: object


@dataclass(frozen=True)
class Cifar10Inventory:
    root: Path
    root_exists: bool
    archive_path: Path
    batch_dir: Path
    archive_exists: bool
    batch_dir_exists: bool
    recognized_files: tuple[Path, ...]

    @property
    def has_data_batch_1(self) -> bool:
        return any(path.name == "data_batch_1" for path in self.recognized_files)

    @property
    def is_usable_for_real_batch(self) -> bool:
        return self.has_data_batch_1 or self.archive_exists


def _path_is_inside(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False
    except FileNotFoundError:
        return False


def _module_origin(module: object) -> str:
    origin = getattr(module, "__file__", None)
    return str(Path(origin).resolve()) if origin else "<built-in or unknown>"


def _print_item(name: str, value: object) -> None:
    print(f"{name}: {value}")


def _ensure_project_context() -> None:
    _print_item("project_root", PROJECT_ROOT)
    _print_item("current_working_directory", Path.cwd())
    _print_item("upstream_root", UPSTREAM_ROOT)
    _print_item("upstream_root_exists", UPSTREAM_ROOT.exists())
    if not UPSTREAM_ROOT.exists():
        raise FileNotFoundError(f"Missing upstream ADJSCC directory: {UPSTREAM_ROOT}")


def _import_runtime_modules() -> RuntimeModules:
    """Import installed dependencies before appending the upstream source path."""

    tf = importlib.import_module("tensorflow")
    tfc = importlib.import_module("tensorflow_compression")
    tfp = importlib.import_module("tensorflow_probability")
    np = importlib.import_module("numpy")

    tfc_origin = Path(_module_origin(tfc))
    if _path_is_inside(tfc_origin, UPSTREAM_ROOT):
        raise RuntimeError(
            "Unsafe tensorflow_compression import: Python loaded the bundled "
            f"upstream copy from {tfc_origin}. Run this wrapper from the project "
            "root without putting external/ADJSCC at the front of PYTHONPATH."
        )

    upstream = str(UPSTREAM_ROOT)
    if upstream not in sys.path:
        sys.path.append(upstream)

    util_module = importlib.import_module("util_module")
    util_channel = importlib.import_module("util_channel")
    return RuntimeModules(tf, tfc, tfp, np, util_module, util_channel)


def _iter_cifar10_candidates(root: Path, max_items: int = 30) -> Iterable[Path]:
    if not root.exists() or not root.is_dir():
        return []

    names = {
        "data_batch_1",
        "data_batch_2",
        "data_batch_3",
        "data_batch_4",
        "data_batch_5",
        "test_batch",
        "batches.meta",
        "cifar-10-python.tar.gz",
    }
    candidates: list[Path] = []
    for path in root.rglob("*"):
        if len(candidates) >= max_items:
            break
        if path.name in names or path.name == "cifar-10-batches-py":
            candidates.append(path)
    return candidates


def inspect_cifar10_dir(root: Path) -> Cifar10Inventory:
    """Inspect local CIFAR-10 files without calling Keras download helpers."""

    archive_path = root / CIFAR10_ARCHIVE
    batch_dir = root / CIFAR10_BATCH_DIR
    recognized: list[Path] = []
    if root.exists() and root.is_dir():
        if archive_path.exists():
            recognized.append(archive_path)
        if batch_dir.exists():
            recognized.append(batch_dir)
        for name in CIFAR10_REQUIRED_FILES:
            path = batch_dir / name
            if path.exists():
                recognized.append(path)
            root_level_path = root / name
            if root_level_path.exists():
                recognized.append(root_level_path)

    return Cifar10Inventory(
        root=root,
        root_exists=root.exists(),
        archive_path=archive_path,
        batch_dir=batch_dir,
        archive_exists=archive_path.exists(),
        batch_dir_exists=batch_dir.exists(),
        recognized_files=tuple(recognized),
    )


def print_cifar10_inventory(inventory: Cifar10Inventory) -> None:
    print("== CIFAR-10 data gate ==")
    _print_item("cifar10_dir", inventory.root)
    _print_item("cifar10_dir_exists", inventory.root_exists)
    _print_item("has_cifar10_archive", inventory.archive_exists)
    _print_item("archive_path", inventory.archive_path)
    _print_item("has_cifar10_batch_dir", inventory.batch_dir_exists)
    _print_item("batch_dir", inventory.batch_dir)

    print("required_batch_files:")
    for name in CIFAR10_REQUIRED_FILES:
        in_batch_dir = inventory.batch_dir / name
        in_root = inventory.root / name
        exists = in_batch_dir.exists() or in_root.exists()
        print(f"- {name}: {exists}")

    if inventory.recognized_files:
        print("recognized_cifar10_files:")
        for path in inventory.recognized_files:
            print(f"- {path}")
    else:
        print("No recognizable CIFAR-10 files found.")

    if inventory.is_usable_for_real_batch:
        print("CIFAR-10 gate result: local CIFAR-10 data is recognizable.")
    else:
        print("CIFAR-10 gate result: local CIFAR-10 data is not recognizable.")
        print("This wrapper will not download CIFAR-10 automatically.")
        print("If you want to download CIFAR-10, confirm that as a separate step first.")


def check_environment(modules: RuntimeModules, cifar10_dir: Path) -> None:
    tf = modules.tf
    tfc = modules.tfc
    tfp = modules.tfp
    np = modules.np

    print("== Runtime ==")
    _print_item("python_executable", sys.executable)
    _print_item("python_version", sys.version.replace("\n", " "))
    _print_item("tensorflow_version", getattr(tf, "__version__", "<unknown>"))
    _print_item("tensorflow_origin", _module_origin(tf))
    _print_item("tensorflow_compression_version", getattr(tfc, "__version__", "<unknown>"))
    _print_item("tensorflow_compression_origin", _module_origin(tfc))
    _print_item("tensorflow_probability_version", getattr(tfp, "__version__", "<unknown>"))
    _print_item("tensorflow_probability_origin", _module_origin(tfp))
    _print_item("numpy_version", getattr(np, "__version__", "<unknown>"))
    _print_item("numpy_origin", _module_origin(np))
    _print_item("tensorflow_gpus", tf.config.list_physical_devices("GPU"))

    print("\n== Upstream imports ==")
    _print_item("util_module_origin", _module_origin(modules.util_module))
    _print_item("util_channel_origin", _module_origin(modules.util_channel))

    print()
    print_cifar10_inventory(inspect_cifar10_dir(cifar10_dir))


def build_model(modules: RuntimeModules, transmit_channel_num: int, learning_rate: float):
    tf = modules.tf
    input_imgs = tf.keras.layers.Input(shape=(32, 32, 3), name="input_imgs")
    input_snrdb = tf.keras.layers.Input(shape=(1,), name="input_snrdb")
    normal_imgs = tf.keras.layers.Lambda(lambda x: x / 255.0, name="normal")(input_imgs)
    encoded = modules.util_module.Attention_Encoder(normal_imgs, input_snrdb, transmit_channel_num)
    channel_out = modules.util_channel.Channel(channel_type="awgn")(encoded, input_snrdb)
    decoded = modules.util_module.Attention_Decoder(channel_out, input_snrdb)
    output_imgs = tf.keras.layers.Lambda(lambda x: x * 255.0, name="denormal")(decoded)
    model = tf.keras.Model(inputs=[input_imgs, input_snrdb], outputs=output_imgs, name="adjscc_cifar10_smoke")
    model.compile(tf.keras.optimizers.Adam(learning_rate), "mse")
    return model


def run_build_only(modules: RuntimeModules, args: argparse.Namespace) -> None:
    print("== Build-only ==")
    model = build_model(modules, args.transmit_channel_num, args.learning_rate)
    _print_item("model_name", model.name)
    _print_item("model_inputs", [tuple(input_tensor.shape) for input_tensor in model.inputs])
    _print_item("model_outputs", [tuple(output_tensor.shape) for output_tensor in model.outputs])
    _print_item("trainable_parameters", model.count_params())
    print("Build-only completed. No dataset was loaded, no training was run, and no checkpoint was written.")


def run_fake_forward(modules: RuntimeModules, args: argparse.Namespace) -> None:
    print("== Fake-forward ==")
    tf = modules.tf
    model = build_model(modules, args.transmit_channel_num, args.learning_rate)
    tf.random.set_seed(args.seed)
    fake_images = tf.random.uniform(
        shape=(args.batch_size, 32, 32, 3),
        minval=0.0,
        maxval=255.0,
        dtype=tf.float32,
    )
    snr = tf.ones((args.batch_size, 1), dtype=tf.float32) * float(args.snr_db)
    outputs = model([fake_images, snr], training=False)
    _print_item("fake_input_shape", tuple(fake_images.shape))
    _print_item("snr_shape", tuple(snr.shape))
    _print_item("fake_output_shape", tuple(outputs.shape))
    _print_item("fake_output_dtype", outputs.dtype.name)
    print("Fake-forward completed. No dataset was loaded, no training was run, and no checkpoint was written.")


def _load_pickled_cifar10_batch(batch_file) -> object:
    return pickle.load(batch_file, encoding="latin1")


def _read_data_batch_1_from_dir(root: Path):
    batch_path = root / CIFAR10_BATCH_DIR / "data_batch_1"
    if not batch_path.exists():
        batch_path = root / "data_batch_1"
    with batch_path.open("rb") as batch_file:
        return _load_pickled_cifar10_batch(batch_file), batch_path


def _read_data_batch_1_from_archive(archive_path: Path):
    # Read from the tar.gz in memory only; this does not extract or write files.
    with tarfile.open(archive_path, mode="r:gz") as archive:
        member = archive.getmember(f"{CIFAR10_BATCH_DIR}/data_batch_1")
        extracted = archive.extractfile(member)
        if extracted is None:
            raise FileNotFoundError(f"Cannot read data_batch_1 inside {archive_path}")
        with extracted:
            return _load_pickled_cifar10_batch(extracted), Path(member.name)


def load_cifar10_batch_images(cifar10_dir: Path, batch_size: int, np_module: object):
    inventory = inspect_cifar10_dir(cifar10_dir)
    if not inventory.is_usable_for_real_batch:
        raise FileNotFoundError(
            "No local CIFAR-10 batch file was found. This wrapper will not download CIFAR-10 automatically."
        )

    if inventory.has_data_batch_1:
        batch, source = _read_data_batch_1_from_dir(cifar10_dir)
    else:
        batch, source = _read_data_batch_1_from_archive(inventory.archive_path)

    raw_data = batch.get("data") if isinstance(batch, dict) else None
    if raw_data is None:
        raise KeyError(f"CIFAR-10 batch from {source} does not contain a 'data' field.")
    if len(raw_data) < batch_size:
        raise ValueError(f"CIFAR-10 batch from {source} has fewer than {batch_size} images.")

    images = np_module.asarray(raw_data[:batch_size], dtype="float32")
    images = images.reshape(batch_size, 3, 32, 32).transpose(0, 2, 3, 1)
    return images, source


def run_real_batch_forward(modules: RuntimeModules, args: argparse.Namespace) -> None:
    print("== Real-batch-forward ==")
    inventory = inspect_cifar10_dir(args.cifar10_dir)
    print_cifar10_inventory(inventory)
    if not inventory.is_usable_for_real_batch:
        print("Real-batch-forward stopped before model execution.")
        print("Reason: local CIFAR-10 files were not found or not recognizable.")
        print("This wrapper will not download CIFAR-10 automatically.")
        print("If you want to download CIFAR-10, confirm that as a separate step first.")
        return

    images, source = load_cifar10_batch_images(args.cifar10_dir, args.batch_size, modules.np)
    tf = modules.tf
    model = build_model(modules, args.transmit_channel_num, args.learning_rate)
    tf.random.set_seed(args.seed)
    snr = tf.ones((args.batch_size, 1), dtype=tf.float32) * float(args.snr_db)
    outputs = model([tf.convert_to_tensor(images, dtype=tf.float32), snr], training=False)
    _print_item("cifar10_batch_source", source)
    _print_item("real_input_shape", tuple(images.shape))
    _print_item("snr_shape", tuple(snr.shape))
    _print_item("real_output_shape", tuple(outputs.shape))
    _print_item("real_output_dtype", outputs.dtype.name)
    print("Real-batch-forward completed. No training was run, no checkpoint was written, and no data was downloaded.")


def _compute_image_metrics_per_image(tf: object, targets, outputs, max_pixel_value: float):
    clipped_outputs = tf.clip_by_value(outputs, 0.0, max_pixel_value)
    squared_error = tf.math.squared_difference(targets, clipped_outputs)
    per_image_mse = tf.reduce_mean(squared_error, axis=(1, 2, 3))
    max_value = tf.constant(max_pixel_value, dtype=per_image_mse.dtype)
    finite_psnr = 10.0 * tf.math.log((max_value * max_value) / per_image_mse) / tf.math.log(10.0)
    per_image_psnr = tf.where(per_image_mse > 0.0, finite_psnr, tf.fill(tf.shape(per_image_mse), float("inf")))
    per_image_ssim = tf.image.ssim(targets, clipped_outputs, max_val=max_pixel_value)
    return per_image_mse, per_image_psnr, per_image_ssim


def run_metrics_smoke(modules: RuntimeModules, args: argparse.Namespace) -> None:
    print("== Metrics-smoke ==")
    if args.batch_size != 2:
        raise ValueError("Metrics-smoke is intentionally limited to --batch-size 2 in this stage.")
    if args.write_run_summary:
        raise RuntimeError("Metrics-smoke only prints values in this stage; it does not write run summaries.")
    if args.save_checkpoint:
        raise RuntimeError("Metrics-smoke does not support checkpoint saving.")

    images, source = load_cifar10_batch_images(args.cifar10_dir, args.batch_size, modules.np)

    tf = modules.tf
    model = build_model(modules, args.transmit_channel_num, args.learning_rate)
    tf.random.set_seed(args.seed)

    inputs = tf.convert_to_tensor(images, dtype=tf.float32)
    targets = tf.convert_to_tensor(images, dtype=tf.float32)
    snr = tf.ones((args.batch_size, 1), dtype=tf.float32) * float(args.snr_db)
    outputs = model([inputs, snr], training=False)

    max_pixel_value = 255.0
    per_image_mse, per_image_psnr, per_image_ssim = _compute_image_metrics_per_image(
        tf,
        targets,
        outputs,
        max_pixel_value=max_pixel_value,
    )
    batch_mse = tf.reduce_mean(per_image_mse)
    batch_psnr = tf.reduce_mean(per_image_psnr)
    batch_ssim = tf.reduce_mean(per_image_ssim)

    mse_values = [float(value) for value in per_image_mse.numpy()]
    psnr_values = [float(value) for value in per_image_psnr.numpy()]
    ssim_values = [float(value) for value in per_image_ssim.numpy()]

    _print_item("cifar10_batch_source", source)
    _print_item("metrics_input_shape", tuple(inputs.shape))
    _print_item("snr_shape", tuple(snr.shape))
    _print_item("metrics_output_shape", tuple(outputs.shape))
    _print_item("pixel_value_range_assumption", "[0, 255]")
    _print_item("psnr_max_pixel_value", max_pixel_value)
    for index, (mse, psnr, ssim) in enumerate(zip(mse_values, psnr_values, ssim_values), start=1):
        _print_item(f"image_{index}_mse", mse)
        _print_item(f"image_{index}_psnr_db", psnr)
        _print_item(f"image_{index}_ssim", ssim)
    _print_item("batch_mean_mse", float(batch_mse.numpy()))
    _print_item("batch_mean_psnr_db", float(batch_psnr.numpy()))
    _print_item("batch_mean_ssim", float(batch_ssim.numpy()))
    print(
        "Metrics-smoke completed. Printed MSE/PSNR/SSIM only; no training, checkpoint, image, "
        "summary, or data download was produced."
    )


def run_tiny_train(modules: RuntimeModules, args: argparse.Namespace) -> None:
    print("== Tiny-train ==")

    if args.save_checkpoint:
        raise RuntimeError("Tiny-train does not support checkpoint saving in this stage.")

    if args.max_steps < 1 or args.max_steps > MAX_TINY_TRAIN_STEPS:
        raise ValueError(f"--max-steps must be between 1 and {MAX_TINY_TRAIN_STEPS}.")

    images, source = load_cifar10_batch_images(args.cifar10_dir, args.batch_size, modules.np)

    tf = modules.tf
    model = build_model(modules, args.transmit_channel_num, args.learning_rate)
    loss_fn = tf.keras.losses.MeanSquaredError()
    optimizer = model.optimizer

    tf.random.set_seed(args.seed)

    inputs = tf.convert_to_tensor(images, dtype=tf.float32)
    targets = tf.convert_to_tensor(images, dtype=tf.float32)
    snr = tf.ones((args.batch_size, 1), dtype=tf.float32) * float(args.snr_db)

    losses: list[float] = []

    for step in range(1, args.max_steps + 1):
        with tf.GradientTape() as tape:
            outputs = model([inputs, snr], training=True)
            loss = loss_fn(targets, outputs)

        gradients = tape.gradient(loss, model.trainable_variables)
        grad_var_pairs = [
            (grad, var)
            for grad, var in zip(gradients, model.trainable_variables)
            if grad is not None
        ]

        if not grad_var_pairs:
            raise RuntimeError("No gradients were produced during tiny training.")

        optimizer.apply_gradients(grad_var_pairs)

        loss_value = float(loss.numpy())
        losses.append(loss_value)
        _print_item(f"tiny_train_step_{step}_loss", loss_value)

    _print_item("cifar10_batch_source", source)
    _print_item("tiny_train_input_shape", tuple(images.shape))
    _print_item("snr_shape", tuple(snr.shape))
    _print_item("tiny_train_output_shape", tuple(outputs.shape))
    _print_item("max_steps", args.max_steps)
    print("Tiny-train completed. No checkpoint was written and no data was downloaded.")

    if args.write_run_summary:
        run_root = args.run_root.expanduser().resolve()
        safe_run_root = DEFAULT_RUN_ROOT.resolve()
        try:
            run_root.relative_to(safe_run_root)
        except ValueError as exc:
            raise ValueError(f"--run-root must be inside {safe_run_root}; got {run_root}") from exc

        run_root.mkdir(parents=True, exist_ok=True)
        summary_path = run_root / f"tiny_train_summary_{time.strftime('%Y%m%d-%H%M%S')}.json"
        summary = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "mode": "tiny-train",
            "python_executable": sys.executable,
            "python_version": sys.version,
            "tensorflow_version": getattr(tf, "__version__", "<unknown>"),
            "tensorflow_probability_version": getattr(modules.tfp, "__version__", "<unknown>"),
            "numpy_version": getattr(modules.np, "__version__", "<unknown>"),
            "input_shape": list(inputs.shape),
            "snr_shape": list(snr.shape),
            "output_shape": list(outputs.shape),
            "run_root": str(run_root),
            "summary_path": str(summary_path),
            "batch_size": args.batch_size,
            "max_steps": args.max_steps,
            "snr_db": args.snr_db,
            "losses": losses,
            "cifar10_batch_source": str(source),
            "checkpoint_saved": False,
            "data_downloaded": False,
            "official_train_eval_used": False,
        }
        summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        _print_item("run_summary_path", summary_path)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Safe ADJSCC CIFAR-10 smoke wrapper: checks imports, builds the model, runs tiny forwards, or prints minimal metrics."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check-only", action="store_true", help="Only check runtime, imports, paths, and CIFAR-10 presence.")
    mode.add_argument("--build-only", action="store_true", help="Build the ADJSCC CIFAR-10 model without data or training.")
    mode.add_argument("--fake-forward", action="store_true", help="Run one tiny random-data forward pass without training.")
    mode.add_argument("--cifar10-check", action="store_true", help="Only inspect local CIFAR-10 files without imports or downloads.")
    mode.add_argument("--real-batch-forward", action="store_true", help="Run one tiny local CIFAR-10 batch forward pass without training.")
    mode.add_argument("--metrics-smoke", action="store_true", help="Print MSE/PSNR for two local CIFAR-10 images without saving artifacts.")
    mode.add_argument("--tiny-train", action="store_true", help="Run a tightly limited tiny training check.")
    parser.add_argument("--cifar10-dir", type=Path, default=DEFAULT_CIFAR10_DIR)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--max-steps", type=int, default=1)
    parser.add_argument("--run-root", type=Path, default=DEFAULT_RUN_ROOT)
    parser.add_argument("--write-run-summary", action="store_true")
    parser.add_argument("--save-checkpoint", action="store_true")
    parser.add_argument("--snr-db", type=float, default=10.0)
    parser.add_argument("--transmit-channel-num", type=int, default=16)
    parser.add_argument("--learning-rate", type=float, default=1e-4)
    parser.add_argument("--seed", type=int, default=2026)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not (
        args.check_only
        or args.build_only
        or args.fake_forward
        or args.cifar10_check
        or args.real_batch_forward
        or args.metrics_smoke
        or args.tiny_train
    ):
        args.check_only = True

    print("ADJSCC CIFAR-10 smoke wrapper")
    print("Safety: no dataset download, no train/eval, no checkpoint write, no image write.")
    _ensure_project_context()

    if args.cifar10_check:
        print_cifar10_inventory(inspect_cifar10_dir(args.cifar10_dir))
        print("\nCIFAR-10 check completed.")
        return 0

    modules = _import_runtime_modules()
    check_environment(modules, args.cifar10_dir)

    if args.build_only:
        print()
        run_build_only(modules, args)
    elif args.fake_forward:
        print()
        run_fake_forward(modules, args)
    elif args.real_batch_forward:
        print()
        run_real_batch_forward(modules, args)
    elif args.metrics_smoke:
        print()
        run_metrics_smoke(modules, args)
    elif args.tiny_train:
        print()
        run_tiny_train(modules, args)
    else:
        print("\nCheck-only completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
