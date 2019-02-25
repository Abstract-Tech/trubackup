EGG := $(wildcard egg/**/*)

build-image : Dockerfile $(EGG)
	docker build . -t registry.abzt.de/edx-backup
	date > build-image

.PHONY: push-image
push-image :
	docker push registry.abzt.de/edx-backup

.PHONY: test
test : build-image
	tests/dump_dbs.sh
