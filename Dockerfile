FROM python:3.9-slim

LABEL maintainer="ShonNahum"
LABEL description="A Prometheus exporter for API's single buzz_word VALUE monitoring"

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
