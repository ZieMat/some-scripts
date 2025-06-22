#!/bin/bash

set -e  # Exit on error

# Install kind binary
[ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.27.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# Create .kube directory if it doesn't exist
mkdir -p ~/.kube

# Backup existing config if it exists
if [ -f ~/.kube/config ]; then
    cp ~/.kube/config ~/.kube/config.backup.$(date +%Y%m%d_%H%M%S)
fi

# Create cluster with explicit config path
kind create cluster --name test

# Export kubeconfig with certificate data
kind get kubeconfig --name test > ~/.kube/config

# Set correct permissions
chmod 600 ~/.kube/config

echo "Testing cluster connection..."
kubectl cluster-info
kubectl get nodes