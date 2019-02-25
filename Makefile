EGG := $(wildcard egg/**/*)
DEFAULT_DOCKER_IMAGE := silviot/edxbackup
DOCKER_IMAGE := $(shell sed -e 's/:.*//' build-image || echo '$(DEFAULT_DOCKER_IMAGE)')
DOCKER_IMAGE_LOCAL_TAG := $(shell git describe --always)

build-image : Dockerfile $(EGG)
	docker build . -t $(DOCKER_IMAGE):$(DOCKER_IMAGE_LOCAL_TAG)
	echo $(DOCKER_IMAGE):$(DOCKER_IMAGE_LOCAL_TAG) > build-image

.PHONY: push-image
push-image :
	docker push $(DOCKER_IMAGE):$(DOCKER_IMAGE_LOCAL_TAG)

.PHONY: test
test : build-image
	tests/dump_dbs.sh
