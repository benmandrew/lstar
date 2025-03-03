.PHONY: examples clean fmt lint ruff pylint

all: examples

examples: | out
	python3 examples.py

out:
	mkdir -p out

clean:
	rm -rf out

fmt:
	python3 -m black -l 80 .

lint: ruff pylint

ruff:
	python3 -m ruff check

pylint:
	find . -name "*.py" -not -path "*/.*" | xargs python3 -m pylint --errors-only
