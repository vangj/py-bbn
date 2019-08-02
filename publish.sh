#!/bin/bash

PY37_WHEEL=/py-bbn/dist/pybbn-${PYBBN_VERSION}-py3-none-any.whl
PY27_WHEEL=/py-bbn/dist/pybbn-${PYBBN_VERSION}-py2-none-any.whl
SOURCE_DIST=/py-bbn/dist/pybbn-${PYBBN_VERSION}.tar.gz

if [[ -f /py-bbn/.pypirc ]]; then
    cp /py-bbn/.pypirc /root/.pypirc
fi

if [[ -f /root/.pypirc ]]; then
    if [[ -f ${PY37_WHEEL} ]]; then
        echo "uploading py37 wheel"
        twine upload --repository ${PYPI_REPO} ${PY37_WHEEL}
    fi

    if [[ "py37" == ${PY_VERSION} ]]; then
        echo "uploading source"
        twine upload --repository ${PYPI_REPO} ${SOURCE_DIST}
    fi

    if [[ -f ${PY27_WHEEL} ]]; then
        echo "uploading py27 wheel"
        twine upload --repository ${PYPI_REPO} ${PY27_WHEEL}
    fi
fi