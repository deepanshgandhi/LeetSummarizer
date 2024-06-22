FROM nvidia/cuda:12.1.0-devel-ubuntu20.04

WORKDIR /app

# install python
RUN apt-get update
RUN apt-get install -y curl git software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install -y python3.10 python3.10-venv python3.10-dev
RUN ls -la /usr/bin/python3
RUN rm /usr/bin/python3
RUN ln -s python3.10 /usr/bin/python3
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
RUN apt-get install -y python3-pip python-is-python3

COPY 