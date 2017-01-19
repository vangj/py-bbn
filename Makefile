init:
	pip3 install -r requirements.txt

lint:
	python3 -m flake8 ./pybbn

test:
	nosetests -v tests
