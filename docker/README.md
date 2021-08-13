# Dockerfiles for running crazyflies

## For the pure python image

```bash
docker build -t my/cf-python:3.8-venv -f docker/Dockerfile.python .
```

Run a container with the following command.

```bash
docker run --rm -it --net=host -v /dev:/dev -v $(pwd)/examples:/examples --privileged my/cf-python:3.8-venv
```
