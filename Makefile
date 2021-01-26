.PHONY: clean test coverage run install install-dev

clean:
	rm -rf .eggs/ build/ dist/ docs/_build/ htmlcov/ *.egg-info/ .coverage
	-find . -name '__pycache__' -prune -exec rm -rf "{}" \;
	-find . -name '*.pyc' -delete

lint:
	python -m black .

test:
	clean
	lint
	python -m unittest discover tests/

coverage:
	python -m coverage run -m unittest
	python -m coverage html	

install-dev:
	python -m pip install -r library/requirements-dev.txt

install:
	python -m pip install -r library/requirements.txt

run:
	python goodreadsapiclient/cli.py