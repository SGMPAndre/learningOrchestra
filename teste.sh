#!/bin/bash
registry_ip=10.96.120.0
registry_port=5050

echo "{
  \"exec-opts\": [\"native.cgroupdriver=systemd\"],
  \"insecure-registries\" : [\"$registry_ip:$registry_port\"]
}
" > /etc/docker/daemon.json

service docker restart