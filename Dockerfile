FROM python:3.7.5-slim-stretch

# install build tools, wget, java
RUN mkdir -p /usr/share/man/man1
RUN apt-get update && \
    apt-get upgrade && \
    apt-get install -y \
    build-essential wget ca-certificates

# get java 8. sigh.
RUN apt-get install -y openjdk-8-jre-headless

# hopefully always true on debian buster
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

# install spark
RUN wget -O spark.tgz https://www-eu.apache.org/dist/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz && \
        tar -xzf spark.tgz -C /

ENV SPARK_HOME=/spark-2.4.4-bin-hadoop2.7
ENV PATH=$SPARK_HOME/python:$PATH:$SPARK_HOME/bin
ENV PYTHONPATH=/app:$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.7-src.zip:$PYTHONPATH
COPY spark-defaults.conf /spark-2.4.4-bin-hadoop2.7/conf

RUN mkdir /app
WORKDIR /app

# install python requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy code
COPY . .
RUN pip install .

CMD [ "python", "-u", "main.py" ]