PROJECT_NAME := "nlprecommend"
VERSIONSTRING := $(shell git describe --long --tags --always) # --dirty=+M)

init:
	pip install -r requirements.txt

test:
	pytest tests/

dockerize:
	docker build . -t $(PROJECT_NAME):$(VERSIONSTRING) 
	docker tag $(PROJECT_NAME):$(VERSIONSTRING) $(PROJECT_NAME):latest


.PHONY: init test dockerize
