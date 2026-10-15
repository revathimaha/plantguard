FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY pyproject.toml README.md ./
COPY src/ ./src/

RUN pip install --no-deps .

EXPOSE 8000

CMD ["uvicorn", "src.plantguard.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
