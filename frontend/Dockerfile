# Usar imagen base de Node.js
FROM node:18-alpine

# Establecer directorio de trabajo
WORKDIR /app

# Variables de entorno
ENV NODE_ENV=development

# Copiar archivos de package
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar el código fuente
COPY . .

# Exponer puerto de Vite (5173)
EXPOSE 5173

# Comando para ejecutar en modo desarrollo
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]