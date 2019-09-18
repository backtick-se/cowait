FROM python:3.7-slim
RUN mkdir /app
WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
    build-essential 

COPY . .
RUN pip install .

WORKDIR /app/task_image