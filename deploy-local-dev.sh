#!/bin/sh
#
# You can use this script to launch Redis and minio on Kubernetes
# and forward their connections to your local computer. That means
# you can then work on your worker-server.py and rest-server.py
# on your local computer rather than pushing to Kubernetes with each change.
#
# To kill the port-forward processes us e.g. "ps augxww | grep port-forward"
# to identify the processes ids
#
kubectl apply -f ./redis/redis-deployment.yaml
kubectl apply -f ./redis/redis-service.yaml

#kubectl apply -f ./rest/rest-deployment.yaml
#kubectl apply -f ./rest/rest-service.yaml
kubectl apply -f ./logs/logs-deployment.yaml
#kubectl apply -f ./worker/worker-deployment.yaml

kubectl port-forward --address 0.0.0.0 service/redis 6379:6379 &
