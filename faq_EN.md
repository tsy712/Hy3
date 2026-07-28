# Frequently Asked Questions (FAQ)

<p align="center">
  <a href="faq.md">🇨🇳 中文</a> · <strong>🇺🇸 English</strong> · <a href="../README_EN.md">⬅ Back to README</a>
</p>

---

### Q: Do I need a GPU? Do I need to install CUDA?

**No.** All AI capabilities in this project are implemented through cloud API calls; only a lightweight web server runs locally. An ordinary laptop is sufficient.

### Q: How is this different from the official Hy3 repo's requirements.txt?

The official Hy3 repo includes model training/fine-tuning dependencies (`torch`, `transformers`, `deepspeed`, `flash-attn`, etc.), which require an NVIDIA GPU + CUDA. This project is an upper-layer application of Hy3 and only depends on a web framework and HTTP client. **The two do not conflict.**

### Q: I want to run the Hy3 model locally. What are the pitfalls?

Please read the [Running Hy3 Locally Guide](local-hy3-model_EN.md) thoroughly. Key points:
- `deepspeed` + `flash-attn` are notoriously difficult to install; you must install in the exact order Torch → CUDA → Deepspeed → Flash-Attn with matching versions
- Requires NVIDIA GPU with ≥ 24 GB VRAM + 32 GB system RAM (to compile flash-attn)
- Strongly recommend Docker deployment over manual compilation
- If you use an ordinary laptop (integrated graphics or < 8GB VRAM), give up on local deployment and use this app's cloud API mode

### Q: What if `pip install` fails?

```bash
# 1. Upgrade pip
python -m pip install --upgrade pip

# 2. If you encounter lxml compilation errors on Windows, install the precompiled version:
pip install lxml --only-binary=lxml

# 3. Check Python version
python --version  # must be >= 3.9
```

### Q: The page doesn't open after the service starts?

1. Confirm the terminal shows `Uvicorn running on http://0.0.0.0:8000`
2. Check whether the firewall is blocking port 8000
3. Try `http://127.0.0.1:8000` instead of localhost

### Q: It says "HY3_API_KEY not set"?

```bash
# Temporary (valid only in current terminal)
# Windows CMD:     set HY3_API_KEY=your_key
# Windows PowerShell: $env:HY3_API_KEY="your_key"
# macOS/Linux:     export HY3_API_KEY=your_key

# Or create a .env file for permanent effect
echo HY3_API_KEY=your_key > .env    # Windows
echo "HY3_API_KEY=your_key" > .env  # macOS/Linux
```

### Q: How can I provide Hy3 capabilities to other LLM clients?

Use the built-in MCP Server:

```bash
cd hy3-mcp-server
pip install -e .
# Then configure the hy3-mcp command in Claude Desktop / Cursor
```

See [MCP Server Configuration Guide](mcp-server_EN.md) for details.

### Q: docker-compose error?

Try `docker compose up -d` (without hyphen), which is built into newer Docker versions.
