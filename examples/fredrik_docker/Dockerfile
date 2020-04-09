FROM backtickse/task-examples

# upgrade pip
RUN pip install --upgrade pip

# install libraries
RUN pip install spacy lemmy

# download spacy model
RUN python -m spacy download en_core_web_sm