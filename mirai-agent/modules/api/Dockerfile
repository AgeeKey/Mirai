FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV PYTHONPATH=/app

CMD ["uvicorn", "modules.api.mirai_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
