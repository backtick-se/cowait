FROM python:3.7-slim

# directory structure
RUN mkdir -p /usr/share/man/man1 && \
    mkdir -p /var/cowait/cowait && \
    mkdir /var/task

# install cowait
COPY setup.py README.md pytest.ini /var/cowait/
COPY cowait/version.py /var/cowait/cowait/
RUN pip install -e /var/cowait --use-feature=2020-resolver --no-cache-dir

# copy code last, to benefit from caching
COPY test /var/cowait/test/
COPY cowait /var/cowait/cowait/

# move to task directory
WORKDIR /var/task

CMD [ "python3", "-Bum", "cowait.worker" ]
