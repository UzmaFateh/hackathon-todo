# Data Model: Kubernetes Resources for Helm Charts

## Kubernetes Resource Templates

### Frontend Application
- **Resource Type**: Deployment
- **Name**: `{{ include "chart.fullname" . }}-frontend`
- **Fields**:
  - replicas: configurable via values.yaml (default: 1)
  - image: configurable image repository and tag
  - ports: exposes port 3000
  - resources: configurable resource requests and limits
  - environment variables: API endpoints, environment configs
  - livenessProbe: HTTP GET on root path
  - readinessProbe: HTTP GET on health check endpoint

### Frontend Service
- **Resource Type**: Service
- **Name**: `{{ include "chart.fullname" . }}-frontend`
- **Fields**:
  - port: 80
  - targetPort: 3000
  - selector: matches frontend deployment
  - type: ClusterIP (internal access) or LoadBalancer/NodePort for external

### Backend Application
- **Resource Type**: Deployment
- **Name**: `{{ include "chart.fullname" . }}-backend`
- **Fields**:
  - replicas: configurable via values.yaml (default: 1)
  - image: configurable image repository and tag
  - ports: exposes port 8000
  - resources: configurable resource requests and limits
  - environment variables: database URL, authentication settings
  - livenessProbe: HTTP GET on /api/health
  - readinessProbe: HTTP GET on /api/health

### Backend Service
- **Resource Type**: Service
- **Name**: `{{ include "chart.fullname" . }}-backend`
- **Fields**:
  - port: 80
  - targetPort: 8000
  - selector: matches backend deployment
  - type: ClusterIP

### PostgreSQL Database
- **Resource Type**: Deployment
- **Name**: `{{ include "chart.fullname" . }}-database`
- **Fields**:
  - replicas: 1 (databases typically run as single instance)
  - image: PostgreSQL image (configurable version)
  - ports: exposes port 5432
  - resources: configurable resource requests and limits
  - environment variables: database name, user, password
  - persistentVolumeClaim: for data persistence
  - livenessProbe: PostgreSQL connection check
  - readinessProbe: PostgreSQL connection check

### Database Service
- **Resource Type**: Service
- **Name**: `{{ include "chart.fullname" . }}-database`
- **Fields**:
  - port: 5432
  - targetPort: 5432
  - selector: matches database deployment
  - type: ClusterIP

### Database PersistentVolumeClaim
- **Resource Type**: PersistentVolumeClaim
- **Name**: `{{ include "chart.fullname" . }}-database-pvc`
- **Fields**:
  - storageClassName: configurable
  - accessModes: ReadWriteOnce
  - resources.requests.storage: configurable size

### Ingress Controller
- **Resource Type**: Ingress
- **Name**: `{{ include "chart.fullname" . }}-ingress`
- **Fields**:
  - rules: map hostname to frontend service
  - tls: configurable TLS settings
  - annotations: ingress controller specific configurations

### ConfigMap
- **Resource Type**: ConfigMap
- **Name**: `{{ include "chart.fullname" . }}-config`
- **Fields**:
  - application configurations that are non-sensitive
  - feature flags
  - environment-specific settings

### Secret
- **Resource Type**: Secret
- **Name**: `{{ include "chart.fullname" . }}-secret`
- **Fields**:
  - database passwords
  - API keys
  - authentication secrets