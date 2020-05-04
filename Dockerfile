FROM continuumio/miniconda3:latest

# install build tools
RUN mkdir -p /usr/share/man/man1
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    build-essential ca-certificates

# create working directory
RUN mkdir /var/cowait && mkdir /var/task
WORKDIR /var/cowait

# install python requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy minimum set of files to install pip package
COPY setup.py README.md ./
COPY bin ./bin
RUN pip install -e .

# copy code
COPY . .

WORKDIR /var/task
CMD [ "python3", "-um", "cowait.exec" ]
