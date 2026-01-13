# Next.js Template for Cloudeefy

Production-ready Next.js deployment template with Istio service mesh integration, auto-scaling, and CI/CD via Argo Workflows.

## Features

- ✅ **Server-Side Rendering (SSR)** - Full Next.js SSR support
- ✅ **Istio Service Mesh** - Traffic management, mTLS, circuit breaking
- ✅ **Auto-Scaling** - HPA based on CPU/memory metrics
- ✅ **High Availability** - Multi-replica with pod anti-affinity
- ✅ **CI/CD Pipeline** - Automated builds with Argo Workflows
- ✅ **GitOps** - ArgoCD automatic sync and self-healing
- ✅ **Health Checks** - Kubernetes liveness & readiness probes
- ✅ **TLS/SSL** - Automatic certificate management
- ✅ **Canary Deployments** - Built-in support for progressive rollouts

## Prerequisites

- **Kubernetes**: 1.24+
- **Istio**: 1.18+ with central-gateway configured
- **ArgoCD**: 2.8+
- **Argo Workflows**: 3.4+
- **Container Registry**: Scaleway, Docker Hub, or private registry

## Quick Start

### 1. Prepare Your Next.js Application

Ensure your Next.js app has a `Dockerfile` in the root:

```dockerfile
# See examples/Dockerfile for a complete example
FROM node:18-alpine AS base
# ... (see full example below)
```

### 2. Deploy with Cloudeefy CLI

```bash
cloudeefy connect \
  --repo https://github.com/yourorg/your-nextjs-app \
  --framework nextjs \
  --name my-nextjs-app \
  --namespace production
```

### 3. Monitor Deployment

```bash
# Watch ArgoCD sync
argocd app get my-nextjs-app --watch

# Watch deployment rollout
kubectl rollout status deployment/my-nextjs-app -n production

# View pods
kubectl get pods -l app=my-nextjs-app -n production

# Check Istio traffic
kubectl get virtualservice my-nextjs-app -n production
```

## Configuration

### Environment Variables

Set in `k8s/configmap.yaml` or via Cloudeefy dashboard:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API endpoint | Yes | - |
| `NEXTAUTH_URL` | NextAuth.js URL | For auth | - |
| `NEXTAUTH_SECRET` | NextAuth.js secret | For auth | - |
| `DATABASE_URL` | Database connection | For DB | - |
| `NODE_ENV` | Node environment | No | `production` |

### Resource Configuration

Default resource limits (edit `k8s/deployment.yaml`):

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### Scaling Configuration

HPA scales between 2-10 replicas based on:
- CPU utilization: 70%
- Memory utilization: 80%

Edit `k8s/hpa.yaml` to customize.

### Istio Configuration

**VirtualService** (`k8s/virtualservice.yaml`):
- CORS enabled
- Retry policy: 3 attempts
- Timeout: 60s
- Static asset caching

**DestinationRule** (`k8s/destinationrule.yaml`):
- Circuit breaker enabled
- Connection pooling
- mTLS within mesh
- Sticky sessions for SSR

## Files Overview

```
nextjs-template/
├── README.md                      # This file
├── manifest.yaml                  # Template metadata
│
├── argocd/
│   └── application.yaml          # ArgoCD Application (GitOps)
│
├── k8s/
│   ├── deployment.yaml           # Kubernetes Deployment
│   ├── service.yaml              # ClusterIP Service
│   ├── virtualservice.yaml       # Istio VirtualService (routing)
│   ├── destinationrule.yaml      # Istio DestinationRule (traffic policy)
│   ├── configmap.yaml            # Environment variables
│   └── hpa.yaml                  # Horizontal Pod Autoscaler
│
├── workflow/
│   └── build-pipeline.yaml       # Argo Workflow (CI/CD)
│
└── examples/
    ├── Dockerfile                # Example Dockerfile
    └── sample-values.yaml        # Example configuration
```

## Example Dockerfile

Your Next.js repository should include this `Dockerfile`:

