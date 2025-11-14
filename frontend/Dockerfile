# ============================================
# DOCKERFILE FRONTEND - PRODUCCIÓN AKS
# ============================================
# Node 18
# Usa 'serve' para servir archivos estáticos
FROM node:18-alpine

# Metadatos
LABEL maintainer="Automotriz JJ"
LABEL version="1.0"
LABEL description="Frontend React - Node 18"

# Variables de entorno para build
ARG REACT_APP_API_URL
ENV REACT_APP_API_URL=${REACT_APP_API_URL}

# Crear usuario non-root
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser

# Directorio de trabajo
WORKDIR /app

# Copiar package files
COPY package*.json ./

# Instalar dependencias de producción
RUN npm ci --only=production

# Instalar 'serve' para servir archivos estáticos
RUN npm install -g serve

# Copiar código fuente
COPY . .

# Build de producción
RUN npm run build

# Cambiar ownership
RUN chown -R appuser:appuser /app

# Cambiar a usuario non-root
USER appuser

# Exponer puerto 80
EXPOSE 80

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:80/ || exit 1

# Comando de inicio con serve
# serve sirve archivos estáticos de forma eficiente
CMD ["serve", "-s", "dist", "-l", "80"]