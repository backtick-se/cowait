FROM continuumio/miniconda3:latest

# install build tools
RUN mkdir -p /usr/share/man/man1
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    build-essential ca-certificates

# create working directory
RUN mkdir -p /app/context
WORKDIR /app

# install python requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy minimum set of files to install pip package
COPY setup.py README.md ./
COPY bin /app/bin
RUN pip install -e .

# copy code
COPY . .

WORKDIR /app/context
CMD [ "cowait", "exec" ]
