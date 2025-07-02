#!/bin/bash

# Exit on error
set -e

# Function to handle errors
handle_error() {
    echo "Error occurred in script at line $1"
    exit 1
}

trap 'handle_error $LINENO' ERR

# Update package list
echo "Updating package list..."
sudo apt-get update

# Install prerequisites
echo "Installing prerequisites..."
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
echo "Adding Docker's GPG key..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Set up the stable repository
echo "Setting up Docker repository..."
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
echo "Installing Docker Engine..."
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Install Docker Compose
echo "Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
echo "Adding user to docker group..."
sudo usermod -aG docker $(echo | whoami)
newgrp docker

# Start Docker service
echo "Starting Docker service..."
sudo systemctl start docker
sudo systemctl enable docker

# Verify installation
echo "Verifying installation..."
docker --version
docker-compose --version
docker run --rm hello-world

# Cleanup
echo "Cleaning up..."
sudo apt-get clean
sudo rm -rf /var/lib/apt/lists/*

echo "Docker installation completed successfully!"
