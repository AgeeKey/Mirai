FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV PYTHONPATH=/app

CMD ["python", "core/master_agent.py"]
