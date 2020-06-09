FROM cowait/task

RUN apt-get update && apt-get install -y wget default-jre-headless

# hopefully always true on debian stretch
ENV JAVA_HOME=/usr/lib/jvm/default-java

# install spark
ENV SPARK_VERSION=3.0.0-preview2
ENV HADOOP_VERSION=3.2
ENV PY4J_VERSION=0.10.8.1

RUN wget \
        -O spark.tgz https://www-eu.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
        --progress=dot:giga && \
    tar -xzf spark.tgz -C /

ENV SPARK_HOME=/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}
ENV PATH=$SPARK_HOME/python:$PATH:$SPARK_HOME/bin
ENV PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-${PY4J_VERSION}-src.zip:$PYTHONPATH
COPY spark-defaults.conf /spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/conf
