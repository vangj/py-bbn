.PHONY: init clean lint test
.DEFAULT_GOAL := build

init:
	pip install -r requirements.txt

lint:
	python -m flake8 ./pybbn

test: clean lint
	nosetests tests

build: test
	python setup.py bdist_egg

install: build
	python setup.py install

publish: build
	python setup.py sdist upload -r pypi

clean:
	find . -type f -name '*.pyc' -delete
	rm -fr coverage/
	rm -fr dist/
	rm -fr build/
	rm -fr pybbn.egg-info/
	rm -fr pybbn/pybbn.egg-info
	rm -fr jupyter/.ipynb_checkpoints
	rm -f .coverage
	rm -f .noseids

