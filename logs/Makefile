VERSION=v1
DOCKERUSER=rezaakb

#
# You should probably update the docker.io user if you update this
#

build:
	docker build -f Dockerfile -t logs  .

#
# The following make rule labels the current docker image with the version
# number specified above and also the "latest" tag. It then pushes it to
# hub.docker.io
#
push:
	docker tag logs  $(DOCKERUSER)/demucs-logs:$(VERSION)
	docker push $(DOCKERUSER)/demucs-logs:$(VERSION)
	docker tag logs  $(DOCKERUSER)/demucs-logs:latest
	docker push $(DOCKERUSER)/demucs-logs:latest
