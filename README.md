## Build docker image

Inside the `./docker` directory:

```bash
docker build -t my/cf-python:3.8-venv -f Dockerfile.python
```


## Run docker container

```bash
docker run --rm -it --net=host -v /dev:/dev -v $(pwd)/examples:/examples --privileged --name cf-test my/cf-python:3.8-venv
```
