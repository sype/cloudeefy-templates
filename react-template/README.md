# React SPA Template for Cloudeefy

Production-ready deployment template for React Single Page Applications (SPAs) with nginx static serving.

## Overview

This template enables deployment of React applications built with:
- **Create React App (CRA)** - React framework with webpack
- **Vite** - Next-generation frontend tooling
- **Custom Webpack** - Custom React build configurations

### Architecture

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   Build     │────▶│   Runtime    │────▶│   Output     │
│  Node.js    │     │    nginx     │     │ Static files │
│   (deps +   │     │  (web server)│     │   (SPA)      │
│    build)   │     │              │     │              │
└─────────────┘     └──────────────┘     └──────────────┘
```

- **Build Stage**: Node.js compiles React app to static files
- **Runtime**: nginx serves static files with SPA routing
- **Deployment**: Kubernetes with ArgoCD GitOps workflow

## Features

- ✅ **Multi-Stage Docker Build**: Node.js builder + nginx runtime
- ✅ **SPA Routing**: All client-side routes return index.html
- ✅ **Aggressive Caching**: Optimized cache headers for static assets
- ✅ **Build-Time Environment Variables**: REACT_APP_* and VITE_* support
- ✅ **Node Version Support**: Auto-detect from package.json or specify (18, 19, 20, 21)
- ✅ **Package Manager Detection**: Supports npm, yarn, pnpm
- ✅ **Health Checks**: Kubernetes liveness/readiness probes
- ✅ **Horizontal Scaling**: Auto-scaling based on CPU/memory
- ✅ **Zero-Downtime Deployments**: Rolling updates with ArgoCD
- ✅ **Security**: Non-root nginx, security headers, gzip compression

## Quick Start

### 1. Prepare Your React App

Ensure your React app has:
- `package.json` with build script
- Lockfile (package-lock.json, yarn.lock, or pnpm-lock.yaml)
- Build output directory (build/ for CRA, dist/ for Vite)

### 2. Connect Your Repository

```bash
# Auto-detect Node version from package.json
cloudeefy custom connect \
  --repo https://github.com/your-org/your-react-app \
  --framework react \
  --name my-react-app \
  --namespace production

# Specify Node version manually
cloudeefy custom connect \
  --repo https://github.com/your-org/your-react-app \
  --framework react \
  --name my-react-app \
  --node-version 20

# With build-time environment variables
cloudeefy custom connect \
  --repo https://github.com/your-org/your-react-app \
  --framework react \
  --name my-react-app \
  --env REACT_APP_API_URL=https://api.example.com
```

### 3. Deploy

The connect command generates:
- Dockerfile with nginx
- nginx.conf with SPA routing
- Kubernetes manifests
- Argo Workflow for CI/CD
- ArgoCD Application

Commit these files to your repository and ArgoCD will handle the rest.

## Environment Variables

### Build-Time Variables

React environment variables are **baked into the JavaScript bundle** at build time.

#### Create React App Convention
```bash
REACT_APP_API_URL=https://api.example.com
REACT_APP_ANALYTICS_ID=UA-123456789
REACT_APP_AUTH_DOMAIN=auth.example.com
```

#### Vite Convention
```bash
VITE_API_URL=https://api.example.com
VITE_ANALYTICS_ID=UA-123456789
```

#### Common Variables
```bash
PUBLIC_URL=https://cdn.example.com  # Base path for static assets
NODE_ENV=production                  # Always set to production
```

### Setting Environment Variables

1. **Via Workflow Parameters**: Edit `workflow/build-pipeline.yaml`
   ```yaml
   parameters:
   - name: react-app-api-url
     value: "https://api.example.com"
   ```

2. **Via Docker Build Args**: In Dockerfile
   ```dockerfile
   ARG REACT_APP_API_URL
   ENV REACT_APP_API_URL=${REACT_APP_API_URL}
   ```

3. **Via GitHub Secrets**: For CI/CD
   ```yaml
   env:
     REACT_APP_API_URL: ${{ secrets.API_URL }}
   ```

## File Structure

```
your-react-app/
├── Dockerfile              # Multi-stage build (generated)
├── nginx.conf              # nginx configuration (generated)
├── k8s/
│   ├── deployment.yaml     # Kubernetes deployment
│   ├── service.yaml        # ClusterIP service
│   ├── configmap.yaml      # Configuration
│   ├── hpa.yaml            # Auto-scaling
│   ├── virtualservice.yaml # Istio routing
│   ├── destinationrule.yaml# Traffic policies
│   └── kustomization.yaml  # Kustomize config
├── argocd/
│   └── application.yaml    # ArgoCD app definition
└── workflow/
    └── build-pipeline.yaml # Argo Workflow
```

## Build Process

### 1. Dependency Installation

The workflow detects your package manager:

```bash
# npm
if [ -f package-lock.json ]; then npm ci; fi

