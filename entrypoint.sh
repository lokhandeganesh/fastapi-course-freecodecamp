#!/bin/sh
WORKERS=$(python -c 'import multiprocessing; print((multiprocessing.cpu_count() * 2) + 1)')
exec /app/.venv/bin/gunicorn \
  --workers "$WORKERS" \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  app.main:app
