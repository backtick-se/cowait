---
title: Pushing & running
---

How to push tasks to your registry so that they can later be run on Kubernetes.

## Pushing

Before you can run anything on kubernetes, your task image must be pushed to a docker registry that can be accessed from the cluster. To push the image to a repository, you must define the image name in `cowait.yml`.

```
my-project/
  ├── cowait.yml
  ├── hello.py
  ├── requirements.txt
  └── sleep.py
```

```yml:title=cowait.yml
version: 1
cowait:
  image: your-repo/task-image-name
```

1. Build your tasks into your image

```shell
cowait build
```

2. Make sure you're authenticated to your registry.

```shell
docker login
```

3. Push the image

This will push the image to registry you defined in your `cowait.yml`

```shell
cowait push
```

## Configuring Pull Secrets

If your repository is not publicly available, you must create a kubernetes secret containing the authentication information. See the [kubernetes documentation](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/).

Once you have created a secret, configure the kubernetes provider to use it for pulling images:

```yml:title=cowait.yml
version: 1
cowait:
  kubernetes:
    pull_secrets:
      - your_secret_name
```

## Running

You should now be ready to run your task on the your cluster. To use the kubernetes task provider, simply use the `--provider` option to `cowait run` as follows. You may pass inputs and other options as you would normally.

```shell
cowait run your_task --provider kubernetes
```
