SHELL=/bin/bash
EGG_FILES = $(wildcard egg/**/*)
CURRENT_DIR = $(shell pwd)
DUMP_FILENAME = dumps/mysql-$(MYSQL_VERSION)_mongo-$(MONGO_VERSION)
DEFAULT_DOCKER_IMAGE = abstract2tech/edxbackup
DOCKER_IMAGE = $(shell sed -e 's/:.*//' build-image 2> /dev/null || echo '$(DEFAULT_DOCKER_IMAGE)')
DOCKER_IMAGE_LOCAL_TAG = ${shell md5sum <(md5sum $(CURRENT_DIR)/Dockerfile $(find $(CURRENT_DIR)/egg -type f))| cut -c -8}
SHELLOPTS=$(if $(SHELLOPTS),$(SHELLOPTS):)pipefail:errexit
DUMP_SOURCE = $(shell find $(CURRENT_DIR)/$(DUMP_FILENAME) -maxdepth 1 -mindepth 1 -type d)

ndef = $(if $(value $(1)),,$(error $(1) not set))

.ONESHELL:

build-image : Dockerfile $(EGG_FILES)
	docker build . -t $(DOCKER_IMAGE):$(DOCKER_IMAGE_LOCAL_TAG)
	echo $(DOCKER_IMAGE):$(DOCKER_IMAGE_LOCAL_TAG) > build-image

# If the first argument is "run-image"...
ifeq (run-image,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run-images"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif
run-image :
	docker run --network host --rm -ti -v $(CURRENT_DIR)/dumps:/dumps -v $(CURRENT_DIR)/egg:/egg $(DOCKER_IMAGE):$(DOCKER_IMAGE_LOCAL_TAG) $(RUN_ARGS)

.PHONY: push-image
push-image :
	docker push $(DOCKER_IMAGE):$(DOCKER_IMAGE_LOCAL_TAG)

.PHONY: test-dump
test-dump : $(DUMP_FILENAME)

.PHONY: pytest
pytest :
	pytest egg

.PHONY: shell
shell :
	docker run --rm -ti --env-file tests/test.env --network host $$(cat build-image) sh

$(DUMP_FILENAME) : $(wildcard tests/insert*.sh)
	$(call ndef,MYSQL_VERSION)
	$(call ndef,MONGO_VERSION)
	rm -rf $(DUMP_FILENAME)
	function tearDown {
		tests/stop_servers.sh
	}
	trap tearDown EXIT
	tests/start_servers.sh
	tests/populate_dbs.sh
	mkdir -p $(DUMP_FILENAME)
	tests/run_backup.sh "$(CURRENT_DIR)/$(DUMP_FILENAME)" "$(DOCKER_IMAGE):$(DOCKER_IMAGE_LOCAL_TAG)"

.PHONY: test-restore
test-restore : $(DUMP_FILENAME)
	$(call ndef,MYSQL_VERSION)
	$(call ndef,MONGO_VERSION)
	function tearDown {
		tests/stop_servers.sh
	}
	trap tearDown EXIT
	tests/start_servers.sh
	tests/run_restore.sh "$(DUMP_SOURCE)" "$(DOCKER_IMAGE):$(DOCKER_IMAGE_LOCAL_TAG)"
	COUNT=$$(docker exec edxbackup_test_mongo mongo test --eval 'db.inventory.count()' |tail -n1)
	if [ "$${COUNT}" != "3" ]; then
		echo Wrong number of records in mongodb: $${COUNT}
	fi
