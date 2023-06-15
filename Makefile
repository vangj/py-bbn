.PHONY: init clean lint test build build-dist install publish compile docker-test docker-test-inspect
.DEFAULT_GOAL := build

CLEAN_OP :=
ifeq ($(OS),Windows_NT)
	CLEAN_OP += clean-win
else
	CLEAN_OP += clean-nix
endif

init:
	pip install -r requirements.txt

lint:
	python -m flake8 ./pybbn

test:
	nose2

build:
	python setup.py bdist_egg sdist bdist_wheel

install: build
	python setup.py install

publish: build
	python setup.py sdist upload -r pypi

compile:
	python -m compileall -f ./pybbn

clean: $(CLEAN_OP)

clean-nix:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -fr coverage/
	rm -fr dist/
	rm -fr build/
	rm -fr pybbn.egg-info/
	rm -fr pybbn/pybbn.egg-info/
	rm -fr jupyter/.ipynb_checkpoints/
	rm -fr joblib_memmap/
	rm -fr docs/build/
	rm -fr .pytest_cache/
	rm -f .coverage
	rm -f .noseids

clean-win:
	del /S *.pyc
	if exist coverage rmdir /S /Q coverage
	if exist dist rmdir /S /Q dist
	if exist build rmdir /S /Q build
	if exist pybbn.egg-info rmdir /S /Q pybbn.egg-info
	if exist pybbn/pybbn.egg-info rmdir /S /Q pybbn/pybbn.egg-info
	if exist jupyter/.ipynb_checkpoints rmdir /S /Q jupyter/.ipynb_checkpoints
	if exist docs/build rmdir /S /Q docs/build
	if exist joblib_memmap rmdir /S /Q joblib_memmap
	if exist .pytest_cache rmdir /S /Q .pytest_cache
	del .coverage
	del .noseids

docker-test:
	docker build -t pybbn-test:local -f Dockerfile.test .

docker-test-inspect:
	docker run --rm -it pybbn-test:local /bin/bash
