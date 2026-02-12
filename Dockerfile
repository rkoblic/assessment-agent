FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
COPY src/ src/

RUN pip install --no-cache-dir .

RUN mkdir -p /data

ENV DB_PATH=/data/assessments.db
ENV PORT=8000

EXPOSE 8000

CMD ["sh", "-c", "uvicorn src.server:app --host 0.0.0.0 --port ${PORT}"]
