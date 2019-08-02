FROM continuumio/anaconda3
LABEL Jee Vang, Ph.D. "vangjee@gmail.com"
ARG APYBBN_VERSION
ARG APYPI_REPO
ENV PYBBN_VERSION=$APYBBN_VERSION
ENV PYPI_REPO=$APYPI_REPO
ENV PATH /opt/conda/bin:$PATH
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install build-essential -y
COPY . /py-bbn
RUN conda env create -f /py-bbn/environment-py27.yml \
    && conda env create -f /py-bbn/environment-py37.yml \
    && /py-bbn/publish.sh