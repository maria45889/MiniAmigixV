# MongoDB Integration - MiniAmigixV

## Configuración Completa de MongoDB

### 1. Dependencias Instaladas
- `mongoengine`: ODM (Object-Document Mapper) para MongoDB en Python
- `pymongo`: Driver de MongoDB para Python

### 2. Configuración en settings.py
- MongoDB conectado a `mongodb://localhost:27017/`
- Base de datos: `miniamigixv_db`
- App `mongodb` agregada a INSTALLED_APPS

### 3. Modelos en MongoDB
Los siguientes modelos están disponibles en `apps/mongodb/models.py`:

#### Modelos Principales
- `ChatMessageMongo`: Mensajes de chat
- `NotificacionMongo`: Notificaciones
- `LogActividadMongo`: Logs de actividad
- `AnaliticaMongo`: Datos analíticos

#### Modelos de Estadísticas y Métricas (Nuevos)
- `EstadisticasUsuarioMongo`: Estadísticas agregadas por usuario
- `MetricasSistemaMongo`: Métricas del sistema
- `RendimientoChatMongo`: Métricas de rendimiento del chat
- `EventoInteraccionMongo`: Eventos de interacción específicos
- `SesionUsuarioMongo`: Sesiones de usuario

### 4. Sistema Dual (SQLite + MongoDB)

#### SQLite (Base de datos principal)
- Datos críticos y relaciones
- Autenticación de usuarios
- Eventos, perfil, configuración
- Datos que requieren integridad referencial

#### MongoDB (Base de datos secundaria)
- Historial de chat
- Logs de actividad
- Datos analíticos
- Notificaciones históricas
- Datos para análisis y reportes
- Estadísticas agregadas
- Métricas de rendimiento
- Sesiones de usuario
- Eventos de interacción

### 5. Servicio DualDatabaseService

Uso del servicio en `apps/mongodb/services.py`:

```python
from apps.mongodb.services import DualDatabaseService

# Guardar mensaje de chat en ambas bases de datos
DualDatabaseService.guardar_chat_mensaje(usuario, mensaje, respuesta)

# Guardar notificación en ambas bases de datos
DualDatabaseService.guardar_notificacion(usuario, titulo, mensaje, tipo)

# Registrar actividad solo en MongoDB
DualDatabaseService.log_actividad(usuario, accion, descripcion, ip_address)

# Registrar datos analíticos solo en MongoDB
DualDatabaseService.registrar_analitica(usuario, pagina, tiempo_duracion)

# Obtener historial desde MongoDB
historial = DualDatabaseService.obtener_historial_chat(usuario)

# Obtener estadísticas del usuario
stats = DualDatabaseService.obtener_estadisticas_usuario(usuario)
```

### 6. Dashboard de Analítica
- **URL**: `/mongodb/dashboard-analitica/`
- **Funcionalidades**:
  - Estadísticas generales del sistema
  - Estadísticas por usuario
  - Top usuarios por chats
  - Top páginas visitadas
  - Notificaciones por tipo
  - Actividad reciente (últimos 7 días)

### 7. Sistema de Logs Automático
Las siguientes vistas tienen logging automático en MongoDB:
- `home`: Registro de visitas a página principal
- `chat`: Registro de visitas a página de chat
- `estudio`: Registro de visitas a página de estudio
- `musica`: Registro de visitas a página de música
- `juegos`: Registro de visitas a página de juegos

### 8. Datos Migrados
- 25 mensajes de chat migrados a MongoDB
- 10 notificaciones migradas a MongoDB

### 9. Comandos de Prueba

#### Probar conexión y operaciones básicas
```bash
python test_mongodb.py
```

#### Migrar datos de SQLite a MongoDB
```bash
python migrate_to_mongodb.py
```

### 10. Ventajas del Sistema Dual
- **SQLite**: Integridad referencial, transacciones ACID, datos críticos
- **MongoDB**: Escalabilidad, esquema flexible, análisis de datos, logs
- **Combinación**: Lo mejor de ambos mundos para diferentes tipos de datos

### 11. Funcionalidades Implementadas
- ✅ Integración de DualDatabaseService en vistas de chat y notificaciones
- ✅ Dashboard de analítica con datos de MongoDB
- ✅ Sistema de logs detallado en vistas principales
- ✅ Nuevos modelos para estadísticas y métricas
- ✅ Cálculo automático de estadísticas agregadas
- ✅ Sistema de alertas basado en métricas
- ✅ Análisis de tendencias
- ✅ Eventos de interacción (click, scroll, submit)
- ✅ Sistema de retención de datos

### 12. Comandos de Gestión

#### Calcular estadísticas agregadas
```bash
python manage.py calcular_estadisticas
```
Calcula estadísticas por usuario y métricas del sistema automáticamente.

#### Verificar alertas
```bash
python manage.py verificar_alertas
```
Verifica métricas y envía alertas cuando se detectan anomalías.

#### Análisis de tendencias
```bash
python manage.py analisis_tendencias
```
Analiza tendencias de actividad, uso del chat y páginas visitadas.

#### Retención de datos
```bash
python manage.py retencion_datos
```
Elimina datos antiguos según la política de retención configurada.

### 13. Nuevos Métodos del Servicio DualDatabaseService

```python
# Registrar eventos de interacción
DualDatabaseService.registrar_click(usuario, elemento, pagina, metadata)
DualDatabaseService.registrar_scroll(usuario, elemento, pagina, metadata)
DualDatabaseService.registrar_submit(usuario, elemento, pagina, metadata)

# Obtener eventos de interacción
eventos = DualDatabaseService.obtener_eventos_interaccion(usuario, limite=50)
```

### 14. Políticas de Retención de Datos
- **Mensajes de chat**: 90 días
- **Notificaciones**: 30 días
- **Logs de actividad**: 60 días
- **Datos analíticos**: 30 días
- **Eventos de interacción**: 45 días

### 15. Próximos Pasos Opcionales
- ✅ Implementar cálculo automático de estadísticas agregadas con cron job
- ✅ Crear sistema de alertas más detallado con umbrales configurables
- ✅ Implementar análisis de tendencias más avanzado con machine learning
- ✅ Agregar más tipos de eventos de interacción (hover, drag, etc.)
- Configurar réplica de MongoDB para producción
- ✅ Implementar sistema de retención de datos automático con cron job

### 16. Cron Jobs Configurados (Windows Task Scheduler)

Todas las tareas programadas están configuradas y funcionando automáticamente:

1. **MiniAmigix MongoDB - Calcular Estadistic**
   - Frecuencia: Diario
   - Horario: 2:00 AM
   - Comando: `python manage.py calcular_estadisticas`

2. **MiniAmigix MongoDB - Verificar Alertas**
   - Frecuencia: Cada hora
   - Horario: 00:00 (inicia cada hora)
   - Comando: `python manage.py verificar_alertas`

3. **MiniAmigix MongoDB - Analisis Tendencias**
   - Frecuencia: Semanal
   - Horario: Domingo 3:00 AM
   - Comando: `python manage.py analisis_tendencias`

4. **MiniAmigix MongoDB - Retencion Datos**
   - Frecuencia: Mensual
   - Horario: Día 1 del mes 4:00 AM
   - Comando: `python manage.py retencion_datos`

**Scripts de instalación:**
- Windows: `setup_mongodb_cron_windows.ps1`
- Linux: `setup_mongodb_cron_linux.sh`

**Verificar tareas configuradas:**
```bash
schtasks /query | findstr "MongoDB"
```
