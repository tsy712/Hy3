# Quick Start Guide

<p align="center">
  <a href="quick-start.md">🇨🇳 中文</a> · <strong>🇺🇸 English</strong> · <a href="../README_EN.md">⬅ Back to README</a>
</p>

---

## 0. Get a Hy3 API Key

Before use, you need a valid Hy3 API key. Please refer to the [Hy3 official documentation](https://github.com/Tencent-Hunyuan/Hy3) for how to obtain one.

## 1. Clone the Project

```bash
git clone https://github.com/Tencent-Hunyuan/Hy3.git
cd hy3-research-assistant
```

## 2. Configure the API Key

### Option A: Environment Variables (Recommended)

| OS | Command |
|----|---------|
| Windows (CMD) | `set HY3_API_KEY=your_api_key` |
| Windows (PowerShell) | `$env:HY3_API_KEY="your_api_key"` |
| macOS / Linux | `export HY3_API_KEY=your_api_key` |

### Option B: `.env` File (Persistent)

```bash
# Copy the template
copy .env.example .env        # Windows CMD
cp .env.example .env          # macOS / Linux

# Open .env in any text editor and fill in the key:
# HY3_API_KEY=your_api_key
```

## 3. Install and Start

### Method 1: pip Install (Recommended, supports CLI launch)

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

# Service runs at http://localhost:8000
```

### Method 2: Manual Install (no CLI entry point)

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

# Service runs at http://localhost:8000
```

### Method 3: One-Click Script (Windows)

```bash
# Double-click start.bat or run in terminal:
.\start.bat
```

After installation, open `http://localhost:8000` in your browser.

## 4. Verify Installation

```bash
# Health check
curl http://localhost:8000/health
# Expected output: {"status":"healthy","hy3_connected":true}

# Or open http://localhost:8000/health directly in your browser
```

## Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HY3_API_KEY` | Hy3 API key (**required**) | - |
| `HY3_BASE_URL` | API endpoint | `https://api.hunyuan.cloud.tencent.com/v1` |
| `HY3_MODEL` | Model name | `hunyuan-pro` |
| `PORT` | Service port | `8000` |
