---
title: Testing on Kubernetes
---

## Prerequisites

- Basic Kubernetes knowledge
- A basic understanding of `cowait build` and `cowait push`, see [building and pushing](/docs/get-started/building-and-pushing/)
- Knowledge of `cowait.yml`, see [Configuration](/docs/setup/configuration/)
- A configured kubernetes cluster, see [Cluster Management](/docs/kubernetes/cluster-management/).

## Testing on Kubernetes

To make sure your tasks work in a cluster environment, Cowait provides running tests on Kubernetes via the `--cluster` argument to `cowait test`.

```
cowait test --cluster my_kubernetes
```

Further, you can include the `--push` argument, to build and push your image to Kubernetes before running. This is just a convenience - you could also just do `cowait build` and `cowait push` before running `cowait test`. Either way, you need to make sure that your recent changes are in the image on your docker registry so that Kubernetes picks up the corrent image.
