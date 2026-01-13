# Cloudeefy Deployment Templates

Production-ready deployment templates for various frameworks with Istio service mesh, ArgoCD GitOps, and Argo Workflows CI/CD.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-1.24+-blue.svg)](https://kubernetes.io/)
[![Istio](https://img.shields.io/badge/Istio-1.18+-blue.svg)](https://istio.io/)
[![ArgoCD](https://img.shields.io/badge/ArgoCD-2.8+-blue.svg)](https://argo-cd.readthedocs.io/)

## Overview

This repository contains deployment templates used by the Cloudeefy platform to deploy applications with a single command. Each template includes:

- 🚀 **Kubernetes Manifests** - Production-ready deployments, services, and configs
- 🌐 **Istio Configuration** - VirtualService and DestinationRule for service mesh
- 📦 **ArgoCD Application** - GitOps automated deployment and sync
- ⚙️ **Argo Workflows** - Complete CI/CD pipeline with build, test, and deploy
- 📊 **Auto-Scaling** - Horizontal Pod Autoscaler for handling load
- 🔒 **Security** - Non-root containers, resource limits, health checks

## Available Templates

| Framework | Type | Status | Documentation |
|-----------|------|--------|---------------|
| [Next.js](nextjs-template/) | Frontend (SSR) | ✅ Ready | [README](nextjs-template/README.md) |
| React (Vite) | Frontend (SPA) | 🔄 Coming Soon | - |
| Vue | Frontend (SPA) | 🔄 Coming Soon | - |
| Nuxt | Frontend (SSR) | 📋 Planned | - |
| Svelte | Frontend | 📋 Planned | - |
| Angular | Frontend (SPA) | 📋 Planned | - |
| Django | Backend (Python) | 📋 Planned | - |
| FastAPI | Backend (Python) | 📋 Planned | - |
| Node.js | Backend (JavaScript) | 📋 Planned | - |
| NestJS | Backend (TypeScript) | 📋 Planned | - |

## Quick Start

### Using Cloudeefy CLI (Recommended)

Deploy any supported framework with a single command:

```bash
cloudeefy connect \
  --repo https://github.com/yourorg/your-app \
  --framework nextjs \
  --name my-app \
  --namespace production
```

The CLI will:
1. Fetch the appropriate template from this repository
2. Customize it with your application details
3. Generate Kubernetes manifests locally
4. Deploy via ArgoCD for GitOps automation
5. Set up CI/CD pipeline with Argo Workflows

### Manual Usage

You can also use templates directly:

```bash
# 1. Copy template
cp -r nextjs-template/ my-project-k8s/

# 2. Replace placeholders
cd my-project-k8s/
find . -type f -exec sed -i '' \
  -e 's/{{APP_NAME}}/my-app/g' \
  -e 's/{{NAMESPACE}}/production/g' \
  -e 's/{{DOMAIN}}/my-app.example.com/g' \
  {} +

# 3. Apply manifests
kubectl apply -f argocd/application.yaml
kubectl apply -f workflow/build-pipeline.yaml
```

## Template Structure

Each template follows this standard structure:

```
framework-template/
├── README.md                    # Framework-specific documentation
├── manifest.yaml               # Template metadata and configuration
│
├── argocd/
│   └── application.yaml        # ArgoCD Application definition
│
├── k8s/
│   ├── deployment.yaml         # Kubernetes Deployment
│   ├── service.yaml            # Kubernetes Service
│   ├── virtualservice.yaml     # Istio VirtualService (routing)
│   ├── destinationrule.yaml    # Istio DestinationRule (traffic policy)
│   ├── configmap.yaml          # Environment variables
│   └── hpa.yaml                # Horizontal Pod Autoscaler
│
├── workflow/
│   └── build-pipeline.yaml     # Argo Workflow (CI/CD)
│
└── examples/
    ├── Dockerfile              # Example Dockerfile for user repo
    └── sample-values.yaml      # Example configuration values
```

## Prerequisites

Templates are designed for the Cloudeefy infrastructure stack:

- **Kubernetes**: 1.24 or later
- **Istio**: 1.18 or later with central-gateway configured
- **ArgoCD**: 2.8 or later
- **Argo Workflows**: 3.4 or later
- **Container Registry**: Scaleway, Docker Hub, or private registry

## Features

### Istio Service Mesh

All templates include Istio configuration for:

- **Traffic Management**: VirtualService for routing rules
- **Traffic Policy**: DestinationRule for load balancing and circuit breaking
- **Security**: mTLS within the service mesh
- **Observability**: Automatic metrics, tracing, and logging
- **Canary Deployments**: Traffic splitting for progressive rollouts

### GitOps with ArgoCD

- Automatic sync from Git repositories
- Self-healing when drift detected
- Declarative configuration management
- Easy rollbacks and history tracking

### CI/CD with Argo Workflows

Complete build pipeline including:

- Git repository cloning
- Dependency installation
- Application building
- Container image creation (Kaniko)
- Image pushing to registry
- Kubernetes deployment update
- Rollout validation

### Production Readiness

- Health checks (liveness and readiness probes)
- Resource limits and requests
- Horizontal Pod Autoscaler
- Pod anti-affinity for high availability
- Non-root container execution
- Graceful shutdown handling

## Template Placeholders

All templates use consistent placeholders:

| Placeholder | Example | Description |
|-------------|---------|-------------|
| `{{APP_NAME}}` | `my-nextjs-app` | Application name |
| `{{NAMESPACE}}` | `production` | Kubernetes namespace |
| `{{TENANT}}` | `acme-corp` | Multi-tenant identifier |
| `{{REPO_URL}}` | `https://github.com/...` | Git repository URL |
| `{{FRAMEWORK}}` | `nextjs` | Framework identifier |
| `{{REGISTRY}}` | `rg.fr-par.scw.cloud` | Container registry URL |
| `{{IMAGE_NAME}}` | `my-app` | Docker image name |
| `{{DOMAIN}}` | `my-app.example.com` | Application domain |
| `{{GIT_SHA}}` | `a1b2c3d` | Git commit hash |

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Adding a New Template

1. Fork this repository
2. Copy an existing template as a starting point
3. Customize for your framework
4. Test thoroughly
5. Submit a pull request

See [Template Development Guide](docs/TEMPLATE_DEVELOPMENT.md) for details.

## Documentation

- [Next.js Template](nextjs-template/README.md) - Complete Next.js deployment guide
- [Template Specification](docs/TEMPLATE_SPEC.md) - Standard template format
- [Istio Integration](docs/ISTIO_INTEGRATION.md) - Service mesh configuration
- [CI/CD Pipeline](docs/CICD_PIPELINE.md) - Argo Workflows details

## Support

- **Documentation**: https://docs.cloudeefy.io
- **Issues**: [GitHub Issues](https://github.com/sype/cloudeefy-templates/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sype/cloudeefy-templates/discussions)
- **Community**: https://discord.cloudeefy.io

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for [Cloudeefy](https://cloudeefy.io) platform
- Powered by [Kubernetes](https://kubernetes.io/), [Istio](https://istio.io/), [ArgoCD](https://argo-cd.readthedocs.io/), and [Argo Workflows](https://argoproj.github.io/workflows/)
- Inspired by best practices from the cloud-native community

---

**Made with ❤️ by the Cloudeefy Team**
