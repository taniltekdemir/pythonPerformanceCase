FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y netcat-openbsd postgresql-client && rm -rf /var/lib/apt/lists/*

COPY sleep_for_docker.sh /app/sleep_for_docker.sh
RUN chmod +x /app/sleep_for_docker.sh

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

CMD ["bash", "-c", "./sleep_for_docker.sh && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
