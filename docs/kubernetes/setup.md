---
title: Setup
---

## Permissions

Task pods must be able to manage the cluster in order to schedule other tasks. Currently, tasks are deployed in the default namespace and use the default service account.

### Basic

The most basic set of permissions allow tasks to create, list and destroy pods. This allows tasks to schedule other tasks on the cluster. This should be sufficient if you do not wish to use any automated routing features.

```yml
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: task-basic-permissions
rules:
  - apiGroups: [""]
    resources: ["pods", "pods/log"]
    verbs: ["get", "create", "list", "delete", "deletecollection"]
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: default-sa-task-permissions
subjects:
  - kind: ServiceAccount
    name: default
    namespace: default
roleRef:
  kind: ClusterRole
  name: task-basic-permissions
  apiGroup: rbac.authorization.k8s.io
```

### Extended

If you wish to use routing features, your task pods also need permissions to create, list and destroy ingresses and services.
Apply the [default configuration](https://raw.githubusercontent.com/backtick-se/cowait/master/k8setup.yml) with:

```shell
kubectl apply -f https://raw.githubusercontent.com/backtick-se/cowait/master/k8setup.yml
```

## Repository Secrets

If you would like to pull images from a private repository, you must create a [Kubernetes secret](https://kubernetes.io/docs/concepts/configuration/secret/) containing the repository credentials.
