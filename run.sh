#!/bin/bash
registry_ip=10.96.120.0
registry_port=5050

echo "learningOrchestra: a distributed machine learning processing tool"
echo "--------------------------------------------------------------------"
echo "Building the learningOrchestra microservice images..."
echo "--------------------------------------------------------------------"

docker build --tag $registry_ip:$registry_port/spark_task microservices/spark_task_image
docker build --tag $registry_ip:$registry_port/database_api microservices/database_api_image
docker build --tag $registry_ip:$registry_port/spark microservices/spark_image
docker build --tag $registry_ip:$registry_port/projection microservices/projection_image
docker build --tag $registry_ip:$registry_port/builder microservices/builder_image
docker build --tag $registry_ip:$registry_port/data_type_handler microservices/data_type_handler_image
docker build --tag $registry_ip:$registry_port/histogram microservices/histogram_image
docker build --tag $registry_ip:$registry_port/model microservices/model_image
docker build --tag $registry_ip:$registry_port/binary_executor microservices/binary_executor_image
docker build --tag $registry_ip:$registry_port/database_executor microservices/database_executor_image
docker build --tag $registry_ip:$registry_port/code_executor microservices/code_executor_image
docker build --tag $registry_ip:$registry_port/observer microservices/observer_image
#docker-compose build

echo "--------------------------------------------------------------------"
echo "Adding the microservice images in docker daemon security exception..."
echo "--------------------------------------------------------------------"

#echo "{
#  \"exec-opts\": [\"native.cgroupdriver=systemd\"],
#  \"insecure-registries\" : [\"$registry_ip:$registry_port\"]
#}
#" > /etc/docker/daemon.json
#
#echo "--------------------------------------------------------------------"
#echo "Restarting docker service..."
#echo "--------------------------------------------------------------------"
#
#service docker restart

#echo "--------------------------------------------------------------------"
#echo "Deploying learningOrchestra in swarm cluster..."
#echo "--------------------------------------------------------------------"

#kubectl apply -f composer_files/
#docker stack deploy --compose-file=docker-compose.yml microservice



echo "--------------------------------------------------------------------"
echo "Pushing the microservice images in local repository..."
echo "--------------------------------------------------------------------"

sleep 5
docker push $registry_ip:$registry_port/spark_task
database_api_repository=$registry_ip:$registry_port/database_api


echo "--------------------------------------------------------------------"
echo "Pushing databaseApi microservice image..."
echo "--------------------------------------------------------------------"
docker push $database_api_repository

spark_repository=$registry_ip:$registry_port/spark

echo "--------------------------------------------------------------------"
echo "Pushing spark image..."
echo "--------------------------------------------------------------------"
docker push $spark_repository

projection_repository=$registry_ip:$registry_port/projection

echo "--------------------------------------------------------------------"
echo "Pushing projection microservice image..."
echo "--------------------------------------------------------------------"
docker push $projection_repository

builder_repository=$registry_ip:$registry_port/builder

echo "--------------------------------------------------------------------"
echo "Pushing builder microservice image..."
echo "--------------------------------------------------------------------"
docker push $builder_repository

data_type_handler_repository=$registry_ip:$registry_port/data_type_handler

echo "--------------------------------------------------------------------"
echo "Pushing dataTypeHandler microservice image..."
echo "--------------------------------------------------------------------"
docker push $data_type_handler_repository

histogram_repository=$registry_ip:$registry_port/histogram

echo "--------------------------------------------------------------------"
echo "Pushing histogram microservice image..."
echo "--------------------------------------------------------------------"
docker push $histogram_repository

model_repository=$registry_ip:$registry_port/model

echo "--------------------------------------------------------------------"
echo "Pushing model microservice image..."
echo "--------------------------------------------------------------------"
docker push $model_repository

binary_executor_repository=$registry_ip:$registry_port/binary_executor

echo "--------------------------------------------------------------------"
echo "Pushing binaryExecutor microservice image..."
echo "--------------------------------------------------------------------"
docker push $binary_executor_repository

database_executor_repository=$registry_ip:$registry_port/database_executor

echo "--------------------------------------------------------------------"
echo "Pushing databaseExecutor microservice image..."
echo "--------------------------------------------------------------------"
docker push $database_executor_repository

code_executor_repository=$registry_ip:$registry_port/code_executor

echo "--------------------------------------------------------------------"
echo "Pushing codeExecutor microservice image..."
echo "--------------------------------------------------------------------"
docker push $code_executor_repository

observer_repository=$registry_ip:$registry_port/observer

echo "--------------------------------------------------------------------"
echo "Pushing observer microservice image..."
echo "--------------------------------------------------------------------"
docker push $observer_repository

#echo "--------------------------------------------------------------------"
#echo "Updating portainer agent microservice in each cluster node..."
#echo "--------------------------------------------------------------------"
#docker service update --image portainer/agent  microservice_agent

echo "--------------------------------------------------------------------"
echo "End."
echo "--------------------------------------------------------------------"
