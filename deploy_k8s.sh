#!/bin/bash
set -e

# Create directory for k8s files if it doesn't exist
#mkdir -p k8s

# Apply configurations in order
echo "Creating namespace..."
kubectl apply -f k8s/namespace.yaml

echo "Creating ConfigMap..."
kubectl apply -f k8s/configmap.yaml

echo "Creating PersistentVolumeClaim..."
kubectl apply -f k8s/pvc.yaml

echo "Creating Deployment and Service..."
kubectl apply -f k8s/deployment.yaml

echo "Creating Traefik IngressRoute..."
kubectl apply -f k8s/traefik.yaml

# Wait for deployment to be ready
echo "Waiting for ChromaDB to be ready..."
kubectl wait --namespace chromadb \
  --for=condition=ready pod \
  --selector=app=chromadb \
  --timeout=300s

# Get the service URLs
echo "ChromaDB is available at:"
echo "HTTP:  http://chromadb.dev.motorenflug.at"
echo "HTTPS: https://chromadb.dev.motorenflug.at"

# Show deployment status
echo "Deployment status:"
kubectl get all -n chromadb

# Show Traefik routes
echo "Traefik routes:"
kubectl get ingressroute -n chromadb

# Show logs
echo "Showing ChromaDB logs (press Ctrl+C to exit)..."
kubectl logs -f -n chromadb -l app=chromadb 