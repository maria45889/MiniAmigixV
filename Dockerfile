# Dockerfile para MiniAmigixV
FROM python:3.14-slim

# Establecer variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . .

# Recopilar archivos estáticos
RUN python manage.py collectstatic --noinput

# Exponer puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
