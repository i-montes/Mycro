#!/bin/bash
# Ask the user for login details
read -p 'Docker container name: ' name
read -p 'Docker local port: ' port
echo
echo Build container $name

docker build -t ${name} .
docker run -d -p 127.0.0.1:${port}:5000 \
  --name=${name} \
  ${name}