# yarn
if [ -f yarn.lock ]; then yarn install --frozen-lockfile; fi

# pnpm
if [ -f pnpm-lock.yaml ]; then pnpm install --frozen-lockfile; fi
```

### 2. Build

```bash
npm run build

# Output detection:
# - Create React App: build/
# - Vite: dist/
# - Custom: Check package.json scripts
```

### 3. Docker Image

Multi-stage Dockerfile:
1. **Stage 1 (deps)**: Install Node.js dependencies
2. **Stage 2 (builder)**: Build React app with environment variables
3. **Stage 3 (runner)**: Copy built files to nginx Alpine image

Final image size: **~50MB** (nginx + static files)

### 4. Deployment

- Kaniko builds and pushes image to registry
- ArgoCD detects new image
- Rolling update to Kubernetes
- Zero-downtime with health checks

## nginx Configuration

### SPA Routing

All routes fallback to index.html for client-side routing:

```nginx
location / {
    try_files $uri $uri/ /index.html;
}
```

### Caching Strategy

```nginx
# No caching for index.html (always fresh)
location = /index.html {
    add_header Cache-Control "no-cache, no-store, must-revalidate";
}

# Aggressive caching for hashed assets (webpack/vite)
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

# No caching for service worker
location = /service-worker.js {
    add_header Cache-Control "no-cache";
}
```

### Security Headers

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
```

### Compression

```nginx
gzip on;
gzip_vary on;
gzip_types text/plain text/css application/javascript application/json;
```

## Resource Limits

Default Kubernetes resources (lighter than Next.js):

```yaml
resources:
  requests:
    memory: "64Mi"
    cpu: "50m"
  limits:
    memory: "128Mi"
    cpu: "200m"
```

Adjust based on your app's needs.

## Scaling

Horizontal Pod Autoscaler configuration:

```yaml
minReplicas: 2
maxReplicas: 10
targetCPUUtilization: 70%
```

## Health Checks

### Liveness Probe
```yaml
httpGet:
  path: /health
  port: 80
initialDelaySeconds: 10
periodSeconds: 10
```

### Readiness Probe
```yaml
httpGet:
  path: /health
  port: 80
initialDelaySeconds: 5
periodSeconds: 5
```

## Troubleshooting

### Build Output Not Found

**Error**: "No build output found in build/ or dist/"

**Solution**:
1. Check your `package.json` build script
2. Verify build command produces output
3. Check if output directory is different (e.g., `out/`)
4. Update Dockerfile COPY command if needed

### SPA Routing Not Working

**Problem**: 404 errors for client-side routes

**Solution**:
- Ensure nginx.conf has `try_files $uri /index.html`
- Verify nginx.conf is copied to image
- Check Istio VirtualService configuration

### Environment Variables Not Set

**Problem**: `undefined` in React app

**Solution**:
1. Verify variables have correct prefix (`REACT_APP_` or `VITE_`)
2. Check they're set in workflow parameters
3. Confirm they're passed as build args in workflow
4. Rebuild Docker image (variables are build-time)

### Image Size Too Large

**Problem**: Docker image > 100MB

**Solution**:
- Use Alpine base images (already configured)
- Ensure multi-stage build is working
- Check node_modules not copied to final stage
- Verify only build output is copied

### Pod Not Starting

**Problem**: CrashLoopBackOff

**Solution**:
1. Check logs: `kubectl logs -n <namespace> <pod-name>`
2. Verify nginx.conf syntax: `nginx -t`
3. Ensure build output exists in image
4. Check resource limits aren't too low

## Best Practices

### 1. Build Optimization

```json
// package.json
{
  "scripts": {
    "build": "react-scripts build",
    "build:prod": "NODE_ENV=production npm run build"
  }
}
```

### 2. Code Splitting

```javascript
// Use React.lazy for route-based splitting
const Dashboard = React.lazy(() => import('./Dashboard'));

<Suspense fallback={<Loading />}>
  <Dashboard />
</Suspense>
```

### 3. Asset Optimization

- Enable source maps in production (for debugging)
- Use webpack-bundle-analyzer to identify large bundles
- Lazy load images and heavy components
- Implement PWA for offline support

### 4. Security

- Set Content Security Policy headers
- Use HTTPS for API endpoints
- Validate all user inputs
- Keep dependencies updated

### 5. Monitoring

- Implement error tracking (Sentry, Rollbar)
- Add analytics (Google Analytics, Mixpanel)
- Monitor Core Web Vitals
- Set up uptime monitoring

## Example Projects

- **Create React App**: https://github.com/facebook/create-react-app
- **Vite React**: https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react
- **React Router**: https://github.com/remix-run/react-router

## Support

For issues or questions:
- GitHub Issues: https://github.com/your-org/cloudeefy/issues
- Documentation: https://docs.cloudeefy.io
- Slack: #cloudeefy-support

## License

MIT License - see LICENSE file for details
