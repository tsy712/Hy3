# 快速开始指南

> 📖 [返回 README](../README.md)

---

## 零、获取 Hy3 API Key

使用前需要有效的 Hy3 API 密钥。获取方式请参考 [Hy3 官方文档](https://github.com/Tencent-Hunyuan/Hy3)。

## 一、克隆项目

```bash
git clone https://github.com/Tencent-Hunyuan/Hy3.git
cd hy3-research-assistant
```

## 二、配置 API 密钥

### 方式 A：环境变量（推荐）

| 操作系统 | 命令 |
|---------|------|
| Windows (CMD) | `set HY3_API_KEY=你的API密钥` |
| Windows (PowerShell) | `$env:HY3_API_KEY="你的API密钥"` |
| macOS / Linux | `export HY3_API_KEY=你的API密钥` |

### 方式 B：.env 文件（持久化）

```bash
# 复制模板
copy .env.example .env        # Windows CMD
cp .env.example .env          # macOS / Linux

# 用任意文本编辑器打开 .env，填入密钥：
# HY3_API_KEY=你的API密钥
```

## 三、安装与启动

### 方式一：pip 安装（推荐，支持命令行启动）

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

# 服务运行在 http://localhost:8000
```

### 方式二：手动安装（不创建命令行入口）

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

# 服务运行在 http://localhost:8000
```

### 方式三：一键脚本（Windows）

```bash
# 双击 start.bat 或在终端中运行：
.\start.bat
```

安装完成后，打开浏览器访问 `http://localhost:8000` 即可使用。

## 四、验证安装

```bash
# 健康检查
curl http://localhost:8000/health
# 预期输出: {"status":"healthy","hy3_connected":true}

# 或直接浏览器打开 http://localhost:8000/health
```

## 可选环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `HY3_API_KEY` | Hy3 API 密钥（**必填**） | - |
| `HY3_BASE_URL` | API 端点地址 | `https://api.hunyuan.cloud.tencent.com/v1` |
| `HY3_MODEL` | 模型名称 | `hunyuan-pro` |
| `PORT` | 服务端口 | `8000` |
