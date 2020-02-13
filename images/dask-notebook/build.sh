IMAGE=docker.backtick.se/dask-notebook
docker build -t $IMAGE .
docker push $IMAGE
