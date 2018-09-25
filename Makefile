CONTAINER_IMAGE=$(shell bash scripts/container_image.sh)
PYTHON ?= "python3"
PYTEST_OPTS ?= "-s -vvv"
PYTEST_DIR ?= "tests"
ABACO_DEPLOY_OPTS ?= "-p"
SCRIPT_DIR ?= "scripts"
PREF_SHELL ?= "bash"
ACTOR_ID ?=
GITREF=$(shell git rev-parse --short HEAD)

GITREF=$(shell git rev-parse --short HEAD)

.PHONY: tests container tests-local tests-reactor tests-deployed datacatalog formats
.SILENT: tests container tests-local tests-reactor tests-deployed datacatalog formats

all: image

datacatalog: formats
	if [ -d ../python-datacatalog/datacatalog ]; then rm -rf datacatalog; cp -R ../python-datacatalog/datacatalog .; fi

image:
	abaco deploy -R -t $(GITREF) $(ABACO_DEPLOY_OPTS)

shell:
	bash $(SCRIPT_DIR)/run_container_process.sh bash

tests: tests-pytest tests-local

tests-pytest:
	bash $(SCRIPT_DIR)/run_container_process.sh $(PYTHON) -m "pytest" $(PYTEST_DIR) $(PYTEST_OPTS)

tests-integration: tests-local
pipelines: create-tasbe create-platereader create-rnaseq create-s3-ingest create-samples-json-capture

tests-local: tests-local-create tests-local-delete

tests-local-create: tests-local-create-tacobot
tests-local-update: tests-local-update-tacobot
tests-local-delete: tests-local-delete-tacobot
tests-local-undelete: tests-local-undelete-tacobot

tests-local-create-tacobot:
	bash $(SCRIPT_DIR)/run_container_message.sh tests/data/0-local-create-tacobot.json

tests-local-update-tacobot:
	bash $(SCRIPT_DIR)/run_container_message.sh tests/data/0-local-update-tacobot-name.json

tests-local-delete-tacobot:
	bash $(SCRIPT_DIR)/run_container_message.sh tests/data/0-local-delete-tacobot.json

tests-local-undelete-tacobot:
	bash $(SCRIPT_DIR)/run_container_message.sh tests/data/0-local-undelete-tacobot.json

create-tasbe:
	bash $(SCRIPT_DIR)/run_container_message.sh tests/data/1-local-create-tasbe.json

create-platereader:
	bash $(SCRIPT_DIR)/run_container_message.sh tests/data/2-local-create-platereader.json

create-rnaseq:
	bash $(SCRIPT_DIR)/run_container_message.sh tests/data/3-local-create-rnaseq.json

create-s3-ingest:
	bash $(SCRIPT_DIR)/run_container_message.sh tests/data/4-ingest-s3-uploads.json

create-samples-json-capture:
	bash $(SCRIPT_DIR)/run_container_message.sh tests/data/5-samples-json-capture.json

tests-local-run:
	echo "not implemented"

tests-deployed:
	echo "not implemented"

clean: clean-image clean-tests

clean-image:
	docker rmi -f $(CONTAINER_IMAGE)

clean-tests:
	rm -rf .hypothesis .pytest_cache __pycache__ */__pycache__ tmp.* *junit.xml

deploy:
	abaco deploy -t $(GITREF) $(ABACO_DEPLOY_OPTS) -U $(ACTOR_ID)

postdeploy:
	bash tests/run_after_deploy.sh

