#!/bin/bash

# Update your package list and install necessary packages to ensure your system can securely install Docker.
sudo apt-get update
sudo apt-get install -y ca-certificates curl

# Secure your Docker installation by verifying the authenticity of the Docker packages.
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the Docker repository to your system's software sources to fetch the latest Docker packages from Docker’s official content.
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package list again
sudo apt-get update

# Install Docker Engine, CLI tools, and additional plugins.
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add your user to the Docker group to manage Docker containers without needing administrative privileges.
sudo groupadd docker
sudo usermod -aG docker $USER

# Refresh group membership
newgrp docker

# Log in to your Docker Hub account to push and pull images from Docker Hub.
docker login
