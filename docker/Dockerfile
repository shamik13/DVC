# https://hub.docker.com/r/wkentaro/labelme/dockerfile

FROM ubuntu:18.04
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /root


COPY requirements_apt.txt requirements_apt.txt
RUN set -xe \
        && apt update -y \
        && apt install -y --no-install-recommends $(cat requirements_apt.txt) \
        && rm -rf /var/lib/apt/lists/* \
        && rm requirements_apt.txt


# https://dvc.org/doc/install/linux#install-from-repository
RUN set -xe \
        && wget https://dvc.org/deb/dvc.list -O /etc/apt/sources.list.d/dvc.list \
        && apt update -y \
        && apt install dvc


ARG PYTHON_VERSION=3.6.5
ENV PYTHONPATH /app/github_actions/DVC:$PYTHONPATH

COPY requirements_pip.txt requirements_pip.txt
RUN set -xe \
        && python3 -m pip install -U pip setuptools wheel \
        && python3 -m pip install -U -r requirements_pip.txt \
        && rm requirements_pip.txt


COPY entrypoint.sh entrypoint.sh
ENTRYPOINT /root/entrypoint.sh
