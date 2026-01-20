FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app /app/app
COPY alembic.ini /app/alembic.ini
EXPOSE 8000

CMD ["sh", "-c", "alembic -c /app/alembic.ini upgrade head && python -m app.db.cli seed && uvicorn app.main:app --host 0.0.0.0 --port 8000"]