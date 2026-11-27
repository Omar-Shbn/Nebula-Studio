FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

# Keep the virtualenv outside /app, so mounting your code over /app
# doesn't replace it with your Windows .venv.
ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/opt/venv/bin:$PATH"

# Install dependencies first, so this layer is cached until pyproject/uv.lock change
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
