# Guide to Publishing to the Smithery Platform

<p align="center">
  <a href="PUBLISH.md">🇨🇳 中文</a> · <strong>🇺🇸 English</strong>
</p>

## Prerequisites

### 1. Install Node.js (if not installed)

Download and install the LTS version from https://nodejs.org/.

### 2. Install the mcpb CLI Tool

```bash
npm install -g @anthropic-ai/mcpb
```

### 3. Install the Smithery CLI

```bash
npm install -g @smithery/cli
```

### 4. Log in to Smithery

```bash
smithery mcp publish --help   # If login is required, run smithery auth
```

## Packaging

```bash
cd hy3-mcp-server

# Repackage (required after code changes)
mcpb pack . server.mcpb
```

> This command reads `manifest.json` and packages the project into `server.mcpb`.
> Files/directories listed in `.mcpbignore` will not be packaged.
> Packaging excludes `*.mcpb` files themselves (exclusion rule in `.mcpbignore`).

## Publishing to Smithery

```bash
# Publish to your Smithery account
smithery mcp publish ./server.mcpb -n your_username/hy3-mcp-server

# Example:
smithery mcp publish ./server.mcpb -n tanchengyi/hy3-mcp-server
```

## Set to Public in the Smithery Web UI

1. Go to https://smithery.ai and log in
2. Enter your Server management page
3. Find `hy3-mcp-server`
4. Change visibility from **Unlisted** to **Public**
5. Go to **Settings → Verification** and complete the official verification checklist to obtain the "Verified" badge

## Verify After Packaging

```bash
# View .mcpb package contents
mcpb info ./server.mcpb
```

## Current Packaging Result

```
📦 hy3-mcp-server@1.0.0
   Package: server.mcpb (17 KB)
   Files: 10
   Ignored: 20 (.mcpbignore rules)

Archive Contents:
  ✅ launcher.py      — Cross-platform self-starting script (auto venv + dependency install)
  ✅ manifest.json     — mcpb manifest (binary type)
  ✅ pyproject.toml    — Python project configuration
  ✅ requirements.txt  — Python dependencies
  ✅ run.bat           — Windows backup startup script
  ✅ run.sh            — Linux/macOS backup startup script
  ✅ smithery.yaml     — Smithery platform configuration reference
  ✅ src/server.py     — MCP Server main program (FastMCP, 5 Tools)
  ✅ src/hy3_client.py — Hy3 API client
  ✅ src/__init__.py   — Package marker

Excluded (.mcpbignore):
  ❌ README.md, PUBLISH.md, setup.bat, setup.sh
  ❌ demo/, configs/, tests/
  ❌ __pycache__, *.pyc, .env, .env.local
```

## Configuration Files Explained

| File | Purpose |
|------|---------|
| `manifest.json` | mcpb packaging manifest (v0.3), binary type, launcher.py self-starting |
| `.mcpbignore` | Exclusion rules (includes `*.mcpb` to prevent recursive packaging) |
| `smithery.yaml` | Smithery platform configuration reference, describes connection mode and parameters |
| `launcher.py` | Cross-platform self-starting script, automatically creates venv + pip install dependencies on first run |
| `run.bat` / `run.sh` | Platform-specific backup startup scripts |
| `PUBLISH.md` | This guide |
