FROM debian:buster-slim

ARG CONDA_VERSION=py37_4.9.2

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# directory structure & dependencies
RUN mkdir -p /usr/share/man/man1 && \
    mkdir -p /var/cowait/cowait && \
    mkdir /var/task && \
    apt-get update -q && \
    apt-get install -q -y \
        bzip2 \
        build-essential \
        ca-certificates \
        git \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender1 \
        mercurial \
        subversion \
        wget \
    && apt-get clean

ENV PATH /opt/conda/bin:$PATH
ENV PYTHONPATH /var/task:$PYTHONPATH

# install conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-${CONDA_VERSION}-Linux-x86_64.sh -O miniconda.sh && \
    mkdir -p /opt && \
    sh miniconda.sh -b -p /opt/conda && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
    /opt/conda/bin/conda clean -afy

# install cowait
WORKDIR /var/cowait
COPY setup.py README.md ./
COPY cowait/version.py cowait
RUN pip install -e . --use-feature=2020-resolver

# jupyter mods
COPY notebook/jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py
COPY notebook/kernel /usr/share/jupyter/kernels/cowait

# copy code last, to benefit from caching
COPY . . 

# move to task directory
WORKDIR /var/task

CMD [ "python3", "-Bum", "cowait.worker" ]
