# 常见问题 (FAQ)

> 📖 [返回 README](../README.md)

---

### Q: 需要 GPU 吗？需要安装 CUDA 吗？

**不需要。** 本项目所有 AI 能力通过云端 API 调用实现，本地仅运行轻量级 Web 服务器。一台普通笔记本即可运行。

### Q: 和 Hy3 官方仓库的 requirements.txt 有何区别？

Hy3 官方仓库包含模型训练/微调依赖（`torch`、`transformers`、`deepspeed`、`flash-attn` 等），需要 NVIDIA GPU + CUDA。本项目是 Hy3 的上层应用，只依赖 Web 框架和 HTTP 客户端，**两者互不冲突**。

### Q: 我想本地运行 Hy3 模型，有什么坑？

请完整阅读 [本地运行 Hy3 模型指南](local-hy3-model.md)。核心要点：
- `deepspeed` + `flash-attn` 安装极其容易失败，必须按 Torch→CUDA→Deepspeed→Flash-Attn 的顺序精确匹配版本
- 需要 NVIDIA GPU ≥ 24 GB 显存 + 32 GB 系统内存（编译 flash-attn）
- 强烈建议用 Docker 部署而非手动编译
- 如果你用的是普通笔记本（集成显卡或 < 8GB 显存），请放弃本地运行，使用本应用的云端 API 模式即可

### Q: pip install 报错怎么办？

```bash
# 1. 升级 pip
python -m pip install --upgrade pip

# 2. 如果在 Windows 上遇到 lxml 编译错误，安装预编译版：
pip install lxml --only-binary=lxml

# 3. 检查 Python 版本
python --version  # 需要 >= 3.9
```

### Q: 服务启动后页面打不开？

1. 确认终端显示 `Uvicorn running on http://0.0.0.0:8000`
2. 检查防火墙是否拦截端口 8000
3. 尝试 `http://127.0.0.1:8000`（而非 localhost）

### Q: 提示 "未设置 HY3_API_KEY"？

```bash
# 临时设置（仅当前终端有效）
# Windows CMD:     set HY3_API_KEY=你的密钥
# Windows PowerShell: $env:HY3_API_KEY="你的密钥"
# macOS/Linux:     export HY3_API_KEY=你的密钥

# 或创建 .env 文件永久生效
echo HY3_API_KEY=你的密钥 > .env    # Windows
echo "HY3_API_KEY=你的密钥" > .env  # macOS/Linux
```

### Q: 如何为其他 LLM 客户端提供 Hy3 能力？

使用项目自带的 MCP Server：

```bash
cd hy3-mcp-server
pip install -e .
# 然后在 Claude Desktop / Cursor 中配置 hy3-mcp 命令
```

详见 [MCP Server 配置指南](mcp-server.md)。

### Q: docker-compose 报错？

试 `docker compose up -d`（无横杠），新版 Docker 内置。
