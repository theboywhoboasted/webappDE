#!/usr/bin/env bash

if [ "$1" == "--dev" ]; then
    tag="dev"
else
    tag="prod"
fi

# Build image
docker build --tag=webapp/deutsch:$tag -f Dockerfile.$tag . 

# List docker images
docker image ls

# Run flask app
docker run -p 127.0.0.1:8080:8080 webapp/deutsch:$tag