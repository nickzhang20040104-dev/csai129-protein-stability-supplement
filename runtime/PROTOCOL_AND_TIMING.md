# Inference protocol and timing evidence

All models used 220 single-chain sequences, seed labels 42/43/44 and one diffusion sample per label. No MSA or template service, binding partner or affinity estimate entered the confidence analysis. Boltz-2 used three recycles, 200 sampling steps and disabled optimized kernels; Chai-1 used three trunk recycles, 200 timesteps and ESM embeddings; Biohub ESMFold2 used 20 loops, 200 sampling steps and local ESMC-6B embeddings. These settings are not equal-compute configurations.

The original launcher selected CUDA device 0. The recorded GPU label is NVIDIA vGPU-32GB. The physical GPU model and virtualization allocation were not recorded. Boltz and Chai ran concurrently on the selected device. ESM ran afterward, with a successful retry after replacing an incompatible PyTorch CUDA build. Concurrent use, startup treatment and different inference paths prevent interpreting the observed times as an isolated architecture comparison.

## Timing definitions

Chai-1 and ESMFold2 have one host wall-clock timer per successful sequence–seed item. The timer includes per-item input preparation, inference, structure/output writing, confidence saves and sequence validation. ESM model/ESMC loading before the item loop is excluded. The first Chai call, including any first-call overhead within that call, remains in the summary. These are not CUDA-event timings or FLOP estimates.

- Chai-1: 660 items, mean 32.397648 s, sample SD 3.783933 s, median 30.787896 s, sum 21,382.447487 s.
- ESMFold2 successful retry: 660 items, mean 5.110025 s, sample SD 1.548819 s, median 4.276490 s, sum 3,372.616768 s.
- Boltz-2: no comparable per-item timer was recorded. The three 220-item batch progress displays show 1,748, 1,743 and 1,746 seconds (29:08, 29:03 and 29:06). Their displayed total is 5,237 seconds. These are batch progress durations with seconds-level precision, not individual observations or full process runtimes.

The Chai/ESM item timers omit Boltz, failed model loading, repair/wait periods and other untimed overhead. They cannot be added and labeled all-model GPU-hours or billed compute. The complete timestamp envelope was 26,502 seconds, including overlap and repair/wait. It is not exclusive GPU time.

`per_inference_seconds.csv` records 1,320 timers and their source-relative paths/hashes. `per_inference_complete_records.jsonl` retains the corresponding original JSON objects and source-file hashes. The source extraction checked each record against its inference-log JSON object. `boltz_progress_timing.csv` gives the final progress reports, counts, source-relative log paths and physical lines. `runtime_intervals.csv` documents ten precisely scoped timestamp differences, with the recorded +08:00 timezone. Timestamp markers must not be substituted for an unrecorded isolated model-start time.

## Software provenance limits

The successful Boltz package capture reports boltz 2.2.1 and PyTorch 2.7.1. Initial Chai/ESM package captures failed because pip was unavailable. Later ESM records identify a local source checkout but not an immutable package or checkpoint revision; the successful retry used PyTorch 2.11.0+cu128. Therefore Chai package 0.6.1 and esm package 3.4.1 cannot be independently established from these archived run records. No physical A100/H100/RTX claim, FLOP count, isolated per-model memory peak, energy use, monetary cost or billed GPU-hour estimate is supported.
