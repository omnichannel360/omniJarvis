FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
RUN pip install --no-cache-dir anthropic fastapi uvicorn pydantic pyyaml python-dotenv

COPY . .

ENV PYTHONPATH=/app:$PYTHONPATH

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "-m", "brain.jarvis_brain.app"]
