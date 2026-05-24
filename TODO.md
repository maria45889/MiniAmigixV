# TODO - LOGIN DASHBOARD MODERNO (MINIAMIGIXV)

## Plan aprobado
- Reemplazar `apps/users/templates/users/login.html` por el diseño moderno provisto.
- Mantener campos `username` y `password` y el POST `action` compatible con `apps/users/views.py`.
- Corregir el link de registro para que apunte a `registro/` (usando `{% url 'registro' %}`).

## Pasos
1. Reemplazar el archivo `apps/users/templates/users/login.html`. ✅
2. Verificar que el template renderiza correctamente con `{% csrf_token %}` y que los inputs usan `name="username"` y `name="password"`. ⏳
3. Ejecutar pruebas rápidas: iniciar servidor y validar `/` (login), y enlace “Regístrate”. ✅




