.PHONY: help docs
.DEFAULT_GOAL := help

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

lint: ## Run code linters
	isort --check apirouter tests
	black --check apirouter tests
	flake8 apirouter tests
	mypy apirouter tests
	safety check --full-report

fmt format: ## Run code formatters
	isort apirouter tests
	black apirouter tests

requirements:  ## Make requirements
	poetry export -f requirements.txt -E docs > requirements.docs.txt