# Paper Reading Notes

Paper: Wireless Image Transmission Using Deep Source Channel Coding With Attention Modules

## Problem

Traditional image transmission usually separates source coding and channel coding. DeepJSCC-style methods learn an end-to-end mapping from image source to channel symbols and back to reconstructed images.

## What To Understand First

- What problem ADJSCC solves compared with basic DeepJSCC.
- What the attention modules change.
- What datasets and channels are used.
- Which metrics are reported, such as PSNR and MS-SSIM.
- Which experiments are essential for a first reproduction.

## Open Questions

- Which TensorFlow/Keras version is closest to the official implementation?
- How many CIFAR-10 settings are needed for a minimal but meaningful reproduction?
- Which code paths correspond to ADJSCC and which correspond to baseline BJSCC?
