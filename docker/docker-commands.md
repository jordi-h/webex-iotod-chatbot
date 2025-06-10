# Docker Commands Cheat Sheet

## Docker Basic Operations

### Login to Docker Hub
```bash
# Logs into Docker Hub using the access token as a password. Remember to replace 'username' with your Docker Hub username.
docker login --username <username>
```

### Build and Manage Images

#### Build an Image Named `webex-iotod-bot` from the Current Directory
```bash
# Builds a Docker image named 'webex-iotod-bot' using the Dockerfile located in the 'docker' directory.
docker build -t webex-iotod-bot -f docker/Dockerfile .
```

#### Tag and Push an Image to Docker Hub
```bash
# Tags the local 'webex-iotod-bot' image for upload to Docker Hub and pushes it.
docker image tag webex-iotod-bot jordih2o/webex-iotod-bot:latest
docker image push jordih2o/webex-iotod-bot:latest
```

#### Display Local Docker Images
```bash
# Lists all Docker images stored on the local machine.
docker images
```

#### Erase an Image with a Specific Name (`app`)
```bash
# Removes the Docker image named 'app'.
docker rmi app
```

### Container Lifecycle Management

#### Stop a Specific Container
```bash
# Stops the container named 'iotod-mindmeld-webapp-1'.
docker stop iotod-mindmeld-webapp-1
```

#### Remove a Specific Container
```bash
# Removes the container named 'iotod-mindmeld-webapp-1' after it has been stopped.
docker rm iotod-mindmeld-webapp-1
```

#### Enter a Running Container in Interactive Mode
```bash
# Accesses the bash shell of the running container 'iotod-mindmeld-webapp-1'.
docker exec -it iotod-mindmeld-webapp-1 bash
```

#### View Logs for a Specific Container
```bash
# Displays the logs for the container named 'iotod-mindmeld-webapp-1'.
docker logs iotod-mindmeld-webapp-1
```

#### Inspect a Container for Detailed Information
```bash
# Provides detailed information about the container 'iotod-mindmeld-webapp-1'.
docker inspect iotod-mindmeld-webapp-1
```

## Docker System Management

### Stop and Remove All Containers, Images, and Volumes
```bash
# Stops all running containers, removes them, and forcibly deletes all images and volumes.
docker stop $(docker ps -aq)
docker rm -f $(docker ps -aq)
docker rmi -f $(docker images -q)
docker volume prune -f
```

### Clean up Docker Resources
```bash
# Removes all unused containers, networks, images (both dangling and unreferenced), and optionally, volumes.
docker system prune -a
```

### Display Both Running and Previously Ran Containers
```bash
# Lists all containers, both running and stopped.
docker ps -a
```

### List All Docker Networks
```bash
# Displays all networks created by Docker on the local system.
docker network ls
```

## Docker Compose Commands

### Start the Elastic, Postgres, and Duckling when running the app locally
```bash
# Starts all services defined in 'docker-compose-local.yml' under 'docker' directory in detached mode.
docker compose -f docker/docker-compose-local.yml up -d
```

### Start the iotod bot
```bash
# Starts all services defined in 'docker-compose.yml' under 'docker' directory in detached mode.
docker compose -f docker/docker-compose.yml up -d
```

### Manage Individual Services

#### Stop the webapp Service
```bash
# Stops the 'webapp' service defined in Docker Compose.
docker compose stop webapp
```

#### Remove the webapp Service's Container
```bash
# Forcefully removes the 'webapp' service's container.
docker compose rm -f webapp
```

#### Rebuild the webapp Image
```bash
# Rebuilds the image used by the 'webapp' service.
docker compose build webapp
```

#### Start (or Restart) the webapp Service
```bash
# Starts or restarts the 'webapp' service in detached mode.
docker compose up -d webapp
```

## Additional Utilities

### Check Server Status
```bash
# Sends an HTTP GET request to 'localhost:8080/test' to check server status.
curl http://localhost:8080/test
```

### Enter Postgres DB
```bash
# Switches to the 'postgres' user and enters the PostgreSQL command-line interface.
su postgres
psql
```