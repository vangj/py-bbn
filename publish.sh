#!/bin/bash

PY37_WHEEL=/py-bbn/dist/pybbn-${PYBBN_VERSION}-py3-none-any.whl
PY27_WHEEL=/py-bbn/dist/pybbn-${PYBBN_VERSION}-py2-none-any.whl
SOURCE_DIST=/py-bbn/dist/pybbn-${PYBBN_VERSION}.tar.gz

cleanUp() {
  echo "cleaning up"
  cd /py-bbn \
    && make clean
}

buildCode() {
  echo "start the build"
  cd /py-bbn \
    && make clean \
    && make \
    && python setup.py sdist bdist bdist_wheel \
    && twine check dist/* \
    && cd /py-bbn/docs \
    && make html
}

updateVersion() {
  echo "replace version of software to ${PYBBN_VERSION}"
  sed -i "s/version='0.2.3'/version='${PYBBN_VERSION}'/g" /py-bbn/setup.py
}

copyCredentials() {
  if [[ -f /py-bbn/.pypirc ]]; then
    echo "copying over .pypirc"
    cp /py-bbn/.pypirc /root/.pypirc
  fi
}

publish27() {
  echo "python 2.7 publish"

  if [[ -f /root/.pypirc ]]; then
    if [[ -f ${PY27_WHEEL} ]]; then
      echo "uploading py27 wheel"
      twine upload --repository ${PYPI_REPO} ${PY27_WHEEL}
    else
      echo "no ${PY27_WHEEL} found!"
    fi
  else
    echo "no .pypirc found!"
  fi
}

publish37() {
  echo "python 3.7 publish"

  if [[ -f /root/.pypirc ]]; then
    if [[ -f ${PY37_WHEEL} ]]; then
      echo "uploading py37 wheel"
      twine upload --repository ${PYPI_REPO} ${PY37_WHEEL}
    else
      echo "no ${PY37_WHEEL} found!"
    fi

    if [[ -f ${SOURCE_DIST} ]]; then
      echo "uploading source"
      twine upload --repository ${PYPI_REPO} ${SOURCE_DIST}
    else
      echo "no ${SOURCE_DIST} found!"
    fi
  else
    echo "no .pypirc found!"
  fi
}

build27() {
  echo "python 2.7 build"
  conda activate pybbn27
  buildCode
  publish27
}

build37() {
  echo "python 3.7 build"
  conda activate pybbn37
  buildCode
  publish37
}

conda init bash
. /root/.bashrc
updateVersion
copyCredentials
build27
build37
cleanUp

echo "done!"