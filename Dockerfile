FROM python:3.11-slim

LABEL maintainer="hy3-research-assistant"
LABEL description="Hy3 Research Assistant - 基于腾讯混元 Hy3 的智能研究助手"

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY pyproject.toml .
COPY backend/requirements.txt backend/

# 安装 Python 依赖
RUN pip install --upgrade pip \
    && pip install -r backend/requirements.txt \
    && pip install -e .

# 复制项目文件
COPY .env.example .env
COPY backend/ backend/
COPY frontend/ frontend/
COPY README.md .

# 创建上传文件目录
RUN mkdir -p /app/uploads

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 启动命令
CMD ["python", "-m", "backend.main"]
