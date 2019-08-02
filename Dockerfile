FROM continuumio/anaconda3
LABEL Jee Vang, Ph.D. "vangjee@gmail.com"
# environment variables
ENV PATH /opt/conda/bin:$PATH
ENV PYBBN_VERSION 0.2.3
ENV PYPI_REPO testpypi
# arguments
ARG PYBBN_VERSION
ARG PYPI_REPO
# do the build
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install build-essential -y
COPY . /py-bbn
RUN conda env create -f /py-bbn/environment-py27.yml \
    && conda env create -f /py-bbn/environment-py37.yml \
    && /py-bbn/publish.sh