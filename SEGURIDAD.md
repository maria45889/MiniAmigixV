# Guía de Seguridad - MiniAmigixV

## Configuración de Seguridad Implementada

### 1. Variables de Entorno Sensibles
Asegúrate de configurar estas variables en tu archivo `.env`:

```bash
# Clave secreta de Django (genera una nueva para producción)
DJANGO_SECRET_KEY=tu_clave_secreta_aleatoria_muy_larga

# Modo DEBUG (False en producción)
DEBUG=False

# Hosts permitidos (separados por coma)
ALLOWED_HOSTS=tudominio.com,www.tudominio.com

# Orígenes CORS permitidos (solo en producción)
CORS_ALLOWED_ORIGINS=https://tudominio.com,https://www.tudominio.com
```

### 2. Cookies Seguras
- `SESSION_COOKIE_SECURE = True` (solo HTTPS)
- `CSRF_COOKIE_SECURE = True` (solo HTTPS)
- `SESSION_COOKIE_HTTPONLY = True` (no accesible desde JavaScript)
- `CSRF_COOKIE_HTTPONLY = True` (no accesible desde JavaScript)
- `SESSION_COOKIE_SAMESITE = 'Lax'` (protección CSRF)

### 3. Headers de Seguridad
- **HSTS**: HTTP Strict Transport Security (1 año en producción)
- **CSP**: Content Security Policy para prevenir XSS
- **X-Frame-Options**: DENY para prevenir clickjacking
- **X-Content-Type-Options**: nosniff
- **Referrer-Policy**: strict-origin-when-cross-origin
- **Permissions-Policy**: Restringe acceso a geolocalización, cámara, etc.

### 4. Rate Limiting
- Usuarios anónimos: 20 requests/minuto
- Usuarios autenticados: 100 requests/minuto
- Protege contra ataques de fuerza bruta y DDoS

### 5. Middleware de Seguridad
- **SecurityHeadersMiddleware**: Agrega headers de seguridad adicionales
- **XSSProtectionMiddleware**: Sanitiza inputs para prevenir XSS

## Recomendaciones Adicionales

### Para Producción

1. **Generar SECRET_KEY seguro**:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

2. **Usar HTTPS obligatorio**:
   - Configurar SSL/TLS en tu servidor
   - Usar Let's Encrypt para certificados gratuitos

3. **Base de datos segura**:
   - Usar PostgreSQL en producción (no SQLite)
   - Configurar firewall para la base de datos
   - Usar contraseñas fuertes para la base de datos

4. **Proteger el panel de administración**:
   - Usar IP whitelist para `/admin/`
   - Configurar `ALLOWED_ADMIN_IPS` en settings.py
   - Usar autenticación de dos factores (2FA)

5. **Regularmente**:
   - Actualizar dependencias: `pip install --upgrade -r requirements.txt`
   - Revisar logs de seguridad
   - Hacer auditorías de seguridad
   - Usar `python manage.py check --deploy` antes de deploy

### Variables de Entorno Críticas

```bash
# Email (Gmail App Password)
DJANGO_SECRET_KEY=...
EMAIL_HOST_PASSWORD=tu_app_password_gmail

# OpenAI API
OPENAI_API_KEY=sk-...

# Clima API
OPENWEATHER_API_KEY=...

# Base de datos
DB_PASSWORD=tu_contraseña_segura
```

### Pruebas de Seguridad

Ejecuta estos comandos regularmente:

```bash
# Verificar configuración de despliegue
python manage.py check --deploy

# Verificar vulnerabilidades en dependencias
pip install safety
safety check

# Escanear código con bandit
pip install bandit
bandit -r apps/
```

### Protección de Datos Sensibles

1. **Nunca** commits el archivo `.env`
2. **Usar** variables de entorno para credenciales
3. **Encriptar** datos sensibles en la base de datos
4. **Implementar** logging seguro (no loggear contraseñas)
5. **Usar** HTTPS para todas las comunicaciones

### Monitoreo

- Configurar alertas para intentos de login fallidos
- Monitorear patrones de tráfico sospechosos
- Implementar bloqueo automático de IPs maliciosas
- Revisar regularmente los logs de Django

## Checklist de Seguridad para Producción

- [ ] DEBUG = False
- [ ] SECRET_KEY generado y seguro
- [ ] ALLOWED_HOSTS configurado correctamente
- [ ] HTTPS/SSL configurado
- [ ] Cookies seguras activadas
- [ ] Headers de seguridad activados
- [ ] Rate limiting configurado
- [ ] CORS configurado con orígenes específicos
- [ ] Base de datos con contraseña fuerte
- [ ] Firewall configurado
- [ ] Logs de seguridad habilitados
- [ ] Dependencias actualizadas
- [ ] Backup automático configurado
- [ ] 2FA para admin activado

## Contacto

Para reportar vulnerabilidades de seguridad, contacta a: miniamigixv@gmail.com
