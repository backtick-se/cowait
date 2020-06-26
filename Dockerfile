FROM continuumio/miniconda3:latest

# install build tools
RUN mkdir -p /usr/share/man/man1
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    build-essential ca-certificates

# create directory structure
RUN mkdir /var/cowait && mkdir /var/task

# install cowait
WORKDIR /var/cowait
COPY setup.py README.md ./
COPY bin ./bin
RUN pip install -e .

# jupyter mods
COPY cowait/notebook/jupyter/jupyter_config.py /root/.jupyter/jupyter_notebook_config.py
COPY cowait/notebook/jupyter/startup.py /root/.ipython/profile_default/startup/startup.py

# copy code last, to benefit from caching
COPY . . 

# move to task directory
WORKDIR /var/task

ENV PYTHONPATH="/var/task:${PYTHONPATH}"
CMD [ "python3", "-Bum", "cowait.exec" ]