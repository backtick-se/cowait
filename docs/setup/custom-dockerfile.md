---
title: Custom Dockerfile
---

Details on docker, configuration and custom images. The default Cowait Dockerfile can be found [here](https://github.com/backtick-se/cowait/blob/master/Dockerfile).

## Overview

To use your own custom docker image, simply add a Dockerfile in the root of your project. `cowait build` will automatically build your task using your own dockerfile.

Example file structure:

```
hello-world
  └── hello.py
  └── Dockerfile
```

## Extending the default Dockerfile

The easiest way to customize the task image is to extend the default task image. This should be sufficient for most use cases, such as installing extra dependencies or adding files.

```Dockerfile
# Dockerfile
FROM cowait/task

RUN echo "Your custom command"
```

## Writing your own Dockerfile

If extending cowait/task is not possible for your use case, you could also create a completely custom docker image. Improvements to this process are planned.

You need to install Cowait in the Dockerfile. In addition there a few things you need to do (you can look at the [default](https://github.com/backtick-se/cowait/blob/master/Dockerfile) Cowait Dockerfile for inspiration):

- Ensure Python 3.6+ is installed
- Install Cowait with `pip`
- Create a directory call `/var/task` and set it as `WORKDIR`
- Set `python -Bum cowait.exec` as entrypoint
