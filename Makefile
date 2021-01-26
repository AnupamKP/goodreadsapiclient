.PHONY: clean test coverage run install install-dev lint

clean:
	@rm -rf .eggs/ build/ dist/ docs/_build/ htmlcov/ *.egg-info/ .coverage
	@-find . -name '__pycache__' -prune -exec rm -rf "{}" \;
	@-find . -name '*.pyc' -delete
	@echo 'cache cleaned....'

lint:
	@python3 -m black .

test: clean lint
	@python3 -m unittest discover tests/

coverage:
	@python3 -m coverage run -m unittest
	@python3 -m coverage report	

install-dev:
	@python3 -m pip install -r library/requirements-dev.txt

install:
	@python3 -m pip install -r library/requirements.txt

run:
	@cd goodreadsapiclient && python3 cli.py