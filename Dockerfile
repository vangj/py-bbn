FROM oneoffcoder/python-java:latest

LABEL author="Jee Vang, Ph.D."
LABEL email="vangjee@gmail.com"

ARG APYBBN_VERSION
ARG APYPI_REPO

ENV PYBBN_VERSION=$APYBBN_VERSION
ENV PYPI_REPO=$APYPI_REPO

RUN apt-get update \
    && apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install graphviz libgraphviz-dev -y
COPY . /py-bbn
RUN pip install -r /py-bbn/requirements.txt
RUN /py-bbn/publish.sh