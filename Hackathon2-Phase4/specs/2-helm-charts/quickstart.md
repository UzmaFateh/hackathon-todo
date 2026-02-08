# Quick Start: Deploying Helm Charts to Minikube

## Prerequisites

- Minikube installed and running
- Helm 3.x installed
- kubectl installed and configured for Minikube
- kubectl-ai and kagent installed (optional, for AI-assisted operations)

## Starting Minikube

```bash
# Start Minikube (if not already running)
minikube start

# Verify Minikube is running
kubectl cluster-info
```

## Installing kubectl-ai and kagent (Optional)

```bash
# Install kubectl-ai (example installation)
# Follow official documentation for your platform

# Verify kubectl-ai is available
kubectl ai --help

# Install kagent (example installation)
# Follow official documentation for your platform
```

## Building and Deploying the Helm Chart

```bash
# Navigate to the Helm chart directory
cd /path/to/your/helm/chart

# Add the dependency repositories if needed
helm repo update

# Install the chart
helm install todo-app . --namespace todo-app --create-namespace

# Or with custom values
helm install todo-app . --namespace todo-app --create-namespace -f values-production.yaml
```

## Verifying the Deployment

```bash
# Check all pods are running
kubectl get pods --namespace todo-app

# Check all services are available
kubectl get svc --namespace todo-app

# Check the ingress (if configured)
kubectl get ingress --namespace todo-app

# Port forward to access the frontend locally (if ingress not available)
kubectl port-forward -n todo-app svc/todo-app-frontend 3000:80
```

## Accessing the Application

```bash
# If using ingress
minikube service todo-app-frontend --namespace todo-app --url

# Or if using LoadBalancer service
minikube service todo-app-frontend --namespace todo-app

# For backend API access
kubectl port-forward -n todo-app svc/todo-app-backend 8000:80
```

## Using AI-Assisted Operations

```bash
# Get AI assistance with kubectl commands
kubectl ai "show me the status of pods in todo-app namespace"

# Troubleshoot with kagent
kagent diagnose "my frontend pods are crashing"

# Get optimization suggestions
kubectl ai "suggest resource optimizations for my deployments"
```

## Updating the Deployment

```bash
# Update with new values
helm upgrade todo-app . --namespace todo-app -f values-production.yaml

# Rollback to previous version
helm rollback todo-app --namespace todo-app
```

## Cleaning Up

```bash
# Uninstall the release
helm uninstall todo-app --namespace todo-app

# Delete the namespace
kubectl delete namespace todo-app
```

## Troubleshooting

```bash
# Check pod logs
kubectl logs -n todo-app deployment/todo-app-frontend
kubectl logs -n todo-app deployment/todo-app-backend
kubectl logs -n todo-app deployment/todo-app-database

# Describe resources for detailed information
kubectl describe -n todo-app deployment/todo-app-frontend

# Get detailed status with kubectl-ai
kubectl ai "analyze the status of my todo-app namespace"
```