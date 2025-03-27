FROM python:3.12.9-bullseye
WORKDIR /app
ENV PYTHONPATH=/app

COPY requirements.txt .
COPY . .

RUN python -m pip install -r requirements.txt
