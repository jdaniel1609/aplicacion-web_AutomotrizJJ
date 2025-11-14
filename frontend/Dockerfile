# ============================================
# DOCKERFILE FRONTEND - PRODUCCIÓN AKS
# ============================================
# Servidor HTTP simple para archivos estáticos de React
# Sin Nginx - Usa servidor HTTP de Python

# Stage 1: Build
FROM node:18-alpine AS builder

WORKDIR /app

# Variables de entorno para build
ARG REACT_APP_API_URL
ENV REACT_APP_API_URL=${REACT_APP_API_URL}

# Copiar package files
COPY package*.json ./

# Instalar dependencias
RUN npm ci --only=production

# Copiar código fuente
COPY . .

# Build de producción
RUN npm run build

# Stage 2: Production - Servidor HTTP simple
FROM python:3.11-alpine

# Metadatos
LABEL maintainer="Automotriz JJ"
LABEL version="1.0"
LABEL description="Frontend React - Servidor HTTP Simple"

# Crear usuario non-root
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser

# Crear directorio para archivos estáticos
WORKDIR /app

# Copiar archivos build desde stage anterior
COPY --from=builder --chown=appuser:appuser /app/dist ./dist

# Cambiar a usuario non-root
USER appuser

# Exponer puerto 80
EXPOSE 80

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# Comando de inicio - Servidor HTTP simple de Python
CMD ["python", "-m", "http.server", "80", "--directory", "dist", "--bind", "0.0.0.0"]