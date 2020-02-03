FROM python:3.7.5-slim-stretch

# install build tools, wget, java
RUN mkdir -p /usr/share/man/man1
RUN apt-get update && \
    apt-get upgrade && \
    apt-get install -y \
    build-essential wget ca-certificates

# get java 8. sigh.
RUN apt-get install -y openjdk-8-jre-headless

# hopefully always true on debian stretch
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

# install spark
ENV SPARK_VERSION=3.0.0-preview2
ENV HADOOP_VERSION=3.2
ENV PY4J_VERSION=0.10.8.1

RUN wget -O spark.tgz https://www-eu.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
        tar -xzf spark.tgz -C /

ENV SPARK_HOME=/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}
ENV PATH=$SPARK_HOME/python:$PATH:$SPARK_HOME/bin
ENV PYTHONPATH=/app:$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-${PY4J_VERSION}-src.zip:$PYTHONPATH
COPY spark-defaults.conf /spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/conf

# create working directory
RUN mkdir /app
WORKDIR /app

# install python requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy code
COPY . .
RUN pip install .

CMD [ "python", "-u", "main.py" ]
