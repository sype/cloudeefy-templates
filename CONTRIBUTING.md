# Contributing to Cloudeefy Templates

Thank you for your interest in contributing to Cloudeefy Templates! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions. We're building a welcoming community.

## How to Contribute

### Reporting Issues

- Use the [GitHub issue tracker](https://github.com/sype/cloudeefy-templates/issues)
- Check if the issue already exists before creating a new one
- Provide clear reproduction steps
- Include relevant logs and screenshots

### Requesting New Templates

To request a new framework template:

1. Check if it's already in progress
2. Open an issue using the "New Framework Request" template
3. Provide:
   - Framework name and version
   - Use case and popularity
   - Example application repository
   - Special requirements

### Submitting Changes

1. **Fork the repository**
   ```bash
   gh repo fork sype/cloudeefy-templates --clone
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feat/add-react-template
   ```

3. **Make your changes**
   - Follow the template structure
   - Test thoroughly
   - Update documentation

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: Add React template with Vite"
   ```

5. **Push and create PR**
   ```bash
   git push origin feat/add-react-template
   gh pr create --fill
   ```

## Template Development Guidelines

### Template Structure

Every template MUST include:

```
framework-template/
├── README.md                    # Required
├── manifest.yaml               # Required
├── argocd/
│   └── application.yaml        # Required
├── k8s/
│   ├── deployment.yaml         # Required
│   ├── service.yaml            # Required
│   ├── virtualservice.yaml     # Required (Istio)
│   ├── destinationrule.yaml    # Required (Istio)
│   ├── configmap.yaml          # Required
│   └── hpa.yaml                # Optional but recommended
├── workflow/
│   └── build-pipeline.yaml     # Required
└── examples/
    ├── Dockerfile              # Required
    └── sample-values.yaml      # Required
```

### Manifest.yaml Format

```yaml
framework: framework-name
version: x.x
runtime: nodejs|python|go|java
node_version: 18  # For Node.js frameworks
python_version: "3.11"  # For Python frameworks

build:
  command: "npm run build"
  install_command: "npm ci"
  output_directory: "dist"

runtime:
  command: "node server.js"
  port: 3000
  health_check: "/health"

features:
  - feature1
  - feature2

env_vars:
  required:
    - VAR_NAME
  optional:
    - OPTIONAL_VAR

resources:
  requests:
    memory: "256Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
    cpu: "500m"

scaling:
  min_replicas: 2
  max_replicas: 10
  target_cpu_utilization: 70
```

### Placeholder Usage

All templates must use standard placeholders:

- `{{APP_NAME}}` - Application name
- `{{NAMESPACE}}` - Kubernetes namespace
- `{{TENANT}}` - Tenant identifier
- `{{REPO_URL}}` - Git repository URL
- `{{FRAMEWORK}}` - Framework name
- `{{REGISTRY}}` - Container registry
- `{{IMAGE_NAME}}` - Docker image name
- `{{DOMAIN}}` - Application domain
- `{{GIT_SHA}}` - Git commit SHA
- `{{GIT_BRANCH}}` - Git branch

### Istio Configuration

#### VirtualService Requirements

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: {{APP_NAME}}
  namespace: {{NAMESPACE}}
spec:
  hosts:
  - {{DOMAIN}}
  gateways:
  - istio-system/central-gateway  # REQUIRED: Use central gateway
  http:
  - route:
    - destination:
        host: {{APP_NAME}}.{{NAMESPACE}}.svc.cluster.local
    timeout: 60s
    retries:
      attempts: 3
```

#### DestinationRule Requirements

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: {{APP_NAME}}
  namespace: {{NAMESPACE}}
spec:
  host: {{APP_NAME}}.{{NAMESPACE}}.svc.cluster.local
  trafficPolicy:
    tls:
      mode: ISTIO_MUTUAL  # REQUIRED: Enable mTLS
    outlierDetection:  # REQUIRED: Circuit breaker
      consecutiveErrors: 5
```

### Security Requirements

All templates must:

1. ✅ Run containers as non-root user
2. ✅ Set resource requests and limits
3. ✅ Include health checks (liveness + readiness)
4. ✅ Use read-only root filesystem (when possible)
5. ✅ No hardcoded secrets or passwords
6. ✅ Follow least privilege principle

### Testing

Before submitting, test your template:

```bash
# 1. YAML syntax
yamllint framework-template/

# 2. Kubernetes validation
kubectl apply --dry-run=client -f framework-template/k8s/

# 3. Istio validation
istioctl analyze framework-template/k8s/virtualservice.yaml

# 4. Template replacement
./scripts/test-template.sh framework-template

# 5. Integration test (if possible)
# Deploy to test cluster and verify
```

### Documentation

Each template README must include:

1. **Overview** - What the framework is
2. **Prerequisites** - Requirements and versions
3. **Quick Start** - One-command deployment
4. **Configuration** - Environment variables and settings
5. **Files Overview** - Description of each file
6. **Customization** - How to modify the template
7. **Troubleshooting** - Common issues and solutions
8. **Example Dockerfile** - Complete working example

### Dockerfile Best Practices

```dockerfile
# Multi-stage builds
FROM node:18-alpine AS builder
# ... build stage

FROM node:18-alpine AS runner
# Minimal runtime image

# Non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 appuser
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD node healthcheck.js || exit 1
```

## Commit Message Format

Follow conventional commits:

- `feat:` - New template or feature
- `fix:` - Bug fix in template
- `docs:` - Documentation changes
- `ci:` - CI/CD changes
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

Examples:
```
feat: Add React template with Vite
fix: Update Next.js health check path
docs: Improve Django template README
ci: Add template validation workflow
```

## Review Process

Pull requests will be reviewed for:

1. **Correctness** - YAML syntax, K8s schema validation
2. **Completeness** - All required files present
3. **Security** - Security best practices followed
4. **Documentation** - Clear and comprehensive docs
5. **Testing** - Template tested and working
6. **Consistency** - Follows established patterns

## Community

- **Questions**: [GitHub Discussions](https://github.com/sype/cloudeefy-templates/discussions)
- **Chat**: Discord (coming soon)
- **Updates**: Follow [@cloudeefy](https://twitter.com/cloudeefy)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Cloudeefy Templates! 🚀
