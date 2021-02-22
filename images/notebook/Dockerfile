FROM cowait/task

ADD requirements.txt /tmp/notebook-requirements.txt
RUN pip install -r /tmp/notebook-requirements.txt

# jupyter mods
COPY jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py
COPY kernel /usr/share/jupyter/kernels/cowait
