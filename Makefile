PYTHON ?= python3

.PHONY: validate test

validate:
	$(PYTHON) scripts/validate_repository.py
	$(PYTHON) -m unittest discover -s tests -v

test: validate
