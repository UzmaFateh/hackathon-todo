# Todo App Helm Chart

A Helm chart for deploying the Todo application on Kubernetes. This chart deploys a full-stack application with:
- Frontend: Next.js application
- Backend: FastAPI application
- Database: PostgreSQL

## Prerequisites

- Kubernetes 1.19+
- Helm 3.2.0+
- PV provisioner support in the underlying infrastructure

## Installing the Chart

To install the chart with the release name `todo-app`:

```bash
# Add the repo if needed
helm repo add todo-app https://your-repo.example.com/todo-app

# Install the chart
helm install todo-app ./charts/todo-app --namespace todo-app --create-namespace
```

## Upgrading the Chart

```bash
helm upgrade todo-app ./charts/todo-app --namespace todo-app
```

## Uninstalling the Chart

```bash
helm uninstall todo-app --namespace todo-app
```

## Configuration

The following table lists the configurable parameters of the todo-app chart and their default values.

### Global parameters

| Parameter | Description | Default |
|-----|-----|-----|
| `global.imageRegistry` | Global Docker image registry | `""` |
| `global.storageClass` | Global storage class for dynamic provisioning | `""` |

### Frontend parameters

| Parameter | Description | Default |
|-----|-----|-----|
| `frontend.replicaCount` | Number of frontend replicas | `1` |
| `frontend.image.repository` | Frontend image repository | `"hackathon2-frontend"` |
| `frontend.image.tag` | Frontend image tag | `"latest"` |
| `frontend.service.type` | Frontend service type | `"ClusterIP"` |
| `frontend.service.port` | Frontend service port | `80` |
| `frontend.ingress.enabled` | Enable ingress for frontend | `false` |

### Backend parameters

| Parameter | Description | Default |
|-----|-----|-----|
| `backend.replicaCount` | Number of backend replicas | `1` |
| `backend.image.repository` | Backend image repository | `"hackathon2-backend"` |
| `backend.image.tag` | Backend image tag | `"latest"` |
| `backend.service.type` | Backend service type | `"ClusterIP"` |
| `backend.service.port` | Backend service port | `80` |

### Database parameters

| Parameter | Description | Default |
|-----|-----|-----|
| `database.enabled` | Enable PostgreSQL deployment | `true` |
| `database.replicaCount` | Number of database replicas | `1` |
| `database.image.repository` | PostgreSQL image repository | `"postgres"` |
| `database.image.tag` | PostgreSQL image tag | `"15-alpine"` |
| `database.postgresql.auth.database` | PostgreSQL database name | `"todoapp"` |
| `database.postgresql.auth.username` | PostgreSQL username | `"postgres"` |
| `database.postgresql.auth.password` | PostgreSQL password | `"postgres"` |

### Resource limits and requests

You can configure resource limits and requests for each component by modifying the corresponding `resources` section in values.yaml.

## Example: Custom Values

```yaml
# custom-values.yaml
frontend:
  replicaCount: 2
  image:
    tag: "v1.0.0"
  resources:
    limits:
      cpu: 200m
      memory: 256Mi
    requests:
      cpu: 100m
      memory: 128Mi

backend:
  replicaCount: 2
  image:
    tag: "v1.0.0"

database:
  postgresql:
    auth:
      password: "securePassword123"
```

Then install with:

```bash
helm install todo-app ./charts/todo-app -f custom-values.yaml --namespace todo-app --create-namespace
```

## Local Development

For local development with Minikube:

```bash
# Start Minikube
minikube start

# Install the chart
helm install todo-app ./charts/todo-app --namespace todo-app --create-namespace

# Port forward to access the frontend
kubectl port-forward -n todo-app svc/todo-app-frontend 3000:80
```

## Troubleshooting

### Checking pod status
```bash
kubectl get pods -n todo-app
```

### Viewing logs
```bash
kubectl logs -n todo-app deployment/todo-app-frontend
kubectl logs -n todo-app deployment/todo-app-backend
kubectl logs -n todo-app deployment/todo-app-database
```

### Describing resources
```bash
kubectl describe -n todo-app deployment/todo-app-frontend
kubectl describe -n todo-app service/todo-app-frontend
```

### Debugging Helm
```bash
helm status todo-app -n todo-app
helm get manifest todo-app -n todo-app
```

## Notes

- The database password is stored in a Kubernetes Secret
- The chart uses ConfigMaps for non-sensitive configuration
- The chart is designed to work with the containerized versions of the applications
- For production deployments, make sure to use secure passwords and image tags