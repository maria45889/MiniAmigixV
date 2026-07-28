# Instrucciones de Configuración - Módulo Entretenimiento

## Pasos para completar la implementación

### 1. Ejecutar migraciones de la base de datos

Abre una terminal en el directorio del proyecto (`c:\Users\majo1\Desktop\MiniAmigixV`) y ejecuta:

```bash
python manage.py makemigrations entretenimiento
python manage.py migrate
```

Si `python` no funciona, intenta con `python3` o la ruta completa a tu ejecutable de Python.

### 2. Cargar datos de ejemplo

Después de ejecutar las migraciones, carga los datos de ejemplo con el comando personalizado:

```bash
python manage.py seed_entretenimiento
```

Esto creará:
- 9 categorías de entretenimiento (Películas, Series, Anime, Libros, Manga, Música, Podcasts, Documentales, Teatro)
- Datos de ejemplo para películas, series, anime, libros, documentales y teatro
- Un contenido destacado (Inception) como "Recomendación del día"

### 3. Verificar la configuración

Asegúrate de que:
- ✅ La app `apps.entretenimiento` está en `INSTALLED_APPS` en `config/settings.py`
- ✅ La ruta `path('entretenimiento/', include('apps.entretenimiento.urls'))` está en `config/urls.py`
- ✅ El enlace a Entretenimiento está en el sidebar en `templates/includes/sidebar.html`

### 4. Probar el módulo

1. Inicia el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

2. Accede a `http://localhost:8000/entretenimiento/`

3. Verifica que:
   - La página carga correctamente
   - Se muestran las categorías de contenido
   - El contenido destacado aparece en la sección "Recomendación del día"
   - Las secciones de tendencias funcionan
   - El buscador y filtros funcionan
   - El sistema de favoritos funciona (requiere estar autenticado)
   - La recomendación IA funciona

### 5. Gestionar contenido desde el admin

Accede al panel de administración Django en `http://localhost:8000/admin/` para:
- Agregar nuevo contenido de entretenimiento
- Editar contenido existente
- Gestionar categorías
- Ver favoritos de usuarios
- Ver recomendaciones IA

## Características implementadas

### Modelos de datos
- **CategoriaEntretenimiento**: Categorías organizadas con iconos y orden
- **ContenidoEntretenimiento**: Contenido de entretenimiento con metadatos completos
- **FavoritoEntretenimiento**: Sistema de favoritos por usuario
- **RecomendacionIA**: Recomendaciones personalizadas por IA

### Vistas
- **entretenimiento_view**: Vista principal con todas las categorías y contenido
- **toggle_favorito**: API AJAX para agregar/quitar favoritos
- **obtener_recomendacion_ia**: API para obtener recomendaciones personalizadas

### Frontend
- Template `entretenimiento.html` con diseño moderno y responsivo
- Estilos CSS en `static/css/pages/entretenimiento.css`
- JavaScript para:
  - Sistema de favoritos conectado al backend
  - Recomendaciones IA con fallback
  - Buscador y filtros
  - Modal de detalles de contenido
  - Partículas animadas de fondo

### Integración
- ✅ Integrado en el menú principal (sidebar)
- ✅ Compatible con modo claro/oscuro
- ✅ Compatible con la mascota Amigis
- ✅ Sistema de notificaciones
- ✅ Perfil de usuario
- ✅ Permisos basados en autenticación

## Solución de problemas

### Error: "No module named 'apps.entretenimiento'"
Verifica que la app esté en `INSTALLED_APPS` en `config/settings.py`.

### Error: "No existe la tabla"
Ejecuta las migraciones:
```bash
python manage.py makemigrations entretenimiento
python manage.py migrate
```

### El contenido no aparece
Ejecuta el comando de seed:
```bash
python manage.py seed_entretenimiento
```

### Los favoritos no funcionan
Verifica que:
- Estés autenticado
- La vista `toggle_favorito` tenga el decorador `@login_required`
- El token CSRF se esté enviando correctamente

## Próximos pasos (opcional)

Para expandir el módulo, puedes:
1. Integrar con OpenAI para recomendaciones personalizadas reales
2. Agregar más tipos de contenido (memes, fondos de pantalla, podcasts, radio)
3. Implementar sistema de calificaciones por usuario
4. Agregar comentarios y reseñas
5. Integrar con APIs externas (TMDB, Goodreads, etc.)
6. Crear sistema de listas personalizadas
7. Implementar sistema de seguimiento de progreso (series vistas, libros leídos, etc.)
