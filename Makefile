.PHONY: help docs
.DEFAULT_GOAL := help

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

lint: ## Run code linters
	black --check apirouter tests
	isort --check apirouter tests
	flake8 apirouter tests
	mypy apirouter

fmt format: ## Run code formatters
	isort apirouter tests
	black apirouter tests
