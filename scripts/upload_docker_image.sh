#!/bin/bash
# Make sure you are logged in.

docker build -t webex-iotod-bot -f docker/Dockerfile .
docker image tag webex-iotod-bot jordih2o/webex-iotod-bot:latest
docker image push jordih2o/webex-iotod-bot:latest
