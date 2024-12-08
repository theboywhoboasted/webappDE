# Global Variables
PROJECT_TAG = webapp/deutsch

install:
	pip install --quiet --root-user-action=ignore black pylint ruff
	docker build --quiet --tag=$(PROJECT_TAG) .

format:
	black src/*.py

lint:
	PYTHONPATH=src pylint src/ --disable=R,C
	ruff check src/
	docker run --rm -i hadolint/hadolint < Dockerfile
	
all: install lint format
