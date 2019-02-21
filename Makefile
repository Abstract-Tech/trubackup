
build-image:
	docker build . -t registry.abzt.de/edx-backup
push-image:
	docker push registry.abzt.de/edx-backup
