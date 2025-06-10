#!/bin/sh
# Stops all running containers, removes the volume, and restarts the services using the specified docker-compose file.

# Stop Docker Compose services
docker compose -f docker/docker-compose-local.yml down

# Remove the specified volume
docker volume rm docker_my_dbdata

# Start Docker Compose services again
docker compose -f docker/docker-compose-local.yml up -d
