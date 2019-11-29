FROM python:3.7-slim
RUN mkdir /app
WORKDIR /app
ENV PYTHONPATH=/app

# install build tools, wget
RUN apt-get update && \
    apt-get upgrade && \
    apt-get install -y \
    build-essential wget

# java depenency workaround from stackoverflow:
RUN mkdir -p /usr/share/man/man1

# install java
RUN apt-get install -y ca-certificates openjdk-11-jre-headless
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# install spark
RUN wget https://www-eu.apache.org/dist/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz && \
        tar -xzf spark-2.4.4-bin-hadoop2.7.tgz 

ENV SPARK_HOME=/app/spark-2.4.4-bin-hadoop2.7
ENV PATH=$PATH:/app/spark-2.4.4-bin-hadoop2.7/bin
ENV PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.7-src.zip:$PYTHONPATH
ENV PATH=$SPARK_HOME/python:$PATH

# install python requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# unused...
RUN apt-get install -y procps

# copy code
COPY . .
RUN pip install .

CMD [ "python", "-u", "main.py" ]