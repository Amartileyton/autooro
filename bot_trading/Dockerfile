# ==========================================
# Multi-stage Dockerfile para XAUUSD Trading Engine
# ==========================================

# Etapa 1: Build del Frontend Astro
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Etapa 2: Backend Python FastAPI
FROM python:3.11-slim
WORKDIR /app

# Variables de entorno de Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar requerimientos de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código del backend y dump inicial
COPY backend /app/backend
COPY dump.sql /app/dump.sql

# Copiar build del frontend si se desea servir estáticamente
COPY --from=frontend-builder /app/frontend/dist /app/frontend_dist

# Exponer puertos (8000 para API REST y WS)
EXPOSE 8000

# Comando de arranque del backend con Uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
