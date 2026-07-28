# Running the Hy3 Model Locally (with DeepSpeed / Flash-Attention)

<p align="center">
  <a href="local-hy3-model.md">🇨🇳 中文</a> · <strong>🇺🇸 English</strong> · <a href="../README_EN.md">⬅ Back to README</a>
</p>

---

## Differences Between the Two Running Modes

Many developers new to Hy3 confuse the following two scenarios. **Please make sure which one you belong to:**

| Dimension | 🟢 Mode A: This App (Recommended) | 🔴 Mode B: Run Hy3 Model Locally |
|-----------|-----------------------------------|----------------------------------|
| What it does | Call Tencent cloud API via HTTP | Load and infer the model on local GPU |
| Need GPU? | **No** | **Yes** (NVIDIA GPU) |
| Need CUDA? | **No** | **Yes** (CUDA 11.8 or 12.1) |
| Install size | ~80 MB | ~20 GB+ (including model weights) |
| Install time | < 2 minutes | 30 minutes ~ 2 hours |
| Will it work the first time? | ✅ Almost certainly | ❌ High chance of issues |

> **If you just want to use Hy3's intelligent capabilities for research, coding, and Q&A → Mode A.** This app fully covers your needs through the cloud API.
> **If you want to deploy the Hy3 model itself on your own GPU server → Mode B.** Continue reading.

---

## Mode B: Known Pitfalls of Running Hy3 Locally

The official Hy3 model repository depends on `deepspeed` + `flash-attn`, two deep-learning components famous for being hard to install. **Incorrect version combinations will cause compilation failures or runtime crashes.**

### 1. DeepSpeed + Flash-Attention Version Compatibility Table

| Torch Version | CUDA Version | DeepSpeed | Flash-Attn | Notes |
|---------------|--------------|-----------|------------|-------|
| 2.1.x | 11.8 | 0.12.x | 2.5.x | Stable combination, try first |
| 2.2.x | 12.1 | 0.13.x | 2.5.x | Newer combination |
| 2.3.x | 12.1 | 0.14.x | 2.6.x | Latest combination, possible compatibility issues |
| 2.4.x+ | 12.4+ | 0.15.x+ | 2.7.x+ | Cutting-edge, stability not fully verified |

> **Key lesson**: Do not install with `pip install deepspeed` directly. First confirm your `torch.__version__` and `nvcc --version`, then choose versions according to the table above.

```bash
# Check versions first
python -c "import torch; print(torch.__version__)"
nvcc --version  # or nvidia-smi to view CUDA Driver version

# Then install precisely (example: CUDA 11.8 + Torch 2.1.x)
pip install torch==2.1.2 torchvision==0.16.2 --index-url https://download.pytorch.org/whl/cu118
pip install deepspeed==0.12.6
pip install flash-attn==2.5.8 --no-build-isolation
```

### 2. Common Causes of flash-attn Compilation Failure

- **Ninja not installed**: `pip install ninja`
- **GCC/G++ version too low**: GCC 9+ (Linux) or Visual Studio Build Tools 2022+ (Windows) required
- **CUDA Toolkit not installed or wrong path**: ensure `nvcc` is executable and in PATH
- **Insufficient RAM**: `flash-attn` compilation peak memory can reach **32 GB+**; insufficient memory will cause OOM Killer termination
- **Windows compatibility**: `flash-attn` has limited Windows support; strongly recommend compiling in WSL2 or native Linux

### 3. Minimum VRAM Requirements

| Model Size | Half Precision (FP16) | Full Precision (FP32) | INT8 Quantization |
|------------|-----------------------|-----------------------|-------------------|
| 7B | ~14 GB | ~28 GB | ~8 GB |
| 13B | ~26 GB | ~52 GB | ~14 GB |
| 34B | ~68 GB | ~136 GB | ~35 GB |

> **⚠️ If you use a MacBook / ultrabook / integrated-graphics desktop**: Mode B is impossible.
> **⚠️ If you only have a single 8GB/12GB consumer GPU (e.g., RTX 3060/4060)**: You can only run the 7B quantized version with CPU offload.
> **Recommended review environment**: NVIDIA GPU with ≥ 24 GB VRAM (e.g., RTX 3090/4090, A5000, A100).

### 4. Recommended: One-Click Docker Deployment (Skip Compilation Hell)

If you must run Hy3 locally, **strongly recommend using the official Docker image** to avoid manually compiling `deepspeed` + `flash-attn`:

```bash
# Pull the official Hy3 image (if available)
docker pull tencent-hunyuan/hy3:latest

# Start (mount model directory)
docker run --gpus all \
  -v /path/to/models:/models \
  -p 7860:7860 \
  tencent-hunyuan/hy3:latest
```

> If the official Docker image has not been released yet, you can file an Issue in the Hy3 official repo or build your own image using the `Dockerfile` template.
