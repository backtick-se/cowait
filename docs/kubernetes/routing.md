---
title: Routing
---

Automated HTTP proxying for tasks

## Using Traefik

Cowait can automatically integrate with a [Traefik](https://traefik.io/traefik/) reverse proxy if it is deployed in your cluster.

- Deploy Traefik to your cluster.
- Point a wildcard subdomain \*.cluster.yourdomain.com to the traefik service

Tasks with route mappings will be available at `task123.cluster.yourdomain.com`
