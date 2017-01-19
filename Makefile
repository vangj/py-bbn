.PHONY: init clean lint test
.DEFAULT_GOAL := test

init:
	pip3 install -r requirements.txt

lint:
	python3 -m flake8 ./pybbn

test: clean lint
	nosetests --with-coverage --cover-erase --cover-html --cover-html-dir=coverage -v tests

clean:
	find . -type f -name '*.pyc' -delete
