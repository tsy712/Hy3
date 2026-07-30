# Running Hy3 Model Locally (DeepSpeed / Flash-Attention Guide) / 本地运行 Hy3 模型指南（含 DeepSpeed / Flash-Attention）

> 📖 [Back to README / 返回 README](../README.md) | Full comparison also in [Environment Requirements](environment.md) / 完整对比另见 [环境要求](environment.md)

---

## Differences Between the Two Modes / 两种运行模式的差异

Many developers new to Hy3 confuse these two scenarios. **Please make sure you know which one you're in:**  
很多第一次接触 Hy3 的开发者会混淆以下两种场景。**请务必确认你属于哪一种：**

| Dimension / 维度 | 🟢 Mode A: This App (Recommended) / 本应用（推荐） | 🔴 Mode B: Run Hy3 Model Locally / 本地运行 Hy3 模型 |
|------|--------------------------|------------------------------|
| What it does / 做什么 | Call Tencent Cloud API via HTTP / 通过 HTTP 调用腾讯云端 API | Load and infer the model on local GPU / 在本地 GPU 上加载并推理模型 |
| Need GPU? / 需要 GPU？ | **No** / **不需要** | **Required** (NVIDIA GPU) / **必须**（NVIDIA GPU） |
| Need CUDA? / 需要 CUDA？ | **No** / **不需要** | **Required** (CUDA 11.8 or 12.1) / **必须**（CUDA 11.8 或 12.1） |
| Install size / 安装大小 | ~80 MB | ~20 GB+ (incl. model weights) / （含模型权重） |
| Install time / 安装时间 | < 2 min / 分钟 | 30 min ~ 2 hours / 小时 |
| Works first try? / 一次能跑通？ | ✅ Almost never fails / 几乎不会出问题 | ❌ High chance of issues / 高概率踩坑 |

> **If you just want to use Hy3's intelligence for research, coding, Q&A → Mode A.** This app covers everything via cloud API.  
> **If you want to deploy the Hy3 model itself on your own GPU server → Mode B.** Read on.  
> **如果你只是想使用 Hy3 的智能能力做研究、写代码、问答 → 模式 A**，本应用通过云端 API 完全覆盖。
> **如果你想在自己的 GPU 服务器上部署 Hy3 模型本身 → 模式 B**，请继续阅读。

---

## Mode B: Known Pitfalls of Running Hy3 Locally / 本地运行 Hy3 模型的已知陷阱

Hy3's official model repo depends on `deepspeed` + `flash-attn` — two deep learning components notorious for difficult installation. **Wrong version combinations cause compilation failures or runtime crashes.**  
Hy3 官方模型仓库依赖 `deepspeed` + `flash-attn` 两个以"安装困难"著称的深度学习组件，**不正确的版本组合会导致编译失败或运行时崩溃**。

### 1. DeepSpeed + Flash-Attention Version Compatibility Table / 版本兼容对照表

| Torch Version | CUDA Version | DeepSpeed | Flash-Attn | Notes / 说明 |
|-----------|----------|-----------|------------|------|
| 2.1.x | 11.8 | 0.12.x | 2.5.x | Stable combo, try first / 稳定组合，推荐先尝试 |
| 2.2.x | 12.1 | 0.13.x | 2.5.x | Newer combo / 较新组合 |
| 2.3.x | 12.1 | 0.14.x | 2.6.x | Latest combo, possible issues / 最新组合，可能有兼容问题 |
| 2.4.x+ | 12.4+ | 0.15.x+ | 2.7.x+ | Cutting-edge, stability unverified / 前沿组合，稳定性未充分验证 |

> **Key lesson**: Don't just `pip install deepspeed`. First check your `torch.__version__` and `nvcc --version`, then choose versions per the table above.  
> **关键教训**: 不要用 `pip install deepspeed` 直接安装，必须先确认你的 `torch.__version__` 和 `nvcc --version`，再按上表选择版本。

