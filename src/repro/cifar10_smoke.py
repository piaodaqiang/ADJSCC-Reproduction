"""Safe CIFAR-10 smoke wrapper for the ADJSCC reproduction project.

This module intentionally avoids dataset downloads, training, checkpoint
writes, and direct execution of the upstream adjscc_cifar10.py train/eval
entrypoints.
"""

from __future__ import annotations

import argparse
import importlib
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
UPSTREAM_ROOT = PROJECT_ROOT / "external" / "ADJSCC"
DEFAULT_CIFAR10_DIR = Path("/mnt/d/Research/ai-data/datasets/CIFAR10")


@dataclass(frozen=True)
class RuntimeModules:
    tf: object
    tfc: object
    tfp: object
    np: object
    util_module: object
    util_channel: object


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

    print("\n== CIFAR-10 directory check ==")
    _print_item("cifar10_dir", cifar10_dir)
    _print_item("cifar10_dir_exists", cifar10_dir.exists())
    if not cifar10_dir.exists():
        print("No CIFAR-10 directory found. This wrapper will not download CIFAR-10 automatically.")
        print("If you want to download CIFAR-10, confirm that as a separate step first.")
        return

    candidates = list(_iter_cifar10_candidates(cifar10_dir))
    if candidates:
        print("recognized_cifar10_files:")
        for path in candidates:
            print(f"- {path}")
    else:
        print("No recognizable CIFAR-10 files found in the configured directory.")
        print("This wrapper will not download CIFAR-10 automatically.")
        print("If you want to download CIFAR-10, confirm that as a separate step first.")


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Safe ADJSCC CIFAR-10 smoke wrapper: checks imports, builds the model, or runs one fake forward pass."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check-only", action="store_true", help="Only check runtime, imports, paths, and CIFAR-10 presence.")
    mode.add_argument("--build-only", action="store_true", help="Build the ADJSCC CIFAR-10 model without data or training.")
    mode.add_argument("--fake-forward", action="store_true", help="Run one tiny random-data forward pass without training.")
    parser.add_argument("--cifar10-dir", type=Path, default=DEFAULT_CIFAR10_DIR)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--snr-db", type=float, default=10.0)
    parser.add_argument("--transmit-channel-num", type=int, default=16)
    parser.add_argument("--learning-rate", type=float, default=1e-4)
    parser.add_argument("--seed", type=int, default=2026)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not (args.check_only or args.build_only or args.fake_forward):
        args.check_only = True

    print("ADJSCC CIFAR-10 smoke wrapper")
    print("Safety: no dataset download, no train/eval, no checkpoint write.")
    _ensure_project_context()
    modules = _import_runtime_modules()
    check_environment(modules, args.cifar10_dir)

    if args.build_only:
        print()
        run_build_only(modules, args)
    elif args.fake_forward:
        print()
        run_fake_forward(modules, args)
    else:
        print("\nCheck-only completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
