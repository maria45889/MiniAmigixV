# Instalación de Bases de Datos en Windows - MiniAmigixV

Este proyecto requiere tres bases de datos:
1. **PostgreSQL** - Base de datos principal de Django
2. **Redis** - Caching y sesiones
3. **MongoDB** - Datos de notificaciones y chats

---

## 1. PostgreSQL

### Instalación
1. Descargar PostgreSQL desde: https://www.postgresql.org/download/windows/
2. Ejecutar el instalador
3. Configurar durante instalación:
   - **Password**: `postgres` (o la que prefieras)
   - **Puerto**: `5432` (default)
4. Marcar "Stack Builder" para instalar herramientas adicionales (opcional)

### Verificar instalación
```powershell
psql --version
```

### Crear base de datos
```powershell
# Abrir psql
psql -U postgres

# Crear base de datos
CREATE DATABASE miniamigixv_db;
\q
```

**Nota:** No necesitas pgAdmin. Puedes gestionar PostgreSQL desde línea de comandos con `psql` o desde Django directamente.

### Variables de entorno (.env)
```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=miniamigixv_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu_contraseña
```

---

## 2. Redis (Memurai)

### Instalación
1. Descargar Memurai desde: https://www.memurai.com/get-memurai
2. Ejecutar el instalador .msi
3. Iniciar servicio:
   - Menú Inicio → Memurai → Start Memurai
   - O desde services.msc

### Verificar instalación
```powershell
memurai-cli ping
# Debe responder: PONG
```

### Variables de entorno (.env)
```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
```

---

## 3. MongoDB

### Instalación
1. Descargar MongoDB Community desde: https://www.mongodb.com/try/download/community
2. Ejecutar el instalador
3. Configurar durante instalación:
   - **Install MongoDB as a Service**: ✓
   - **Data Directory**: `C:\data\db` (default)
   - **Log Directory**: `C:\data\log` (default)

### Verificar instalación
```powershell
mongod --version
```

### Iniciar servicio (si no está corriendo)
```powershell
# Desde services.msc
# O desde PowerShell como admin:
net start MongoDB
```

### Crear base de datos (opcional)
```powershell
mongosh
use miniamigixv_db
db.createCollection('test')
exit
```

### Variables de entorno (.env)
```env
MONGODB_URI=mongodb://localhost:27017/
MONGODB_NAME=miniamigixv_db
```

---

## 4. Configuración en Django

### Instalar dependencias
```powershell
pip install psycopg2-binary django-redis redis mongoengine
```

### Actualizar requirements.txt
```
psycopg2-binary==2.9.9
django-redis==7.0.0
redis==8.0.1
mongoengine==0.28.0
```

### Configuración en settings.py

#### PostgreSQL
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'miniamigixv_db'),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}
```

#### Redis
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{":" + os.getenv("REDIS_PASSWORD", "") + "@" if os.getenv("REDIS_PASSWORD") else ""}{os.getenv("REDIS_HOST", "localhost")}:{os.getenv("REDIS_PORT", "6379")}/{os.getenv("REDIS_DB", "0")}',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'miniamigixv',
        'TIMEOUT': 300,
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

#### MongoDB
```python
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
MONGODB_NAME = os.getenv('MONGODB_NAME', 'miniamigixv_db')

try:
    from mongoengine import connect
    connect(db=MONGODB_NAME, host=MONGODB_URI, alias='default')
    print(f"✓ Conectado a MongoDB: {MONGODB_NAME}")
except Exception as e:
    print(f"✗ Error al conectar a MongoDB: {str(e)}")
```

---

## 5. Archivo .env completo

```env
# Django
DJANGO_SECRET_KEY=tu_secret_key_aqui
DEBUG=True
SITE_URL=http://127.0.0.1:8000

# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=miniamigixv_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu_contraseña_postgres

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# MongoDB
MONGODB_URI=mongodb://localhost:27017/
MONGODB_NAME=miniamigixv_db

# APIs
OPENAI_API_KEY=tu_openai_key
GROQ_API_KEY=tu_groq_key
GEMINI_API_KEY=tu_gemini_key
OPENWEATHER_API_KEY=tu_openweather_key
YOUTUBE_API_KEY=tu_youtube_key
OLLAMA_API_URL=http://localhost:11434
OLLAMA_MODEL=llama3.3

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password
```

---

## 6. Migraciones y Pruebas

### Migrar base de datos PostgreSQL
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Crear superusuario
```powershell
python manage.py createsuperuser
```

### Probar conexión a PostgreSQL
```powershell
python manage.py dbshell
# Debe abrir psql
\q
```

### Probar conexión a Redis
```powershell
python manage.py shell
>>> from django.core.cache import cache
>>> cache.set('test', 'hello', 60)
>>> cache.get('test')
'hello'
```

### Probar conexión a MongoDB
```powershell
python manage.py shell
>>> from mongoengine import connect
>>> connect(db='miniamigixv_db', host='mongodb://localhost:27017/')
```

---

## 7. Servicios en Windows

### Verificar servicios corriendo
```powershell
# Abrir services.msc
# Buscar:
# - PostgreSQL
# - Memurai
# - MongoDB
```

### Iniciar/Parar servicios
```powershell
# PostgreSQL
net start postgresql-x64-16
net stop postgresql-x64-16

# MongoDB
net start MongoDB
net stop MongoDB

# Memurai (desde services.msc o menú inicio)
```

---

## 8. Troubleshooting

### PostgreSQL: Connection refused
- Verificar que el servicio esté corriendo
- Verificar puerto 5432 no esté bloqueado por firewall
- Verificar contraseña correcta en .env

### Redis: Connection refused
- Verificar que Memurai esté corriendo
- Verificar puerto 6379
- Verificar configuración de firewall

### MongoDB: Connection refused
- Verificar que el servicio esté corriendo
- Verificar puerto 27017
- Verificar que el directorio de datos exista

### Django: Error al conectar
- Verificar que todas las variables de entorno estén en .env
- Reiniciar el servidor Django después de cambios
- Verificar logs de Django para errores específicos

---

## 9. Alternativa: Docker (Opcional)

Si prefieres usar Docker en lugar de instalar directamente:

```yaml
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: miniamigixv_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
  
  redis:
    image: redis:latest
    ports:
      - "6379:6379"
  
  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
```

Ejecutar:
```powershell
docker-compose up -d
```
