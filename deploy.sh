#!/bin/bash

kubectl create configmap krakend --from-file=microservices/krakend/krakend.json
kubectl apply -f composer_files
kubectl apply -f kompose