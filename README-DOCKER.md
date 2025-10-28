# 🐳 Guía Docker Hub y Kubernetes - Automotriz JJ

## 📋 Requisitos Previos

- Docker instalado
- Cuenta en Docker Hub (https://hub.docker.com)
- kubectl instalado (para Kubernetes)
- Cluster de Kubernetes (Minikube, AKS, EKS, GKE, etc.)

---

## 🚀 Paso 1: Construir y Publicar Imágenes en Docker Hub

### 1.1 Login en Docker Hub

```bash
docker login
# Ingresa tu username y password de Docker Hub
```

### 1.2 Construir y Publicar Backend

```bash
# Navegar a la carpeta del backend
cd automotriz-jj-backend

# Construir la imagen (reemplaza 'tuusuario' con tu usuario de Docker Hub)
docker build -t tuusuario/automotriz-backend:latest .
docker build -t tuusuario/automotriz-backend:v1.0.0 .

# Publicar en Docker Hub
docker push tuusuario/automotriz-backend:latest
docker push tuusuario/automotriz-backend:v1.0.0

# Verificar
docker images | grep automotriz-backend
```

### 1.3 Construir y Publicar Frontend

```bash
# Navegar a la carpeta del frontend
cd ../automotriz-jj-frontend

# Construir la imagen
docker build -t tuusuario/automotriz-frontend:latest .
docker build -t tuusuario/automotriz-frontend:v1.0.0 .

# Publicar en Docker Hub
docker push tuusuario/automotriz-frontend:latest
docker push tuusuario/automotriz-frontend:v1.0.0

# Verificar
docker images | grep automotriz-frontend
```

---

## 🧪 Paso 2: Probar Imágenes Localmente

### Probar Backend

```bash
docker run -d \
  --name automotriz-backend \
  -p 8000:8000 \
  -e DATABASE_TYPE=sqlite \
  -e SECRET_KEY=test_secret_key \
  -e ALLOWED_ORIGINS="http://localhost:5173" \
  tuusuario/automotriz-backend:latest

# Ver logs
docker logs -f automotriz-backend

# Probar API
curl http://localhost:8000/health
```

### Probar Frontend

```bash
docker run -d \
  --name automotriz-frontend \
  -p 5173:5173 \
  tuusuario/automotriz-frontend:latest

# Ver logs
docker logs -f automotriz-frontend

# Abrir en navegador
# http://localhost:5173
```

### Limpiar contenedores de prueba

```bash
docker stop automotriz-backend automotriz-frontend
docker rm automotriz-backend automotriz-frontend
```

---

## ☸️ Paso 3: Desplegar en Kubernetes

### 3.1 Crear Namespace

```bash
kubectl create namespace automotriz-jj
```

### 3.2 Crear ConfigMap para Backend

Archivo: `k8s/backend-configmap.yaml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: backend-config
  namespace: automotriz-jj
data:
  DATABASE_TYPE: "sqlite"
  ALGORITHM: "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES: "30"
  ALLOWED_ORIGINS: "http://frontend-service:5173,http://localhost:5173"
  DEFAULT_USERNAME: "admin"
  DEFAULT_PASSWORD: "admin123"
```

Aplicar:
```bash
kubectl apply -f k8s/backend-configmap.yaml
```

### 3.3 Crear Secret para Backend

```bash
kubectl create secret generic backend-secrets \
  --from-literal=SECRET_KEY='tu_clave_secreta_super_segura' \
  -n automotriz-jj
```

### 3.4 Deployment del Backend

Archivo: `k8s/backend-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: automotriz-jj
  labels:
    app: automotriz-backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: automotriz-backend
  template:
    metadata:
      labels:
        app: automotriz-backend
    spec:
      containers:
      - name: backend
        image: tuusuario/automotriz-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: backend-secrets
              key: SECRET_KEY
        envFrom:
        - configMapRef:
            name: backend-config
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: backend-service
  namespace: automotriz-jj
spec:
  selector:
    app: automotriz-backend
  ports:
  - protocol: TCP
    port: 8000
    targetPort: 8000
  type: ClusterIP
```

Aplicar:
```bash
kubectl apply -f k8s/backend-deployment.yaml
```

### 3.5 Deployment del Frontend

Archivo: `k8s/frontend-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: automotriz-jj
  labels:
    app: automotriz-frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: automotriz-frontend
  template:
    metadata:
      labels:
        app: automotriz-frontend
    spec:
      containers:
      - name: frontend
        image: tuusuario/automotriz-frontend:latest
        ports:
        - containerPort: 5173
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /
            port: 5173
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 5173
          initialDelaySeconds: 10
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  namespace: automotriz-jj
spec:
  selector:
    app: automotriz-frontend
  ports:
  - protocol: TCP
    port: 5173
    targetPort: 5173
  type: LoadBalancer  # Cambia a NodePort si no tienes LoadBalancer
```

Aplicar:
```bash
kubectl apply -f k8s/frontend-deployment.yaml
```

### 3.6 Crear Ingress (Opcional)

Archivo: `k8s/ingress.yaml`

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: automotriz-ingress
  namespace: automotriz-jj
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: automotriz.local  # Cambia por tu dominio
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: backend-service
            port:
              number: 8000
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 5173
```

Aplicar:
```bash
kubectl apply -f k8s/ingress.yaml
```

---

## 📊 Paso 4: Verificar el Despliegue

### Ver Pods

```bash
kubectl get pods -n automotriz-jj
kubectl get pods -n automotriz-jj -w  # Watch mode
```

### Ver Servicios

```bash
kubectl get services -n automotriz-jj
```

### Ver Logs

```bash
# Backend
kubectl logs -f deployment/backend -n automotriz-jj

# Frontend
kubectl logs -f deployment/frontend -n automotriz-jj

# Logs de un pod específico
kubectl logs -f <pod-name> -n automotriz-jj
```

### Describe Resources

```bash
kubectl describe deployment backend -n automotriz-jj
kubectl describe pod <pod-name> -n automotriz-jj
```

---

## 🌐 Paso 5: Acceder a la Aplicación

### Opción 1: Port Forward (Desarrollo)

```bash
# Frontend
kubectl port-forward -n automotriz-jj service/frontend-service 5173:5173

# Backend
kubectl port-forward -n automotriz-jj service/backend-service 8000:8000
```

Acceder en:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000

### Opción 2: LoadBalancer (Producción)

```bash
# Obtener IP externa
kubectl get service frontend-service -n automotriz-jj

# Acceder usando la EXTERNAL-IP
```

### Opción 3: NodePort

```bash
# Si usas NodePort, obtén el puerto
kubectl get service frontend-service -n automotriz-jj

# Acceder usando
# http://<node-ip>:<node-port>
```

---

## 🔄 Paso 6: Actualizar Imágenes

### Actualizar Backend

```bash
cd automotriz-jj-backend

# Construir nueva versión
docker build -t tuusuario/automotriz-backend:v1.0.1 .

# Push a Docker Hub
docker push tuusuario/automotriz-backend:v1.0.1

# Actualizar en Kubernetes
kubectl set image deployment/backend \
  backend=tuusuario/automotriz-backend:v1.0.1 \
  -n automotriz-jj

# O actualizar el YAML y aplicar
kubectl apply -f k8s/backend-deployment.yaml
```

### Actualizar Frontend

```bash
cd automotriz-jj-frontend

# Construir nueva versión
docker build -t tuusuario/automotriz-frontend:v1.0.1 .

# Push a Docker Hub
docker push tuusuario/automotriz-frontend:v1.0.1

# Actualizar en Kubernetes
kubectl set image deployment/frontend \
  frontend=tuusuario/automotriz-frontend:v1.0.1 \
  -n automotriz-jj
```

---

## 🔍 Paso 7: Troubleshooting

### Pods no inician

```bash
# Ver eventos
kubectl get events -n automotriz-jj --sort-by='.lastTimestamp'

# Describe el pod
kubectl describe pod <pod-name> -n automotriz-jj

# Ver logs
kubectl logs <pod-name> -n automotriz-jj

# Entrar al pod
kubectl exec -it <pod-name> -n automotriz-jj -- /bin/sh
```

### Problemas de conexión

```bash
# Probar conectividad desde un pod
kubectl run -it --rm debug \
  --image=alpine \
  --restart=Never \
  -n automotriz-jj \
  -- sh

# Dentro del pod
wget -O- http://backend-service:8000/health
```

### Limpiar todo

```bash
kubectl delete namespace automotriz-jj
```

---

## 📝 Paso 8: Escalado

### Escalar manualmente

```bash
# Escalar backend a 3 réplicas
kubectl scale deployment backend --replicas=3 -n automotriz-jj

# Escalar frontend a 3 réplicas
kubectl scale deployment frontend --replicas=3 -n automotriz-jj
```

### Autoescalado (HPA)

Archivo: `k8s/hpa.yaml`

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
  namespace: automotriz-jj
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: frontend-hpa
  namespace: automotriz-jj
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: frontend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

Aplicar:
```bash
kubectl apply -f k8s/hpa.yaml
```

---

## 🔒 Paso 9: Seguridad

### Network Policies

Archivo: `k8s/network-policy.yaml`

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-network-policy
  namespace: automotriz-jj
spec:
  podSelector:
    matchLabels:
      app: automotriz-backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: automotriz-frontend
    ports:
    - protocol: TCP
      port: 8000
```

---

## 📚 Recursos Adicionales

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Docker Hub](https://hub.docker.com/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)