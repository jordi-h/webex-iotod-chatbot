#!/bin/sh
# A script to completely clean up Docker by removing all containers, images, volumes, and networks.

# Stop all running containers
docker ps -q | xargs -r docker stop

# Remove all containers (including stopped ones)
docker ps -aq | xargs -r docker rm -f

# Remove all images
docker images -q | xargs -r docker rmi -f

# Remove all volumes
docker volume ls -q | xargs -r docker volume rm

# Remove all networks except the default ones (bridge, host, none)
docker network ls -q | grep -vE 'bridge|host|none' | xargs -r docker network rm

# Remove dangling images, containers, volumes, and networks (extra cleanup)
docker system prune -af --volumes
