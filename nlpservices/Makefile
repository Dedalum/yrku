PROJECT_NAME := "nlprecommend"
VERSIONSTRING := $(shell git describe --long --tags --always) # --dirty=+M)

all: help

init: ## Install dependencies
	pip install -r requirements.txt

test: ## Run tests
	pytest tests/

dockerize: ## Dockerize 
	docker build . -t $(PROJECT_NAME):$(VERSIONSTRING) 
	docker tag $(PROJECT_NAME):$(VERSIONSTRING) $(PROJECT_NAME):latest

help: ## Display this message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.PHONY: init test dockerize
