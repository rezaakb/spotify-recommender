VERSION=v9
DOCKERUSER=rezaakb

build:
	docker build --no-cache -f Dockerfile -t worker-server .
push:
	docker tag worker-server $(DOCKERUSER)/worker-server:$(VERSION)
	docker push $(DOCKERUSER)/worker-server:$(VERSION)
	docker tag worker-server $(DOCKERUSER)/worker-server:latest
	docker push $(DOCKERUSER)/worker-server:latest
