APP_NAME := flask_app
APP_PORT := 5000
VERSION := $(shell cat VERSION)
DOCKER_REGISTRY := 'mtulio/flask_sample'
MODULE := "none"

# #############
# BASE
# #############

.PHONY: show-version
show-version:
	@echo $(VERSION)

.PHONY: dependencies
dependencies:
	virtualenv -p python3 venv

.PHONY: setup
setup: dependencies
	./venv/bin/pip install -r requirements.txt
	#if [ "$(MODULE)" == "zabbix" ]; then \
	#	./venv/bin/pip install -r requirements/requirements-zabbix.txt \
	#fi
	#if [ "$(MODULE)" == "librato" ]; then \
	#	./venv/bin/pip install -r requirements/requirements-librato.txt \
	#fi

.PHONY: run
run:
	./venv/bin/python app.py

# #############
# DOCKER
# #############

.PHONY: docker-build
docker-build:
	sudo docker build -t $(APP_NAME):$(VERSION) .

.PHONY: docker-run
docker-run:
	sudo docker run --rm -p $(APP_PORT):$(APP_PORT) --name $(APP_NAME) -d $(APP_NAME):$(VERSION)
	sleep 2 && curl http://localhost:$(APP_PORT)/status

.PHONY: docker-stop
docker-stop:
	sudo docker stop $(APP_NAME)

.PHONY: docker-kill
docker-kill:
	sudo docker rm -f $(APP_NAME)

.PHONY: docker-deinit
docker-deinit: docker-clean docker-build docker-run
	sudo docker ps --filter "name=$(APP_NAME)"
	sleep 2 && curl http://localhost:$(APP_PORT)/status

.PHONY: docker-clean
docker-clean:
	sudo docker rm $(APP_NAME); \
		sudo docker rmi $(APP_NAME):$(VERSION)

.PHONY: docker-tag
docker-tag:
	sudo docker tag $(APP_NAME):$(VERSION) $(DOCKER_REGISTRY):$(APP_NAME)-$(VERSION)

.PHONY: docker-deploy
docker-deploy: docker-tag
	sudo docker push $(DOCKER_REGISTRY):$(APP_NAME)-$(VERSION)


# #############
# LAMBDA (TODO)
# ############
.PHONY: lambda-deploy-prod
lambda-deploy-prod:
	zappa deploy production

.PHONY: lambda-update-prod
lambda-update-prod:
	zappa update production
