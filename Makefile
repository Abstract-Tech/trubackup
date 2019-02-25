EGG_FILES := $(wildcard egg/**/*)
CURRENT_DIR := $(shell pwd)
DUMP_FILENAME := dumps/mysql-$(MYSQL_VERSION)_mongo-$(MONGO_VERSION)
DEFAULT_DOCKER_IMAGE := silviot/edxbackup
DOCKER_IMAGE := $(shell sed -e 's/:.*//' build-image || echo '$(DEFAULT_DOCKER_IMAGE)')
DOCKER_IMAGE_LOCAL_TAG := $(shell git describe --always)
SHELL:=/bin/bash
SHELLOPTS:=$(if $(SHELLOPTS),$(SHELLOPTS):)pipefail:errexit

.ONESHELL:

build-image : Dockerfile $(EGG_FILES)
	docker build . -t $(DOCKER_IMAGE):$(DOCKER_IMAGE_LOCAL_TAG)
	echo $(DOCKER_IMAGE):$(DOCKER_IMAGE_LOCAL_TAG) > build-image

# If the first argument is "run-image"...
ifeq (run-image,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif
run-image :
	docker run --rm -ti -v $(CURRENT_DIR)/dumps:/dumps -v $(CURRENT_DIR)/egg:/egg $(DOCKER_IMAGE):$(DOCKER_IMAGE_LOCAL_TAG) $(RUN_ARGS)

.PHONY: push-image
push-image :
	docker push $(DOCKER_IMAGE):$(DOCKER_IMAGE_LOCAL_TAG)

.PHONY: test
test : build-image $(DUMP_FILENAME)

$(DUMP_FILENAME) : build-image tests/insert_mysql_test_data.sh
	rm -rf $(DUMP_FILENAME)
	function tearDown {
		tests/stop_servers.sh
	}
	trap tearDown EXIT
	tests/start_servers.sh
	tests/populate_dbs.sh
	tests/run_backup.sh
	mkdir -p $(DUMP_FILENAME)
