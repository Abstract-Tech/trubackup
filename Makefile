EGG := $(wildcard egg/**/*)
DEFAULT_DOCKER_IMAGE := silviot/edxbackup
DOCKER_IMAGE := $(shell sed -e 's/:.*//' build-image || echo '$(DEFAULT_DOCKER_IMAGE)')
DOCKER_IMAGE_LOCAL_TAG := $(shell git describe --always)
SHELL:=/bin/bash
SHELLOPTS:=$(if $(SHELLOPTS),$(SHELLOPTS):)pipefail:errexit

.ONESHELL:

build-image : Dockerfile $(EGG)
	docker build . -t $(DOCKER_IMAGE):$(DOCKER_IMAGE_LOCAL_TAG)
	echo $(DOCKER_IMAGE):$(DOCKER_IMAGE_LOCAL_TAG) > build-image

.PHONY: push-image
push-image :
	docker push $(DOCKER_IMAGE):$(DOCKER_IMAGE_LOCAL_TAG)

.PHONY: test
test : build-image
	@function tearDown {
		@tests/stop_servers.sh
	@}
	trap tearDown EXIT
	tests/start_servers.sh
	tests/dump_dbs.sh
