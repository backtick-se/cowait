---
title: Dependency management
---

## Adding dependencies

Cowait can automatically install Python dependencies as part of the build step. Adding a `requirements.txt` in your project root folder installs the requirements during `cowait build`.

1. Add a `requirements.txt` to the root of your project

```
my-project/
  ├── cowait.yml
  ├── hello.py
  ├── parallel.py
  ├── requirements.txt
  └── sleep.py
```

2. Populate it

```
pandas==1.2.4
```

3. Build

```shell
cowait build
```

Cowait will identify the `requirements.txt` file and install dependencies in the build step using `pip install`. During local development, Cowait mounts your directory into the container. However, adding new dependencies requires you to build your image using `cowait build`.
