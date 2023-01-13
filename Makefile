EGG_FILES = $(wildcard egg/**/*)
CURRENT_DIR = $(shell pwd)
DUMP_FILENAME = dumps/mysql-$(MYSQL_VERSION)_mongo-$(MONGO_VERSION)
DEFAULT_DOCKER_IMAGE = abstract2tech/edxbackup
DOCKER_IMAGE = $(shell sed -e 's/:.*//' build-image 2> /dev/null || echo '$(DEFAULT_DOCKER_IMAGE)')
DOCKER_IMAGE_LOCAL_TAG = ${shell git describe || git rev-parse --short HEAD}
SHELLOPTS=$(if $(SHELLOPTS),$(SHELLOPTS):)pipefail:errexit

ndef = $(if $(value $(1)),,$(error $(1) not set))

.ONESHELL:

.PHONY: build-image
build-image : Dockerfile $(EGG_FILES)
	docker build . -t $(DOCKER_IMAGE):$(DOCKER_IMAGE_LOCAL_TAG)
	echo $(DOCKER_IMAGE):$(DOCKER_IMAGE_LOCAL_TAG) > build-image

.PHONY: push-image
push-image :
	docker push $(DOCKER_IMAGE):$(DOCKER_IMAGE_LOCAL_TAG)

.PHONY: test
test :
	tests/start_servers.sh
	tests/populate_dbs.sh
	pytest egg
