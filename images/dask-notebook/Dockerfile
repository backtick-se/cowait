FROM daskdev/dask-notebook

USER root

RUN apt-get update && apt-get install -y build-essential

RUN pip install fastparquet git+https://github.com/dask/distributed dask_kubernetes

COPY --chown=1000:100 cluster.py cluster.ipynb /home/$NB_USER/
#ENV DASK_KUBERNETES__WORKER_TEMPLATE_PATH=/home/$NB_USER/worker-spec.yml

USER $NB_USER

CMD ["start.sh", "jupyter", "lab", "/home/jovyan/cluster.ipynb"]