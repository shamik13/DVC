FROM ubuntu:18.04
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /root


COPY requirements_apt.txt requirements_apt.txt
RUN set -xe \
        && apt update -y \
        && apt install -y --no-install-recommends $(cat requirements_apt.txt) \
        && rm -rf /var/lib/apt/lists/* \
        && rm requirements_apt.txt


RUN set -xe \
        && wget https://dvc.org/deb/dvc.list -O /etc/apt/sources.list.d/dvc.list \
        && apt update -y \
        && apt install dvc


ARG PYTHON_VERSION=3.6.5
ENV PATH /opt/conda/bin:$PATH

COPY requirements_pip.txt requirements_pip.txt
RUN set -xe \
        && curl -o ~/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
        && chmod +x ~/miniconda.sh \
        && ~/miniconda.sh -b -p /opt/conda \
        && rm ~/miniconda.sh \
        && /opt/conda/bin/conda install -y python=$PYTHON_VERSION \
        && pip install --no-cache-dir -r requirements_pip.txt \
        && rm requirements_pip.txt


COPY entrypoint.sh entrypoint.sh
ENTRYPOINT /root/entrypoint.sh
