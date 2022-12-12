VERSION=v6
DOCKERUSER=rezaakb

build:
	docker build -f Dockerfile -t rest-server .

push:
	docker tag rest-server $(DOCKERUSER)/rest-server:$(VERSION)
	docker push $(DOCKERUSER)/rest-server:$(VERSION)
	docker tag rest-server $(DOCKERUSER)/rest-server:latest
	docker push $(DOCKERUSER)/rest-server:latest