```bash
# Check versions first / 先查版本
python -c "import torch; print(torch.__version__)"
nvcc --version  # Or nvidia-smi to check CUDA Driver version / 或 nvidia-smi 查看 CUDA Driver 版本

# Then install precisely (example: CUDA 11.8 + Torch 2.1.x) / 再精确安装（示例：CUDA 11.8 + Torch 2.1.x）
pip install torch==2.1.2 torchvision==0.16.2 --index-url https://download.pytorch.org/whl/cu118
pip install deepspeed==0.12.6
pip install flash-attn==2.5.8 --no-build-isolation
```

### 2. Common Reasons for flash-attn Compilation Failures / flash-attn 编译失败的常见原因

- **Ninja not installed**: `pip install ninja` / **Ninja 未安装**: `pip install ninja`
- **GCC/G++ version too low**: Need GCC 9+ (Linux) or Visual Studio Build Tools 2022+ (Windows) / **GCC/G++ 版本过低**: 需要 GCC 9+（Linux）或 Visual Studio Build Tools 2022+（Windows）
- **CUDA Toolkit not installed or wrong path**: Ensure `nvcc` is executable and in PATH / **CUDA Toolkit 未安装或路径不对**: 确保 `nvcc` 可执行且在 PATH 中
- **Insufficient RAM**: flash-attn compilation peak memory can reach **32 GB+**; OOM Killer may terminate the process / **RAM 不足**: `flash-attn` 编译峰值内存可达 **32 GB+**，内存不足会导致编译被 OOM Killer 终止
- **Windows compatibility**: flash-attn has limited Windows support; strongly recommend WSL2 or native Linux / **Windows 兼容性**: `flash-attn` 对 Windows 支持有限，强烈建议在 WSL2 或 Linux 原生环境下编译

### 3. Minimum VRAM Requirements / 显存最低要求

| Model Size / 模型规模 | FP16 / 半精度 | FP32 / 全精度 | INT8 Quantized / INT8 量化 |
|---------|-------------|-------------|----------|
| 7B | ~14 GB | ~28 GB | ~8 GB |
| 13B | ~26 GB | ~52 GB | ~14 GB |
| 34B | ~68 GB | ~136 GB | ~35 GB |

> **⚠️ If you're using a MacBook / thin-and-light / integrated-graphics desktop**: Mode B is impossible to run.  
> **⚠️ If you only have a single 8GB/12GB consumer GPU (e.g. RTX 3060/4060)**: Only 7B quantized version, and CPU offload is needed.  
> **Recommended setup**: NVIDIA GPU ≥ 24 GB VRAM (e.g. RTX 3090/4090, A5000, A100).  
> 
> **⚠️ 如果你用 MacBook / 轻薄本 / 核显台式机**：模式 B 不可能跑通。  
> **⚠️ 如果你只有单张 8GB/12GB 消费级显卡（如 RTX 3060/4060）**：只能跑 7B 量化版，且需要 CPU offload。  
> **推荐评审环境**: NVIDIA GPU ≥ 24 GB 显存（如 RTX 3090/4090, A5000, A100）。

### 4. Recommended: Use Docker for One-Click Deployment (Skip Compilation Hell) / 推荐：使用 Docker 一键部署（跳过编译地狱）

If you must run Hy3 locally, **strongly recommend using the official Docker image** to avoid manually compiling `deepspeed` + `flash-attn`:  
如果必须本地运行 Hy3 模型，**强烈建议使用官方 Docker 镜像**，避免手动编译 `deepspeed` + `flash-attn`：

```bash
# Pull Hy3 official image (if available) / 拉取 Hy3 官方镜像（如可用）
docker pull tencent-hunyuan/hy3:latest

# Start (mount model directory) / 启动（挂载模型目录）
docker run --gpus all \
  -v /path/to/models:/models \
  -p 7860:7860 \
  tencent-hunyuan/hy3:latest
```

> If an official Docker image is not yet available, file an Issue on the Hy3 official repo or build from the `Dockerfile` template yourself.  
> 如官方尚未发布 Docker 镜像，可在 Hy3 官方仓库提交 Issue 请求，或参考 `Dockerfile` 模板自行构建。
