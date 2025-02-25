.PHONY: fmt lint

all: fmt lint

fmt:
	python3 -m black -l 80 .

lint:
	python3 -m ruff check
