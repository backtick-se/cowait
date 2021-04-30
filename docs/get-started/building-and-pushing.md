---
title: Building and pushing
---

## Overview

Cowait comes with sensible defaults, but allows you to easily configure certain aspects of your environments, such as docker image names, kubernetes clusters and more.

Cowait uses a concept called Task Context, which is achieved through a simple `cowait.yml` file added to the root of your project.

## Task Context

A task context is defined as a directory containing a `cowait.yml` file. This directory will act as the root of a project. Everything in this folder is copied into the resulting docker image during the build step. If you have not created a `cowait.yml` file, the current working directory (when exectuing `cowait build`) will be used.

Example:

```
/my_project
  └── cowait.yml
  └── hello.py
  └── parallel.py
  └── sleep.py
```

In this case, `my_project` will be the context directory.

## Cowait.yml

In a scenario when you want to run your task(s) on a remote machine or cluster, Cowait provides `cowait build` to package your code into a Docker image and `cowait push` to distribute it to docker registries.

To do this, you simply provide your docker image name (and registry) in `cowait.yml`:

```yml
version: 1
cowait:
  image: docker.io/username/cowait-task
```

Now, if you run

```shell
cowait build
cowait push
```

Cowait will build your image and push it to the registry. You can use the shorthand `--push` to `cowait build` to push it after building completes:

```shell
cowait build --push
```
