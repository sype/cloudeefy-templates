# Multi-stage build for React SPA with nginx runtime
# This Dockerfile should be copied to the root of your React repository

# ==============================================================================
# Stage 1: Dependencies
# ==============================================================================
FROM node:{{NODE_VERSION}}-alpine AS deps

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* yarn.lock* pnpm-lock.yaml* ./

# Install dependencies based on lockfile
RUN \
  if [ -f package-lock.json ]; then npm ci; \
  elif [ -f yarn.lock ]; then yarn install --frozen-lockfile; \
  elif [ -f pnpm-lock.yaml ]; then npm install -g pnpm && pnpm install --frozen-lockfile; \
  else echo "No lockfile found." && exit 1; \
  fi

# ==============================================================================
# Stage 2: Builder
# ==============================================================================
FROM node:{{NODE_VERSION}}-alpine AS builder

WORKDIR /app

# Copy dependencies from deps stage
COPY --from=deps /app/node_modules ./node_modules

# Copy application code
COPY . .

# Build arguments for environment variables (injected at build time)
ARG REACT_APP_API_URL
ARG REACT_APP_ANALYTICS_ID
ARG REACT_APP_AUTH_DOMAIN
ARG PUBLIC_URL
ARG VITE_API_URL
ARG VITE_ANALYTICS_ID

# Export as environment variables for the build
ENV REACT_APP_API_URL=${REACT_APP_API_URL}
ENV REACT_APP_ANALYTICS_ID=${REACT_APP_ANALYTICS_ID}
ENV REACT_APP_AUTH_DOMAIN=${REACT_APP_AUTH_DOMAIN}
ENV PUBLIC_URL=${PUBLIC_URL}
ENV VITE_API_URL=${VITE_API_URL}
ENV VITE_ANALYTICS_ID=${VITE_ANALYTICS_ID}
ENV NODE_ENV=production

# Build the application
# Output directory detection:
# - Create React App: build/
# - Vite: dist/
RUN npm run build

# ==============================================================================
# Stage 3: Production Runtime (nginx)
# ==============================================================================
FROM nginx:1.25-alpine AS runner

# Remove default nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built static files from builder stage
# Try both common output directories
RUN mkdir -p /usr/share/nginx/html
COPY --from=builder /app/build /usr/share/nginx/html 2>/dev/null || \
     COPY --from=builder /app/dist /usr/share/nginx/html || \
     (echo "ERROR: No build output found. Expected /app/build or /app/dist" && exit 1)

# Create health check endpoint
RUN echo "OK" > /usr/share/nginx/html/health

# nginx runs on port 80 by default
EXPOSE 80

# Start nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
