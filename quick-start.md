# Quick Start Guide / 快速开始指南

> 📖 [Back to README / 返回 README](../README.md)

---

## 0. Get a Hy3 API Key / 获取 Hy3 API Key

You need a valid Hy3 API key. See [Hy3 Official Docs](https://github.com/Tencent-Hunyuan/Hy3) for instructions.  
使用前需要有效的 Hy3 API 密钥。获取方式请参考 [Hy3 官方文档](https://github.com/Tencent-Hunyuan/Hy3)。

## 1. Clone the Repo / 克隆项目

```bash
git clone https://github.com/Tencent-Hunyuan/Hy3.git
cd hy3-research-assistant
```

## 2. Configure API Key / 配置 API 密钥

### Method A: Environment Variables (Recommended) / 方式 A：环境变量（推荐）

| OS / 操作系统 | Command / 命令 |
|---------|------|
| Windows (CMD) | `set HY3_API_KEY=your-api-key` / `set HY3_API_KEY=你的API密钥` |
| Windows (PowerShell) | `$env:HY3_API_KEY="your-api-key"` / `$env:HY3_API_KEY="你的API密钥"` |
| macOS / Linux | `export HY3_API_KEY=your-api-key` / `export HY3_API_KEY=你的API密钥` |

### Method B: .env File (Persistent) / 方式 B：.env 文件（持久化）

```bash
# Copy template / 复制模板
copy .env.example .env        # Windows CMD
cp .env.example .env          # macOS / Linux

# Open .env in any text editor, fill in your key: / 用任意文本编辑器打开 .env，填入密钥：
# HY3_API_KEY=your-api-key / HY3_API_KEY=你的API密钥
```

## 3. Install & Launch / 安装与启动

### Method 1: pip Install (Recommended, with CLI entry) / 方式一：pip 安装（推荐，支持命令行启动）

```bash
# === Windows (PowerShell) ===
python -m venv venv
.\venv\Scripts\activate
pip install -e .
hy3-research

# === macOS / Linux ===
python3 -m venv venv
source venv/bin/activate
pip install -e .
hy3-research

# Server runs at http://localhost:8000 / 服务运行在 http://localhost:8000
```

### Method 2: Manual Install (no CLI entry) / 方式二：手动安装（不创建命令行入口）

```bash
# === Windows (PowerShell) ===
python -m venv venv
.\venv\Scripts\activate
cd backend
pip install -r requirements.txt
python main.py

# === macOS / Linux ===
python3 -m venv venv
source venv/bin/activate
cd backend
pip install -r requirements.txt
python main.py

# Server runs at http://localhost:8000 / 服务运行在 http://localhost:8000
```

### Method 3: One-Click Script (Windows) / 方式三：一键脚本（Windows）

```bash
# Double-click start.bat or run in terminal: / 双击 start.bat 或在终端中运行：
.\start.bat
```

After installation, open your browser to `http://localhost:8000` to use the app.  
安装完成后，打开浏览器访问 `http://localhost:8000` 即可使用。

## 4. Verify Installation / 验证安装

```bash
# Health check / 健康检查
curl http://localhost:8000/health
# Expected output / 预期输出: {"status":"healthy","hy3_connected":true}

# Or open http://localhost:8000/health in browser / 或直接浏览器打开 http://localhost:8000/health
```

## Optional Environment Variables / 可选环境变量

| Variable / 变量名 | Description / 说明 | Default / 默认值 |
|--------|------|--------|
| `HY3_API_KEY` | Hy3 API key (**required**) / Hy3 API 密钥（**必填**） | - |
| `HY3_BASE_URL` | API endpoint / API 端点地址 | `https://api.hunyuan.cloud.tencent.com/v1` |
| `HY3_MODEL` | Model name / 模型名称 | `hunyuan-pro` |
| `PORT` | Server port / 服务端口 | `8000` |
