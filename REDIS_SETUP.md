# Configuración de Redis en MiniAmigixV

## Instalación de Redis

### Windows (Opción 1: Memurai - Recomendado)
Memurai es una alternativa compatible con Redis para Windows:

1. Descargar Memurai desde: https://www.memurai.com/get-memurai
2. Instalar el .msi
3. Iniciar Memurai desde el menú de inicio o services.msc
4. Verificar: `memurai-cli ping` (debe responder PONG)

### Windows (Opción 2: WSL2)
Si tienes WSL2 instalado:

```powershell
wsl
sudo apt-get update
sudo apt-get install redis-server
sudo service redis-server start
redis-cli ping
```

### Windows (Opción 3: Redis para Windows - Versión antigua)
1. Descargar desde: https://github.com/microsoftarchive/redis/releases
2. Descomprimir y ejecutar `redis-server.exe`
3. En otra terminal: `redis-cli ping`

### Linux
```bash
sudo apt-get install redis-server
sudo service redis-server start
```

### macOS
```bash
brew install redis
brew services start redis
```

## Configuración en .env

Agrega las siguientes variables a tu archivo `.env`:

```env
# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=  # Dejar vacío si no hay contraseña
```

Si usas Redis con contraseña:
```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=tu_contraseña_aqui
```

Si usas Redis Cloud o Redis en producción:
```env
REDIS_HOST=redis-12345.redislabs.com
REDIS_PORT=12345
REDIS_DB=0
REDIS_PASSWORD=tu_contraseña_aqui
```

## Uso en Django

### Caching Básico

```python
from django.core.cache import cache

# Guardar en caché
cache.set('mi_clave', 'mi_valor', 60)  # 60 segundos

# Recuperar de caché
valor = cache.get('mi_clave')

# Eliminar de caché
cache.delete('mi_clave')

# Verificar si existe
if cache.get('mi_clave'):
    print('Existe en caché')
```

### Caching de Vistas

```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cachear por 15 minutos
def mi_vista(request):
    # ...
```

### Caching de Templates

```python
from django.template import Library

register = Library()

@register.simple_tag
@cache(60)  # Cachear por 60 segundos
def mi_tag():
    # ...
```

### Caching de Consultas a Base de Datos

```python
from django.core.cache import cache
from myapp.models import Producto

def get_productos():
    productos = cache.get('productos_lista')
    
    if not productos:
        productos = list(Producto.objects.all())
        cache.set('productos_lista', productos, 60 * 15)  # 15 minutos
    
    return productos
```

### Caching con Keys Dinámicas

```python
from django.core.cache import cache

def get_clima(ciudad):
    cache_key = f'clima_{ciudad.lower()}'
    clima = cache.get(cache_key)
    
    if not clima:
        clima = obtener_clima_api(ciudad)
        cache.set(cache_key, clima, 60 * 30)  # 30 minutos
    
    return clima
```

## Sesiones con Redis

Las sesiones ya están configuradas para usar Redis. Esto permite:
- Sesiones más rápidas
- Escalabilidad horizontal (múltiples servidores)
- Persistencia de sesiones

## Comandos Útiles

### Verificar conexión a Redis
```bash
redis-cli ping
# Debe responder: PONG
```

### Ver todas las keys
```bash
redis-cli KEYS '*'
```

### Ver valor de una key
```bash
redis-cli GET 'miniamigixv:mi_clave'
```

### Eliminar todas las keys
```bash
redis-cli FLUSHDB
```

### Eliminar keys por patrón
```bash
redis-cli KEYS 'miniamigixv:*' | xargs redis-cli DEL
```

## Monitoreo de Redis

### Ver estadísticas
```bash
redis-cli INFO
```

### Ver uso de memoria
```bash
redis-cli INFO memory
```

### Ver clientes conectados
```bash
redis-cli CLIENT LIST
```

## Troubleshooting

### Error: Connection refused
- Verificar que Redis esté corriendo: `redis-cli ping`
- Verificar que el puerto sea correcto (default: 6379)
- Verificar firewall

### Error: NOAUTH Authentication required
- Verificar que REDIS_PASSWORD sea correcto en .env
- Si no usas contraseña, déjalo vacío en .env

### Caché no funciona
- Verificar que Redis esté corriendo
- Verificar las variables de entorno
- Revisar logs de Django

## Beneficios de Redis en MiniAmigixV

1. **Caching de API de Clima**: Reducir llamadas a OpenWeather API
2. **Caching de Traducciones**: Evitar traducir el mismo texto múltiples veces
3. **Sesiones Escalables**: Soportar múltiples usuarios simultáneamente
4. **Caching de Consultas**: Mejorar rendimiento de consultas frecuentes
5. **Rate Limiting**: Implementar límites de tasa para APIs

## Próximos Pasos

1. Implementar caching en vistas de clima
2. Implementar caching en traductor
3. Usar Redis como broker para Celery (tareas asíncronas)
4. Implementar rate limiting con Redis
