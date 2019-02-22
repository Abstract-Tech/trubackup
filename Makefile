EGG := $(wildcard egg/**/*)

build-image : Dockerfile $(EGG)
	docker build . -t registry.abzt.de/edx-backup
	date > build-image
push-image :
	docker push registry.abzt.de/edx-backup

test :