```dockerfile
# Multi-stage build for Next.js with standalone output

# Stage 1: Dependencies
FROM node:18-alpine AS deps
WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Builder
FROM node:18-alpine AS builder
WORKDIR /app

# Copy dependencies
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Set environment
ENV NEXT_TELEMETRY_DISABLED 1
ENV NODE_ENV production

# Build with standalone output
RUN npm run build

# Stage 3: Runner
FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy standalone output
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
```

## Next.js Configuration

Update `next.config.js` for standalone output:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',

  // Optimize for production
  poweredByHeader: false,
  compress: true,

  // Image optimization
  images: {
    domains: ['your-cdn.com'],
  },
}

module.exports = nextConfig
```

## Health Check API

Create `app/api/health/route.ts` (App Router) or `pages/api/health.ts` (Pages Router):

```typescript
// app/api/health/route.ts
import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
  })
}
```

## Istio Traffic Management

### Canary Deployment

Update `k8s/virtualservice.yaml` for traffic splitting:

```yaml
http:
- match:
  - uri:
      prefix: /
  route:
  - destination:
      host: my-nextjs-app
      subset: stable
    weight: 90
  - destination:
      host: my-nextjs-app
      subset: canary
    weight: 10
```

### A/B Testing

Route based on headers:

```yaml
http:
- match:
  - headers:
      x-version:
        exact: "v2"
  route:
  - destination:
      host: my-nextjs-app
      subset: canary
```

## Troubleshooting

### Build Failures

```bash
# Check Argo Workflow logs
argo logs -n argo <workflow-name> --follow

# Common issues:
# - Out of memory: Increase workflow resources
# - Dependencies fail: Check package-lock.json
```

### Pod Crashes

```bash
# Check pod logs
kubectl logs -n production deployment/my-nextjs-app

# Check pod events
kubectl describe pod -n production <pod-name>

# Common issues:
# - Missing environment variables
# - Image pull errors
# - Health check failures
```

### Istio Traffic Issues

```bash
# Check VirtualService
kubectl get virtualservice -n production my-nextjs-app -o yaml

# Check DestinationRule
kubectl get destinationrule -n production my-nextjs-app -o yaml

# Test connectivity
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -- \
  curl http://my-nextjs-app.production.svc.cluster.local
```

### Performance Tuning

1. **Increase replicas**:
   ```bash
   kubectl scale deployment/my-nextjs-app --replicas=5 -n production
   ```

2. **Adjust HPA**:
   - Edit `k8s/hpa.yaml`
   - Lower CPU threshold for faster scaling

3. **Optimize build**:
   - Enable SWC in `next.config.js`
   - Use `pnpm` instead of `npm`
   - Add `.dockerignore` to reduce context

## Advanced Configuration

### Static Asset CDN

Configure Next.js to use CDN:

```javascript
// next.config.js
module.exports = {
  assetPrefix: process.env.CDN_URL || '',
}
```

### Redis Session Store

Add Redis for ISR cache:

```yaml
# k8s/deployment.yaml
env:
- name: REDIS_URL
  value: "redis://redis.production.svc.cluster.local:6379"
```

### Database Connection

For apps with databases:

```yaml
# k8s/deployment.yaml
env:
- name: DATABASE_URL
  valueFrom:
    secretKeyRef:
      name: my-nextjs-app-secrets
      key: database-url
```

## Best Practices

1. ✅ **Use standalone output** - Reduces image size significantly
2. ✅ **Implement health checks** - `/api/health` endpoint required
3. ✅ **Set resource limits** - Prevents OOM kills
4. ✅ **Enable HPA** - Auto-scale based on load
5. ✅ **Use mTLS** - Secure service-to-service communication
6. ✅ **Monitor metrics** - Integrate with Prometheus
7. ✅ **Test locally** - Use `docker-compose` before deploying

## Support

- **Documentation**: https://docs.cloudeefy.io
- **Community**: https://discord.cloudeefy.io
- **Issues**: https://github.com/cloudeefy/templates/issues

## License

MIT License - See LICENSE file for details
