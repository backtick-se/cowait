FROM python:3.7-slim
RUN mkdir /app
WORKDIR /app
ENV PYTHONPATH=/app

RUN apt-get update && \
    apt-get install -y \
    build-essential 

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install .

CMD [ "python", "-u", "main.py" ]