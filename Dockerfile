FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY src ./src

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && pip install -q "uv>=0.12.12,<0.13.0" \
    && UV_HTTP_TIMEOUT=180 UV_HTTP_RETRIES=5 uv sync --frozen

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "uv run python manage.py migrate && uv run python manage.py seed_demo && uv run python manage.py runserver 0.0.0.0:8000"]