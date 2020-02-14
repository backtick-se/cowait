FROM continuumio/miniconda3:latest

# install build tools
RUN mkdir -p /usr/share/man/man1
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    build-essential ca-certificates

ENV PYTHONPATH=/app:/app/context:$PYTHONPATH

# create working directory
RUN mkdir -p /app/context
WORKDIR /app

# install python requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy code
COPY . .
RUN pip install .

CMD [ "python", "-u", "main.py" ]
