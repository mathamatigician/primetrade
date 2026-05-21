FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt README.md ./
COPY bot ./bot
COPY tests ./tests

RUN pip install --no-cache-dir -r requirements.txt

RUN useradd --create-home --shell /usr/sbin/nologin appuser \
    && mkdir -p /app/logs \
    && chown -R appuser:appuser /app

USER appuser

ENTRYPOINT ["python", "-m", "bot.cli"]
CMD ["--help"]
